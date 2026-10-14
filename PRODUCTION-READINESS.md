# Delivery status and production readiness

CTROTECH / The HTML Playbook / Vercel candidate 0.3 / 14 October 2026

Author: **Odejobi Abiola Samuel**

## Decision

The **self-deployment package is prepared and locally verified**. It can be deployed to the author's Vercel account without GitHub. This is not a claim that every requested behavior, cross-specification API, exercise answer or accessibility requirement has received exhaustive independent review.

The author created the `ctrobook` Vercel project and published the source to GitHub. The agent has not created, linked or deployed a project. The supplied Vercel log shows a failed build, not a successful hosted deployment. Actual Vercel routing, domain ownership, TLS, search-engine ownership verification and search indexing remain untested on a hosted destination. These are distinct from the checks already executed.

## Delivered

- All 74 chapter drafts, exact example downloads and seven static reference projects
- An expanded, retained HTML WebIDL register with 314 owners, 1,574 direct members and 73 includes statements
- 1,398 direct member-definition routes and 176 explicitly labelled owner-route fallbacks
- 437 keyword/event/state/enumeration-value records, plus an owner/keyword search index
- A 401-page PDF with 400 bookmarks, selectable coloured code, language/XMP/author metadata and all five applicable notice attachments
- Local assets and fonts, functional local reading controls, draft exercise explanations and opaque-origin editable previews
- A Node 24 static compiler, root `vercel.json`, clean routes, security/cache headers and real 404 handling
- Domain-aware metadata, JSON-LD, social images, sitemaps, a release feed, Markdown and plain-text discovery documents
- Full original/third-party notices and explicit reuse-status wording without inventing an open editorial license

The declaration register closes a substantial inventory/discovery gap. It is a source-linked declaration reference, not a substitute for algorithm-level explanations, edge-case tests, complete browser compatibility analysis or all APIs imported from other standards.

## Executed evidence

| Check | Result and scope | Receipt |
| --- | --- | --- |
| Source HTML conformance | 493 documents, zero Nu messages; deliberately invalid fixture rejected | `tests/nu-full-result.json`, `tests/nu-expected-failure.json` |
| Generated Vercel HTML | 497 documents, zero Nu messages | `tests/seo-nu-result.json` |
| Sources | 2,654 URL/document/fragment targets resolved in 75 fetched documents | `tests/citation-checks.json` |
| Metadata and graph integrity | All 497 output documents checked; 408 intended indexable pages; real route/asset/fragment targets checked | `tests/seo-verification.json`, `tests/seo-static-final.json` |
| Deployment modes | Missing/invalid production origin rejected; local noindex; preview noindex with production canonical; synthetic production build indexable | `tests/seo-verification.json` |
| Exact code | 74 HTML examples match the canonical code, raw files and ZIP entries; 349 WebIDL declaration blocks preserve their source | `tests/syntax-verification.json` |
| PDF | Author, language, XMP, all five notice attachments, text recovery and geometric checks passed | `tests/syntax-verification.json`, `tests/release-evidence.json` |
| Syntax palette | Minimum PDF code-token contrast 5.42:1; four-page split/wrap regression passed | `tests/syntax-verification.json` |
| Browser flows | Chromium 156.0.8078.4, Firefox 157.0, WebKit 27.2; local HTTPS, real production security policy | `tests/seo-verification.json` |
| Mobile overflow | None at 390px across 397 Chromium pages; 12 representative pages in each other engine | `tests/seo-verification.json` |
| Automated accessibility | 16 representative pages; zero axe violations, not a WCAG or assistive-technology certification | `tests/seo-verification.json` |
| Vercel configuration | Official schema instance validation, not a real hosted deployment test | `tests/vercel-schema.json` |
| Package | ZIP CRC, duplicate/path checks, per-file SHA-256 manifest and Node-only clean-room rebuild | `PACKAGE-MANIFEST.json`, `tests/package-rebuild.json` |

Synthetic verification origins and tokens are test fixtures, not claimed owned domains or submitted verification credentials. The final local preview is intentionally noindex. Deployment does not need Python, Java, browser binaries or the Nu JAR.

## Still open

1. Exhaustive behavior/value/default/algorithm coverage, including non-HTML-standard interfaces and imported members.
2. Individual editorial reconciliation of every inventory/coverage ID against substantive teaching, exceptions and evidence. Historical foundation ledgers remain audit inputs, not completed coverage claims.
3. Independent technical and explained-answer review across the complete manuscript.
4. Broader real-device, assistive-technology, keyboard and cognitive/usability testing beyond automated samples.
5. Complete security and privacy assessment, and any legal certification appropriate to the author's actual publication use.
6. Tagged PDF remediation and independent PDF accessibility testing. Language metadata, selectable text and bookmarks do not supply a semantic tag tree.
7. Hosted Vercel deployment, primary-domain redirects and live response checks.
8. Optional Search Console/Bing/Yandex/Pinterest verification, crawler-policy choices, sitemap submission and actual indexing. None is guaranteed or silently performed.

The author already supplied the name, design approval and permission to proceed. The remaining manuscript/review work is not caused by missing author permission, and independent review is not a demand that the author personally become the reviewer.

## Rights and publication

No open reuse license was selected for original editorial work. Upstream permissions and font rights remain intact. The author can self-deploy; an editorial reuse choice is not being manufactured as a blocker. This file is a factual release-status record, not legal advice or a certification.

## Git-backed build repair

The public repository at commit `c4f2ebd` contains a lockfile with one extra blank line compared with the original archive. This was enough to fail the old raw-byte guard. The version-2 manifest now ignores only insignificant JSON whitespace outside strings. Actual source strings, dependencies and non-JSON edits still invalidate the compiled snapshot. It also reports all mismatches rather than sending the owner through one-file-at-a-time repairs. A clean-source Python build now creates missing parent directories.

Eight integrity regressions and three output checks are provided. A pinned-action, read-only GitHub workflow is configured for Node 24 on Linux and Windows. Hosted Actions and Windows execution are not claimed to have run in this Linux environment.

### Hosted build confirmation

GitHub Actions run 38593506190 passed for repair commit c95404d on both ubuntu-latest and windows-latest with Node 24. Installation, integrity regressions, the production-mode fixture build and output checks all succeeded. The observed result is retained in `tests/github-hosted-build.json`; it is not a Vercel hosting or whole-book correctness certificate. Runtime `tests/seo-build.json` is now ignored rather than tracked, avoiding build-generated changes during the pull/update workflow.

### Hosting configuration boundary repair

A subsequent owner log showed `vercel.json` triggering the book-cache guard. The uploaded file’s exact changes were not supplied. Inspection confirmed that the Node compiler does not consume it as manuscript input. Hosting configuration is now excluded from the precompiled-book input manifest and validated independently for compatible static output and routes. Book content and dependency inputs remain protected. A compiler regression changes hosting settings and property order, simulates stale local output, and confirms actual manuscript edits still fail. Local build/ is excluded from CLI uploads.

The full verification fingerprint still includes vercel.json so local deployment-check receipts retain configuration provenance. This is separate from the narrower snapshot manifest used to decide whether a manuscript rebuild is necessary.
