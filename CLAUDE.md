# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Current state

`SPEC.md` is the design spec (the Book Extraction Multi-Agent System build guide). The older `Book Extraction Multi-Agent System — Beginner Build Guide.docx` is superseded by it and is deleted in git. This directory is a git repository.

The system is built in `book-project/` (one folder per book). Steps 1–5 of the spec are written: scripts in `scripts/`, four agents in `.claude/agents/`, `schema.json`, and `book-project/CLAUDE.md` with the Boss rules. `scripts/compile_book.py` (Step 5b) is written and passed an offline test on synthetic data (docx and md). Offline tests passed on synthetic data. **Reading mode now: Claude only.** There is no Google key, so `ocr_page.py` is not used; the three readers are three fresh blind `text-reader` runs (`text_a.json`, `text_b.json`, tiebreak `text_c.json`) and `vote_text.py` was changed to match (tested offline). Not yet done: a real run on AN3-01 (the PDF is in `input/`; pages are cut and the text-layer check logged `bad_unicode_order` for all 18 pages, so the PDF text is not usable), `check_text_layer.py` with a real Bijoy page (needs `pip install bijoy2unicode`), `scripts/bangla_words.txt` (needs the user to approve a word list and its licence), and the Step 6 five-page test. When building, follow the spec's step order and test each step before starting the next.

## What the system does

It extracts a book (Bangla and English text) page by page. For each page it saves the text, its styling, the pictures and the background. It then checks the saved data against the real page. The main Claude Code session acts as the "Boss" and runs the pipeline. There is no `meaning-writer` agent any more: `purpose` fields describe visual objects only, never the meaning of the text.

## Pipeline (per page, run in this order)

1. `scripts/cut_pages.py` (program): PDF → `pages/page-NNN.png` at 300 DPI, plus `page-NNN.txt` from the PDF text layer. Prefer the original PDF or InDesign file over scans.
   `scripts/check_text_layer.py` (program, once per book) keeps real Unicode Bangla, converts Bijoy/SutonnyMJ text to `page-NNN.unicode.txt`, or logs `no_text_layer`.
2. *(Skipped while there is no Google key.)* `scripts/ocr_page.py` (Google Cloud Vision) is not run; reader 1 is the first blind `text-reader` run instead.
3. `layout-reader` agent (looks at the page image only): text blocks with box, type, font, size, bold, italic, colour, alignment and reading order. Writes `layout.json`. It never writes any words.
4. `scripts/crop_blocks.py` (program): cuts each text block out of the page image into `blocks/tN.png` with 10 px padding.
5. `text-reader` agent: a **blind** reader. It sees only the block images and types what is printed. Run twice as separate fresh runs: `text_a.json` (**reader 1**) and `text_b.json` (**reader 2**).
6. `scripts/vote_text.py` (program): compares readers 1 and 2 (`text_a.json`, `text_b.json`) word by word, lists disagreeing blocks in `tiebreak.txt` and writes `text_agreement` to `log.csv`. If `tiebreak.txt` is not empty, the Boss runs `text-reader` again as a fresh run on only those blocks (`text_c.json`, **reader 3**) and runs `vote_text.py` again. A word kept by at least 2 of 3 readers wins (`voted`). If all 3 differ the block is `human`, keeping reader 1's word with `[?]` in front. Writes `text_final.json` and `votes.json`, and lists `unknown_words` against `scripts/bangla_words.txt`.
7. `picture-saver` agent (+ `scripts/crop.py`): crops pictures, icons, shapes, borders and the background into `images/` and writes `images.json` (box, layer, rotation, opacity, overlaps, description, purpose, style, colours, rebuild notes).
8. `scripts/merge_page.py` (program): joins `layout.json`, `images.json` and `text_final.json` into `page.json` and validates it against `schema.json`. A missing file or schema error marks the page `redo`.
9. `scripts/check_page.py` (program, no AI): **coverage** (ink inside saved boxes ÷ all ink; leftovers go to `leftovers.json`) and **crop_ssim** (lowest SSIM of each picture crop against the page).
10. `checker` agent: compares `page.json` with the page image, reads `votes.json` and `leftovers.json`, writes `report.md` with mistakes, doubts and a 0–100 confidence score. It never fixes anything.
11. `scripts/set_status.py` (program): applies the thresholds below and writes the status to `log.csv` and `page.json`.

At the end (when the user says "Compile the book"): `scripts/compile_book.py docx` and `compile_book.py md` (programs) join every `checked` or `approved` page into `Output/book.docx` and `Output/book.md`. The docx is the **single deliverable**: all text with its saved style, box positions, the real pictures embedded, descriptions, rebuild notes, doubts and unknown words. Pages not ready are listed under NOT READY and left out. It only copies, never changes a word, and reads the file back to check every text block and picture id appears exactly once. The per-page files in `work/` are working data only.

Agent definitions live in `.claude/agents/*.md`. Each agent reads `schema.json` and writes only its own file; no agent edits `page.json`.

## Rules that span files

- **Text comes only from the vote** (`votes.json`). No single reader may write `text`. Claude may invent or alter Bangla letters, so the layout-reader writes no words, and a suspect word goes into `doubts` or `unknown_words` instead of being corrected. Only a human may change `text` afterwards.
- **The text-reader is blind.** It may open only the block images (or only the blocks in `tiebreak.txt`) and must never open `layout.json`, `page.json`, an earlier run's `text_*.json` or any other answer.
- **`schema.json` is a fixed contract.** Never change it without telling everyone. Boxes are `[left, top, right, bottom]` in pixels from the top-left of the page image. `status` is one of `new`, `extracted`, `checked`, `redo`, `needs_human`, `approved`. `text_status` is one of `agreed`, `voted`, `human`. Every image needs a `file`, a `description`, a `purpose` and `rebuild_notes`.
- **The Checker must be a separate agent** from the ones that produce the data, and is the only agent allowed to read another agent's output.
- **Pictures cannot be rebuilt from words.** Save the real crop as a file and also save its description.
- **Never skip a page.** Skip pages that are already `approved`.

## Thresholds and batching

- Process 5–10 pages per batch, never the whole book at once.
- A page is `checked` only if confidence ≥95, coverage ≥0.98, crop_ssim ≥0.98 and text_agreement ≥0.99, and no text block is `human`.
- Confidence ≥90, coverage ≥0.95, crop_ssim ≥0.95 and text_agreement ≥0.97 → `needs_human`. Anything lower → `redo` once, then `needs_human` if it fails again. Any `human` block → `needs_human`.
- The 0.98 and 0.95 limits are starting guesses; tune them after the 5-page test.
- If 3 or more pages fail for the same reason, stop and fix the agent instructions, then rerun only the failed pages.
- Do a human spot-check of 1 random page in every 20. If any has mistakes, move to 1 in 10.
- Test on 5 varied pages first: text-heavy, picture-heavy, a table, a cover and an exercise page.

## Setup and commands

Python 3.11+ is required. Install the dependencies once (from `book-project/`):

```
pip install -r requirements.txt
```

This covers pymupdf, pillow, google-cloud-vision, scikit-image, scipy, numpy, jsonschema, bijoy2unicode and python-docx. Google Cloud Vision needs an API key. The key must never be pasted into chat, printed or committed. Set it in the terminal as `GOOGLE_API_KEY`. Vision is paid after a free tier, so check the pricing and test on 5 pages first.

```
python scripts/cut_pages.py              # book PDF in input/ -> pages/
python scripts/check_text_layer.py       # Bijoy check of the PDF text layer
python scripts/ocr_page.py pages/page-001.png   # only with a Google key -> work/page-001/ocr.json (not used now)
python scripts/crop_blocks.py page-001
python scripts/vote_text.py page-001
python scripts/merge_page.py page-001
python scripts/check_page.py page-001
python scripts/set_status.py page-001 --confidence 96
python scripts/compile_book.py docx      # all ready pages -> Output/book.docx (single file)
python scripts/compile_book.py md        # -> Output/book.md
```

There are no lint or test commands. The 5-page test is the acceptance test.

## Expected layout per book

`input/` (the PDF), `pages/` (page images), `work/page-NNN/{layout.json, blocks/, text_a.json, text_b.json, text_c.json, tiebreak.txt, text_final.json, votes.json, images.json, images/, page.json, leftovers.json, report.md}`, `scripts/`, `.claude/agents/`, `schema.json`, `CLAUDE.md` (Boss rules), `Output/{book.docx, book.md}` (made by `compile_book.py`), `log.csv` (one row per page: status, confidence, coverage, crop_ssim, text_agreement, text_layer, attempts, note).

Small Bangla marks such as ি ু ঁ and conjuncts such as ক্ষ and ন্ত are the most common errors. Scans below 300 DPI make them unreadable, so rescan at 400 DPI if they fail.
