# Book

## Page 1

Status: approved | Confidence: 85.0 | Size: 2550x3270 px

### Background

Colour #F8D0A4. Warm peach page background with a few faint lighter diagonal light streaks on the left and right edges
Rebuild notes: Flat peach colour across the page; faint pale light rays from upper left and along the left and right edges, no pattern and no printed text. Plain colour used because the streaks are very faint.

### Text

আমি ও আমার পরিবার

_t1 | heading | box [630, 185, 1920, 385] | agreed | read-agreement 1.0 | SolaimanLipi 36 pt | bold yes | italic no | colour #E31E24 | align center | order 1_

আমি নাবিল। আমার বোন নুহা। এই আমার বাবা, এই আমার মা। এই আমার দাদি। আমার দাদা বাড়িতে নেই। এই আমার পরিবার। আমরা সবাই একসাথে থাকি।

_t2 | body | box [215, 2385, 2360, 3065] | agreed | read-agreement 1.0 | SolaimanLipi 30 pt | bold no | italic no | colour #1B1B1B | align center | order 2_

### Pictures

- i1 | illustration | file [images/i1.png](../work/page-001/images/i1.png) | box [110, 620, 2425, 2250] | layer 2 | rotation 0 | opacity 1.0 | overlaps text: none
  - Description: A 3D-style rendered overhead view of a family sitting at a wooden dining table: a woman in a beige headscarf and sage-green sleeves on the upper right, a small boy in blue on the left, a girl in purple pyjamas on the right, and a boy in a white shirt and a woman in a pink patterned headscarf seated at the bottom. Six wooden chairs surround the table. On the table are a pot of yellow dal with a ladle, a plate of flatbread (roti), a bowl of fruit (bananas and apples), a bowl of cooked vegetables, a plate of cucumber and tomato, three plates of rice with side dishes, and four metal cups.
  - Purpose: Shows the family sitting together at the meal, as the picture for the page
  - Style: photorealistic-style 3D render, soft even lighting, soft shadows under the chairs and table, no outline
  - Main colours: #E0A24A, #F7E7CF, #2B7BD6, #8E4FA3, #F4F2EE, #C9708C, #D9B07A, #F0C94A, #D63A2F
  - Rebuild notes: One crop of the whole scene (table, six chairs, people and food together). The people, chairs and food are not saved as separate pictures because they sit in one scene and touch each other. Include the chair shadows at the bottom. The scene has no printed text. The table is a warm orange wood with plank lines. Each person is seen from above and behind.

### Doubts and unknown words

- doubt: t1: font name and size are a guess from the image
- doubt: t2: font name and size are a guess; box covers 4 lines, top and bottom margins set at about 30 px by eye
- doubt: t2: the four lines may need splitting into separate blocks if the vote fails on line breaks
- doubt: Background colour #F8D0A4 is estimated by eye from the image; check against the real page
- doubt: The faint light streaks on the background were left out (image_file null); a checker may want them as bg.png if they matter
- doubt: The illustration box was set by eye from the displayed image (scale 1.64); the chair edges and shadows at the bottom should be checked against the crop

## Page 2

Status: approved | Confidence: 55.0 | Size: 2550x3270 px

### Background

Colour #F9D98C. Warm sandy-yellow ground behind the house scene and the lower text area
Rebuild notes: Flat warm sand colour with a soft lighter patch near the lower middle; no printed text. Bottom-middle is a pale grey-white street, which is part of the scene picture i3 and the top scene i1, not the background

### Text

Working

_t1 | heading | box [690, 1310, 1870, 1700] | agreed | read-agreement 1.0 | Serif (English display) 72 pt | bold no | italic no | colour #231F20 | align center | order 1_

আমাদের বাড়ি

_t2 | heading | box [510, 1850, 1300, 2070] | agreed | read-agreement 1.0 | SolaimanLipi 36 pt | bold yes | italic no | colour #E0202A | align center | order 2_

এটা আমাদের বাড়ি। শোবার ঘরে আমরা ঘুমাই। খাবার ঘরে আমরা খাই। মেহমানের ঘরে মেহমান বসেন। বাথরুমে হাত-মুখ ধুই। বারান্দায় খেলি।

_t3 | body | box [200, 2069, 1630, 3113] | agreed | read-agreement 1.0 | SolaimanLipi 28 pt | bold no | italic no | colour #231F20 | align center | order 3_

### Pictures

- i1 | illustration | file [images/i1.png](../work/page-002/images/i1.png) | box [0, 0, 2550, 1263] | layer 2 | rotation 0 | opacity 1.0 | overlaps text: none
  - Description: Isometric 3D cutaway of a family house: several rooms with beds, a pink desk and chair, a green wardrobe, a wooden dining table with six chairs, a bathroom toilet, rugs and blue-grey walls, seen from above
  - Purpose: Full-page scene that sets the story setting above the title
  - Style: photo-like 3D render, soft shading, no outlines, soft shadows on the floor
  - Main colours: #F3D9A4, #8FA0D6, #C9793A, #F5B8C0, #4E7A4E, #FFFFFF
  - Rebuild notes: Bottom edge is cut at the top of the grey label box, so the lower rooms and street continue in i3 and the lower-left rooms are cut through. Contains the pink desk, green wardrobe, dining set and bed pieces, all part of this one scene (no separate pictures cropped from it)
- i2 | shape | file [images/i2.png](../work/page-002/images/i2.png) | box [530, 1263, 2040, 1738] | layer 3 | rotation 0 | opacity 0.5 | overlaps text: t1
  - Description: Semi-transparent dark grey rectangle with the English word Working printed in large black serif letters across it
  - Purpose: Label box that holds the English heading over the scene
  - Style: flat grey, about 50% opacity, sharp corners, no outline
  - Main colours: #6E6E6E, #231F20
  - Rebuild notes: The word Working is printed on this box and is text (heading t1), not part of the picture; it is included in the crop only because it sits on the box. Box edges are estimated by eye. Behind the box the scene shows through
- i3 | illustration | file [images/i3.png](../work/page-002/images/i3.png) | box [2050, 1263, 2550, 2870] | layer 2 | rotation 0 | opacity 1.0 | overlaps text: none
  - Description: Right-hand part of the house scene: the lower-right bedroom with a bed with a red blanket and a rug, a green sofa, and a pale grey-white street running diagonally
  - Purpose: Continues the house scene down the right edge
  - Style: photo-like 3D render, soft shading
  - Main colours: #F4E3C4, #C9793A, #D9454F, #4E7A4E, #E4E0E0
  - Rebuild notes: Cut along a vertical line at x 2050; the lighter street and wall in the middle of the page (x 1100 to 2050) are not cropped and stay in the background/scene, so this crop is only the right edge. Contains a bed and a sofa that are part of this scene
- i4 | illustration | file [images/i4.png](../work/page-002/images/i4.png) | box [0, 1476, 525, 1968] | layer 2 | rotation 0 | opacity 1.0 | overlaps text: none
  - Description: Cluster of pink flowering shrubs with dark green leaves at the left edge
  - Purpose: Decorates the lower-left corner beside the text
  - Style: photo-like 3D render, soft shading
  - Main colours: #E0479A, #2F5A2A, #7DB35A
  - Rebuild notes: Several dozen small pink blossoms on dark green bushes, in a loose cluster
- i5 | illustration | file [images/i5.png](../work/page-002/images/i5.png) | box [0, 1952, 330, 2706] | layer 2 | rotation 0 | opacity 1.0 | overlaps text: none
  - Description: Green grass lawn patch at the left edge of the ground
  - Purpose: Decorates the lower-left ground
  - Style: photo-like 3D render, soft shading
  - Main colours: #6FAE4A, #3E7A2E
  - Rebuild notes: Solid green lawn with a straight right edge and a rounded bottom edge

### Doubts and unknown words

- doubt: t1: English heading 'Working' sits on a grey translucent box; box edges are a judgement by eye
- doubt: t1: font name and size are guesses
- doubt: t2: font name and size are guesses; the red title has a light glow behind it
- doubt: t3: six Bangla lines in one block; line 1 top and line 6 bottom are estimated, font size is a guess
- doubt: i1 and i3 are cut through rooms and the street at the edges, so the scene is in several pieces; box edges are estimated by eye
- doubt: i2 box edges are estimated; the word Working is printed on the box (t1), so the crop contains text
- doubt: background colour is a guess from the sand colour; the street at the middle is not cropped and may need a separate picture or a redraw
- doubt: the lower-middle and bottom sand area is plain background; no separate crop was made

## Page 3

Status: approved | Confidence: 55.0 | Size: 2550x3270 px

### Background

Colour #8FC9EC. Full-page illustration of a sunny school scene. Sky is light blue with white cumulus clouds at the top; the lower page is a warm sand-coloured paved ground. The page's scene is drawn in a 3D-style cartoon (soft lighting, realistic-looking shading).
Rebuild notes: No background crop saved: the sky and sand ground contain printed text (title in the sky, three body lines on the sand), so no text-free crop exists. Sky: top ~270 px of the page, blue gradient to pale near horizon, clouds at left top and right top, one small cloud near the flag. Ground: sand/peach #E8C49A-like flat tone with soft shadows under the children and the gates. Grass lawn sits between the building and the ground (y about 1100-1300 at display scale, roughly 1800-2100 px original). Left and right brick pillar bases are brick red #A4553A with cream plaster above.

### Text

আমাদের স্কুল

_t1 | heading | box [890, 200, 1660, 407] | agreed | read-agreement 1.0 | unknown Bangla font 42 pt | bold no | italic no | colour #000000 | align center | order 1_

এটা আমাদের স্কুল। আমাদের স্কুল ভালো।

_t2 | body | box [320, 2560, 2240, 2720] | agreed | read-agreement 1.0 | unknown Bangla font 30 pt | bold no | italic no | colour #000000 | align center | order 2_

স্কুলের মাঠ সুন্দর। আমি ছাত্র। নুহা ছাত্রী।

_t3 | body | box [306, 2742, 2236, 2900] | agreed | read-agreement 1.0 | unknown Bangla font 30 pt | bold no | italic no | colour #000000 | align center | order 3_

আমরা স্কুলে যাই। স্যার আমাদের পড়ান।

_t4 | body | box [350, 2881, 2203, 3064] | agreed | read-agreement 1.0 | unknown Bangla font 30 pt | bold no | italic no | colour #000000 | align center | order 4_

### Pictures

- i1 | illustration | file [images/i1.png](../work/page-003/images/i1.png) | box [1484, 500, 1763, 1419] | layer 2 | rotation 0 | opacity 1.0 | overlaps text: none
  - Description: A tall silver-grey flagpole with a Bangladesh flag: green field with a red disc, flying to the right. Pole has a small gold finial at the top.
  - Purpose: Stands in the middle of the scene as the focal point above the courtyard
  - Style: 3D cartoon render, soft shading, slight highlight on the pole
  - Main colours: #C9CED3, #1B6B3A, #E0202E, #F2C14E
  - Rebuild notes: Pole is thin (about 14 px wide original). Flag is about 150 by 110 px display, red disc about 40 percent of flag height and centred slightly left of middle. Crop includes a small piece of sky and building behind the pole; the pole base sits in a round flower bed (included at the bottom edge).
- i2 | illustration | file [images/i2.png](../work/page-003/images/i2.png) | box [722, 1414, 1509, 2332] | layer 4 | rotation 0 | opacity 1.0 | overlaps text: none
  - Description: Two young children seen from behind, walking away towards the school gate. Left child: short black hair, white shirt, blue backpack with a gold diamond badge, navy trousers, white shoes. Right child: white headscarf, white long-sleeved top, navy skirt, white socks, black shoes, pink backpack with a floral pattern and a gold diamond badge.
  - Purpose: The two main characters of the scene, walking into the school
  - Style: 3D cartoon render, soft lighting, cast shadows on the ground
  - Main colours: #1F3A8A, #2B5BB5, #F4A7C3, #FFFFFF, #111111, #F2C14E
  - Rebuild notes: Front-most figures. Ground shadows under both children are included at the bottom of the crop. Backpack straps and the gold diamond badges are small (about 40 px). Pink backpack has a floral print in pale pink and green.
- i3 | illustration | file [images/i3.png](../work/page-003/images/i3.png) | box [1862, 1115, 2419, 1451] | layer 2 | rotation 0 | opacity 1.0 | overlaps text: none
  - Description: Children's playground set: a red slide with a yellow handrail, a blue metal frame with two swings, and a red and yellow canopy on the top of the slide.
  - Purpose: Shows the play area on the right of the school grounds
  - Style: 3D cartoon render, glossy plastic look
  - Main colours: #E0202E, #F2C14E, #2B5BB5, #B0B8C0
  - Rebuild notes: Blue frame: two upright poles and a crossbar, two swing seats hanging on chains. Red slide is angled to the lower right. Crop includes a few green bushes at the base.
- i4 | illustration | file [images/i4.png](../work/page-003/images/i4.png) | box [151, 1246, 358, 2214] | layer 3 | rotation 0 | opacity 1.0 | overlaps text: none
  - Description: Left school gate: a tall brown metal gate with vertical bars, hinged to a cream plaster pillar with a brick-red lower section. Gate is opened outwards.
  - Purpose: Frames the school entrance on the left
  - Style: 3D cartoon render, dark metal bars with light edge highlights
  - Main colours: #5A4A3F, #A4553A, #F3EBDD
  - Rebuild notes: Gate has about 9 vertical bars and two horizontal rails. Bottom of the crop is at the paved ground level. The crop does not include the left pillar, which is part of the building scene (i7).
- i5 | illustration | file [images/i5.png](../work/page-003/images/i5.png) | box [2283, 1246, 2480, 2214] | layer 3 | rotation 0 | opacity 1.0 | overlaps text: none
  - Description: Right school gate: a tall brown metal gate with vertical bars, hinged to a cream plaster pillar with a brick-red lower section. Gate is opened outwards.
  - Purpose: Frames the school entrance on the right
  - Style: 3D cartoon render, dark metal bars with light edge highlights
  - Main colours: #5A4A3F, #A4553A, #F3EBDD
  - Rebuild notes: Mirror of i4: same bar count and rails. The crop does not include the right pillar.
- i6 | illustration | file [images/i6.png](../work/page-003/images/i6.png) | box [381, 1312, 853, 1578] | layer 2 | rotation 0 | opacity 1.0 | overlaps text: none
  - Description: Three children in white shirts and navy shorts on a green lawn: two run on the left, one stands kicking, and a black-and-white football lies on the grass in front of them.
  - Purpose: Shows other pupils playing football on the field behind the children
  - Style: 3D cartoon render, small figures, soft shadows
  - Main colours: #FFFFFF, #1F3A8A, #111111, #4CAF50, #7CC04A
  - Rebuild notes: Figures are about 80 px tall at this scale. Ball is about 30 px diameter with black pentagons. Crop includes grass and a small patch of the lawn border at the bottom.
- i7 | illustration | file [images/i7.png](../work/page-003/images/i7.png) | box [0, 443, 1484, 1255] | layer 1 | rotation 0 | opacity 1.0 | overlaps text: none
  - Description: The left and centre part of the two-storey school building: cream plaster walls, flat roof with a deep overhang, columns, windows with brown frames, balconies with railings, brown wooden doors, blue plinth at the base, a small green tree and shrubs in front.
  - Purpose: Forms the back wall of the school courtyard
  - Style: 3D cartoon render, architectural, soft lighting
  - Main colours: #F3EBDD, #D9CDB8, #8B5E3C, #2B5BB5, #4CAF50
  - Rebuild notes: Contains the flagpole base area on its right edge (the flagpole i1 is saved separately, so the crop only includes its base shadow). Left pillar and the top of the left gate (i4) sit on the left edge of this crop. The crop does not include the title text, which is in the sky above this crop. Shrubs and tree in front of the building are included.
- i8 | illustration | file [images/i8.png](../work/page-003/images/i8.png) | box [1755, 861, 2460, 1255] | layer 1 | rotation 0 | opacity 1.0 | overlaps text: none
  - Description: The right part of the school building: cream walls, a row of windows with blue glass, brown doors, white railings on the balconies, and a blue plinth at the base.
  - Purpose: Forms the back wall of the school courtyard on the right side
  - Style: 3D cartoon render, architectural, soft lighting
  - Main colours: #F3EBDD, #2B5BB5, #8B5E3C, #D9CDB8
  - Rebuild notes: Crop starts just right of the flagpole. Bottom edge is at the lawn line. Right edge touches the right gate pillar (i5 is saved separately).

### Doubts and unknown words

- doubt: t1: font name and size are guesses from the image; box edges estimated by eye from a downscaled view (display 1559x2000 mapped to 2550x3270 by x1.64)
- doubt: t2-t4: body lines are placed as one block per line; font name and size are guesses
- doubt: Page size taken from the original image dimensions (2550x3270); confirm against pages/page-003.png if the saved PNG differs
- doubt: No background crop: the sky and sand ground both contain printed text, so bg.png cannot be made without text. image_file is null and the scene is described in rebuild_notes instead.
- doubt: i1 (flag pole) and i7/i8 (building) touch: a small piece of building is inside the flagpole box and the base of the flagpole sits on the building crop edge. Check the seam.
- doubt: i4/i5 (gates) and i7/i8 (building) touch at the top edge of the gates: the pillars sit in the building crops. Pillars are in i7 (left) and the right pillar is partly in i8.
- doubt: Box edges are estimated by eye from a downscaled view (display 1559x2000 mapped to 2550x3270 by x1.64). Confirm the crop edges against the page image; crops may be a few px short or long.
- doubt: The scene is one connected illustration split into objects. Some pixels are shared between neighbouring crops (lawn, grass, shadows). This is a deliberate choice so no object is cut in half.

## Page 4

Status: approved | Confidence: 70.0 | Size: 2550x3270 px

### Background

Colour #8EC8F0. Full-page outdoor scene: blue sky with white clouds at top, sandy brown ground at bottom, river and green trees behind. Printed text sits over the sky (top) and over the sand (bottom).
Rebuild notes: Sky is light blue #8EC8F0 fading to paler blue near the horizon; ground is sandy orange-brown #E8B873. The scene contains the flag and pole (i1), the boat (i2) and the house at the left edge (i3), which are saved separately and not repeated here. The remaining landscape (banana trees, bamboo fence, bushes, river, distant tree line, grass strip) is not cropped as a separate picture; it cannot be cut out without also cutting the pictures above or the text.

### Text

আমাদের দেশ, আমাদের পতাকা

_t1 | heading | box [420, 190, 2130, 375] | agreed | read-agreement 1.0 | unknown Bangla sans (guess) 36 pt | bold yes | italic no | colour #000000 | align center | order 1_

আমাদের দেশ বাংলাদেশ। আমরা দেশকে ভালোবাসি। এই আমাদের পতাকা। পতাকার রং লাল আর সবুজ । আমাদের পতাকা সুন্দর।

_t2 | body | box [220, 2560, 2330, 3060] | agreed | read-agreement 1.0 | unknown Bangla sans (guess) 30 pt | bold no | italic no | colour #000000 | align center | order 2_

### Pictures

- i1 | illustration | file [images/i1.png](../work/page-004/images/i1.png) | box [828, 582, 1476, 2244] | layer 2 | rotation 0 | opacity 1.0 | overlaps text: none
  - Description: A tall metal flagpole standing on a two-step grey-white concrete base, with the Bangladesh flag flying from the top: dark green field with a red disc slightly left of centre.
  - Purpose: Central focal picture of the page, shows the national flag the page is about
  - Style: photo-realistic, soft natural lighting, slight folds in the flag cloth
  - Main colours: #006A4E, #F42A41, #B8A27A, #9C9C9C
  - Rebuild notes: Pole is thin and pale brass/grey, about 10 px wide in the crop; red disc is centred roughly at 45% of the flag width; flag is waving to the right. Box includes the plants and river behind the pole base, which are part of the background scene.
- i2 | photo | file [images/i2.png](../work/page-004/images/i2.png) | box [2168, 1752, 2550, 1829] | layer 2 | rotation 0 | opacity 1.0 | overlaps text: none
  - Description: A small wooden river boat with a dark grey canopy over the middle, with one person standing at the back, on brown river water.
  - Purpose: Adds a small detail of river life to the right side of the scene
  - Style: photo-realistic, small and distant
  - Main colours: #3E3A36, #6E6A63, #8A7558
  - Rebuild notes: Boat is about 230 px long and 50 px high in the crop; the canopy is a rounded grey metal shape; the person is at the stern on the right.
- i3 | photo | file [images/i3.png](../work/page-004/images/i3.png) | box [0, 910, 426, 2788] | layer 2 | rotation 0 | opacity 1.0 | overlaps text: none
  - Description: The left edge of the scene: a corner of a small building with a sloped corrugated roof and a light grey concrete pillar, plus its concrete step at the bottom.
  - Purpose: Frames the left side of the scene as the edge of a house
  - Style: photo-realistic, cut off by the page edge on the left
  - Main colours: #D9D6CF, #7A6A55, #8C8C8C
  - Rebuild notes: Roof is a dark sloped edge running from top-left to right; pillar is pale grey and about 40 px wide; the bottom steps are at the foot of the crop. Box includes some banana leaves and bushes at the right edge of the crop which are part of the background scene.

### Doubts and unknown words

- doubt: t1: font name and size are a guess by eye (heading over the sky, black on blue)
- doubt: t2: font name and size are a guess by eye; 3 centred lines in one block, box made wide and tall for the top and bottom margins
- doubt: t1: box top edge chosen with extra margin above the headmarks; scale taken from the displayed size (1559x2000) to the real image (2550x3270)
- doubt: t2: block ends near the bottom of the last line (the lower margin is about 30 px)
- doubt: Background: the landscape between the pictures (river, banana trees, bamboo fence, bushes, grass strip, distant trees) is not saved as a separate image. It cannot be cut out without also cutting the flag, boat or house, so background image_file is null. A human should decide whether to keep it as one image with holes.
- doubt: i1 and i3 boxes include small pieces of the background scene (plants, river, leaves) inside the rectangle; these are not pictures of their own.
- doubt: Box edges are estimated from the displayed image (scale 1.64); check that the boat box and the house box include the whole object.

## Page 5

Status: approved | Confidence: 35.0 | Size: 2550x3270 px

### Background

Colour #F2D9A6. Sandy beige schoolyard ground with soft shadows of trees; below the last text line it is plain sand with a faint speckled pattern
Rebuild notes: Sand colour about #F2D9A6 with lighter and darker speckles and soft blurred shadow patches on the upper half. The upper part of the page is a blue sky with white clouds (not saved as a crop; see doubts). Crop bg.png is only the text-free sand strip below the last text line.
File: [images/bg.png](../work/page-005/images/bg.png)

### Text

আমাদের দেশ, আমাদের পতাকা

_t1 | heading | box [425, 190, 2120, 382] | agreed | read-agreement 1.0 | unknown Bangla sans 30 pt | bold no | italic no | colour #000000 | align center | order 1_

আমাদের দেশ বাংলাদেশ।

_t2 | body | box [700, 2255, 1845, 2390] | agreed | read-agreement 1.0 | unknown Bangla sans 24 pt | bold no | italic no | colour #000000 | align center | order 2_

আমরা দেশকে ভালোবাসি।

_t3 | body | box [685, 2415, 1860, 2550] | agreed | read-agreement 1.0 | unknown Bangla sans 24 pt | bold no | italic no | colour #000000 | align center | order 3_

এই আমাদের পতাকা।

_t4 | body | box [780, 2585, 1765, 2720] | agreed | read-agreement 1.0 | unknown Bangla sans 24 pt | bold no | italic no | colour #000000 | align center | order 4_

পতাকার রং লাল আর সবুজ ।

_t5 | body | box [605, 2750, 1950, 2885] | agreed | read-agreement 1.0 | unknown Bangla sans 24 pt | bold no | italic no | colour #000000 | align center | order 5_

আমাদের পতাকা সুন্দর।

_t6 | body | box [730, 2915, 1815, 3065] | agreed | read-agreement 1.0 | unknown Bangla sans 24 pt | bold no | italic no | colour #000000 | align center | order 6_

### Pictures

- i1 | illustration | file [images/i1.png](../work/page-005/images/i1.png) | box [1309, 463, 1800, 941] | layer 3 | rotation 0 | opacity 1.0 | overlaps text: none
  - Description: Bangladesh national flag: dark green rectangle with a red circle, waving on a tall silver flagpole with a round ball finial at the top
  - Purpose: Shows the flag that the page title and poem are about
  - Style: photo-like digital painting, soft shading, no outline, slight fold shadows on the flag
  - Main colours: #006A4E, #F42A41, #C0C0C0, #FFFFFF
  - Rebuild notes: Flag is about 2:3 with the red disc slightly left of centre; flag edge is wavy. Pole is a thin silver shaft with a ball on top. Pole shaft below the flag (down to the base) is inside the building scene and is not part of this crop.
- i2 | illustration | file [images/i2.png](../work/page-005/images/i2.png) | box [0, 941, 1351, 2119] | layer 2 | rotation 0 | opacity 1.0 | overlaps text: none
  - Description: Left half of a one-storey school building: cream walls, pink roof edge, cream columns, a blue-framed window with grey grid bars, an open blue door showing a classroom with a green blackboard, students in white shirts and blue skirts at desks, potted plants, concrete steps, and a tree at the top
  - Purpose: Shows the school in the scene
  - Style: photo-like digital painting, soft light, no outline
  - Main colours: #F5DEB3, #E9867A, #2F6FB0, #2E7D32, #1F4E23, #FFFFFF
  - Rebuild notes: Building is one storey with a flat pink-edged roof. Pillars are cream. Blue wood doors and window frames. Chalkboard on the classroom wall has tiny chalk writing and a small map drawing; it is too small to redraw as text. The classroom door at the centre-right of this crop is open. The flagpole base and the flower bed in front are not in this crop (see i4). The tree at the top of this crop is part of the sky scene.
- i3 | illustration | file [images/i3.png](../work/page-005/images/i3.png) | box [1374, 941, 2021, 2119] | layer 2 | rotation 0 | opacity 1.0 | overlaps text: none
  - Description: Right half of the school building: a blue-framed window with a classroom behind it, a green blackboard and a wall map poster, an open blue door with students at desks, potted plants, and the cream end wall with its pink roof edge
  - Purpose: Shows the school in the scene
  - Style: photo-like digital painting, soft light, no outline
  - Main colours: #F5DEB3, #E9867A, #2F6FB0, #2E7D32, #FFFFFF
  - Rebuild notes: Same style as i2. Blue door at the right of the building is open. A map poster hangs on the cream wall to the left of the door. The flagpole passes in front of the building left edge of this crop; the pole itself is not in this crop.
- i4 | illustration | file [images/i4.png](../work/page-005/images/i4.png) | box [965, 2119, 1857, 2184] | layer 4 | rotation 0 | opacity 1.0 | overlaps text: none
  - Description: Round pale stone base ring around the flagpole with a flower bed of green and red-orange plants in front of the building steps
  - Purpose: Frames the base of the flagpole
  - Style: photo-like digital painting
  - Main colours: #D8CFC0, #4E8F3A, #E0523A, #2E7D32
  - Rebuild notes: Only the bottom strip of the base ring and flower bed. The top of the flower bed is in i2 and i3. The flagpole base (grey square plinth) is at the centre of this crop.
- i5 | illustration | file [images/i5.png](../work/page-005/images/i5.png) | box [0, 82, 180, 941] | layer 1 | rotation 0 | opacity 1.0 | overlaps text: none
  - Description: Leafy green tree branches at the top-left edge of the page, cut off by the page edge
  - Purpose: Frames the top-left corner of the scene
  - Style: photo-like digital painting
  - Main colours: #4E8F3A, #7CB342, #2E7D32, #87CEEB
  - Rebuild notes: Tree is cut by the left page edge. Light blue sky behind it.
- i6 | illustration | file [images/i6.png](../work/page-005/images/i6.png) | box [2021, 491, 2550, 2111] | layer 1 | rotation 0 | opacity 1.0 | overlaps text: none
  - Description: Right-hand trees and garden: large leafy trees, a palm tree in the distance, a small pink-roofed house on the hill, a cream boundary wall and green shrubs in front of it
  - Purpose: Frames the right side of the scene
  - Style: photo-like digital painting
  - Main colours: #4E8F3A, #7CB342, #2E7D32, #F5DEB3, #E9867A, #87CEEB
  - Rebuild notes: Trees cut by the right page edge. The cream boundary wall starts at the right end of the school building (i3 ends at x 2021). Shrubs in front of the wall are green with small orange flowers.

### Doubts and unknown words

- doubt: t1: font weight looks regular or medium, not clearly bold; size and font name are estimates
- doubt: t2-t6: font name and size_pt are estimates from the image, not measured
- doubt: t1-t6: boxes re-drawn with at least 30 px margin above the first mark and below the last mark (attempt 2); edges still judged by eye from the display scale (x1.64)
- doubt: Tiny chalk writing on the blackboard and the map/poster on the wall are inside the picture, not listed as text blocks; left for the picture-saver
- doubt: No page number seen on this page
- doubt: Sky with clouds at the top of the page is not saved as a crop: it is behind the title and would need a crop that avoids the title text. The background crop is therefore sand only; the sky is described here but not saved as a file.
- doubt: The flagpole shaft between the flag bottom (y 941) and the base is not in any crop (it runs between i2 and i3, x 1351 to 1374). It is part of the scene and may show as leftover ink.
- doubt: Tree and bush areas between the building crops and the side trees (i5, i6) are split on the box edges; a few leaves may fall in the gap between crops.
- doubt: Boxes were judged by eye from the displayed image (scale x1.64); edges may be off by a few pixels.
- doubt: Chalk writing on the classroom blackboard and the wall map are too small to read and are not separate pictures.
