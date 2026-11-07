# Report page-001 (attempt 2)

(Saved by the Boss verbatim from the checker agent's text reply, because the checker's own write was refused.)

## Mistakes found
- i1 description: says "three plates of rice with side dishes". The page shows two rice plates (left and right). The plate at top centre is roti, not rice.
- i1 description: says "four metal cups". The page shows five metal cups (top left, upper right, lower left, bottom centre, lower right).

## Doubts
- votes.json has wordlist_missing: true (scripts/bangla_words.txt is absent), so unknown_words could not be checked against a word list. The Bangla words were checked by eye only and match the image.
- page.json ocr_confidence 1.0 on t1 and t2 comes from the old Google Vision step, which is not run now. The value has no meaning here.
- Background colour #F8D0A4 and the faint light streaks cannot be measured exactly. The streaks are not ink, so they are not a leftover.
- Box edges for t1, t2 and i1 were checked by eye at display scale. Nothing is cut off; the boxes contain all visible text and the whole illustration, within a few tens of pixels.
- Font names and sizes cannot be verified from the image.

## Leftover spots
- none listed in leftovers.json; no missed ink seen on the page.

## Confidence
85
