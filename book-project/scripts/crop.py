"""Crop one box out of a page image and save it as a PNG.

Usage:  python scripts/crop.py <page image> <out.png> <left> <top> <right> <bottom>
Example: python scripts/crop.py pages/page-001.png work/page-001/images/i1.png 1300 150 2200 900

The box is [left, top, right, bottom] in pixels from the top-left of the page
image. It is clamped to the image edges.
"""
import sys
from pathlib import Path

from PIL import Image


def crop(image_path, out_path, box, pad=0):
    with Image.open(image_path) as im:
        im = im.convert("RGB")
        l, t, r, b = box
        l, t = max(0, l - pad), max(0, t - pad)
        r, b = min(im.width, r + pad), min(im.height, b + pad)
        if r <= l or b <= t:
            raise ValueError(f"empty box after clamping: {box} on {im.size}")
        out_path = Path(out_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        im.crop((l, t, r, b)).save(out_path)
    return (l, t, r, b)


def main():
    if len(sys.argv) != 7:
        sys.exit(__doc__)
    image, out = sys.argv[1], sys.argv[2]
    try:
        box = [int(v) for v in sys.argv[3:7]]
    except ValueError:
        sys.exit("ERROR: box values must be whole numbers")
    try:
        saved = crop(image, out, box)
    except (OSError, ValueError) as e:
        sys.exit(f"ERROR: {e}")
    print(f"Saved {out} from box {list(saved)}")


if __name__ == "__main__":
    main()
