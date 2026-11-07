"""Step 4c - Merge program.

Joins layout.json, images.json and text_final.json (plus votes.json) into
work/page-XXX/page.json in the shape of schema.json, and checks it against
schema.json. If a file is missing or the result breaks the schema, nothing is
written to page.json and the page is marked "redo" in log.csv.

Usage:  python scripts/merge_page.py page-001
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import WORK_DIR, ROOT, read_log_row, update_log  # noqa: E402

NEEDED = ("layout.json", "images.json", "text_final.json", "votes.json")


def fail(name, reason):
    update_log(name, status="redo", note=f"merge: {reason}")
    sys.exit(f"{name}: REDO - {reason}")


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    name = sys.argv[1]
    d = WORK_DIR / name

    missing = [f for f in NEEDED if not (d / f).is_file()]
    if missing:
        fail(name, "missing " + ", ".join(missing))

    try:
        layout, images, final, votes = (json.loads((d / f).read_text(encoding="utf-8")) for f in NEEDED)
    except json.JSONDecodeError as e:
        fail(name, f"bad JSON: {e}")

    blocks = []
    for b in layout["text_blocks"]:
        bid = b["id"]
        if bid not in final or bid not in votes["blocks"]:
            fail(name, f"block {bid} has no final text")
        v = votes["blocks"][bid]
        blocks.append({
            "id": bid, "type": b["type"], "text": final[bid], "text_status": v["status"],
            "box": b["box"], "font": b["font"], "align": b["align"], "order": b["order"],
            "ocr_confidence": v["ocr_confidence"],
        })

    page = {
        "page": int(name.split("-")[1]),
        "size": layout["size"],
        "background": images["background"],
        "text_blocks": blocks,
        "images": images["images"],
        "unknown_words": votes.get("unknown_words", []),
        "doubts": list(layout.get("doubts", [])) + list(images.get("doubts", [])),
        "status": "extracted",
    }

    import jsonschema

    schema = json.loads((ROOT / "schema.json").read_text(encoding="utf-8"))
    errors = sorted(jsonschema.Draft202012Validator(schema).iter_errors(page), key=lambda e: list(e.path))
    if errors:
        e = errors[0]
        where = "/".join(str(p) for p in e.path) or "(top level)"
        fail(name, f"schema error at {where}: {e.message[:200]}")

    (d / "page.json").write_text(json.dumps(page, ensure_ascii=False, indent=2), encoding="utf-8")
    if read_log_row(name).get("status") != "approved":
        update_log(name, status="extracted", note="")
    print(f"{name}: page.json written ({len(blocks)} text blocks, {len(page['images'])} images)")


if __name__ == "__main__":
    main()
