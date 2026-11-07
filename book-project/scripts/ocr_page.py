"""Step 2 - OCR Reader (reader 1). NOT USED while there is no Google key:
the readers are three blind Claude text-reader runs instead (see CLAUDE.md).
Kept for when a key is available.

Sends one page image to Google Cloud Vision (document text detection, language
hints "bn" and "en") and saves every word with its box and confidence to
work/page-XXX/ocr.json.

Usage:  python scripts/ocr_page.py pages/page-001.png

The API key is read from the environment variable GOOGLE_API_KEY (or
GOOGLE_VISION_API_KEY). It is never printed or written to disk.
Alternatively, a service-account file named in GOOGLE_APPLICATION_CREDENTIALS
also works.
"""
import io
import json
import os
import re
import sys
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import WORK_DIR  # noqa: E402

LANGUAGE_HINTS = ["bn", "en"]
MAX_BYTES = 18 * 1024 * 1024  # Vision limit is 20 MB per request


def make_client():
    from google.cloud import vision

    key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GOOGLE_VISION_API_KEY")
    if key:
        return vision.ImageAnnotatorClient(client_options={"api_key": key})
    if os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
        return vision.ImageAnnotatorClient()
    sys.exit(
        "ERROR: no Google credentials found. Set GOOGLE_API_KEY in your terminal "
        "(do not paste the key into chat), then run again."
    )


def image_bytes(path: Path):
    """Return (bytes, width, height). Re-encodes as JPEG only if the PNG is too big.

    Re-encoding keeps pixel size, so all box coordinates stay valid.
    """
    with Image.open(path) as im:
        width, height = im.size
        data = path.read_bytes()
        if len(data) > MAX_BYTES:
            buf = io.BytesIO()
            im.convert("RGB").save(buf, format="JPEG", quality=95)
            data = buf.getvalue()
    return data, width, height


def box_of(vertices):
    xs = [v.x for v in vertices]
    ys = [v.y for v in vertices]
    return [min(xs), min(ys), max(xs), max(ys)]


def parse_response(response):
    """Turn a Vision full_text_annotation into a list of word dicts."""
    words = []
    annotation = response.full_text_annotation
    for page in annotation.pages:
        for block_no, block in enumerate(page.blocks, start=1):
            for para_no, para in enumerate(block.paragraphs, start=1):
                for word in para.words:
                    text = "".join(s.text for s in word.symbols)
                    words.append({
                        "text": text,
                        "box": box_of(word.bounding_box.vertices),
                        "confidence": round(float(word.confidence), 4),
                        "block": block_no,
                        "paragraph": para_no,
                    })
    return annotation.text, words


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python scripts/ocr_page.py <page image>")
    image_path = Path(sys.argv[1])
    if not image_path.is_file():
        sys.exit(f"ERROR: file not found: {image_path}")

    name = image_path.stem  # page-001
    if not re.fullmatch(r"page-\d+", name):
        sys.exit(f"ERROR: expected a file named like page-001.png, got {image_path.name}")

    data, width, height = image_bytes(image_path)

    from google.cloud import vision

    client = make_client()
    response = client.document_text_detection(
        image=vision.Image(content=data),
        image_context=vision.ImageContext(language_hints=LANGUAGE_HINTS),
    )
    if response.error.message:
        sys.exit(f"ERROR from Google Vision: {response.error.message}")

    full_text, words = parse_response(response)

    out_dir = WORK_DIR / name
    out_dir.mkdir(parents=True, exist_ok=True)
    result = {
        "page": int(name.split("-")[1]),
        "size": {"width": width, "height": height},
        "language_hints": LANGUAGE_HINTS,
        "full_text": full_text,
        "words": words,
    }
    (out_dir / "ocr.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"{name}: {len(words)} words saved to {out_dir / 'ocr.json'}")


if __name__ == "__main__":
    main()
