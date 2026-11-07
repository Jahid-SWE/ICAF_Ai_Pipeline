"""Step 5b - Book compiler (program, no AI).

Joins every ready page (status checked or approved) into ONE file:
  python scripts/compile_book.py docx   -> Output/book.docx  (the single file with everything)
  python scripts/compile_book.py md     -> Output/book.md

It only copies what is saved in work/page-NNN/page.json. It never changes,
fixes or shortens a word. If a word is wrong, fix it in that page's page.json
and compile again. Never fix it in the book file.

Per page: number, status, confidence, size; background (colour, description,
rebuild notes, image); every text block in reading order (exact text, then a
line with its id, box, text_status, reader agreement and style); every picture
(real file embedded in docx, then its id, box, layer, rotation, opacity,
overlaps, kind, description, purpose, style, colours, rebuild notes);
doubts and unknown_words. Pages that are not ready are listed under
"NOT READY" at the top and their content is left out.

After writing, the file is read back and every text block id and picture id of
every ready page must appear exactly once (and, for docx, every picture must be
embedded). Missing or doubled ids are printed and the exit code is 1.
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import WORK_DIR, ROOT, read_log_row  # noqa: E402

BOOK_DIR = ROOT / "Output"
READY = ("checked", "approved")
FONT = "Noto Sans Bengali"
CONTENT_WIDTH_IN = 6.5
ID_LINE = re.compile(r"^([ti]\d+) \| ")


def load_pages():
    """Return a list of (name, page_dict, status, confidence) in page order."""
    pages = []
    for d in sorted(WORK_DIR.glob("page-*")):
        pj = d / "page.json"
        if not pj.is_file():
            pages.append((d.name, None, "no page.json", ""))
            continue
        page = json.loads(pj.read_text(encoding="utf-8"))
        row = read_log_row(d.name)
        status = row.get("status") or page.get("status", "new")
        pages.append((d.name, page, status, row.get("confidence", "")))
    return pages


def box_str(box):
    return "[" + ", ".join(str(v) for v in box) + "]"


def style_line(b):
    f = b["font"]
    return (f"{b['id']} | {b['type']} | box {box_str(b['box'])} | {b['text_status']} | "
            f"read-agreement {b['ocr_confidence']} | {f['name']} {f['size_pt']} pt | "
            f"bold {'yes' if f['bold'] else 'no'} | italic {'yes' if f['italic'] else 'no'} | "
            f"colour {f['color']} | align {b['align']} | order {b['order']}")


def image_lines(im):
    """Return the lines of notes for one picture; the first starts with its id."""
    return [
        f"{im['id']} | {im['kind']} | file {im['file']} | box {box_str(im['box'])} | layer {im['layer']} | "
        f"rotation {im['rotation_deg']} | opacity {im['opacity']} | "
        f"overlaps text: {', '.join(im['overlaps_text']) or 'none'}",
        f"Description: {im['description']}",
        f"Purpose: {im['purpose']}",
        f"Style: {im['style']}",
        f"Main colours: {', '.join(im['main_colors']) or 'none'}",
        f"Rebuild notes: {im['rebuild_notes']}",
    ]


def split_pages(pages):
    ready = [p for p in pages if p[1] is not None and p[2] in READY]
    not_ready = [p for p in pages if p not in ready]
    return ready, not_ready


# ----------------------------------------------------------------- markdown

def write_md(ready, not_ready, path):
    out = ["# Book", ""]
    if not_ready:
        out += ["## NOT READY", ""]
        out += [f"- {n}: {s}" for n, _, s, _ in not_ready]
        out.append("")
    for name, page, status, conf in ready:
        out += [f"## Page {page['page']}", "",
                f"Status: {status} | Confidence: {conf or 'n/a'} | "
                f"Size: {page['size']['width']}x{page['size']['height']} px", ""]
        bg = page["background"]
        out += ["### Background", "", f"Colour {bg['color']}. {bg['description']}", f"Rebuild notes: {bg['rebuild_notes']}"]
        if bg["image_file"]:
            out.append(f"File: [{bg['image_file']}](../work/{name}/{bg['image_file']})")
        out.append("")
        out += ["### Text", ""]
        for b in sorted(page["text_blocks"], key=lambda b: b["order"]):
            out += [b["text"], "", f"_{style_line(b)}_", ""]
        out += ["### Pictures", ""]
        for im in page["images"]:
            lines = image_lines(im)
            link = f"[{im['file']}](../work/{name}/{im['file']})"
            lines[0] = lines[0].replace(f"file {im['file']}", f"file {link}")
            out += [f"- {lines[0]}"] + [f"  - {x}" for x in lines[1:]]
        out.append("")
        out += ["### Doubts and unknown words", ""]
        out += [f"- doubt: {x}" for x in page["doubts"]]
        out += [f"- unknown word: {x}" for x in page["unknown_words"]]
        if not page["doubts"] and not page["unknown_words"]:
            out.append("- none")
        out.append("")
    path.write_text("\n".join(out), encoding="utf-8")


def check_md(path, ready):
    problems = []
    sections = re.split(r"^## Page (\d+)\s*$", path.read_text(encoding="utf-8"), flags=re.M)
    found = {int(sections[i]): sections[i + 1] for i in range(1, len(sections), 2)}
    for _, page, _, _ in ready:
        body = found.get(page["page"], "")
        ids = Counter(re.findall(r"^(?:_|- )([ti]\d+) \| ", body, flags=re.M))
        problems += compare_ids(page, ids)
    return problems


# --------------------------------------------------------------------- docx

def set_font(run, size_pt=None, bold=None, italic=None, color=None):
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.shared import Pt, RGBColor

    run.font.name = FONT
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.append(rfonts)
    for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rfonts.set(qn(attr), FONT)
    if size_pt is not None:
        run.font.size = Pt(size_pt)
        sz_cs = OxmlElement("w:szCs")  # size for complex scripts such as Bangla
        sz_cs.set(qn("w:val"), str(int(round(size_pt * 2))))
        rpr.append(sz_cs)
    if bold is not None:
        run.bold = bold
        if bold:
            rpr.append(OxmlElement("w:bCs"))
    if italic is not None:
        run.italic = italic
        if italic:
            rpr.append(OxmlElement("w:iCs"))
    if color:
        run.font.color.rgb = RGBColor.from_string(color.lstrip("#").upper())


def add_picture(doc, path, width_px, page_width_px, notes):
    from docx.shared import Inches

    if not path.is_file():
        notes.append(f"picture file missing: {path}")
        p = doc.add_paragraph()
        set_font(p.add_run(f"[picture file missing: {path.name}]"), 9, italic=True, color="#B00020")
        return False
    width_in = min(CONTENT_WIDTH_IN, max(0.5, CONTENT_WIDTH_IN * width_px / page_width_px))
    doc.add_picture(str(path), width=Inches(width_in))
    return True


def write_docx(ready, not_ready, path):
    from docx import Document
    from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
    from docx.oxml.ns import qn

    align_map = {"left": WD_ALIGN_PARAGRAPH.LEFT, "center": WD_ALIGN_PARAGRAPH.CENTER,
                 "right": WD_ALIGN_PARAGRAPH.RIGHT, "justify": WD_ALIGN_PARAGRAPH.JUSTIFY}
    notes = []
    doc = Document()
    normal = doc.styles["Normal"]
    normal.font.name = FONT
    normal.element.rPr.rFonts.set(qn("w:cs"), FONT)
    normal.element.rPr.rFonts.set(qn("w:eastAsia"), FONT)

    doc.add_heading("Book", 0)
    if not_ready:
        doc.add_heading("NOT READY", 1)
        for n, _, s, _ in not_ready:
            doc.add_paragraph(f"{n}: {s}", style="List Bullet")

    def small(text, color="#555555"):
        p = doc.add_paragraph()
        set_font(p.add_run(text), 8, color=color)
        return p

    for idx, (name, page, status, conf) in enumerate(ready):
        if idx > 0 or not_ready:
            doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
        doc.add_heading(f"Page {page['page']}", 1)
        small(f"Status: {status} | Confidence: {conf or 'n/a'} | "
              f"Size: {page['size']['width']}x{page['size']['height']} px")
        pw = page["size"]["width"]
        d = WORK_DIR / name

        bg = page["background"]
        doc.add_heading("Background", 2)
        small(f"Colour {bg['color']}. {bg['description']}")
        small(f"Rebuild notes: {bg['rebuild_notes']}")
        if bg["image_file"]:
            add_picture(doc, d / bg["image_file"], pw, pw, notes)

        doc.add_heading("Text", 2)
        for b in sorted(page["text_blocks"], key=lambda b: b["order"]):
            f = b["font"]
            p = doc.add_paragraph()
            p.alignment = align_map[b["align"]]
            set_font(p.add_run(b["text"]), f["size_pt"], f["bold"], f["italic"], f["color"])
            small(style_line(b))

        doc.add_heading("Pictures", 2)
        for im in page["images"]:
            add_picture(doc, d / im["file"], im["box"][2] - im["box"][0], pw, notes)
            for line in image_lines(im):
                small(line)

        doc.add_heading("Doubts and unknown words", 2)
        items = [f"doubt: {x}" for x in page["doubts"]] + [f"unknown word: {x}" for x in page["unknown_words"]]
        for x in items or ["none"]:
            doc.add_paragraph(x, style="List Bullet")

    path.parent.mkdir(exist_ok=True)
    doc.save(str(path))
    return notes


def check_docx(path, ready):
    from docx import Document

    problems = []
    doc = Document(str(path))
    per_page, pictures, current = {}, Counter(), None
    for p in doc.paragraphs:
        m = re.match(r"^Page (\d+)$", p.text)
        if p.style.name.startswith("Heading") and m:
            current = int(m.group(1))
            per_page[current] = Counter()
            continue
        if current is None:
            continue
        m = ID_LINE.match(p.text)
        if m:
            per_page[current][m.group(1)] += 1
        pictures[current] += len(p._element.findall(".//{*}drawing"))
    for _, page, _, _ in ready:
        problems += compare_ids(page, per_page.get(page["page"], Counter()))
        want = len(page["images"]) + (1 if page["background"]["image_file"] else 0)
        if pictures[page["page"]] != want:
            problems.append(f"page {page['page']}: {pictures[page['page']]} pictures embedded, expected {want}")
    return problems


def compare_ids(page, found):
    want = [b["id"] for b in page["text_blocks"]] + [i["id"] for i in page["images"]]
    problems = []
    for x in want:
        if found.get(x, 0) != 1:
            problems.append(f"page {page['page']}: {x} appears {found.get(x, 0)} times, expected 1")
    return problems


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ("md", "docx"):
        sys.exit(__doc__)
    fmt = sys.argv[1]
    pages = load_pages()
    if not pages:
        sys.exit("No work/page-*/ folders found.")
    ready, not_ready = split_pages(pages)
    BOOK_DIR.mkdir(exist_ok=True)
    path = BOOK_DIR / f"book.{fmt}"

    notes = []
    if fmt == "md":
        write_md(ready, not_ready, path)
        problems = check_md(path, ready)
    else:
        notes = write_docx(ready, not_ready, path)
        problems = check_docx(path, ready)

    blocks = sum(len(p["text_blocks"]) for _, p, _, _ in ready)
    pics = sum(len(p["images"]) for _, p, _, _ in ready)
    print(f"{path}: {len(ready)} ready pages, {len(not_ready)} NOT READY, {blocks} text blocks, {pics} pictures")
    for n in notes + problems:
        print("PROBLEM:", n)
    if problems or notes:
        sys.exit(1)
    print("Check passed: every text block and picture appears exactly once.")


if __name__ == "__main__":
    main()
