# Next-edition work: behaviour depth and specialist review

**CTROTECH HTML Playbook | 17 October 2026**

Production edition 2026.1 remains unchanged. This checkpoint contains substantive new teaching and executed evidence, not a new release or a claim that all remaining gates are closed.

## Read the new material

**[Storage: the six-member behaviour contract](storage-01/storage-behavior-review.md)**

The approximately 2,900-word review manuscript covers `length`, `key`, `getItem`, `setItem`, `removeItem` and `clear`. It explains argument conversions, missing versus empty values, mutations and no-op branches, exceptions, ordering, cross-document events, session boundaries, privacy and security. A complete theme-preference exercise includes markup, controller, event wiring and an explained solution that works without storage access.

The sole authored unit is `storage-01/contract-source.json`. The Markdown manuscript is generated from it. It is deliberately a review source, not an extra production manuscript maintained in parallel with the website/PDF. Integration into both publication outputs, regeneration of the PDF and exact-artifact validation are still required before release.

## Executed results

| Work | Result | Limits |
|---|---|---|
| Six-member Storage probes | 267 observations across Chromium, Firefox and WebKit | One WebKit unrelated-page event-delivery observation needs triage; not 267 passing assertions |
| Exact theme exercise | 30 scenarios across the same three engines passed | Access/quota failure branches use explicit fault injection; not a private-browsing policy survey |
| Actual Orca/native-keyboard session | Nine keyboard/DOM checks completed; 308 recorded speech utterances; expected speech fragments in eight task windows | Skip-link label needs triage; practice-dialog verbosity needs listener review; no human listener or independent approval |
| Existing repository tests | 14 passed | Regression check, not a full new publication build |
| Production inputs and PDF | Unchanged fingerprint and PDF hash checked | No new edition built, deployed or independently certified |

Exact browser versions, observations and scope statements are retained in the JSON reports. The Orca transcript includes complete multiline utterances, not only the first line of each message. An actual output recording and raw debug trace are preserved, with checksums.

## Independent review is ready to assign, not completed

Read the **[independent review packet](INDEPENDENT-REVIEW-PACKET.md)**. It provides separate technical and security work orders, an AT protocol, conflict/scope requirements, a findings/return form and a 74-chapter assignment queue. No reviewer identity or approval has been invented. The chapter queue is entirely awaiting independent review.

Existing formal coverage and outstanding requirements are not silently changed. Six authored draft contracts are not six newly published or independently approved contracts. The established production release remains the accepted reading edition while this work is reviewed.

## Reproduce

From a repository checkout with the existing Python/Node and Playwright dependencies installed:

```sh
python3 docs/review-work/storage-01/render_review.py
python3 tests/test_storage_behavior.py "$PWD" /tmp/storage-results.json
python3 tests/test_storage_exercise.py "$PWD" /tmp/exercise-results.json
npm test
python3 docs/review-work/storage-01/verify_checkpoint.py
```

The tests start disposable loopback HTTP fixtures and fresh browser contexts. They do not use readers' data or the production site's storage. Browser binaries must already be installed; version changes can change observations and should generate new dated evidence, not overwrite a historical report without review.

For the Linux Orca harness, see [the environment and replay instructions](storage-01/README.md). Installing a screen reader, DOM assertions or speech-output strings alone are not a human accessibility assessment.

## Next gates

1. Triage the WebKit observation and the two Orca observations with controlled reproductions and experienced listeners.
2. Obtain independent technical/security and cross-platform AT reviews against exact targets.
3. Integrate the reviewed unit into the shared website/PDF generation path, then rebuild and validate both artifacts together.
4. Continue owner-by-owner behaviour teaching and full manuscript/answer review without reducing the promised scope.
