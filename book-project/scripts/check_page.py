"""Step 4d - Score program (no AI).

Two checks with plain maths:
 (1) Coverage: paint over every text box, image box and declared background
     graphic from page.json, count the ink that is left. Coverage = ink inside
     boxes / all ink. 1.00 means nothing was missed. Leftover ink spots are
     saved as boxes in leftovers.json.
 (2) Crop match: for each picture, compare images/iN.png with the same box on
     the page image using SSIM. crop_ssim = the lowest score (1.0 if no pictures).

"Ink" = any pixel clearly different from the page background colour. If the
page declares a background graphic (background.image_file points to a real
file), the pixels that already match that graphic are not counted as ink.

Writes coverage and crop_ssim into log.csv.
Usage:  python scripts/check_page.py page-001
"""
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage
from skimage.metrics import structural_similarity

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import WORK_DIR, PAGES_DIR, update_log  # noqa: E402

INK_THRESHOLD = 40      # 0-255 colour difference that counts as ink
BOX_PAD = 4             # px of slack around boxes for anti-aliased edges
MIN_SPOT_PIXELS = 12    # ignore specks smaller than this
CLUSTER_DILATE = 12     # join nearby leftover ink into one spot


def hex_to_rgb(h):
    h = h.lstrip("#")
    return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], dtype=np.int16)


def ink_mask(page_rgb, page_json, d):
    bg = page_json["background"]
    bg_file = bg.get("image_file")
    if bg_file and (d / bg_file).is_file():
        ref = Image.open(d / bg_file).convert("RGB")
        if ref.size != (page_rgb.shape[1], page_rgb.shape[0]):
            ref = ref.resize((page_rgb.shape[1], page_rgb.shape[0]))
        ref = np.asarray(ref, dtype=np.int16)
    else:
        ref = hex_to_rgb(bg["color"])
    return np.abs(page_rgb.astype(np.int16) - ref).max(axis=-1) > INK_THRESHOLD


def covered_mask(shape, page_json):
    h, w = shape
    covered = np.zeros(shape, dtype=bool)
    boxes = [b["box"] for b in page_json["text_blocks"]] + [i["box"] for i in page_json["images"]]
    for l, t, r, b in boxes:
        covered[max(0, t - BOX_PAD):min(h, b + BOX_PAD), max(0, l - BOX_PAD):min(w, r + BOX_PAD)] = True
    return covered


def leftover_boxes(uncovered_ink):
    grown = ndimage.binary_dilation(uncovered_ink, iterations=CLUSTER_DILATE)
    labels, n = ndimage.label(grown)
    out = []
    for i, sl in enumerate(ndimage.find_objects(labels), start=1):
        if sl is None:
            continue
        if uncovered_ink[sl][labels[sl] == i].sum() < MIN_SPOT_PIXELS:
            continue
        out.append([int(sl[1].start), int(sl[0].start), int(sl[1].stop), int(sl[0].stop)])
    return out


def crop_ssim(page_img, page_json, d):
    scores = {}
    for im in page_json["images"]:
        path = d / im["file"]
        if not path.is_file():
            scores[im["id"]] = 0.0
            continue
        l, t, r, b = im["box"]
        want = page_img.crop((l, t, r, b)).convert("L")
        got = Image.open(path).convert("L")
        if got.size != want.size:
            got = got.resize(want.size)
        a, c = np.asarray(want), np.asarray(got)
        small = min(a.shape)
        if small < 3:
            scores[im["id"]] = 1.0
            continue
        win = min(7, small if small % 2 else small - 1)
        scores[im["id"]] = float(structural_similarity(a, c, win_size=win))
    return scores


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    name = sys.argv[1]
    d = WORK_DIR / name
    page_path, image_path = d / "page.json", PAGES_DIR / f"{name}.png"
    for p in (page_path, image_path):
        if not p.is_file():
            sys.exit(f"ERROR: {p} not found.")

    page_json = json.loads(page_path.read_text(encoding="utf-8"))
    page_img = Image.open(image_path).convert("RGB")
    rgb = np.asarray(page_img)

    ink = ink_mask(rgb, page_json, d)
    inside = ink & covered_mask(ink.shape, page_json)
    total = int(ink.sum())
    coverage = round(int(inside.sum()) / total, 4) if total else 1.0
    spots = leftover_boxes(ink & ~inside)
    (d / "leftovers.json").write_text(json.dumps({"leftovers": spots}, indent=2), encoding="utf-8")

    scores = crop_ssim(page_img, page_json, d)
    worst = round(min(scores.values()), 4) if scores else 1.0

    update_log(name, coverage=coverage, crop_ssim=worst)
    print(f"{name}: coverage {coverage} ({len(spots)} leftover spot(s)), crop_ssim {worst}")
    for iid, s in scores.items():
        if s < 0.98:
            print(f"  low crop match: {iid} = {s:.4f}")


if __name__ == "__main__":
    main()
