# Batch 06 checker and regression notes

- A first harness assertion used Playwright enabled/disabled semantics on a fieldset. Playwright treated the container as enabled despite its native disabled property and disabled descendant controls. The harness now checks the fieldset native disabled property and real control operability. The product baseline was not changed to satisfy that assertion.
- The next native run found actual horizontal overflow in wrapped example 73 at 320 CSS pixels. Its three width=640 images had no responsive display rule. The maintained fragment now gives each image max-width:100% and height:auto while retaining 640 by 400 attributes. The full source/compiled reflow suite must pass before the fix is recorded as verified.
- The proposed tables processing-model-1 citation did not resolve. It was replaced with the actual table-header-cell definition before publication. The WAI two-header table guidance is used for this row-and-column-header design.

- The final source-integrity guard rejected a stale generated status page after fresh QA had been saved. Rebuilding the HTML without regenerating the already checked PDF refreshed that page. The unchanged guard then passed 496 documents and 13,874 local destinations. The compiled static/Nu and package checks were repeated afterward; no guard was relaxed.
