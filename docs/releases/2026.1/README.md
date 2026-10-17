# The HTML Playbook: production release 2026.1

**Odejobi Abiola Samuel | CTROTECH | 17 October 2026**

## Accepted for publication

The author expressly approved the current book and asked for final production completion. He also reported positive feedback from approximately five friends. This is recorded as author acceptance and general-reader feedback. No reader identity, specialist qualification or independent review certificate has been invented.

The release comprises the 74-chapter curriculum, seven complete static teaching projects, explained exercises, exact chapter-code downloads and captured source-linked reference. The production release decision does not silently close the original whole-Standard or independent-review requirements.

## What changed for the production edition

- Aligned publication date, production-edition wording and release notes across the maintained website/PDF source.
- Promoted the **full tagged book to the standard PDF download**, replacing the older untagged export. Removed the competing candidate download from the reader-facing guide.
- Retained selectable syntax-coloured examples, structured links, language metadata, chapter/reference bookmarks and scoped table headers. Running margins are artifacts, not part of the meaningful reading tree.
- Added a small, licensed and renamed Noto CJK TrueType subset for the three Japanese characters in the ruby example. The PDF no longer depends on an unlisted system fallback for those characters. All **six** font/source notices are attached and the source-font/subset hashes are recorded.
- Added a reproducible production PDF builder and a fail-closed artifact/proof/source-fingerprint guard. Rendering, structural/text checks and veraPDF validation must pass before promotion. Guard unit tests include tampering, stale inputs, bad profile/result, missing proof and renderer failure without overwriting the old artifact.
- Retained the enlarged reference-link targets from the previous checkpoint and repeated release-specific checks rather than reusing old fingerprinted results.

## Exact PDF evidence

- **594 pages**, **404 bookmarks**, all 74 canonical chapter code examples and their deks/explanations/mistakes/questions/answers present as text.
- **349 captured API declaration strings** checked against extracted PDF body text, with none missing.
- 2089 structured link annotations; six attached notices; no parser syntax warnings or detected text-bound outliers.
- **veraPDF 1.30.3 / PDF/UA-1 machine profile: compliant**, 106 passed rules, zero failed rules and zero failed checks. Exact SHA-256:

`5685f8eb1dd9f073835e89a538e678e4151e809b8d4d26a801dbf1d99101590d`

The installer bytes matched the previously reviewed installer hash, its detached signature verified, and its signing-key fingerprint matched the official documentation. Full current XML and compressed diagnostics are retained. An initial CFF subset failed the profile and was not promoted; its failure XML is retained. The corrected TrueType subset passed a small glyph fixture and then the complete book validation.

The cover, a chapter page and the Japanese example were visually inspected. This is selected visual inspection, not an independent visual review of every page. Numerical code-colour contrast and actual full-export code/text/bounds checks passed. The retained synthetic Reportlab flowable test checks the legacy helper, not the WeasyPrint renderer; do not confuse its scope with full-export checks.

## Current verification records

- `source-verification.json`: all 496 source HTML documents with Nu positive/negative control, 74 examples and exercise records, seven project ZIPs, website/PDF guide consistency, font notices, syntax/text/layout and selected browser behaviour.
- `pdf-validation.json`, `pdf-verapdf.xml`, `pdf-verapdf-diagnostics.log.gz` and `pdf-structure-checks.json`: exact-artifact machine PDF evidence.
- `deployment-verification.json` and `static-verification.json`: compiled metadata, canonicals, links/fragments, exact code, asset hashes, headers/routes, synthetic-origin and selected multi-engine checks. Local deployment emulation is not Vercel deployment.
- `entire-site-a11y-*.json.gz` and `reading-site-summary.json`: release-specific complete reading-site audit, with exact HTML hashes and retained incomplete/manual-check targets.
- `entire-site-security.json.gz` and `sandbox-candidate-regression.json`: all-reading-document static boundary checks and selected real isolated-editor channels in three engines. Not a complete penetration test.
- `package-rebuild.json`: fresh-extraction ZIP build verification when packaging is complete.

## Reader expectations and continuing improvements

Read the source definition when an edge case matters. Captured declarations and source routes are not complete treatment of every value/default, conversion, exception, lifecycle algorithm or cross-specification contract. That expansion remains tracked without exclusions in the formal audit ledger.

Author acceptance does not establish specialist answer-key correctness, independent WCAG conformance, actual NVDA/JAWS/VoiceOver operation, complete security assessment, universal browser support or legal certification. These distinctions remain visible in the review records without treating the accepted book as a perpetual candidate.

No new open editorial licence was chosen. Copyright, third-party rights and AI-assisted preparation disclosure remain intact. Feedback and corrections should not include private data or credentials.

## Delivery status

Repository push, hosted CI, release-asset publication and actual production deployment are separate checks. Their observed results are recorded in a dated delivery receipt. A successful local build alone is not a claim that the public website has updated.
