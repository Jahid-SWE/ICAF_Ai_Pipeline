"""Step 1 - Page Cutter.

Opens the PDF in input/, saves each page as pages/page-001.png at 300 DPI,
and saves the PDF's own text layer (if any) to pages/page-001.txt.
Prints how many pages were made.

Usage:  python scripts/cut_pages.py [path/to/book.pdf]
If no path is given, the single PDF in input/ is used.
"""
import sys
from pathlib import Path

import pymupdf as fitz  # PyMuPDF

DPI = 300
ROOT = Path(__file__).resolve().parent.parent
INPUT_DIR = ROOT / "input"
PAGES_DIR = ROOT / "pages"


def find_pdf(argv):
    if len(argv) > 1:
        pdf = Path(argv[1])
        if not pdf.is_file():
            sys.exit(f"ERROR: file not found: {pdf}")
        return pdf
    pdfs = sorted(INPUT_DIR.glob("*.pdf")) + sorted(INPUT_DIR.glob("*.PDF"))
    pdfs = sorted(set(pdfs))
    if not pdfs:
        sys.exit(f"ERROR: no PDF found in {INPUT_DIR}. Put the book PDF there.")
    if len(pdfs) > 1:
        names = ", ".join(p.name for p in pdfs)
        sys.exit(f"ERROR: more than one PDF in input/ ({names}). Pass the one to use as an argument.")
    return pdfs[0]


def main():
    pdf_path = find_pdf(sys.argv)
    PAGES_DIR.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(pdf_path)
    total = doc.page_count
    width = max(3, len(str(total)))
    made = 0
    with_text = 0

    for i in range(total):
        page = doc[i]
        name = f"page-{i + 1:0{width}d}"
        pix = page.get_pixmap(dpi=DPI, alpha=False)
        pix.save(PAGES_DIR / f"{name}.png")

        text = page.get_text("text").strip()
        (PAGES_DIR / f"{name}.txt").write_text(text, encoding="utf-8")
        if text:
            with_text += 1
        made += 1

    doc.close()
    print(f"Source: {pdf_path.name}")
    print(f"Pages made: {made} (PNG at {DPI} DPI in {PAGES_DIR})")
    print(f"Pages with a text layer: {with_text}; without: {made - with_text}")


if __name__ == "__main__":
    main()
