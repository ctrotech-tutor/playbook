# Publication and delivery status

CTROTECH / The HTML Playbook / October 2026 reading edition / edition 2026.1

Author: **Odejobi Abiola Samuel**. Publication date: 14 October 2026.

## Current content checkpoint: 15 October 2026

**74 of 74 substantive same-assistant first passes are recorded.** There are zero independent chapter approvals and no approved exclusions. All 81 original requirements and four final-publication gates remain open. The website and 456-page reading PDF use the same maintained source. This is not the final tagged PDF. Batch06 is locally verified; repository delivery is blocked by unavailable transient write authorization. The previous checkpoint's CI is not evidence for this batch.

See `docs/final-audit/README.md`, `batch05-report.md`, the 74-chapter register and current fingerprinted receipts. Current checks cover 495 source HTML documents, 499 generated documents and 2,718 citation targets; Node 24 integrity/hosting/output checks and scoped native browser regressions pass. They do not establish exhaustive API behavior, OS assistive-technology approval or complete security review.

The reading-edition account and metrics below are retained as **historical baseline details**, not current whole-candidate counts or proof that this later checkpoint is deployed. Repository synchronization and live deployment are separate operations.

## Decision and scope

The reading edition is prepared as a matching website and PDF, with a reader-facing publication pass and executed checks. It is not an exhaustive whole-Standard behavioral reference or an independently approved technical, answer-key, accessibility or security publication. Existing internal review states remain open; they were not changed to make the edition appear complete.

The public site at https://ctrobook.vercel.app/ works. The author confirmed this, and nine representative unauthenticated GET routes were checked: eight returned 200, including the PDF, and a deliberately nonexistent route returned 404. The homepage still identifies release candidate 0.3. `tests/hosted-observation.json` records that limited observation, not deployment of this reading edition, domain ownership or search indexing.

The author authorized repository publication of this edition on 15 October 2026. The earlier package was prepared without repository write authentication; that limitation has now been resolved for the authorized push. Deployment to Vercel is separate and is not claimed here. The previous source commit, d5ef36c111f87776176e1ff00c5f9fe63de45376, passed actual Node 24 Linux and Windows CI in run 38597536097. That historical run does not certify these new changes. The agent did not sign in to Vercel or deploy this package.

## Publication improvements

- Replaced reader-facing release-candidate, owner-review and predeployment language with accurate reading-edition information.
- Added a shared reading guide with three routes, a practice loop, source-literacy notes, format limits, correction guidance and edition notes.
- Corrected Chapter 60: 166 foundation interface discovery routes and 314 WebIDL declaration owners count different inventories. The expanded register contains 1,574 direct member declarations; it is not a complete inherited-member or behavioral reference.
- Expanded targeted explanations in Chapters 29, 34, 41, 44, 57, 60, 65 and 67. Added a fictional-data warning to the Chapter 70 registration brief. This was an AI-assisted, bounded publication pass, not an independent review of all 74 lessons.
- Preserved the author name, local fonts, syntax highlighting, original and third-party notices, exact code files and seven static projects. No author biography, endorsement, open license or certification was invented.
- Preserved hosting configuration and the content-integrity boundary. Page-count checks now derive the expected output count from the source, so adding a reading page does not require pretending the old count is still correct.

## Executed evidence for this edition

| Check | Result and scope | Receipt |
| --- | --- | --- |
| Source HTML | 494 HTTP-served documents, zero Nu messages; deliberately invalid fixture rejected | `tests/release-evidence.json`, `tests/nu-full-result.json` |
| Output HTML | 498 generated documents, zero Nu messages | `tests/seo-verification.json`, `tests/seo-static-final.json` |
| Source links | 2,661 URL/document/fragment targets resolved in 81 documents; link availability is not assertion correctness | `tests/citation-checks.json` |
| SEO and graph | 409 intended indexable pages in a synthetic production-origin fixture; real targets, metadata, canonicals, code and assets checked | `tests/seo-verification.json`, `tests/seo-static-final.json` |
| Deployment modes | Missing/invalid origin rejected; local and preview noindex; production fixture indexable | `tests/seo-verification.json` |
| Shared guide | Reading routes, practice routine, scope, corrections and edition notes found in both HTML and selectable PDF text | `tests/release-evidence.json` |
| Exact syntax | All 74 HTML examples and 349 WebIDL blocks preserved; syntax colours and synthetic splitting/wrapping checked | `tests/syntax-verification.json` |
| PDF | 405 pages, 401 bookmarks, author/language/XMP metadata, five notice attachments and text bounds checked | `tests/release-evidence.json` |
| Browser flows | Local HTTPS smoke tests in Chromium 156.0.8078.4, Firefox 157.0 and WebKit 27.2 | `tests/seo-verification.json` |
| Narrow layout | No page-level overflow at 390px on 398 Chromium routes and 13 representative routes in each other engine | `tests/seo-verification.json` |
| Automated accessibility | Zero axe violations on 17 representative pages; not WCAG or assistive-technology approval | `tests/seo-verification.json` |
| Added form claims | Isolated three-engine tests of entry eligibility, repeated names, submitter data, validation and submit versus requestSubmit; requests intercepted | `tests/publication-behavior-checks.json` |
| Archive | ZIP CRC, exact payload SHA-256 manifest and extracted Node-only rebuild | `deliverables/package-checksums.json`, `tests/package-rebuild.json` |

Verification origins under `.example.test` and intercepted form requests under `.example.invalid` are fixtures, not owned production services. Historical receipts with a different publication fingerprint describe their own earlier artifacts, not this edition. The final local build is intentionally noindex. Deployment needs neither Python, Java, browser binaries nor a specification fetch.

## Remaining work

1. Exhaustive behavior, algorithm, conversion, exception, keyword/value/default and cross-specification coverage.
2. Individual reconciliation of every inventory and coverage ID against substantive teaching and evidence. Historical foundation ledgers remain audit inputs, not completed coverage claims.
3. Independent technical and explained-answer review across the complete manuscript.
4. Broader real-device, keyboard, assistive-technology and usability review beyond the executed samples.
5. Complete security/privacy assessment and any appropriate legal review.
6. Tagged PDF remediation and independent PDF accessibility testing. Selectable text, bookmarks and language metadata do not create a semantic tag tree.
7. Verified repository synchronization and separately verified deployment, including checks of the new live pages, downloads and primary-domain redirects. A push alone does not establish deployment.
8. Optional search-console ownership verification, sitemap submission and observation of actual indexing. No ranking, AI inclusion or search-engine approval is guaranteed.

These are not caused by missing author permission. The author has already supplied the name, visual approval and permission to proceed. Independent review does not mean the author must personally become the reviewer. Repository authorization does not close the acknowledged content-review work.

## Rights

No open reuse license was selected for original editorial work. Upstream permissions and font notices remain intact. This status document is not a legal opinion or certification.
