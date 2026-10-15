# Reference reasoning: Build a media gallery

The three alternatives match the actual geometric drawings and do not describe people, colours or photographic settings that the files do not show. Captions explain why each subject appears in the gallery. The wrapped chapter example links to the supplied project image files; the extracted gallery uses sibling-relative paths. HTML width/height and SVG viewBox all share a 1.6:1 ratio. Local assets and explicit dimensions make the reference self-contained, but loading="lazy" remains a browser hint rather than proof of faster loading.

## Explained exercise answer

Restore an accurate six-pane alternative. Keep the supplied 640 by 400 width/height pair so its reserved ratio matches the 0 0 640 400 SVG viewBox; CSS may scale the display while height remains automatic. Check the actual loaded image and the blocked-image state, then verify all three files from the extracted ZIP. Neither a plausible alternative nor successful image loading proves the other requirement.

## Sources

- HTML Living Standard: the img element: https://html.spec.whatwg.org/multipage/embedded-content.html#the-img-element
- WAI Images Tutorial: informative images: https://www.w3.org/WAI/tutorials/images/informative/
- WCAG 2.2 Understanding: Reflow: https://www.w3.org/WAI/WCAG22/Understanding/reflow.html

Same-assistant reference reasoning, not an independent assessment or certification. Record actual observations against BRIEF.md; do not award points for unperformed checks.
