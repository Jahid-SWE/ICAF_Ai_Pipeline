# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Current state

This directory contains no code yet, only `Book Extraction Multi-Agent System — Beginner Build Guide.docx`. It is the design spec for a planned system, and it is not a git repository. The guide says each book gets its own `book-project/` folder, and its Step 6 has Claude write that folder's own `CLAUDE.md` with the Boss rules. When building, follow the guide's step order (Page Cutter → OCR → schema → agents → Rebuilder → Boss rules → 5-page test) and test each step before starting the next.

## What the system does

It extracts a book (Bangla and English text) page by page. For each page it saves the text, its styling, the pictures, the background and the page's meaning. It then checks the saved data against the real page. The main Claude Code session acts as the "Boss" and runs the pipeline.

## Pipeline (per page, run in this order)

1. `scripts/cut_pages.py` (program): PDF → `pages/page-NNN.png` at 300 DPI, plus `page-NNN.txt` from the PDF text layer if there is one. Prefer the original PDF or InDesign file over scans, because its text is more exact.
2. `scripts/ocr_page.py` (program): Google Cloud Vision document text detection with language hints `bn` and `en`. Writes `output/page-NNN/ocr.json` with every word, its box and its confidence.
3. `layout-reader` agent: groups words into blocks (heading, body, caption, table, label) and adds font, size, bold, italic, colour, alignment and reading order.
4. `picture-saver` agent: finds pictures, icons, shapes and the background. It crops each one with `scripts/crop.py` into `images/` and writes a description of each.
5. `meaning-writer` agent: writes the page's purpose and its links to other pages, in 3–6 lines.
6. `scripts/rebuild.py` (program): redraws the page from `page.json` as `rebuild.png` and scores it against the original with SSIM. It writes the score to `log.csv`.
7. `checker` agent: compares `page.json` with the page image and writes `report.md` with mistakes, doubts and a 0–100 confidence score. It never fixes anything.

Agent definitions live in `.claude/agents/*.md`. Each agent reads `schema.json` and writes only its own part of `page.json`.

## Rules that span files

- **Text comes only from OCR.** Claude may invent or alter Bangla letters, so `layout-reader` must copy text exactly from `ocr.json`. A suspect word goes into the `doubts` list instead of being corrected. Only the Checker or a human may change `text`.
- **`schema.json` is a fixed contract.** Never change it without telling everyone. Boxes are `[left, top, right, bottom]` in pixels from the top-left of the page image. `status` is one of `new`, `extracted`, `checked`, `needs_human`, `approved`; the pseudo-code also uses `redo`. Every image needs both a `file` and a `description`.
- **The Checker must be a separate agent** from the ones that produce the data. The same agent should never make and check its own work.
- **Pictures cannot be rebuilt from words.** Save the real crop as a file and also save its description.
- **Never skip a page.** Skip pages that are already `approved`.

## Thresholds and batching

- Process 5–10 pages per batch, never the whole book at once.
- Status by score: confidence ≥95 and SSIM ≥0.90 → `checked`. Confidence 90–94 or SSIM 0.85–0.89 → `needs_human`. Anything lower → `redo` once, then `needs_human` if it fails again. (The Step 6 prompt is simpler: confidence <90 or SSIM <0.85 → NEEDS HUMAN.)
- If 3 or more pages fail for the same reason, stop and fix the agent instructions, then rerun only the failed pages.
- Do a human spot-check of 1 random page in every 20. If any has mistakes, move to 1 in 10.
- Test on 5 varied pages first: text-heavy, picture-heavy, a table, a cover and an exercise page.

## Setup and commands

Python 3.11+ is required. Install the dependencies once:

```
pip install pymupdf pillow google-cloud-vision scikit-image
```

Google Cloud Vision needs an API key, and the key must never be pasted into chat or committed. Vision is paid after a free tier, so check the pricing and test on 5 pages first. Planned commands, none of which exist yet:

```
python scripts/cut_pages.py        # book PDF in input/ -> pages/
python scripts/ocr_page.py <image> # -> output/page-NNN/ocr.json
python scripts/rebuild.py          # -> rebuild.png + SSIM score in log.csv
```

The guide defines no lint or test commands. The 5-page test is the acceptance test.

## Expected layout per book

`input/` (the PDF), `pages/` (page images), `output/page-NNN/{page.json, ocr.json, images/, rebuild.png, report.md}`, `scripts/`, `.claude/agents/`, `schema.json`, `log.csv` (one row per page with status, confidence and SSIM).

Small Bangla marks such as ি ু ঁ and conjuncts such as ক্ষ and ন্ত are the most common errors. Scans below 300 DPI make them unreadable, so rescan at 400 DPI if they fail.
