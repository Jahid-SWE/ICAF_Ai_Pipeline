# Report page-002 (attempt 2)

(Saved by the Boss verbatim from the checker agent's text reply, because the checker's own write was refused.)

## Mistakes found
- i2: the crop contains the printed word "Working" (baked into the grey label box). t1 also holds "Working", so a rebuild would print the word twice. The crop should be the empty box, or the rebuild notes must say the word is removed.
- i3: the description and rebuild notes say it contains a green sofa, but the sofa is at the top right (about x 2280-2550, y 600-880), inside i1's box (y 0-1263), not i3's (y 1263-2870).
- Leftover [517,1503,2058,2602]: the grey street across the middle, the blue wall pieces and the small blue bollard near (1490, 2110) are not saved in any picture. The background is flat colour, so this scene content is lost. Real miss.
- Leftover [0,1255,538,1484]: the lower-left room below i1's cut (rug, blue wall, window edge) is not saved. Real miss.
- Leftover [2032,1255,2058,1427]: a thin wall sliver between i1 and i3 (gap x 2032-2050) is in no crop. Small real miss.

## Doubts
- t1 and t2 font names and sizes are guesses; t3 font size is a guess and its box edges are estimated.
- i2 box edges are judged by eye (about x 527-2030, y 1260-1731); they look right.
- The soft white glow behind the red heading t2 is a visual effect, not in the flat background. The text itself is correct.
- ocr_confidence is 1.0 for every block, but no OCR was run (no Google key).
- wordlist_missing is true, so unknown_words is empty only because the word list does not exist.
- The i5 lawn right edge is near straight at the top and angled below; the rebuild note is close enough.

## Leftover spots
- [0,1255,538,1484]: real miss (see Mistakes).
- [2032,1255,2058,1427]: real miss, small.
- [517,1503,2058,2602]: real miss.
- [330,1960,425,1997] and [442,1960,518,2031]: not a text miss; the halo behind the red heading (see Doubts).
- [0,2698,208,3106] and [158,2811,208,2850]: not a miss; plain sand and the lawn's lower edge.
- [2499,2862,2550,2919]: not a miss; the street's tail at the right edge, just below i3's box.

## Confidence
55
