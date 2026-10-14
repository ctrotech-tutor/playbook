# CTROTECH HTML Playbook — editorial and technical standard

**Version:** 0.2, planning edition. **Review date:** 14 October 2026. **Approval:** pending. This standard is a production contract, not evidence that its requirements have already been met.

## 1. Product and scope

Build one maintained publication with two connected reading modes: a guided beginner-to-professional curriculum and an exhaustive, searchable reference at the agreed HTML scope. Generate the documentation website and PDF from the same chapter sources. Do not maintain separately edited prose editions.

Retain 74 chapters as a provisional teaching structure, not a completeness measure. Add explicit reference inventories for APIs, value registries and compatibility evidence. HTML-defined web-platform APIs need an agreed integration depth: merely naming Worker, CanvasRenderingContext2D or Window does not document their members. Until this is resolved, never advertise complete coverage of the entire HTML Living Standard.

HTML owns a language, document processing and numerous APIs. SVG, MathML, CSS, ECMAScript, DOM, ARIA, HTTP, Fetch, CSP, SRI and Permissions Policy have separate authorities. Teach their HTML integration; explicitly declare delegated depth. A justified scope boundary is acceptable; an invisible omission is not.

## 2. Source hierarchy and claim labels

Every consequential factual assertion must be traceable to an exact section, with a review date. Discovery indexes are useful but do not replace normative definitions.

- **Standard requirement:** the actual WHATWG HTML normative definition or processing requirement. Preserve distinctions between author conformance and user-agent requirements. Use DOM, URL, Fetch or another specification where that specification owns the assertion.
- **Authoring recommendation:** a standards recommendation or explicitly labeled CTROTECH recommendation. Do not convert should into must or a house convention into a language rule.
- **Observed behavior:** a recorded browser/version/platform test or qualified implementation documentation; do not infer this from standard presence.
- **Accessibility requirement/guidance:** cite WCAG 2.2 success criteria where relevant; use WAI guidance, ARIA in HTML, HTML-AAM, WAI-ARIA and AccName for the claims they actually support. A tutorial pattern is not itself WCAG certification.
- **Compatibility metadata:** MDN Browser Compatibility Data with retrieval date and pinned release/commit for publication. Preserve flags, partial implementations, notes, removal versions and preview labels. MDN prose explains; it is not the HTML normative authority.
- **Engineering choice:** explicitly identify an optional approach and its trade-offs.

Do not use search snippets, a model's recollection or another tutorial as final evidence for a normative claim. WPT can supply useful implementation evidence; a test's existence is not proof that it passed in our tested browser versions.

## 3. Three independent status axes

Record specification/conformance status, implementation maturity and publication-review status separately. An experimental BCD label is not the same as an obsolete HTML feature. Conversely, a standard-track feature is not necessarily widely available.

Specification labels include conforming indexed HTML, foreign-vocabulary integration, autonomous-custom-element category, obsolete-but-conforming under conditions, obsolete/nonconforming for authors, and externally defined/proposal pending authority review. Implementation labels must be evidence-backed. Publication labels are planned, partial, complete, justified out-of-scope or blocked, with independent normative/example/exercise/accessibility/security/compatibility checks.

An extraction test passing only verifies that the captured records were extracted and reconciled as asserted. It does not close any teaching-material review gate.

## 4. Definition of a complete feature entry

A feature entry requires: stable ID; name and aliases; namespace and authority; normative definition URL(s); specification status; teaching owner and reference owner; semantics; permitted contexts and content; conditional exceptions; applicable attributes; values, defaults and invalid/missing-value behavior; reflection/API ties where relevant; practical examples; common mistakes; accessibility and security implications; compatibility evidence and fallback; exercises and explained solutions when pedagogically applicable; reviewer and review date.

Not every obscure feature needs an equally long tutorial, but every in-scope feature needs a deliberate treatment. A reference-only decision must say why and link to prerequisite teaching. Mark irrelevant review fields as not applicable **with a reason**, not silently omitted.

## 5. Definition of a complete chapter

Each chapter must have measurable objectives, prerequisites, terms, a concept map, purposeful examples and explanations, limitations and mistakes, accessibility/security integration, exercises with explained answers, source references and internal links. Include basic, intermediate and advanced examples where they serve the topic; do not add artificial complexity to satisfy a quota.

A completed chapter has valid example source, reviewed expected outcomes, appropriate automated/manual checks, editorial review, working cross-references and verification of every assigned coverage record. All required checks need evidence. Planned examples do not satisfy this gate.

## 6. Example rules

Show complete context when it affects validity: doctype, document language, encoding, title, MIME type, containing form/table, accessible label, resource origin or script position. An intentionally incomplete snippet must say what surrounds it. An intentionally invalid example must be visibly labeled and paired with a corrected version and an explanation of the violation.

Distinguish tag syntax from elements and the parsed DOM; HTML source from the live DOM; absent attributes from empty values; content attributes from IDL properties; boolean presence from strings; void elements from XML empty-element syntax. Explain defaults and error recovery without teaching tolerated parser behavior as recommended authoring.

Do not imply that adding a role repairs incorrect semantics, that every button needs aria-pressed, that placeholders replace labels, that client-side validation secures a server, or that a successful conformance check proves accessibility or security.

Examples must use non-sensitive, fictional data and local or clearly documented resources. Never include live credentials, untrusted unsanitized content, tracking or unnecessary external requests. Cover real trust boundaries, not generic security badges.

## 7. Testing and evidence

Maintain examples as real files, not screenshots. Record expected validity and runtime behavior in example metadata. Run a pinned Nu checker where relevant and store its version, command, output and intentional-warning rationale. Nu tests HTML conformance, not complete accessibility, security or usability.

Add parsing/DOM assertions, submission fixtures and browser tests for behavior-sensitive examples. Record browser/version, operating system, date and relevant flags. Prefer semantic behavior assertions to screenshot-only tests. Automated accessibility checks supplement keyboard, focus, names/roles/states and appropriate assistive-technology review; they do not certify WCAG conformance.

Include expected-failure fixtures for common mistakes; prove that the check detects the intended problem. Do not report a test as passed until it has executed. Do not report every-browser support from one successful run. No teaching examples have been authored or validated in this foundation edition.

## 8. Accessibility and security are cross-cutting

Integrate headings, names, labels, keyboard operation, focus, landmarks, text alternatives, form errors, tables, language and media alternatives into their original chapters. Keep dedicated accessibility chapters for synthesis rather than postponing all accessibility instruction until the end.

Likewise, explain embedding policies, sandbox boundaries, injection risks, URL/navigation implications, form submission, referrers, script/resource loading, server-side validation and authentication/authorization only where applicable. Distinguish HTML mechanisms from server and infrastructure controls. Review progressive enhancement and unsupported-feature behavior.

## 9. Exercise and answer design

Use prediction, diagnosis, repair and small builds rather than recall alone. Every question has an answer with reasoning and rejected alternatives explained where useful. Practical tasks need acceptance criteria and a runnable reference implementation. Rubrics assess semantics, conformance, accessibility, robustness and maintainability, not merely visual similarity.

Keep quiz answers and code fixtures versioned with the chapter. Do not call an answer correct just because it runs: permissive parser recovery can conceal authoring errors.

## 10. Single-source publication architecture

Proposed repository: `content/chapters/`, `content/reference/`, `examples/`, `answers/`, `data/`, `tests/`, `tools/` and `site/`. Each chapter has front matter with ID, slug, title, prerequisites, objectives, coverage IDs, sources and review state. Write prose once in a documented Markdown/MDX subset and extract code from tested example files. Reject duplicate chapter IDs, missing references and undefined coverage IDs in CI.

Use the same content graph and example versions for HTML and PDF. The website needs semantic navigation, search, visible status badges and usable keyboard behavior. The PDF needs selectable text, useful links, bookmarks, a generated contents list and an accessible export workflow. A normal PDF export is **not** automatically a tagged accessible PDF; inspect and test the chosen pipeline before promising accessibility compliance.

This foundation's HTML, PDF and workbook are planning outputs generated from the same captured data and audit source. They are not the final chapter-publishing system.

## 11. Change control and release procedure

For a release, pin the HTML Standard revision and BCD revision; retain URLs, retrieval dates, hashes, applicable licenses and attribution requirements. Reconcile refreshed element/attribute/input/category/interface/section inventories, and inspect changed definitions. Do not silently overwrite historical source snapshots.

A standards delta can add/remove features, change content models, modify values or alter processing behavior. A BCD delta can change support without a standards change. Both require reviewed updates, changelog entries and relevant test reruns. Assign an actual maintainer and review cadence before launch; a proposed cadence is not an operating maintenance service.

## 12. Readiness for the HTML lead magnet

Prepare a clearly versioned download and working delivery method before publishing a 'comment HTML' video. Test the public link from a logged-out/mobile context, test the actual manual or authorized automated DM flow, and ensure branding matches the delivered artifact. Do not promise free automation, automatic DMs or subscriber handling that has not been configured and tested. Disclose any data collected, purpose and retention.

The campaign can say 'HTML starter playbook' only if that specific resource exists and has passed its stated scope gates. Do not offer a complete beginner-to-professional reference while delivering this planning pack. Build the publication first; write the promotion around the actual finished promise.
