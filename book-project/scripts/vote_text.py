"""Step 4b - Text Vote Program (no AI).

No OCR is used (no Google key). All three readers are blind Claude runs of the
text-reader agent, each a fresh run that never sees the others' files:
Reader 1 = text_a.json (first run, every block).
Reader 2 = text_b.json (second, fresh run, every block).
Reader 3 = text_c.json (tiebreak run, only the blocks listed in tiebreak.txt).

First run (no usable text_c.json):
  compare reader 1 and 2 word by word; blocks with differences go to
  tiebreak.txt; if tiebreak.txt is empty, text_final.json + votes.json are written.
Second run (text_c.json exists):
  for each differing word keep the version that at least 2 of 3 readers match.
  If all 3 differ, the block is "human": reader 1's word is kept with [?] in front.

Usage:  python scripts/vote_text.py page-001
"""
import difflib
import json
import re
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import WORK_DIR, ROOT, update_log  # noqa: E402

WORDLIST = ROOT / "scripts" / "bangla_words.txt"
BANGLA = re.compile(r"[ঀ-৿]")
QUOTES = {"‘": "'", "’": "'", "‚": "'", "‛": "'",
          "“": '"', "”": '"', "„": '"', "‟": '"'}
DASHES = {"‐": "-", "‑": "-", "‒": "-", "–": "-",
          "—": "-", "―": "-", "−": "-"}
SPACES = re.compile(r"[\s  -   　]+")


def clean(text: str) -> str:
    """Same cleaning for every reader. Never changes letters."""
    text = unicodedata.normalize("NFC", text)
    text = "".join(QUOTES.get(c, DASHES.get(c, c)) for c in text)
    return SPACES.sub(" ", text).strip()


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def word_agreement(w1, w2):
    """Share of words the two readers agree on (1.0 = identical). Stored as the block confidence."""
    if not w1 and not w2:
        return 1.0
    matched = sum(m.size for m in difflib.SequenceMatcher(None, w1, w2, autojunk=False).get_matching_blocks())
    return round(matched / max(len(w1), len(w2)), 4)


def differing_chars(a: str, b: str) -> int:
    matched = sum(m.size for m in difflib.SequenceMatcher(None, a, b, autojunk=False).get_matching_blocks())
    return max(len(a), len(b)) - matched


def start_in(opcodes, i):
    """Index in the other word list matching the START of base position i (None if inside a changed run)."""
    pos = 0
    for tag, a1, a2, b1, b2 in opcodes:
        if tag == "equal" and a1 <= i <= a2:
            return b1 + (i - a1)
        if tag != "equal" and a1 < i < a2:
            return None
        if a2 <= i:
            pos = b2
    return pos


def end_in(opcodes, i):
    """Index in the other word list matching the END of base position i (None if inside a changed run)."""
    for tag, a1, a2, b1, b2 in opcodes:
        if tag == "equal" and a1 <= i <= a2:
            return b1 + (i - a1)
        if tag != "equal" and a1 < i < a2:
            return None
        if a1 >= i:
            return b1
    return None


def vote_block(w1, w2, w3):
    """Return (final_words, status, diffs). w3 may be None (no tiebreak read)."""
    ops12 = difflib.SequenceMatcher(None, w1, w2, autojunk=False).get_opcodes()
    ops13 = difflib.SequenceMatcher(None, w1, w3, autojunk=False).get_opcodes() if w3 is not None else None
    final, diffs, human = [], [], False
    for tag, i1, i2, j1, j2 in ops12:
        if tag == "equal":
            final.extend(w1[i1:i2])
            continue
        seg1, seg2 = w1[i1:i2], w2[j1:j2]
        seg3 = None
        if ops13 is not None:
            s, e = start_in(ops13, i1), end_in(ops13, i2)
            if s is not None and e is not None and s <= e:
                seg3 = w3[s:e]
        if seg3 is not None and seg3 == seg1:
            final.extend(seg1)
            winner = "reader1"
        elif seg3 is not None and seg3 == seg2:
            final.extend(seg2)
            winner = "reader2"
        else:
            human = True
            final.extend(["[?]" + w for w in seg1] or ["[?]"])
            winner = "human"
        diffs.append({"reader1": " ".join(seg1), "reader2": " ".join(seg2),
                      "reader3": None if seg3 is None else " ".join(seg3), "kept": winner})
    return final, ("human" if human else "voted"), diffs


def load_wordlist():
    if not WORDLIST.is_file():
        return None
    return {unicodedata.normalize("NFC", w.strip()) for w in WORDLIST.read_text(encoding="utf-8").splitlines() if w.strip()}


def unknown_words(final_texts, words):
    found = []
    for text in final_texts.values():
        for token in text.split():
            token = token.replace("[?]", "").strip(".,;:!?()[]{}\"'‘’“”।-")
            if token and BANGLA.search(token) and token not in words and token not in found:
                found.append(token)
    return found


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    name = sys.argv[1]
    d = WORK_DIR / name
    for need in ("layout.json", "text_a.json", "text_b.json"):
        if not (d / need).is_file():
            sys.exit(f"ERROR: {d / need} not found. Run the text-reader agent twice (fresh runs) first.")

    layout = load_json(d / "layout.json")
    r1 = {k: clean(v) for k, v in load_json(d / "text_a.json").items()}
    text_b = {k: clean(v) for k, v in load_json(d / "text_b.json").items()}
    blocks = layout["text_blocks"]
    confs = {}

    tie_path, text_c_path = d / "tiebreak.txt", d / "text_c.json"
    tie_ids = [l.strip() for l in tie_path.read_text(encoding="utf-8").splitlines() if l.strip()] if tie_path.is_file() else []
    text_c = None
    if tie_ids and text_c_path.is_file() and text_c_path.stat().st_mtime >= (d / "text_b.json").stat().st_mtime:
        text_c = {k: clean(v) for k, v in load_json(text_c_path).items()}

    total_diff = total_len = 0
    results, tiebreak = {}, []
    for b in blocks:
        bid = b["id"]
        t1, t2 = r1.get(bid, ""), text_b.get(bid, "")
        total_diff += differing_chars(t1, t2)
        total_len += max(len(t1), len(t2))
        w1, w2 = t1.split(), t2.split()
        confs[bid] = word_agreement(w1, w2)
        if w1 == w2:
            results[bid] = {"words": w1, "status": "agreed", "diffs": [], "reader3": None}
            continue
        if text_c is not None and bid in tie_ids:
            w3 = text_c.get(bid, "").split() if bid in text_c else None
            words, status, diffs = vote_block(w1, w2, w3)
            results[bid] = {"words": words, "status": status, "diffs": diffs, "reader3": " ".join(w3) if w3 is not None else None}
        else:
            tiebreak.append(bid)
            results[bid] = {"words": w1, "status": "pending", "diffs": [], "reader3": None}

    agreement = round(1 - total_diff / total_len, 4) if total_len else 1.0
    update_log(name, text_agreement=agreement)

    if tiebreak:
        tie_path.write_text("\n".join(tiebreak) + "\n", encoding="utf-8")
        print(f"{name}: text_agreement {agreement}; {len(tiebreak)} block(s) need a tiebreak: {', '.join(tiebreak)}")
        return
    tie_path.write_text("", encoding="utf-8")

    final = {bid: " ".join(r["words"]) for bid, r in results.items()}
    wordlist = load_wordlist()
    votes = {
        "text_agreement": agreement,
        "blocks": {bid: {"status": r["status"], "ocr_confidence": confs[bid], "reader1": r1.get(bid, ""),
                         "reader2": text_b.get(bid, ""), "reader3": r["reader3"], "diffs": r["diffs"]}
                   for bid, r in results.items()},
        "unknown_words": unknown_words(final, wordlist) if wordlist is not None else [],
        "wordlist_missing": wordlist is None,
    }
    (d / "text_final.json").write_text(json.dumps(final, ensure_ascii=False, indent=2), encoding="utf-8")
    (d / "votes.json").write_text(json.dumps(votes, ensure_ascii=False, indent=2), encoding="utf-8")
    counts = {s: sum(r["status"] == s for r in results.values()) for s in ("agreed", "voted", "human")}
    print(f"{name}: text_agreement {agreement}; final text written ({counts})")
    if wordlist is None:
        print("WARNING: scripts/bangla_words.txt is missing, so unknown_words was not checked.")


if __name__ == "__main__":
    main()
