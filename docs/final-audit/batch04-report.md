# Batch 04: interaction, attributes and metadata

**The HTML Playbook | Odejobi Abiola Samuel | CTROTECH**  
Review date: **15 October 2026**

## Checkpoint

**53 of 74 chapters have now received a substantive first pass. Twenty-one remain.** This batch covers Chapters 42 to 53. There are no independently approved chapters, no approved scope exclusions and no closed requirements. All 81 original requirements and all four final-publication gates remain open.

The maintained source, compiled website and reading PDF are updated together. This is a checked content checkpoint, not the completed final publication or an accessible tagged-PDF release. Repository delivery is to `main`; a repository push is not proof that Vercel has deployed this version.

## Actual manuscript and example changes

| Chapters | Correction or addition |
| --- | --- |
| 42 | Reset restores defaults, not necessarily empty values. Explained button Auto submission/command conditions, same-tree invokers, built-in/custom commands and submit/reset/button/image input distinctions. |
| 43 | Added exclusive details-group constraints, first-summary behavior and queued/coalesced toggle notifications. Explained why browser enforcement does not make invalid initial markup conforming. |
| 44 | Added a real auto-popover and explicit initial dialog focus. Distinguished modal/nonmodal opening, `close`, cancelable `requestClose`, `closedby` defaults, lifecycle exceptions and popover enumerated states. |
| 45 | Replaced inert movement controls with actual local reordering. Boundary controls are disabled, actions have item-specific names, focus follows the moved item and visible status explains the result. No backend persistence is implied. Added editing/drag state and input-path boundaries. |
| 46 | Extended template fragments, slot assignment, declarative shadow parsing, closed-root limitations, registration exceptions and cloning/serialization boundaries. Newly evolving streaming/scoped-registry work is explicitly still open. |
| 47 | Replaced the unimplemented Save control with a real validated dataset-to-text display. Added conversion/deletion rules and microdata item/value/vocabulary boundaries. |
| 48–49 | Expanded hidden/until-found, inert, id escaping, editing/keyboard hints, CSS Shadow Parts ownership, contextual attribute definitions and event-handler cancellation/reflection distinctions. |
| 50 | Made the description and body agree about fictional hours and absent real contact details. Added meta/header, one-base and style authoring boundaries. |
| 51 | Replaced absent stylesheet/icon resources with actual supplied publication paths. Extended preload, modulepreload, preconnect and relation-context distinctions. |
| 52 | Supplied `assets/integrity-demo.js` and its actual SHA-384 digest. Added strongest-digest, CORS, nonce-generation/hiding and Referrer Policy boundaries. |
| 53 | Extended pristine/dirty/default/reset behavior, nonce special reflection, form/radio/options collections and legacy `document.all` behavior. |

All twelve exercise/answer pairs were cross-checked and extended where appropriate. This is same-assistant review, not independent answer-key approval. Natural prose, author credit, syntax highlighting, third-party notices and the no-em-dash requirement are preserved.

The full batch manuscript is retained losslessly in `batch04-chapters42-53.md.gz`. The canonical source remains `content/chapters.json`; the archived excerpt is not a second maintained edition.

## Executed evidence

### Selected native behavior in three engines

`reproduce-batch04.py` ran against Chromium **156.0.8078.4**, Firefox **157.0** and WebKit **27.2**. Every primary example from 42 to 53 loaded successfully. Selected checks include:

- Actual reset behavior and keyboard activation of native disclosure controls.
- Modal opening, the chosen initial focus, Escape closure and keyboard-opener focus restoration.
- Auto-popover opening and explicit dismissal.
- Real reordering by Enter and pointer, disabled boundaries, moved-item focus and visible result.
- Exclusive details and coalesced toggle notifications.
- Native custom command/source events and show-modal commands. The form-owned Auto invoker neither submitted nor dispatched a second custom action in these versions. Its `type` IDL getter reported `button`; that getter string is not the normative internal Auto state.
- Inert focus exclusion, a hidden eligible form entry, editing states, a punctuated id and dataset conversion/deletion exceptions.
- Declarative shadow creation, named slot assignment without moving the light-DOM child, fragment querying, retained closed-root references and custom-element registration exceptions. Clone/serialization observations are recorded for these versions only.
- Pristine versus dirty/default/reset state, `RadioNodeList`, options and legacy `document.all` behavior.
- Popover defaults and selected exceptions, canceled opening, nonmodal focus, dialog mode mismatch and cancelable `requestClose` with `closedby="none"`.
- Successful execution for matching integrity metadata, blocked mismatches and a stronger mismatching digest not rescued by a matching weaker digest.
- Actual cross-origin CORS-enabled versus non-enabled script execution; connected nonce hiding; allowed versus blocked scripts under a real local CSP response header; fresh cryptographically generated nonce values between responses.
- Actual navigation with no referrer and origin-only referrer, rather than just reading the stored policy attribute.
- One matched preload request in this controlled case. This is not a general reuse/performance guarantee.
- `until-found` fragment discovery and no page-level overflow at 320px across all twelve chapter pages.

These are headless Playwright engine observations, not universal stable-browser support, actual touch/native-drag/IME evaluation, OS screen-reader evidence or a complete security review.

### Checker gaps are not authoring permission

Nu **26.10.12** accepted nine positive fixtures and rejected the deliberately invalid popover keyword. It also missed two retained invalid controls:

1. Two matching-name details authored open together.
2. A dialog with `tabindex`.

Both remain invalid under the cited Standard. They are recorded as checker gaps, not silently reclassified as conforming. A zero-message checker result cannot close the behavioral/authoring gate.

### Whole-candidate checks and previous regressions

Current fingerprint: `439f8ba540d68e88145e2be29719eddb1249f0dbe3242638edd882de7b015a94`.

- Full source verification passed: **495 built HTML documents**, all 74 canonical examples, seven project downloads, internal references, manuscript structure, exact syntax/source and author credits.
- **2,701 citation/document/fragment targets** resolved across **96 documents**. Availability is not assertion correctness.
- The rebuilt reading PDF has **427 pages**, **401 bookmarks**, selectable syntax-coloured examples and author/language/notices checks. It is **not the tagged final PDF**.
- Full deployment-fixture and final output verification passed for **499 generated HTML documents**, metadata, canonical routes, structured data, source exports and hashed assets.
- The **14 integrity/hosting tests** and **three generated-output tests** passed under Node 24.
- Chapters 14–27, Chapters 28–41 and selected editable-preview security regressions were re-executed in three engines against the current candidate.
- Existing automated accessibility samples and responsive checks passed within their recorded scopes. No WCAG or OS assistive-technology approval is inferred.

## Sources and coverage boundaries

`batch04-source-retrievals.json` records **53 dated retrieval targets** and response hashes. Bounded extracts are retained in `batch04-source-excerpts.json.gz`, with source-rights notices. This includes selected owning HTML, DOM, CSS Shadow Parts, SRI, CSP, Referrer Policy and WAI dragging guidance. Retrieval or a heading match is not complete review of every nested definition.

The **248 overlapping captured owner-route rows** in `batch04-coverage-review.csv.gz` all remain **open**: 11 elements, one integration entry, 82 contextual attributes, 89 event-handler attributes, 29 globals, three global families, four input states, 26 interfaces and three compatibility checks. Inventory mentions and chapter passes are not complete taught API/algorithm coverage.

Outstanding work includes streaming template updates and scoped registries; full shadow/parts/microdata behavior; every promised conversion/default/exception/event algorithm; command/Hint/close-watcher corner cases; global applicability; actual editing/drag/touch/IME and OS AT; resource/security cross-specification review; geolocation compatibility-route reconciliation; independent exercises and a tagged full-book PDF. No silent exclusion is made.

## Next content batch

**Chapters 54 to 67: browser behavior and professional practice.** Chapters 68 to 74 and the final reconciliations/reviews then remain. The audit is the method for finishing the content, not a substitute for that work or a burden transferred to the author.

## Repository synchronization

The checked source, compiled website, reading PDF and audit records were committed and pushed to `main` as **`8b0228f640e4f056c11b2b65ff98e004d153d7ce`**. The remote head was read back and matched. No force push was used. `repository-sync.json` records delivery separately from content and deployment approval.

On your local `main`, run `git pull --ff-only origin main`. Local changes are not discarded. The new Vercel deployment has not been verified.

Hosted **Node 24 / Ubuntu and Windows CI both passed for this content commit**. The exact run and job URLs are retained in `repository-sync.json`. Hosted CI checks the build/integrity/output contract; it is not independent content approval or deployment verification.
