# Chapter 73: Build a media gallery

## Objectives

- Describe the supplied drawings accurately rather than inventing photographic detail.
- Pair each image with a caption that contributes context instead of duplicating its alternative.
- Keep local image assets usable offline and reserve a matching aspect ratio.

## Before you start

Review Chapters 19, 28, 29, 33. Choose alternatives from an image's purpose, pair figures with captions and compare an asset's dimensions with its display.

## Working terms

A text alternative supplies image-equivalent meaning for its context. A caption adds related visible context. An intrinsic aspect ratio comes from the resource geometry; the supplied drawings are 640 by 400. Lazy loading is a browser loading hint, not a promise about a request time.

## Build contract
Deliver three self-contained drawings named `shelves.svg`, `window.svg` and `tables.svg`. State that these are illustrations, not photographs of a real library. Use a list of figures with an image and caption in each. The reference drawings are made from simple geometric shapes and need no external font, network image or attribution to an unknown photographer. Retain the publication credit and rights notice when using the supplied package; do not assume the whole book has an open licence.

## Implementation route
The shelves drawing has three rows of six book shapes. The window has six panes. The tables drawing shows two tables from above, each with a book shape. Write alternatives from those visible facts. Captions provide the learning context, such as organising a collection, rather than repeating the full alternative. These images carry information in this exercise, so an empty alternative would remove part of the intended content. A genuinely decorative image in another context could require a different decision.

## Acceptance and recovery
Set both HTML dimensions and SVG viewBox to the same 640 by 400 ratio, then constrain display size with CSS without distorting the image. The first image uses eager loading; later images use lazy loading as a hint. This is an authoring choice, not a timing guarantee or a measured performance improvement. Check actual rendering after scrolling the lazy images into view. Extract the ZIP and confirm all three local files load without network access. Block image loading once and confirm the text alternatives and captions still preserve meaningful information.

## Reference walkthrough
The generated SVGs contain their own drawing instructions and no remote URLs or scripts. The img elements supply alternatives in the embedding HTML. Width and height reserve the intended ratio even when display width changes. There is no lightbox or synthetic button because viewing these figures requires neither a custom interaction nor a modal. The layout uses a responsive list grid and keeps source order intact when it collapses to one column.

## Assessment rubric: 28 observable points
Award one point for each demonstrated check below, four per area. Record the evidence next to the check; untested checks receive no point. These points are an authoring assessment aid, not WCAG conformance or security certification. A broken primary task, a misleading service claim, unsafe data collection or a dead required destination blocks readiness regardless of the score.

### Asset delivery (4 points)
- All three SVG files are supplied.
- SVGs contain no remote resources.
- The page says they are drawings.
- No real venue photography is claimed.

### Accurate alternatives (4 points)
- The shelves alternative describes three rows.
- The shelves alternative matches six shapes per row.
- The window alternative matches six panes.
- The tables alternative matches two tables with book shapes.

### Figure relationships (4 points)
- The gallery is a native list.
- Each list item contains a figure.
- Each image has its caption in that figure.
- Captions add context instead of duplicating alternatives.

### Geometry (4 points)
- HTML width is 640 for every image.
- HTML height is 400 for every image.
- Each SVG viewBox is 0 0 640 400.
- Narrow rendering preserves the ratio.

### Loading (4 points)
- The first image is not lazy.
- Later images carry the lazy hint.
- All images render after scrolling into view.
- No measured speed claim is invented.

### Fallback (4 points)
- Local files load after ZIP extraction.
- Images require no network resource.
- Blocked images leave meaningful alternatives.
- Captions remain readable with images blocked.

### Presentation and rights (4 points)
- The 320-pixel page has no horizontal overflow.
- The list reading order is meaningful.
- No unnecessary lightbox control is offered.
- Publication credit and rights limits are retained.

## Exercise

The window SVG has six panes, but its alternative says four and its HTML height is changed to 640 while width stays 640. What should be repaired?
