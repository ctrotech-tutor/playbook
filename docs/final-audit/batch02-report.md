# Content audit: Chapters 14 to 27

**The HTML Playbook | Odejobi Abiola Samuel | CTROTECH**  
Review date: **15 October 2026**

## Result

The next 14 chapters have received a source-based first pass through their lessons, worked examples, mistakes, exercises and explained answers. Corrections are applied to the working manuscript, and the website and reading PDF have been rebuilt and checked from that source.

**Cumulative progress: 27 of 74 chapter first passes; 47 remain.** This is not independent approval, complete per-feature coverage or a final-publication certificate. All four final gates remain open.

Read the actual revised text in **[batch02-chapters14-27.md](batch02-chapters14-27.md.gz)**. The candidate has not been pushed or deployed, and the existing published edition and durable baseline ZIP/PDF have not been replaced.

## Material improvements

| Chapters | Changes made |
| --- | --- |
| 14 | Added `hgroup` with a worked subtitle example. Distinguished the practical single-page-heading convention from the current outline requirements. Explained heading offsets, reset boundaries, the cap of 9 and the shadow-host traversal rule, with explicit implementation limits. |
| 15–16 | Added `dfn` and its term-selection conditions, meaningful `sub`/`sup`, the immediate-newline parser rule for `pre`, and platform-dependent keyboard notation. Clarified quotation boundaries and cross-referenced `s` teaching. |
| 17–18 | Corrected the fragment-only-link explanation when `base` changes the target document. Corrected the exercise answer that treated ordered lists as inherently procedural. Added `menu` limits, complete `dl` groups and ordered-list value behavior. |
| 19 | Replaced the missing image reference with a supplied original SVG teaching schematic. Inspected its rendering and compared the room relationships with its alternative text. Added caption placement and a diagram-specific question with an explained answer. The schematic explicitly does not describe real premises. |
| 20–21 | Added visible abbreviation expansion and grammatical-number rules; distinguished edit timestamp syntax from broader `time` values. Added `wbr`, ruby fallback, automatic isolation and explicit directional overrides. |
| 22–25 | Removed a supposedly fictional but dialable telephone placeholder rather than claiming an unverified reserved number. Added quotation attribution, named-region distinctions, contextual header/footer mappings, address restrictions and the precise `main` hidden-attribute condition. |
| 26–27 | Added column groups, span limits, zero-rowspan behavior, explicit same-table header references and the `cellIndex` caveat. Clarified deployment prefixes and current-page versus disabled state without changing hosting. |

Nine chapters gained an additional testable objective. Ten exercises and their explained answers were extended to cover the added material. Other existing answers in this batch were also read and cross-checked; none has independent approval.

## Browser findings that affected the wording

### New heading attributes are not a universal-support promise

The tested Chromium 156.0.8078.4 and Firefox 157.0 builds did not expose `headingOffset` or `headingReset` reflection properties. WebKit 27.2 exposed both.

In the Chromium CDP accessibility tree, the offset fixture retained heading levels **1, 2, 2, 2**, rather than the current Standard's intended computed sequence **1, 2, 3, 2**. This is a concrete reason not to replace the ordinary hierarchy with an untested offset-based design.

WebKit reflection alone does not prove complete algorithm or accessibility support. Firefox and WebKit accessibility-tree output, OS assistive technology, and released stable-browser coverage were not established by this fixture.

### The image is now inspectable

The supplied `library-floor-plan.svg` loaded at its intended 640 by 360 dimensions in all three tested engines. A same-agent visual check confirmed that the reading room is left of reception and the lift is opposite reception across the corridor. This is evidence about this schematic, not independent image-accessibility approval or real-world directions.

## Executed checks

- **Three engines:** Chromium, Firefox and WebKit loaded all 14 primary examples, checked selected native fragment/skip-link behavior, and checked the 14 chapter pages at 320px without page-level horizontal overflow.
- **Focused fixtures:** actual DOM behavior for `pre` newlines, `wbr` text, bidirectional CSS direction, ruby annotation text, base/relative/root URL resolution, list structure and selected IDL values, same-table header targets, zero row spans and cell indexes.
- **Conformance controls:** five conforming supplemental fixtures passed Nu; two deliberately invalid fixtures were rejected, covering a bare-time edit timestamp and a column group that incorrectly combines `span` with child columns.
- **Full source build:** 494 HTML documents passed the recorded Nu checks. Static integrity checked 13,864 local destinations, all 74 chapter records, seven project ZIPs and PDF bookmarks.
- **Source targets:** 2,680 of 2,680 URL/document/fragment targets resolved across 84 documents. This is a link check, not proof of assertion correctness.
- **Generated output:** the current 498-document output passed metadata, link, asset and Nu checks. Three-engine local reading flows and the 17-page automated accessibility sample passed, with manual/incomplete-check boundaries retained.
- **Regression:** 14 integrity/hosting tests and three output tests passed. The selected preview-isolation regression also passed again in three engines; this does not certify arbitrary-code safety.
- **Durability:** the cumulative maintained-source patch includes the new SVG and passes reverse-application and source-whitespace checks. Generated PDF bytes are not treated as prose-whitespace input.

Current candidate fingerprint:

`59132dff387305a7fe8b3ce460280c1d5052d02ccaa56ad4fff24247125a6c81`

## Coverage and remaining gates

The route review identifies **124 captured inventory rows** assigned to these chapters: 71 element rows, 24 attribute rows, two global-attribute rows, one global-attribute-family row, 24 interface rows and two compatibility rows. Some represent different routes to the same feature; they are not 124 newly completed features.

Every row remains explicitly **open** in `batch02-coverage-review.csv.gz`. The chapter first pass does not establish all content-model exceptions, every API conversion/default/exception, full anchor auditing/referrer behavior, complex table algorithms, XML language serialization or complete heading-offset interoperability. The original snapshot was not silently relabelled complete.

| Final gate | State after this batch |
| --- | --- |
| Complete manuscript and explained answers | Open: 47 chapter first passes remain, with further claim-level and independent review required. |
| Full promised feature/API coverage | Open: all 81 original requirements remain open; no exclusions invented. |
| Accessibility and security review | Open: meaningful browser probes have run, but no OS assistive-technology run or complete security review is claimed. |
| Accessible tagged full-book PDF | Open: the rebuilt reading PDF is not the tagged final edition. The separate earlier prototype still has unresolved table/reading-order/validation work. |

**Next content batch: Chapters 28 to 41, covering media and forms.** The remaining work is not a missing-author-permission problem and is not being assigned back to the author as a technical-review obligation.

## Evidence and recovery

- `audit-register.json`: chapter notes, original requirements, findings and gates.
- `batch02-browser-checks.json` and `reproduce-batch02.py`: executed observations and repeatable assertions, with fixtures in `batch02-fixtures/`.
- `batch02-source-retrievals.json`: dated URLs and original-page hashes; `batch02-source-excerpts.json.gz` retains the retrieved excerpts with third-party-rights notice.
- `candidate-verification.json` and `candidate-static-verification.json`: current full candidate receipts.
- `candidate-source.patch`: cumulative maintained-source corrections against commit `41550987440d2b9cb59f1eac11d46c7463ba42e7`, not an upload-ready release bundle.
- `library-floor-plan.svg`: supplied fictional teaching schematic.
- `AUDIT-FILES.json`: hashes of the durable audit material.

Reproduce the supplemental checks from an installed candidate checkout, after applying the patch and running `python3 tools/build.py --pdf`, with `python3 /path/to/final-audit/reproduce-batch02.py`. Use Java 21 for the recorded Nu checker and the repository's installed Playwright engines. No production service is contacted by those local fixture checks.
