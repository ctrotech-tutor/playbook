# Independent technical, security and accessibility review

**CTROTECH HTML Playbook | Odejobi Abiola Samuel**  
Prepared 17 October 2026. **No independent reviewer has been engaged or approved this packet.**

This is a request for evidence, not a certification. Author acceptance and positive reader feedback are valuable but do not establish a specialist technical, security or assistive-technology review. The assistant's own research, code execution and Orca trace analysis are explicitly not independent review.

## Two separate targets

1. **Published edition 2026.1:** production content commit `01d0a20057312a7b03334c13f2907133448b5783`; receipt baseline `b7d54a3bd625d31af0d2b440a9535774172a3ec7`. The production site and tagged PDF are unchanged by this review checkpoint. Historical evidence is in `docs/releases/2026.1/`.
2. **Unreleased Storage unit:** `storage-01/contract-source.json`, rendered as `storage-01/storage-behavior-review.md`. This unit is not yet part of the maintained website/PDF or production coverage counts. Review its exact hash from `storage-01/evidence-manifest.json`, not an unspecified future copy.

The six new draft contracts do not close all API coverage, all 81 formal requirements, all security assessment or all accessibility gates. Preserve the historical audit register rather than silently treating these scoped results as full-book approval.

## Before accepting a review

Record reviewer name or agreed public identifier, relevant experience, affiliation if relevant, relationship to the author, conflicts of interest, date, exact files/commit/hashes and permission to publish the report. Distinguish a second perspective from a genuinely independent reviewer. A different assistant within the same authoring process is not automatically an independent specialist.

For each finding record: stable ID, target and paragraph or code location, severity with rationale, normative requirement versus recommendation, source URL and reviewed date, reproduction steps, expected result, actual result, evidence, proposed correction, disposition and retest evidence. A finding is not closed merely because code changed. Use `not reviewed`, `needs triage`, `confirmed finding`, `corrected pending retest`, `verified corrected`, or `no finding in reviewed scope`. Never use an unqualified all-book PASS.

## Technical reviewer work order

Read the new manuscript before its test results to avoid treating browser agreement as standards proof. The preserved normative retrieval identities and excerpts support traceability but are not a substitute for checking current algorithms.

- Reconcile all six direct Storage declarations with `content/api-register.json`. Window getters and StorageEvent dependencies are not extra owners silently completed by this unit.
- Check each conversion: required argument versus explicit `undefined`; DOMString versus explicit JavaScript `String(Symbol())`; unsigned-long truncation, nonfinite values and modulo; incompatible receivers and constructor exposure.
- Check map semantics: absent versus empty; readonly count; implementation-defined ordering; equal converted values; replacement versus insertion; missing removal; empty clear; exceptions before mutation; ignored extra clear arguments.
- Check legacy named-property collisions against the full Web IDL algorithms. The three-engine results do not by themselves prove those normative statements.
- Check asynchronous broadcast eligibility, excluded mutator, receiver storageArea identity, old/new/null fields, session frame sharing, unrelated-tab separation, opener copy and document activation.
- Triage the open WebKit unrelated-page observation. Compare controlled opener and unrelated contexts, browser/automation configuration, agent-cluster eligibility and relevant WPT tests. Do not infer permanent non-delivery from a bounded timeout.
- Verify the allowlisted theme exercise, guarded getters, honest read/write reporting, in-memory fallback and explained answers. The 30 exercise scenarios include explicit fault injections, not a claim to have reproduced every browser privacy policy.
- Assess wording about quota, durability, privacy, origin/path boundaries, untrusted strings and the opaque-origin practice lab. No fixed quota or universal retention promise is acceptable.

Use `chapter-review-queue.csv` to assign the remaining 74-chapter independent manuscript/answer review. Every row begins unreviewed. The existing same-assistant first passes remain historical work, not independent approvals.

## Security reviewer work order

**Scope and permission:** inspect this repository and locally served disposable fixtures. The public site is a static publication, not authorization to attack the hosting provider, unrelated origins, accounts or other users. Use fictional data. Obtain explicit authorization before any active testing outside the local fixtures. No secrets, production storage or real credentials belong in reproductions or reports.

Review `assets/site.js`, `deploy/`, `vercel.json`, dependency locks, build/download verification and the served output. Check both source intent and actual response behaviour. Historical automated static and sandbox checks are supporting evidence, not an independent security audit.

| Boundary | Questions requiring evidence |
|---|---|
| Editor to preview | Can supplied HTML escape the sandbox or reach the parent DOM? Are opaque origin and sandbox restrictions preserved after every rerun/reset? |
| Preview to network | Test relevant fetch, image, frame, script, form and navigation paths against the actual preview policy. Document allowed paths and limitations rather than claiming a general malware sandbox. |
| Main publication DOM | Trace search input, storage values, URL parameters and copied example text to sinks. Prefer text rendering; establish whether any untrusted value reaches HTML or script execution. |
| Storage trust | Confirm that preferences are optional, origin paths are not isolation, and stored text cannot select arbitrary themes or become trusted markup. |
| Dialog/focus control | Verify modal dismissal, escape routes and focus restoration without weakening the sandbox to solve a usability issue. |
| Resource exhaustion | Assess very large markup and looping scripts. An iframe is not a promise that hostile code cannot freeze a tab or exhaust resources. |
| Hosting and downloads | Review actual headers, cache behaviour, MIME types, archive handling, exact-artifact checksums and the limits of local-server evidence for Vercel deployment. |
| Supply chain | Review pinned dependencies, downloaded tool provenance, signatures where applicable, font/third-party notices and least-privilege release steps. Report secret exposures privately without reproducing values. |

Deliver a threat model, reviewed surface list, evidence-backed findings and residual risks. Static header presence alone is insufficient. Any active assessment needs its own date and environment, not recycled historical timestamps.

## Assistive-technology reviewer work order

The new bounded Linux run used actual Orca, headed Chromium, native X11 keyboard input, AT-SPI and a recorded speech-dispatcher/eSpeak output stream. It is not a human usability study. Read `storage-01/orca-evidence/assessment.json` and the complete multiline transcript. The raw debug trace and PCM recording are preserved with checksums.

Nine keyboard/DOM checks completed. Eight task windows contained their expected speech fragments; the skip-link label needs triage. Opening the practice dialog also caused source text to be submitted as part of a long utterance. That verbosity needs listener review, not an automatic WCAG-failure label. Search-result announcements and expanded/collapsed states were verified from the complete post-session trace, avoiding buffered-log timing mistakes.

Required next sessions, all **not independently completed**:

- Orca with an experienced listener: repeat skip link after settled page load, landmarks/headings, search and result navigation, narrow-width chapter navigation, editor entry/exit, code reading/copying and dialog verbosity. Distinguish the accessibility name from extra content the screen reader elects to present.
- NVDA on Windows with supported Firefox/Chromium combinations.
- JAWS on Windows with a supported browser, where available.
- VoiceOver on macOS/Safari and relevant mobile reading flows.
- Tagged PDF with representative Windows and Apple reader/AT combinations: reading order, headings, bookmarks, links, tables, code, language and Unicode extraction. Machine PDF/UA validation does not certify these experiences.

Record browser, operating system, screen-reader version/settings, viewport/zoom, input method and exact target hash/URL. Check task comprehension and error recovery, not just whether a label appears in a trace. Do not claim all combinations passed because one did. The virtual X11 environment is not equivalent to every user's desktop.

## Review return form

- Reviewer / experience / independence statement: **unassigned**
- Target commit and file hashes: **to be recorded**
- Review dates and environment: **not reviewed**
- Reviewed scope / exclusions with reasons: **not reviewed**
- Normative sources checked: **not reviewed**
- Findings with IDs and evidence: **not reviewed**
- Author response and corrected-file hashes: **not applicable yet**
- Reviewer retest / unresolved risks: **not applicable yet**
- Permission to publish name and report: **not obtained**
- Decision: **NO INDEPENDENT APPROVAL RECORDED**
