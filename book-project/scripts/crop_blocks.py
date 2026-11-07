"""Step 4b - cut every text block out of the page image.

Reads work/page-XXX/layout.json and saves work/page-XXX/blocks/t1.png, t2.png ...
Each cut has 10 px of extra space around the block.

Usage:  python scripts/crop_blocks.py page-001
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import WORK_DIR, PAGES_DIR  # noqa: E402
from crop import crop  # noqa: E402

PAD = 10


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    name = sys.argv[1]
    layout_path = WORK_DIR / name / "layout.json"
    image_path = PAGES_DIR / f"{name}.png"
    if not layout_path.is_file():
        sys.exit(f"ERROR: {layout_path} not found. Run the layout-reader first.")
    if not image_path.is_file():
        sys.exit(f"ERROR: {image_path} not found.")

    layout = json.loads(layout_path.read_text(encoding="utf-8"))
    blocks_dir = WORK_DIR / name / "blocks"
    blocks_dir.mkdir(parents=True, exist_ok=True)
    for old in blocks_dir.glob("t*.png"):  # stale crops from an earlier layout
        old.unlink()

    count = 0
    for block in layout.get("text_blocks", []):
        crop(image_path, blocks_dir / f"{block['id']}.png", block["box"], pad=PAD)
        count += 1
    print(f"{name}: {count} block images saved to {blocks_dir}")


if __name__ == "__main__":
    main()
