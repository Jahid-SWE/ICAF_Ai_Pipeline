# Book Extraction Multi-Agent System — Build Guide

Nov 2, 2026 · @Peace Maker

## 1. What we are building

We are building a team of AI helpers (called **agents**) inside Claude Code. Together they read a book one page at a time and save everything on each page: the words, how the words look, the pictures and the background. Then a checker agent compares the saved data with the real page and marks mistakes.

**The team, in order:**

1. **Page Cutter** (a small program, not an AI): turns the book into one clear image per page.
2. **OCR Reader** (OCR tool): reads every letter on the page and notes where it sits. This is the first reader of the words.
3. **Layout Reader** (Claude, looking at the image): finds each text block and its box, plus headings, bold, colours, sizes and reading order. It does not type the words.
4. **Text Reader** (Claude, looking at one cut-out block at a time): types what it sees without seeing OCR or any other answer. This is the second, blind reader. It runs a third time only to break ties.
5. **Text Vote Program** (a small program, not an AI): compares the readers word by word and decides the final text.
6. **Picture Saver** (Claude + a small program): cuts out each picture as its own file, then writes what it shows, why it is there, and notes for redrawing it later.
7. **Score Program** (a small program, not an AI): uses maths to check that nothing was missed and that the cut-out pictures match the page.
8. **Checker** (a separate Claude): compares everything with the real page and lists mistakes.
9. **Boss** (main Claude Code session): runs all of the above, page by page, and keeps a log.

**Honest limit: 100% is only possible for text, not for pictures.** A picture cannot be redrawn exactly from words. So we save the real picture file AND its description. The file keeps it exact. The description keeps the meaning.

**Why do OCR and Claude both read the words?** OCR is good at exact letters but does not understand the page. Claude vision understands the page but sometimes changes or invents Bangla letters. So each one reads the words alone, without seeing the other's answer, and a small program compares them. If they differ, a second blind Claude read breaks the tie. If all three differ, a human decides.

**Additional Notes (for non Tech-guy):**

- **OCR** means "a tool that turns a picture of text into real, typeable text."
- **Agent** means "one AI helper with one job and its own written instructions."
- If you have the original PDF or InDesign file of the book, tell the developer first. Pulling text from that file is far more exact than reading a scanned image.

## 2. What you need before starting

Set up these things once. It takes about 1–2 hours.

| Item | Why you need it | How to get it |
| --- | --- | --- |
| A computer (Windows, Mac or Linux) | Runs everything | Any normal laptop works |
| Claude Code | Runs the agents | Install from Anthropic's Claude Code page; sign in with your Claude account |
| Python 3.11 or newer | Runs the small programs | python.org → Download |
| Google Cloud account + Vision API key | Best OCR for Bangla | console.cloud.google.com → turn on "Cloud Vision API" → make a key |
| The book as a PDF | The input | Best: the original PDF. Fallback: scan at 300 DPI or more |
| VS Code (optional) | Easy way to see and edit files | code.visualstudio.com |

**Make this folder layout** (one folder per book):

```
book-project/
  input/            ← put the book PDF here
  pages/            ← page images (made by Page Cutter)
  output/
    page-001/
      page.json     ← all saved info for this page
      images/       ← cut-out pictures
      blocks/       ← cut-out text blocks
      text_final.json ← the final words, after the vote
      votes.json    ← how each text block was decided
      report.md     ← Checker's list of mistakes
      leftovers.json ← spots the Score Program says were missed
  scripts/          ← small Python programs
  .claude/agents/   ← one instruction file per agent
  CLAUDE.md         ← rules for the Boss
  log.csv           ← one line per page: status and score
```

Install the Python tools by running this once in the terminal:

```
pip install pymupdf pillow google-cloud-vision scikit-image
```

**Additional Notes (for non Tech-guy):**

- The **terminal** is the black text window. On Windows, search "PowerShell". On Mac, search "Terminal".
- An **API key** is like a password that lets the program use Google's OCR. Keep it secret. Never paste it into a chat or share it.
- Google Vision is paid after a free amount. Check the current price on Google's pricing page before running a whole book. Test on 5 pages first.
- **DPI** means how sharp a scan is. 300 or more is good. Lower than 300 makes small Bangla marks (like ি, ু, ঁ) hard to read.

## 3. Build it, step by step

You do not need to write code by hand. In each step, open Claude Code inside the `book-project` folder and paste the prompt shown. Claude Code writes the file. You check that it works before moving on.

**Step 1 — Page Cutter (program).** Paste into Claude Code:

> Write scripts/cut\_pages.py. It opens the PDF in input/, saves each page as pages/page-001.png at 300 DPI, and also saves any text layer the PDF already has to pages/page-001.txt. Print how many pages were made.

Test: run `python scripts/cut_pages.py` and open 2–3 images. They must be sharp.

**Step 1b — Check the text layer (Bangla books).** Many Bangladeshi books are typed in Bijoy or SutonnyMJ fonts. Their hidden text comes out as nonsense, like "Avgvi" instead of "আমার". Paste:

> Write scripts/check\_text\_layer.py. For each pages/page-XXX.txt: if it has real Bangla Unicode letters, keep it. If it looks like Bijoy/ANSI text, convert it to Unicode with a Bijoy-to-Unicode converter and save page-XXX.unicode.txt. If it is empty or unreadable, write "no\_text\_layer" in log.csv so only OCR is used for that page.

Test: open 2 converted files and compare 3 lines with the page.

**Additional Notes (for non Tech-guy):** If the converted text still looks wrong, do not use it. OCR alone is safer than bad text.

**Step 2 — OCR Reader (program).** Paste:

> Write scripts/ocr\_page.py. Input: one page image. Send it to Google Cloud Vision (document text detection, language hint "bn" and "en"). Save every word with its box position and confidence score to output/page-XXX/ocr.json.

Test on 1 page. Open ocr.json and compare 3 lines by eye with the page.

**Step 3 — Write the page format.** Copy the JSON format from Section 4 of this doc into a file named `schema.json` in the main folder. Every agent must follow it. Do not change it later without telling everyone.

**Step 4 — Make the agent instruction files.** Each agent is one file in `.claude/agents/`. Paste:

> Create these agent files in .claude/agents/: layout-reader.md, text-reader.md, picture-saver.md, checker.md. Use the job descriptions below. Each must read schema.json. Each agent writes ONLY its own file: layout-reader writes layout.json, text-reader writes text\_a.json (or text\_b.json on the tiebreak run), picture-saver writes images.json, checker writes report.md. No agent edits page.json.

Then paste the four job descriptions:

- **layout-reader:** Look at the page image. You may look at ocr.json to see where words sit, but you must never write any words. Find every text block (heading, body, caption, table, label) and give it a box. Add font size, bold, italic, colour, alignment and reading order. If a block's edges are unclear, add it to the "doubts" list.
- **text-reader:** You are a blind reader. You see only the block images in blocks/ (or only the blocks listed in tiebreak.txt). Type exactly what is printed, letter by letter, in the same language and script. Keep the line breaks. Do NOT fix spelling. Do NOT guess missing letters. Do NOT make the sentence sensible. If a part is unreadable, write \[?\] there. Never open ocr.json, layout.json, page.json or any other file. Write text\_a.json, or text\_b.json when run for the tiebreak, like this: {"t1": "text", "t2": "text"}.
- **picture-saver:** Find every picture, icon, shape, border and background graphic. For each one save: its box position, its layer (what sits on top of what), rotation, see-through level, and which text boxes overlap it. Run scripts/crop.py to save each as its own PNG in images/. Write a description (what it shows), a purpose (why it is on the page), the style (photo, cartoon, line drawing and so on), the main colours as hex codes, and rebuild notes (line thickness, shadows, shapes, anything an artist needs to redraw it). Do the same for the page background colour or pattern. Describe only the visual object. Never write about the meaning of the page's text.
- **checker:** You did not make this data. Compare page.json with the page image line by line. Check every word, every picture box, every picture description and every style. Also read votes.json and leftovers.json. Look hardest at blocks marked voted or human, and at unknown\_words. Say if each leftover spot is a real miss. Write report.md with: mistakes found, doubts, and a confidence score from 0 to 100. Do not fix anything yourself.

**Step 4b — Text vote programs.** These steps decide what the words are. Two readers read the text alone, and a program compares them. A third read happens only when they disagree. Paste each prompt in turn:

> Write scripts/crop\_blocks.py. For one page, read layout.json and cut every text block out of the page image with 10 px of extra space around it. Save them as output/page-XXX/blocks/t1.png, t2.png and so on.

> Write scripts/vote\_text.py. For one page: (1) Take the OCR words from ocr.json and put each word into the text block whose box it sits in, in reading order. This is reader 1. (2) Read text\_a.json. This is reader 2. (3) Clean both texts the same way before comparing: Unicode NFC, one kind of space, one kind of quote mark and dash. Never change letters. (4) Compare the two texts word by word (use Python's difflib). Save text\_agreement = 1 minus (differing characters divided by all characters) into log.csv. (5) Blocks with no differences are marked "agreed". List every other block in output/page-XXX/tiebreak.txt. If tiebreak.txt is empty, write text\_final.json and votes.json now. (6) When text\_b.json exists, for each differing word keep the version that at least 2 of the 3 readers match, and mark that block "voted". If all 3 readers differ, mark the block "human" and keep reader 1's word with \[?\] in front. Then write text\_final.json and votes.json. (7) Check every word against scripts/bangla\_words.txt and list the words not found as unknown\_words in votes.json.

> Write scripts/bangla\_words.txt by downloading an open Bangla word list. Tell me which list you used and its licence before saving it.

The text-reader agent runs after crop\_blocks.py. If tiebreak.txt is not empty, the Boss runs the text-reader again, as a fresh run, on only the listed blocks. It saves text\_b.json, and vote\_text.py runs once more.

Test on 1 page: open votes.json. Most blocks should say "agreed". Then change one letter in text\_a.json by hand and run vote\_text.py again. That block must appear in tiebreak.txt.

**Additional Notes (for non Tech-guy):** *Blind* means a reader is never shown anyone else's answer, so it cannot copy a mistake. *Unicode NFC* means the same Bangla letter is saved the same way in both texts; without it the program would see fake differences. Two readers agreeing is strong proof, not perfect proof, so the 1-in-20 human check stays. The text-reader runs on every block, but the third read happens only on disagreements, which keeps token use low.

**Step 4c — Merge program.** Paste:

> Write scripts/merge\_page.py. It reads layout.json, images.json and text\_final.json for one page and joins them into page.json in the schema.json shape. If any file is missing, stop and write the page as "redo" in log.csv.

**Additional Notes (for non Tech-guy):** If three agents write into the same file, they erase each other's work. Separate files plus one merge step stops that.

**Step 4d — Score program (no AI).** This gives you scores from maths, not from Claude's opinion. Paste:

> Write scripts/check\_page.py. For one page it runs two checks with plain maths, no AI. (1) Coverage: take the page image and paint over every text box, image box and declared background graphic from page.json. Count the ink that is left (anything clearly different from the page background colour). Coverage = ink inside boxes divided by all ink. 1.00 means nothing was missed. Save every leftover ink spot as a box in output/page-XXX/leftovers.json. (2) Crop match: for each picture, compare images/iN.png with the same box on the page image using SSIM (scikit-image). Save the lowest score as crop\_ssim. If the page has no pictures, crop\_ssim is 1.0. Write coverage and crop\_ssim into log.csv.

Test: take one good page and delete one text block from its page.json by hand. Run the script. Coverage must drop and leftovers.json must show the missing spot.

**Additional Notes (for non Tech-guy):** These two scores do not prove the words are right. They prove nothing was missed and the picture crops are accurate. The limits (0.98 and 0.95) are starting guesses; tune them after your 5-page test. A true page-versus-page SSIM needs a rebuilt page, which we dropped for now.

**Step 5 — Boss rules.** Paste:

> Write CLAUDE.md. For each page in pages/, in this order: run ocr\_page.py; run the layout-reader agent; run crop\_blocks.py; run the text-reader agent; run vote\_text.py; if tiebreak.txt has any blocks, run the text-reader agent again as a fresh run on only those blocks, then run vote\_text.py again; run the picture-saver agent; run merge\_page.py; run check\_page.py; run the checker agent. Work in batches of 5 pages. Set each page's status by the pseudo-code in Section 5. Use only these status names: new, extracted, checked, redo, needs\_human, approved. Never skip a page. Never change schema.json. Never let one agent read another agent's answer, except the checker.

**Step 6 — Test on 5 pages only.** Pick 5 different kinds of pages (text-heavy, picture-heavy, a table, a cover, an exercise page). Fix problems before running the full book.

**Additional Notes (for non Tech-guy):**

- Always test one step before building the next. If you build everything first, you will not know which part broke.
- The Checker must be a separate agent. If the same agent makes and checks the work, it tends to approve its own mistakes.
- Save a copy of the whole folder (or use Git) after each working step, so you can go back if something breaks.

## 4. The page data format (schema.json)

Every page is saved in one file called `page.json`, always in this shape. Positions are in pixels from the top-left corner of the page image.

```
{
  "page": 1,
  "size": {"width": 2480, "height": 3508},
  "background": {
    "color": "#FFF8E7",
    "image_file": "images/bg.png",
    "description": "Light cream page with a green leaf border",
    "rebuild_notes": "Border is 60 px wide, leaf shapes repeat every 200 px, leaf colour #4A7C3A"
  },
  "text_blocks": [
    {
      "id": "t1",
      "type": "heading",
      "text": "অ – অজগর",
      "text_status": "agreed",
      "box": [200, 150, 1200, 320],
      "font": {"name": "SolaimanLipi", "size_pt": 36, "bold": true, "italic": false, "color": "#C0392B"},
      "align": "left",
      "order": 1,
      "ocr_confidence": 0.97
    }
  ],
  "images": [
    {
      "id": "i1",
      "file": "images/i1.png",
      "box": [1300, 150, 2200, 900],
      "kind": "illustration",
      "description": "A green snake curled in a circle, cartoon style, smiling",
      "purpose": "Shows the word for the letter অ",
      "style": "flat cartoon, thick dark outline, no shadow",
      "main_colors": ["#4CAF50", "#1B5E20", "#FFFFFF"],
      "layer": 2,
      "rotation_deg": 0,
      "opacity": 1.0,
      "overlaps_text": [],
      "rebuild_notes": "Outline about 8 px; eye is a white circle with a black dot; body has 3 lighter stripes"
    }
  ],
  "unknown_words": [],
  "doubts": ["t3: second word unclear, OCR says X, image may say Y"],
  "status": "checked"
}
```

`text_status` is one of: `agreed`, `voted`, `human`.

**Rules:**

- `box` is always `[left, top, right, bottom]`.
- `text` comes from the vote (votes.json). No single reader may write it. Only a human may change it afterwards.
- `status` is one of: `new`, `extracted`, `checked`, redo, `needs_human`, `approved`.
- Every image must have a `file`, a `description`, a `purpose` and `rebuild_notes`. These fields are for pictures and visual objects only. Text blocks get no purpose and no meaning.

**Additional Notes (for non Tech-guy):**

- **JSON** is just a neat way to write information so a computer can read it. Think of it like a form with labelled boxes.
- The colour code like `#C0392B` is a standard way to write an exact colour. Many free websites show the colour if you paste the code.

## 5. Running it and checking results

Once the 5-page test passes, run the whole book in parts. Do not run 200 pages at once.

1. Put the book PDF in `input/`.
2. Open the terminal in `book-project` and type `claude` to start Claude Code.
3. Type: **"Run pages 1 to 10 using the rules in CLAUDE.md."**
4. When it finishes, open `log.csv`. Each page shows a status and a score.
5. Open every page marked `needs_human`. Read its `report.md`, compare it with the original page, and fix the words in `page.json` by hand.
6. Change that page's status to `approved`.
7. Repeat for the next 10 pages.

**The same steps as pseudo-code:**

```
START
  PUT book.pdf INTO input/
  RUN cut_pages.py                      # makes pages/page-001.png ...
  RUN check_text_layer.py               # fixes Bijoy text, if any
  SET batch_size = 10
  SET all_pages = list of files in pages/

  FOR EACH batch OF batch_size pages IN all_pages:

      FOR EACH page IN batch:
          IF page.status == "approved":
              SKIP this page             # never redo finished work

          RUN ocr_page.py ON page        # -> ocr.json (reader 1)
          RUN agent layout-reader        # -> layout.json (boxes + styles, no words)
          RUN crop_blocks.py             # -> blocks/t1.png ...
          RUN agent text-reader          # -> text_a.json (reader 2, blind)
          RUN vote_text.py               # -> tiebreak.txt, text_agreement
          IF tiebreak.txt is not empty:
              RUN agent text-reader AGAIN    # fresh run, only the listed blocks -> text_b.json
              RUN vote_text.py               # -> text_final.json, votes.json
          RUN agent picture-saver        # -> images.json + images/
          RUN merge_page.py              # -> page.json
          RUN check_page.py              # -> coverage, crop_ssim, leftovers.json
          RUN agent checker              # -> report.md + confidence

          IF any text block is marked "human":
              SET page.status = "needs_human"
          ELSE IF confidence >= 95 AND coverage >= 0.98 AND crop_ssim >= 0.98 AND text_agreement >= 0.99:
              SET page.status = "checked"
          ELSE IF confidence >= 90 AND coverage >= 0.95 AND crop_ssim >= 0.95 AND text_agreement >= 0.97:
              SET page.status = "needs_human"     # small check
          ELSE:
              SET page.status = "redo"            # run again once
              IF page failed twice:
                  SET page.status = "needs_human"

          WRITE page, status, confidence, coverage, crop_ssim, text_agreement INTO log.csv

      # human part, after each batch
      FOR EACH page WITH status "needs_human":
          HUMAN opens report.md, votes.json, leftovers.json, original page, page.json
          HUMAN fixes page.json by hand
          SET page.status = "approved"

      IF 3 OR MORE pages failed for the same reason:
          STOP
          FIX the agent instructions
          RERUN only the failed pages

  # final quality check
  PICK 1 random page out of every 20
  HUMAN checks each fully
  IF any spot-checked page has mistakes:
      FIX them, then check 1 in 10 pages instead

  IF every page is "approved" OR "checked":
      BACK UP the whole folder
      DONE
END
```

**Additional Notes (for non Tech-guy):** Read it top to bottom like a recipe. Lines starting with `#` are just notes, not steps. `FOR EACH` means "do this again for every item." `IF ... ELSE` means "choose a path based on the score."

**How to read the scores:** a page is `checked` only if all four scores are Good and no text block is marked human.

| Score | Good | Check by hand | Redo |
| --- | --- | --- | --- |
| Checker confidence (0–100) | 95 or more | 90–94 | Below 90 |
| Coverage (0–1, no AI) | 0.98 or more | 0.95–0.97 | Below 0.95 |
| Crop match, SSIM (0–1, no AI) | 0.98 or more | 0.95–0.97 | Below 0.95 |
| Text agreement, OCR vs blind Claude (0–1, no AI) | 0.99 or more | 0.97–0.98 | Below 0.97 |

**Human spot-check, even on "good" pages:** pick 1 page out of every 20 at random and check it fully. This tells you if the system is fooling itself.

**Additional Notes (for non Tech-guy):**

- `log.csv` opens in Excel or Google Sheets. Sort by status to see problem pages first.
- Bangla joined letters (যুক্তবর্ণ like ক্ষ, ন্ত) and vowel signs are the most common mistakes. Check those first.
- If many pages fail for the same reason, do not fix them one by one. Tell the developer; the agent instructions need a fix.

## 6. Common problems and fixes

| Problem | Likely cause | Fix |
| --- | --- | --- |
| Bangla letters wrong or broken | Low scan quality, or Claude retyped text | Rescan at 400 DPI; check votes.json; make sure text-reader saw only the block images |
| Words in wrong order | Two-column page or text around a picture | Ask layout-reader to number columns first, then lines |
| Picture cut too small or too big | Box guessed wrong | check\_page.py flags it (low crop match or leftovers.json); fix the box numbers by hand and run crop.py again |
| Claude Code stops halfway | Too many pages at once | Run 5–10 pages per batch |
| "API key" error | Key missing or wrong | Ask the developer to check the key setting; never paste the key in chat |
| Cost getting high | Running full book many times | Only rerun failed pages, not the whole book |

**Final checklist before calling a book "done":**

- [ ] Every page has `page.json`, `images/` and `report.md`
- [ ] No page left as `needs_human`
- [ ] Random 1-in-20 spot-check done and passed
- [ ] Every image has a file, a description, a purpose and rebuild notes
- [ ] Whole folder backed up

**Additional Notes (for non Tech-guy):**

- When stuck, copy the exact error message into Claude Code and ask "What does this mean and how do I fix it?" It usually solves it.
- Ask the developer for help only when the same problem happens on 3 or more pages.
