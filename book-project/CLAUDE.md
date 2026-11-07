# CLAUDE.md — Boss rules for this book

You (the main Claude Code session) are the **Boss**. You run the pipeline page by page and keep `log.csv`. The design is in `../SPEC.md`; this file is the short version you follow.

## For each page in `pages/`, in this order

Use the page name, e.g. `page-001`. **Skip a page whose status in `log.csv` is `approved`. Never skip any other page.**

**Reading mode: Claude only (no Google key, so no OCR).** `ocr_page.py` is NOT run. The three readers are three separate, fresh runs of the **text-reader** agent. Use a new agent run each time and never tell a run what an earlier run typed.

1. Run the **layout-reader** agent on the page image → `layout.json` (boxes and styles, no words)
2. `python scripts/crop_blocks.py page-NNN` → `blocks/t1.png ...`
3. Run the **text-reader** agent, run 1 → `text_a.json` (reader 1, blind)
4. Run the **text-reader** agent again as a fresh run, run 2 → `text_b.json` (reader 2, blind)
5. `python scripts/vote_text.py page-NNN` → `tiebreak.txt` and text_agreement
6. If `tiebreak.txt` has any blocks: run the **text-reader** agent a third time as a **fresh run** on only those blocks → `text_c.json`; then run `vote_text.py` again → `text_final.json`, `votes.json`
7. Run the **picture-saver** agent → `images.json` and `images/`
8. `python scripts/merge_page.py page-NNN` → `page.json` (if it says REDO, the page is `redo`; fix the cause and rerun)
9. `python scripts/check_page.py page-NNN` → coverage, crop_ssim, `leftovers.json`
10. Run the **checker** agent → `report.md` (its last line is the confidence score)
11. `python scripts/set_status.py page-NNN --confidence <score from report.md>` sets the status

Work in **batches of 5 pages** (never more than 10, never the whole book at once). After each batch, list the `needs_human` pages for the user.

## Compile the book (only when the user says "Compile the book")

Run `python scripts/compile_book.py docx` and then `python scripts/compile_book.py md`. This writes `Output/book.docx` (the one single file with everything: text with its saved style, positions, embedded pictures, notes, doubts) and `Output/book.md`. Only pages that are `checked` or `approved` are included; the rest are listed under NOT READY. The script reads the file back and prints a PROBLEM line for any text block or picture id that is missing or doubled — report these to the user. The compiler only copies. If a word is wrong in the book, fix it in that page's `page.json` (human only) and compile again; never edit the book file.

## Status rules (set by `scripts/set_status.py`, from SPEC.md section 5)

Use only these status names: `new`, `extracted`, `checked`, `redo`, `needs_human`, `approved`.

- any text block marked `human` → `needs_human`
- confidence ≥ 95 and coverage ≥ 0.98 and crop_ssim ≥ 0.98 and text_agreement ≥ 0.99 → `checked`
- confidence ≥ 90 and coverage ≥ 0.95 and crop_ssim ≥ 0.95 and text_agreement ≥ 0.97 → `needs_human`
- otherwise → `redo` (run the page again once); if it fails twice → `needs_human`

Only a human sets `approved`.

## Never

- Never change `schema.json`.
- Never let one agent read another agent's answer, except the checker. The text-reader must never open `layout.json`, `page.json`, an earlier run's `text_*.json` or any other file.
- Never type or fix Bangla text yourself. Text comes only from the vote (`votes.json`). Only a human may change `text` afterwards.
- Never let an agent write another agent's file: layout-reader → `layout.json`; text-reader → `text_a.json` / `text_b.json` / `text_c.json`; picture-saver → `images.json`; checker → `report.md`. `page.json` is written only by `merge_page.py` (and by a human fixing it).
- Never paste or print the Google API key. It lives only in the `GOOGLE_API_KEY` environment variable.
- Never run the checker on a page before `check_page.py`.

## When things go wrong

- If **3 or more pages fail for the same reason**, STOP. Fix the agent instructions in `.claude/agents/`, then rerun only the failed pages.
- Claude-only reading shares blind spots between runs, so agreement does not prove the letters are right. Do a human spot-check of **1 random page in every 5** at first (not 1 in 20), and always check pages with many `voted` blocks.
- Do a human spot-check of **1 random page in every 20**, even on good pages. If any has mistakes, check 1 in 10.
- Small Bangla marks (ি ু ঁ) and joined letters (ক্ষ, ন্ত) are the most common errors. Scans below 300 DPI make them unreadable; rescan at 400 DPI if they fail.
- Cost: only rerun failed pages, not the whole book.

## Files

`input/` (the PDF), `pages/` (page images), `work/page-NNN/{layout.json, blocks/, text_a.json, text_b.json, text_c.json, tiebreak.txt, text_final.json, votes.json, images.json, images/, page.json, leftovers.json, report.md}`, `scripts/`, `.claude/agents/`, `schema.json`, `log.csv`, `Output/{book.docx, book.md}` (made by `compile_book.py`; `book.docx` is the single deliverable, the `work/` files are working data).
