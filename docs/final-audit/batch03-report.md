# Content audit: Chapters 28 to 41

**The HTML Playbook | Odejobi Abiola Samuel | CTROTECH**  
Review date: **15 October 2026**

## Result

The media and forms chapters have received a source-based first pass through their objectives, explanations, worked examples, mistakes, exercises and explained answers. The corrections are applied to the working manuscript, and the website and reading PDF were rebuilt and checked from that source.

**Cumulative progress: 41 of 74 chapter first passes; 33 remain.** No chapter has independent approval, and all 81 original required requirements remain open. This is not complete per-feature coverage or a final-publication certificate.

Read the actual text in **[batch03-chapters28-41.md](batch03-chapters28-41.md.gz)**. The published edition and durable baseline ZIP/PDF remain unchanged. Nothing in this batch was pushed or deployed.

## What changed

| Chapters | Improvements |
| --- | --- |
| 28–29 | Replaced missing image resources with the original supplied schematic and three correctly dimensioned raster derivatives. Added complete matching-layout markup for responsive candidates, decoding-failure boundaries, preference defaults, CORS and auto-sizes conditions. |
| 30 | Supplied a four-second fictional schematic video in WebM and MP4, an English WebVTT sound cue, and a descriptive transcript. Explained track kinds, missing/invalid defaults, default-track limits and the difference between loading a cue and reviewing captions. |
| 31–32 | Measured a real image-map region and linked it to a real fragment target, with an ordinary text alternative. Replaced the missing iframe preview with a static srcdoc notice; explained precedence, injection and capability boundaries without weakening the lab. |
| 33 | Added Canvas bitmap/context/reset and origin-clean export behavior, plus a MathML structure example. Kept assigned API work in the open ledger instead of treating the introductory chapter as an exclusion. |
| 34–35 | Added entry-list special cases, repeated names, submitter participation, output exclusion, empty file entries, dirname and charset behavior. Tightened radio owner/tree conditions, labels and the first-legend exception. Added the owning XMLHttpRequest Standard source for FormData. |
| 36–38 | Added telephone/URL/email distinctions, password autocomplete purposes, temporal units, step bases, numeric/date API defaults and exceptions, range defaults and color-extension values. Explained current/default checked state and file-value restrictions, with upload-defense guidance. |
| 39–40 | Added selectedcontent cloning and label distinctions, exact placeholder context, selected/default state and textarea wrapping. Added the assigned output, progress and meter elements, alongside validation/recovery explanations and purposeful snippets. |
| 41 | Added UTF-8 authoring, submission overrides, requestSubmit exceptions, named-property collisions, bypass flags and dialog behavior. Kept the static interface separate from a real application service. |

All 14 chapters gained a further testable objective and an extended exercise with an explained answer. Reading and cross-checking those answers is a same-agent first pass, not independent answer-key approval.

## Observations that matter to the teaching

### Form construction is not submission

In all three tested engines, the local fixture showed:

- Disabled controls, an unchecked checkbox and the output result were excluded as described.
- Repeated checked `topic` controls produced two entries, not one overwritten object property.
- A checked checkbox without a value contributed `on`.
- The disabled fieldset's first-legend input remained eligible in the tested structure, while its other input was excluded.
- An externally associated control belonged to the form; its visually adjacent unassociated peer did not.
- A file input with no selection contributed the defined empty File entry.
- FormData construction fired `formdata` but did not itself issue a request. Reentrant construction from that form's native formdata listener threw `InvalidStateError`.

The fixture also recorded the named submitter only when supplied to construction. Output current/default/reset behavior was exercised separately from submission.

### Submission methods have different effects

An invalid required field stopped `requestSubmit()`, produced an invalid event and produced no submit event. Direct `submit()` bypassed those steps and reached the controlled local receiver.

Other local fixtures inspected an actual GET query, a submit-button override to POST, and a multipart upload with a browser-generated boundary. The upload bytes were deliberately fictional, including a PDF name/type paired with non-PDF content. This illustrates why client metadata does not validate a file; it is not a file-chooser usability test or evidence of server safety.

A dialog form closed with its expected return value without an application request. All receivers were loopback fixtures, not a deployed submission service.

### Cross-origin drawing does not grant pixel access

The controlled cross-origin image could be drawn, but `toDataURL()` and `toBlob()` both threw `SecurityError` without the required CORS access. Export succeeded for the separate controlled CORS-enabled source. This supports the explanation of the browser boundary, not a complete security assessment.

The Canvas default size, incompatible context request, dimension-reset bitmap/state behavior and MathML namespace were also checked.

### Retaining a new tag is not implementing it

In the tested Chromium 156.0.8078.4 and WebKit 27.2 builds, selectedcontent changed from the selected option's child text to the new selection's child text, not its label attribute. Firefox 157.0 retained the element but did not expose the interface or perform those observed updates.

Color-extension reflection also differed: Chromium exposed neither tested property, Firefox exposed colorSpace but not alpha, and WebKit exposed both. Reflection is not complete picker, serialization or accessibility support.

### Media resources are now real, but usability approval is still open

All three engines decoded the supplied WebM at 640 by 360, loaded the caption cue and had it active at the tested point. A user-activated harness control called play; this is not a test of every native media-control interaction.

The MP4 container and an actually decoded first frame were inspected separately with FFmpeg. The source signal and cue schedule are known; there was **no human listening or caption-usability review**. The clip has no speech, and its descriptive transcript is not a claim that transcripts replace audio description for every audiovisual lesson.

## Checker limits retained as findings

Five supplemental HTML fixtures passed Nu. Three deliberately invalid controls were rejected: a number input carrying an inapplicable pattern, two default caption tracks, and a required select without its required placeholder structure.

However, the checker did **not** reject selectedcontent placed outside its Standard-defined context. That fixture remains marked invalid under the Standard; a zero-message checker result did not approve it.

The same checker rejected the tested new customizable-select CSS syntax. HTML conformance and runtime CSS-support probes were therefore kept separate. The running manuscript select remains a conventional native baseline. See `batch03-checker-limits.json` and the fixture-level results in `batch03-browser-checks.json`.

## Current candidate checks

- **495 source-built HTML documents** and **499 generated output documents** passed the recorded full-document Nu checks, subject to the checker limits above.
- **2,689 of 2,689 source targets** resolved across 89 documents. Availability is not assertion correctness.
- Static integrity checked **13,864 local destinations**, 74 chapter records, seven project ZIPs and PDF bookmarks.
- All 14 primary examples loaded in Chromium, Firefox and WebKit; the 14 chapter pages had no page-level horizontal overflow at 320px.
- Responsive-image observations used fresh contexts at different viewport widths and device scales. The actual CSS slot matched sizes; no exact resource choice was promised.
- Pointer and keyboard image-map activation reached the real fragment target. The static srcdoc notice rendered in all three engines.
- State-specific numeric/date/file/stepping exceptions, empty-value NaN, pattern matching, genuine keyboard length correction, custom-validity clearing, select-placeholder and gauge behavior were exercised.
- Fourteen integrity/hosting tests and three output tests passed. The previous chapter fixtures and selected preview-security regression passed again against this candidate.
- Generated-output checks, three-engine local reading flows and the 17-page automated accessibility sample passed. These are not WCAG or OS assistive-technology approval.

Current candidate fingerprint:

`64c1f685b32e132bac216c76977c18a3b5575153a70a048a51524f9c28d526b9`

## Coverage and final gates

The owner-route triage contains **235 captured rows**: 26 elements, two foreign-integration entries, 91 attribute rows, 18 input states, 52 interfaces, one compatibility entry and 45 input-applicability rows. These are overlapping routes and applicability records, not 235 newly completed features. All remain **open** in `batch03-coverage-review.csv.gz`.

Further work includes full media/text-track algorithms, input state/applicability and mutation paths, native picker/control accessibility, responsive selection and CORS/referrer edge cases, complete assigned Canvas/OffscreenCanvas member behavior, and deeper customizable-select review. The retrieved Standard's newer img controls definition also needs explicit inventory/implementation reconciliation; it was not silently counted complete.

| Final gate | State |
| --- | --- |
| Complete manuscript and answers | Open: 33 chapter first passes remain, then further claim-level and independent review. |
| Full promised coverage | Open: all 81 required requirements remain open; no reduced-scope exclusions approved. |
| Accessibility and security | Open: useful browser, visual and local-request probes, but no OS assistive-technology run, human media review or complete security assessment. |
| Accessible tagged full-book PDF | Open: the reading PDF was rebuilt, but is not the final tagged edition. The separate earlier prototype remains unresolved. |

**Next content batch: Chapters 42 to 53, interaction and attributes/metadata.** The remaining work is not caused by missing author permission and is not being assigned back to the author as a review obligation.

## Durable evidence

The revised manuscript, chapter notes, browser assertions and fixtures are retained alongside current candidate receipts. Dated source hashes and bounded retrieved excerpts are in `batch03-source-retrievals.json` and `batch03-source-excerpts.json.gz`. Resource hashes, generation details and review limits are in `batch03-resource-provenance.json`.

For space-efficient recovery, **`candidate-source.patch.gz` supersedes the earlier uncompressed patch**. It contains the cumulative maintained-source changes against baseline commit `41550987440d2b9cb59f1eac11d46c7463ba42e7`, including the supplied resources. Decompress it before applying it in a separate checkout, then use the repository builders and checks. It is not a deployable release ZIP.

The owner-route CSVs are also losslessly compressed. `AUDIT-FILES.json` records hashes of the durable files. No credentials are included, and no generated full-book binary was duplicated into this audit folder.
