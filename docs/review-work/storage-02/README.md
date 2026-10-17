# Storage integration and controlled follow-up

**17 October 2026 | CTROTECH HTML Playbook | Odejobi Abiola Samuel**

This follow-up moves the first Storage unit from an isolated review manuscript into the maintained website/PDF build. It does not close the full coverage ledger, independent manuscript/answer review, human cross-platform AT review or independent security assessment.

## Teaching now integrated

`content/api-behavior.json` is the sole maintained authored behaviour source. `tools/behavior_reference.py` renders it for both the existing Storage reference page and the full tagged PDF. It also exports Markdown and machine-readable data. Search has a real target for the new unit; the compiled full-text export includes it.

The unit covers all six direct Storage declarations in the captured register, with conversions, defaults, errors, branches, ordering, examples, exercise markup/controller/wiring, scope and security boundaries. Window getters and StorageEvent dependencies are explained without silently counting those other owners as fully taught.

The readonly-length discussion was tightened after further Web IDL reading. An IDL readonly declaration alone is not a sufficient explanation of every legacy named-property assignment rule. The reference recommends explicit methods for potentially colliding key names and keeps exhaustive legacy binding conformance open. Three-engine observations remain evidence, not a replacement for normative reasoning.

## Controlled event-delivery follow-up

`event-initialization-results.json` records **45 observations**: five receiver-initialization modes, three repetitions, three exact engine versions, with fresh contexts and disposable origins.

- Chromium and Firefox delivered the measured event in all 15 trials per engine.
- WebKit delivered it in all 12 getter/read/write initialization trials.
- WebKit delivered no event within 800 ms in its three listener-only trials, which did not explicitly acquire a Storage object before mutation.

A fresh rerun of the complete 267-observation suite again retained one WebKit unrelated-page observation; all 30 exercise scenarios passed. The earlier mixed-workload report obtained a getter but did not observe the event. The simpler follow-up did not reproduce that result. Its ordering and additional script round trips differ. Initialization and timing are a useful investigation direction, not an established engine-internal cause. The original observation is retained and not relabelled PASS. This does not establish a universal Safari/WebKit incompatibility, permanent non-delivery or device-wide compatibility.

## Actual Orca follow-up

`orca-evidence/assessment.json` records **14 native task windows** against the existing baseline chapter UI, not a screen-reader comprehension test of the newly added Storage text. Actual Orca, headed Chromium, native X11 input and recorded speech output were used. No human listener or independent approval is claimed.

- The skip link received DOM focus but its label was absent from the initial-Tab window in all three settled-load trials.
- Returning to that same link with Shift+Tab produced its label in all three trials. This narrows the issue to the initial announcement path rather than proving a missing accessible name. Longer settled loading did not resolve it.
- The original practice dialog submitted example source in its opening utterance. Title focus, a short explicit description, and their combination did not suppress this in the three runtime-only fixture variants.
- Escape restored the trigger in all four dialog variants. Diagnostic accessibility-tree values were recorded separately from actual Orca output.

**None of the ineffective candidate dialog adjustments was shipped as a fix.** The first-announcement issue and dialog verbosity remain open for browser/AT investigation and experienced-listener review. The raw trace, complete multiline utterances, exact served baseline hash and actual PCM output are retained. A speech submission can be interrupted by later input; a transcript is not proof that the listener heard the complete message.

## Matched PDF and corrected publication copy

The regenerated full book contains **607 pages** and a bookmark for the Storage unit. Structural/text checks preserve all 74 chapter examples, all captured declaration strings, tagged links, language, scoped table headers and six attached notices. Unit-specific tests additionally check every authored teaching field, algorithms and exact example/exercise code against the HTML and extracted PDF body text.

The exact PDF passed veraPDF 1.30.3's **PDF/UA-1 machine profile**, with zero failed rules/checks. Its validation records are in `docs/releases/2026.1-storage-update/`. The original 2026.1 records remain untouched. A metadata-selected, release-directory-contained proof path keeps the old release historical and rejects stale PDFs for current inputs.

The compiled accessibility page previously said the promoted PDF was untagged. That stale statement is corrected. Semantic tagging and machine compliance still do not claim independent reading-order, WCAG or human AT approval.

## Reproducible checks and boundaries

- `tests/test_storage_integration.py`: complete same-source text/code, canonical register reconciliation, real search target, export identity, protected inputs, attribute escaping and current snapshot.
- `tests/test_pdf_release.py`: exact-artifact/stale-input guards, selected record directory, out-of-directory rejection and failed-renderer preservation.
- `normative-anchor-checks.json`: 29 targets checked in the retained dated captures, not a fresh live-link survey or independent claim approval.
- `updated-page-browser-results.json`: two actual compiled pages in three engines at desktop and 390 px, 12 axe/reflow combinations. Incomplete/manual targets are retained. Not whole-site recertification.
- Current source/deployment verification is recorded separately from the earlier 2026.1 reports. Runtime setup initially failed because the available Java 11 could not load this Nu checker's Java-17+ classes. That failure is retained; the corrected verification uses Java 21. No checker hash was bypassed.

The previous Storage-01 packet describes its recorded baseline and remains useful history. Its frozen verifier is not a requirement that later editions preserve the old production fingerprint. Review the current source and exact new artifact hashes for this update.

## Still open

Independent technical/security review, human NVDA/JAWS/VoiceOver and relevant mobile/PDF sessions, the two Orca observations, the original mixed-workload event observation, exhaustive legacy bindings and the wider owner-by-owner teaching programme. No requirement or exclusion has been silently closed.

## Additional code-inspection follow-up

The existing Clear reading progress handler announces a cleared state without checking the return from its persistence helper. This unchanged path needs an injected write-failure reproduction and an honest visit-only status if persistence fails. It is recorded as an open interface-review item, not silently counted as a passed failure branch or an independent security finding.
