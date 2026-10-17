# Production edition 2026.1

**Release date: 17 October 2026. Author: Odejobi Abiola Samuel. Imprint: CTROTECH.**

## Publication decision

The author explicitly accepted the current edition and requested final production completion. He also reported positive reviews from approximately five friends. Their identities, specialist qualifications and detailed review scope were not supplied. Record this as author acceptance and reported general-reader feedback, not independent technical, answer-key, accessibility or security approval.

This release is a production edition of the 74-chapter curriculum, seven static projects and captured reference. It is not represented as an exhaustive whole-HTML-Standard behavioural manual. The original requirements and known gaps remain tracked without exclusions. Specialist/expanded-coverage work is not silently marked complete by this release decision.

## Deliverables

- One standard full-book tagged PDF at `deliverables/ctrotech-html-playbook.pdf` and `site/downloads/ctrotech-html-playbook.pdf`.
- The same maintained chapter, publication, reading-guide and reference source for HTML and PDF.
- Syntax-coloured selectable code, 74 exact-code examples, seven complete static project downloads and bundled font/source notices.
- Precompiled website, deterministic input manifest, production metadata/search builder and existing Vercel configuration.
- Exact-artifact PDF/UA-1 machine-validation evidence and scoped source/build/browser/security/accessibility evidence under `docs/releases/2026.1/`.
- A downloadable ZIP with every payload file hashed in its package manifest and a fresh-extraction build check.

The earlier tagged-review artifact and audit reports are historical checkpoints. They are not the current standard download or evidence for changed release bytes.

## Repeatable maintainer checks

Node-only deployment uses the checked-in precompiled source and does not require a PDF renderer:

```sh
npm ci --ignore-scripts
npm test
npm run build
npm run check:site
```

The production environment must provide the real canonical origin using the existing deployment configuration. A local/development build is deliberately non-indexable; do not treat its metadata as production metadata.

For a manuscript or renderer change, install `requirements-verify.txt`, the browser engines and the recorded Nu checker with Java 21. Install the reviewed veraPDF CLI and set `VERAPDF` if it is not at `.cache/verapdf/verapdf`. Then build the PDF and source site, run the Python source checks, rebuild to incorporate current evidence, synchronise `site/`, and execute the Node/deployment checks. The builders preserve checks rather than accepting stale fingerprints.

```sh
python3 tools/build.py --pdf
python3 tools/verify.py
python3 tools/build.py
python3 tools/check_build.py
python3 tests/test_pdf_release.py
```

The primary-PDF guard rejects a missing/failed/wrong-profile proof, altered PDF bytes or a stale source fingerprint. Rendering, structural/text checks and veraPDF validation must succeed before a new artifact is promoted. A renderer failure does not overwrite the previous artifact/proof. A PDF/UA generation target alone is not a validation result.

## What this release does not certify

- Exhaustive per-member, default/value, conversion, exception, lifecycle/algorithm and cross-specification teaching.
- Independent technical or explained-answer correctness.
- WCAG conformance, full real-device/zoom/forced-colour testing or actual NVDA, JAWS or VoiceOver operation.
- Complete penetration testing, dependency/legal certification or universal browser support.
- Search ranking, search-account ownership, indexing, or deployment merely because source was pushed.

These are scope distinctions, not a request for the author to perform the release work. Actual observations and unperformed checks must remain distinguishable. Detailed formal review records are retained in `docs/final-audit/`.

## Delivery

A non-force push must be read back from `origin/main`. Hosted CI, release-asset publication and the public website are separate observations. Do not label the production site updated until its actual public release manifest and PDF bytes match this edition. Delivery results are recorded separately to avoid a circular commit/hash claim.
