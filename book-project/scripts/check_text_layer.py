"""Step 1b - Check the PDF text layer (Bangla books).

For each pages/page-XXX.txt:
  * real Bangla Unicode letters  -> keep it (log text_layer = "unicode")
  * looks like Bijoy/SutonnyMJ   -> convert to Unicode, save page-XXX.unicode.txt
                                    (log text_layer = "bijoy_converted")
  * empty or unreadable          -> log text_layer = "no_text_layer" (OCR only)

The converted text is only a helper. If it still looks wrong, do not use it:
OCR alone is safer than bad text. This script is a heuristic, so always compare
2-3 converted lines with the page by eye.

Needs:  pip install bijoy2unicode   (only when a page looks like Bijoy)
"""
import re
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import PAGES_DIR, update_log  # noqa: E402

BANGLA = re.compile(r"[ঀ-৿]")
# Characters that Bijoy text uses for kars / conjuncts (Latin-1 + cp1252 range).
BIJOY_MARKERS = re.compile(r"[\u0080-ÿŒœŠšŸƒˆ˜–-›•™]")
MISORDERED_KAR = re.compile(r"(?:^|[\sঅ-ঔ])[িেৈ]")
COMMON_ENGLISH = {
    "the", "and", "of", "to", "in", "is", "that", "it", "for", "with", "as",
    "was", "on", "are", "this", "be", "by", "or", "an", "at", "from", "not",
}

_converter = None


def bijoy_to_unicode(text: str) -> str:
    global _converter
    if _converter is None:
        try:
            from bijoy2unicode import converter
        except ImportError:
            sys.exit(
                "ERROR: a page looks like Bijoy text but the converter is missing. "
                "Run: pip install bijoy2unicode"
            )
        _converter = converter.Unicode()
    return _converter.convertBijoyToUnicode(text)


def bangla_ratio(text: str) -> float:
    letters = [c for c in text if not c.isspace()]
    return len(BANGLA.findall(text)) / len(letters) if letters else 0.0


def english_ratio(text: str) -> float:
    words = re.findall(r"[A-Za-z]+", text.lower())
    return sum(w in COMMON_ENGLISH for w in words) / len(words) if words else 0.0


def classify(text: str) -> str:
    """Return 'empty', 'unicode', 'english', or 'bijoy'."""
    if len(text.strip()) < 5:
        return "empty"
    if bangla_ratio(text) >= 0.2:
        # Legacy-font PDFs put ি ে ৈ BEFORE the consonant (visual order), e.g. "আিম"
        # instead of "আমি". In real Unicode a pre-kar never follows a vowel letter,
        # a space, or starts a word. Also private/odd glyphs (e.g. "ƅ") mean garbage.
        bad_order = len(MISORDERED_KAR.findall(text))
        stray = len(re.findall(r"[Ā-ɏͰ-ϿÀ-ÿ]", text))
        if bad_order >= 2 or stray >= 2:
            return "bad_unicode"
        return "unicode"
    # No real Bangla: plain English, or Bijoy that looks like Latin gibberish.
    if english_ratio(text) >= 0.08:
        return "english"
    if BIJOY_MARKERS.search(text) or english_ratio(text) < 0.02:
        return "bijoy"
    return "english"


def main():
    txt_files = sorted(PAGES_DIR.glob("page-*.txt"))
    txt_files = [p for p in txt_files if not p.name.endswith(".unicode.txt")]
    if not txt_files:
        sys.exit(f"ERROR: no page text files in {PAGES_DIR}. Run cut_pages.py first.")

    counts = {}
    for path in txt_files:
        name = path.stem
        text = unicodedata.normalize("NFC", path.read_text(encoding="utf-8"))
        kind = classify(text)

        if kind == "unicode" or kind == "english":
            layer = "unicode" if kind == "unicode" else "english"
        elif kind == "bijoy":
            converted = unicodedata.normalize("NFC", bijoy_to_unicode(text))
            if bangla_ratio(converted) >= 0.4:
                (PAGES_DIR / f"{name}.unicode.txt").write_text(converted, encoding="utf-8")
                layer = "bijoy_converted"
            else:
                layer = "no_text_layer"  # conversion did not produce Bangla: use OCR only
        elif kind == "bad_unicode":
            layer = "bad_unicode_order"  # wrong vowel-sign order: do not use, OCR only
        else:
            layer = "no_text_layer"

        update_log(name, text_layer=layer)
        counts[layer] = counts.get(layer, 0) + 1

    print("Text layer check:", ", ".join(f"{k}: {v}" for k, v in sorted(counts.items())))
    if counts.get("bijoy_converted"):
        print("Open 2 of the page-XXX.unicode.txt files and compare 3 lines with the page.")


if __name__ == "__main__":
    main()
