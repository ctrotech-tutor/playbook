# Final-readiness audit: batch 01

**The HTML Playbook** by **Odejobi Abiola Samuel**, CTROTECH  
Audit date: **15 October 2026**  
Baseline: repository commit `41550987440d2b9cb59f1eac11d46c7463ba42e7`

## Decision

**The audit has started, not finished. This is not a final-release certificate.**

The structured chapter-by-chapter audit is the method for completing manuscript correctness and coverage. It is not a fifth task to postpone until after those tasks. Accessibility, security and PDF work proceed alongside it.

This batch contains a source-based first pass over **Chapters 1 to 13**, scoped browser checks, a tested correction candidate and an initial PDF accessibility experiment. **Chapters 14 to 74 have not yet received this phase's substantive audit.** No chapter has been independently approved by this work.

The published edition and its delivered ZIP/PDF have not been replaced. Candidate changes are retained separately as `candidate-source.patch`, and were exercised in a local working branch. They have **not been pushed, merged or deployed**.

## Progress against the four requirements

| Workstream | Work actually performed | Still required |
| --- | --- | --- |
| Manuscript and answers | Read and source-cross-checked the opening 13 lessons, explanations, mistakes, questions and answers. Ran their selected example claims in three browser engines. Prepared corrections to history, encoding explanation, optional tags, boolean/enumerated values and exact source citations. | Remaining 61 chapters; complete claim-level verification beyond the selected fixtures; independent technical and answer review. |
| Coverage | Carried forward all 81 original requirements, mapped their chapter owners, identified concrete gaps in the initial batch and retained the existing reference/API inventory boundaries. | All requirements remain open. Complete per-feature teaching, algorithm/exception/value/default coverage and cross-specification reconciliation. No exclusions were approved or manufactured. |
| Accessibility and security | Exercised search, disclosure, native dialog and skip-link keyboard paths in Chromium, Firefox and WebKit, plus a 320px sample. Reproduced a preview-navigation gap and tested a narrower candidate policy and clearer wording. | Real screen-reader/PDF-reader work, broader task/usability checks, and a complete security assessment. Agent-operated browser probes are not a human or OS assistive-technology review. |
| PDF accessibility | Inspected the actual release PDF and built a separate four-page tagged-export prototype from maintained chapter examples. Checked its structure tree, headings, list/table/link roles, selectable code and attached notices. | Full-book semantic export, correct table-header associations, reading/tab order and code review, appropriate PDF/UA validation, and actual assistive-technology testing. The prototype is not an accessible-release approval. |

## Findings and candidate corrections

### 1. History was assigned but insufficiently taught

Requirement C01 includes history. The original opening chapters explained a Living Standard but did not supply the assigned historical context. The candidate adds a short account covering early HTML, HTML 3.2/HTML4, XHTML 1.0, WHATWG and the 2019 collaboration agreement. It explicitly identifies the Standard's history section as non-normative explanation.

Source: [HTML Standard history](https://html.spec.whatwg.org/multipage/introduction.html#history-2).

### 2. Syntax explanations needed more precise boundaries

The candidate:

- Formats the exact Chapter 9 source answer as code and adds a transport/encoding diagnostic caveat.
- Adds a worked `li` end-tag omission example, without presenting it as the rule for every optional tag.
- Distinguishes permitted boolean-attribute spellings from browser handling of invalid `true`/`false` strings.
- Explains missing, empty and invalid enumerated-attribute defaults as different inputs.
- Adds the disabled-fieldset caveat rather than claiming that removing a control's own attribute overrides every condition.
- Adds direct DOM Standard, language-attribute, encoding, anchor and button definition citations where earlier source routes were too broad.

These changes improve assigned coverage. They do not close the entire optional-tag, attribute/default or per-element content-model audit.

### 3. The editable preview made an overly broad network claim

**Observed:** under the published parent policy, code in the isolated preview could initiate a same-origin navigation request. This was reproduced using fictional query data against a local HTTPS fixture in three engines. It contradicts a blanket statement that all network requests are blocked.

**Not demonstrated:** access to the parent document, disclosure of stored settings, or compromise of the published site. This is a specific restriction/wording gap, not evidence of those broader outcomes.

**Candidate:** restrict parent `frame-src` to `about:`, keep the opaque-origin sandbox, replace the blanket claim with specific restrictions, and warn against secrets and untrusted scripts. Targeted candidate checks observed blocked parent-DOM access, blocked opaque-origin storage, rejected fetch and no tested image/form/navigation requests reaching the local fixture.

**Limit:** these are selected channels and bounded observations. They are not a universal guarantee that arbitrary scripts cannot cause network activity or other harm. Full security review remains open.

Evidence: `sandbox-navigation-checks.json` and `sandbox-candidate-regression.json`. Authority: [CSP frame-src](https://www.w3.org/TR/CSP3/#directive-frame-src) and the [HTML iframe definition](https://html.spec.whatwg.org/multipage/iframe-embed-object.html#the-iframe-element).

### 4. The release PDF is structurally untagged

Object inspection of the actual 405-page release PDF found:

- PDF version 1.4, language `en`.
- No `/StructTreeRoot` or marked flag.
- No structure-based tab-order declaration on its 405 pages.
- 1,891 link annotations with no `/StructParent` association.

The supplied language metadata, selectable text and bookmarks do not create document semantics. This confirms an open release gate rather than merely repeating a disclaimer.

Guidance: [WAI PDF reading and tab order](https://www.w3.org/WAI/WCAG22/Techniques/pdf/PDF3).

### 5. Tagged export is feasible, but the prototype is not the solution yet

The separate `tagged-workflow-prototype.pdf` has four pages, PDF 1.7, a marked structure tree, heading/list/table/link roles, structured links and five source/font notices. Selected code text from Chapters 1 and 9 is preserved, ignoring layout whitespace.

However, its table-header attributes did not carry explicit `/Scope` metadata in the inspected fixture, despite `scope` in the source HTML. That relationship needs verification and remediation. The engine's PDF/UA output setting and XMP identifier are **not a validator result**. No full-book accessible export or screen-reader assessment has been completed.

Guidance: [WAI PDF table markup](https://www.w3.org/WAI/WCAG22/Techniques/pdf/PDF6).

## Executed candidate checks

- 494 source-built HTML documents and 498 generated output documents: zero Nu messages in the current recorded checks.
- 2,665 source URL/document/fragment targets resolved in 81 documents. This checks target availability, not every assertion's correctness.
- Three-engine local HTTPS reading flows and a 17-page automated accessibility sample passed. This is not WCAG certification.
- Fourteen integrity/hosting tests and three output tests passed on local Node 24.22.0.
- The candidate source patch passes a reverse-application check against the tested working tree.
- Current candidate fingerprint: `0e49cc0ca83b015a7a2e0ec17c5f8416b5248d42ca3f1d16ee2bdbae4085f08b`.

Evidence is in `candidate-verification.json`, `candidate-static-verification.json`, the scoped browser receipts and `audit-register.json`. No hosted CI or Vercel deployment of this candidate is claimed.

## How to read the register

`audit-register.json` tracks all 74 chapters, the 81 original requirements, findings and release gates. It records **13 initial chapter passes, 61 not yet substantively audited, zero independently approved chapters, zero closed requirements and zero approved exclusions**.

The captured snapshot contains 857 inventory rows across its groups. The separate API CSV retains 314 owner records, 1,574 direct member records and 437 definition records. These are captured inventories, not totals of completed behavioral teaching. This batch did not perform a fresh normative reconciliation of every row.

## Next work

1. Audit Chapters 14 to 27 with the same explanation/example/answer/source separation.
2. Continue requirement-level and API-member behavior mapping, including actual edge-case examples rather than signatures alone.
3. Expand accessibility tasks beyond the sampled keyboard flows; obtain actual screen-reader and PDF-reader observations.
4. Resolve prototype semantic/table issues before generating and validating the full tagged book.
5. Merge and publish a correction batch only with a regenerated, verified site/PDF pair. Do not call the full book final while the register has open required coverage or review gates.

The remaining review work is not caused by missing author permission. It is also not an instruction that the author must personally become the technical or accessibility reviewer.

## Reproduction notes

`candidate-source.patch` contains maintained-source changes against the baseline commit, not a ready-to-upload deployment. Apply it in a separate checkout and rebuild the website and PDF through the real builders before testing or publishing. It deliberately excludes expanded generated trees and PDF binaries to avoid duplicate workspace artifacts.

`reproduce-baseline-samples.py` runs from an installed baseline checkout with its generated `dist/`. `reproduce-candidate-security.py` runs from the candidate checkout after generating its output. The tagged-prototype builder accepts the extracted repository path. Install the repository verification requirements and the additional pinned packages in `requirements-audit.txt`; browser engines and the recorded Nu checker are separate verification dependencies.

Original editorial rights and all third-party rights remain unchanged. Source retrieval records identify WHATWG/DOM definitions; quoted or derived source material retains its upstream terms. The existing publication's source/font notices remain applicable. No new open editorial license or endorsement is implied.
