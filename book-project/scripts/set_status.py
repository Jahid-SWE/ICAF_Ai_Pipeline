"""Set a page's status from its scores (SPEC.md section 5 pseudo-code).

Usage:  python scripts/set_status.py page-001 --confidence 96

Reads coverage, crop_ssim and text_agreement from log.csv (written by
check_page.py and vote_text.py) and the checker's confidence from the command
line. Writes status (and attempts) to log.csv and to page.json.

  any text block "human"                                  -> needs_human
  confidence>=95 coverage>=0.98 crop_ssim>=0.98 agree>=0.99 -> checked
  confidence>=90 coverage>=0.95 crop_ssim>=0.95 agree>=0.97 -> needs_human
  otherwise -> redo (first failure); needs_human if it already failed once.
An "approved" page is never changed.
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import WORK_DIR, read_log_row, update_log  # noqa: E402

GOOD = dict(confidence=95, coverage=0.98, crop_ssim=0.98, text_agreement=0.99)
SMALL = dict(confidence=90, coverage=0.95, crop_ssim=0.95, text_agreement=0.97)


def decide(scores, has_human, attempts):
    if has_human:
        return "needs_human"
    if all(scores[k] >= v for k, v in GOOD.items()):
        return "checked"
    if all(scores[k] >= v for k, v in SMALL.items()):
        return "needs_human"
    return "redo" if attempts < 1 else "needs_human"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("page")
    ap.add_argument("--confidence", type=float, required=True, help="checker confidence 0-100")
    args = ap.parse_args()

    row = read_log_row(args.page)
    if row.get("status") == "approved":
        print(f"{args.page}: already approved, not changed")
        return
    try:
        scores = {k: float(row[k]) for k in ("coverage", "crop_ssim", "text_agreement")}
    except (KeyError, ValueError):
        sys.exit(f"ERROR: log.csv has no coverage/crop_ssim/text_agreement for {args.page}. Run check_page.py and vote_text.py first.")
    scores["confidence"] = args.confidence

    votes_path = WORK_DIR / args.page / "votes.json"
    has_human = False
    if votes_path.is_file():
        votes = json.loads(votes_path.read_text(encoding="utf-8"))
        has_human = any(b["status"] == "human" for b in votes["blocks"].values())

    attempts = int(row.get("attempts") or 0)
    status = decide(scores, has_human, attempts)
    if status == "redo":
        attempts += 1
    update_log(args.page, status=status, confidence=args.confidence, attempts=attempts)

    page_path = WORK_DIR / args.page / "page.json"
    if page_path.is_file():
        page = json.loads(page_path.read_text(encoding="utf-8"))
        page["status"] = status
        page_path.write_text(json.dumps(page, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{args.page}: {status} (human block: {has_human}, scores: {scores})")


if __name__ == "__main__":
    main()
