# Report page-005 (attempt 2)

(Saved by the Boss verbatim from the checker agent's text reply, because the checker's own write was refused.)

## Mistakes found
- background (sky): the upper part of the page (y 0 to about 949) is a blue sky with white clouds, a tree at the top-left and a tree at the top-right. It is not saved as any file. bg.png is sand only, so the sky is missing from the rebuild. Leftover box [0, 0, 2550, 949] is a real miss.
- background (sand): the sand ground between the building steps and the text (about y 2111 to 2915) has soft shadow patches and speckles. Only a sand colour is recorded, and bg.png is the text-free strip below the last line. The shadow patches in the middle are a real miss (leftovers such as [0, 2111, 1768, 2915] and [1426, 2934, 2550, 3270]).
- i1 / i2 / i3 (flagpole): the pole shaft between the flag bottom (y about 941) and the base (y about 2119) is in no crop. Leftover [1343, 933, 1382, 2127] is a real miss, as page.json's own doubts say.
- i5 (top-left tree): the description covers the top-left tree, but the lower left-edge tree (about y 940 to 1280) sits in i2's box, and i2 only says "a tree at the top". Small mismatch, not serious.

## Doubts
- All six text lines are agreed by 2 readers, but votes.json has wordlist_missing true, so unknown_words is empty because the word list did not run, not because words were checked. The lines were checked by eye against the image and match.
- Font name and size_pt are estimates; t1 weight could be regular or medium.
- Box edges were judged by eye at display scale x1.64; margins look like 20 to 30 px, which matches the image.
- Small leftovers at y 2382 to 2423 across the full text width (between the t2 and t3 boxes) may be the bottom of line 1 or sand shadow. Could not decide.
- Tiny chalk writing on the blackboard and the wall map are inside i2/i3, not separate text. Too small to read here.
- No page number is visible on this page.
- bg.png exists but is not listed in images.json.

## Leftover spots
- [0, 0, 2550, 949]: real miss. Sky with clouds and trees, not saved.
- [1343, 933, 1382, 2127]: real miss. Flagpole shaft between i2 and i3.
- [1694, 2103, 2550, 2987]: partly a miss. Right boundary wall and bushes below i6, and sand shadow on the right.
- [0, 2111, 1768, 2915]: partly a miss. Sand ground with shadows between the steps and the text.
- [698, 2382, 1736, 2423] and [1738, 2387, 1846, 2423]: could not decide (see doubts).
- [268, 2844, 1212, 3270] and [1426, 2934, 2550, 3270]: sand texture and shadow. Real miss only for the shadow patches.
- Small spots near the text and at the page edges: sand speckles or anti-aliasing, not a miss.

## Confidence
35
