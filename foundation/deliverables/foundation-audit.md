# CTROTECH HTML Playbook

## Foundation audit and editorial blueprint

**Planning edition v0.2 · 14 October 2026 · architecture approval pending**

A traceable starting point. Not a finished book.

## 1. What this milestone establishes

The captured WHATWG element, ordinary-attribute, handler, category, input-state, interface and detailed contents indexes have been extracted and structurally reconciled. Normative obsolete lists and the global-attribute section are separately inventoried. Each working feature record has a proposed teaching/reference owner.

**This is not a completed specification audit or a public lead magnet.** Full per-feature definition review, external accessibility/security integration, complete API/value inventories, teaching examples, exercises, projects and publication testing remain open. No chapter has been drafted. A planned owner is not completed coverage.

## 2. Verified snapshot counts

| Inventory | Count and counting rule |
| --- | --- |
| Named built-in HTML elements | 113; expanded names, excluding SVG/MathML roots and custom-element category |
| Physical element index rows | 111; h1-h6 is one physical row |
| Integration entries | 3; svg, math, autonomous custom elements |
| Ordinary attributes | 180 contextual rows / 144 unique names |
| Event-handler attributes | 89 rows; 71 names listed as global in the DOM chapter |
| Linked applicability contexts | 387; ordinary plus handler contexts, not all element/attribute pairs |
| Explicit named global attributes | 31; 28 brief-list names plus id/class/slot |
| Other global/family/integration records | 8; separately typed and conditional |
| Content-category index rows | 15; includes form-related subcategories and exceptions |
| Input states | 22 keywords/states |
| Input applicability | 48 physical rows / 45 data rows / 15 grouped columns / 990 expanded state cells |
| Obsolete authoring elements | 29 individually inventoried names |
| Obsolete attribute contexts | 143; not a unique-name count |
| Obsolete-but-conforming conditions | 7 normative conditional paragraphs |
| Named interfaces / main events | 166 / 49; both have explicit inventory boundaries |
| Header / MIME discovery entries | 10 / 29; not full HTTP/IANA registries |
| Detailed contents entries | 1236 unique links, including 17 numbered top-level areas |
| MDN discovery names | 139; secondary discovery, not HTML conformance count |
| Targeted BCD records | 6; metadata only, no runtime browser tests |
| Working coverage requirements | 81; C01-C15, E01-E16, A01-A18, B01-B20, L01-L12 |
| Teaching architecture | 74 proposed chapters + original A-H references + proposed I-K additions |
| Completed chapters / completed per-feature reviews | 0 / 0 |

## 3. Method and evidence boundaries

Extraction uses BeautifulSoup with html5lib. HTML5 parsing matters for optional dt end tags in grouped obsolete lists. Raw physical rows, contextual records, conditional text, applicability links, input cell classes and source URLs are retained. SHA-256 checks bind records to 13 captured source files. Rebuilding uses local snapshots, without refetching live pages.

The automated reconciliation currently passes **222 checks**: source hashes, expected table structure, counting rules, unique IDs, proposed owner validity, all 81 working requirement IDs, disjoint conforming/obsolete names, MDN discovery overlap, input-state grouping and captured source/definition anchors. These are inventory checks, not Nu, browser, accessibility or teaching-material tests.

The C/E/A/B/L wording is an operationalized working version of the supplied coverage structure, not a verbatim transcription. Wording and assignments require editorial approval. Full contents entries currently have routing-level owners; subsection-to-lesson mapping is not yet a reviewed teaching plan.

## 4. Findings and required architecture changes

### F01 · Four named HTML elements need explicit ownership

**Priority:** P0 · **State:** proposed_fix

The supplied family architecture did not explicitly account for canvas, picture, source and selectedcontent. All four appear in the captured conforming HTML element index.

**Action:** Assign canvas to CH-33, picture to CH-29, source jointly to CH-29/CH-30, and selectedcontent to CH-39; include all in APP-A.

**Closure gate:** Architecture approval.

**Evidence:** [indices](https://html.spec.whatwg.org/multipage/indices.html), [form-elements](https://html.spec.whatwg.org/multipage/form-elements.html).

### F02 · Move param out of modern embedding instruction

**Priority:** P0 · **State:** proposed_fix

param is in the normative nonconforming obsolete element list, not the conforming element index.

**Action:** Cover param in APP-F with contextual migration guidance. Explain object without treating param as a current authoring option.

**Closure gate:** Architecture approval.

**Evidence:** [obsolete](https://html.spec.whatwg.org/multipage/obsolete.html), [indices](https://html.spec.whatwg.org/multipage/indices.html).

### F03 · Keep element names, integration vocabularies and custom-element rules distinct

**Priority:** P0 · **State:** reconciled_snapshot

111 physical element-index rows expand to 113 named built-in HTML elements plus svg, math and the autonomous-custom-element category. The h1-h6 group expands to six names.

**Action:** Retain the physical rows for reconciliation; maintain separate named-HTML and integration records. Give autonomous custom elements an explicit CH-46/APP-A owner. Do not claim 111 or 116 named built-in HTML elements.

**Closure gate:** Inventory arithmetic.

**Evidence:** [indices](https://html.spec.whatwg.org/multipage/indices.html).

### F04 · A single attribute-name list is not an attribute audit

**Priority:** P0 · **State:** open

The ordinary attribute index has 180 contextual rows but 144 unique names. Attribute semantics and permitted values vary by element and input state.

**Action:** Preserve contextual rows, all linked definition targets and separate applicability contexts. Review defaults, state restrictions, reflection and value registries before completing coverage.

**Closure gate:** Per-feature normative review.

**Evidence:** [indices](https://html.spec.whatwg.org/multipage/indices.html), [input](https://html.spec.whatwg.org/multipage/input.html).

### F05 · Correct three discovered index-link mismatches in our reference routing

**Priority:** P0 · **State:** reconciled_snapshot

In the captured informative index, headingoffset and headingreset have applicability links targeting tabindex; slot targets the id definition. The normative global section/definitions provide the appropriate separate targets.

**Action:** Keep the observed links as evidence and use the extracted global-section definition links in our reference. Do not mistake intentionally specialized title or bdo/dir links for errors.

**Closure gate:** Definition-link resolution.

**Evidence:** [indices](https://html.spec.whatwg.org/multipage/indices.html), [dom](https://html.spec.whatwg.org/multipage/dom.html), [sections](https://html.spec.whatwg.org/multipage/sections.html).

### F06 · Newer features require independent compatibility treatment

**Priority:** P0 · **State:** partial_metadata_only

The snapshot includes selectedcontent, headingoffset/headingreset, command/commandfor, closedby, color alpha/colorspace and newer shadowroot attributes. Standard presence alone does not establish broad availability.

**Action:** Use separate conformance, compatibility and publication-review fields. Six targeted BCD metadata records are captured; browser runtime checks and remaining feature reviews are still pending.

**Closure gate:** Compatibility release review.

**Evidence:** [indices](https://html.spec.whatwg.org/multipage/indices.html), [bcd-selectedcontent](https://raw.githubusercontent.com/mdn/browser-compat-data/main/html/elements/selectedcontent.json), [bcd-global-attributes](https://raw.githubusercontent.com/mdn/browser-compat-data/main/html/global_attributes.json), [bcd-button](https://raw.githubusercontent.com/mdn/browser-compat-data/main/html/elements/button.json).

### F07 · Reconcile MDN without treating it as the HTML normative boundary

**Priority:** P0 · **State:** reconciled_discovery_only

MDN's captured element tables list 139 names: all 113 conforming HTML names, two foreign-vocabulary roots, 19 matches to the captured obsolete list, and five secondary-only names: geolocation, content, fencedframe, image and shadow.

**Action:** Keep secondary-only entries in a separate discovery ledger. geolocation's captured BCD source links a WICG proposal, not the WHATWG HTML definition. Historical aliases and external proposals need their own authority/status review.

**Closure gate:** External/proposal authority review.

**Evidence:** [mdn-elements](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements), [bcd-geolocation](https://raw.githubusercontent.com/mdn/browser-compat-data/main/html/elements/geolocation.json), [indices](https://html.spec.whatwg.org/multipage/indices.html), [obsolete](https://html.spec.whatwg.org/multipage/obsolete.html).

### F08 · The Standard is larger than an element-and-attribute reference

**Priority:** P0 · **State:** blocked_scope_decision

The full contents snapshot has 17 numbered top-level areas, including separate workers, worklets, storage, communication, processing, rendering and IANA material. Named interfaces alone do not inventory members or algorithms.

**Action:** Add proposed APP-I for API/interface coverage and explicit depth boundaries. Retain every detailed contents entry with a provisional routing owner. Resolve the depth promise before claiming whole-Standard completeness.

**Closure gate:** API-depth approval and member inventory.

**Evidence:** [contents](https://html.spec.whatwg.org/multipage/), [indices](https://html.spec.whatwg.org/multipage/indices.html).

### F09 · Microsyntax and keyword registries need their own audit

**Priority:** P0 · **State:** blocked_pending_inventory

The current extraction does not enumerate all rel values, meta names, autocomplete tokens, script-type/import-map rules, sandbox flags, encodings and enumerated attribute states/defaults.

**Action:** Add proposed APP-J and build definition-level value registries. The captured headers/MIME index is a starting list, not the full HTTP/IANA registry.

**Closure gate:** Value/default registry reconciliation.

**Evidence:** [contents](https://html.spec.whatwg.org/multipage/), [indices](https://html.spec.whatwg.org/multipage/indices.html), [input](https://html.spec.whatwg.org/multipage/input.html).

### F10 · Accessibility authority and mappings are not yet reconciled

**Priority:** P0 · **State:** blocked_pending_external_audit

HTML's global section refers to ARIA annotations but does not replace an inventory of allowed roles/properties, accessible names or accessibility mappings. These external documents have not been audited in this foundation.

**Action:** Reconcile WCAG 2.2, WAI guidance, ARIA in HTML, WAI-ARIA, HTML-AAM and AccName; connect the resulting records to each relevant chapter. Keep this gate explicitly open.

**Closure gate:** Accessibility coverage and example review.

**Evidence:** [dom](https://html.spec.whatwg.org/multipage/dom.html).

### F11 · Global attributes include ownership and serialization boundaries

**Priority:** P1 · **State:** partial_inventory

The brief global list has 28 HTML-listed names; DOM-owned id, class and slot bring the explicit named set here to 31. data-*, ARIA, CSS Shadow Parts and XML-related allowances are not all the same kind of global attribute.

**Action:** Keep eight separate family/integration records. Review part/exportparts under CSS Shadow Parts and preserve HTML-versus-XML conditions; do not describe wildcard families as unrestricted attributes.

**Closure gate:** Cross-specification attribute review.

**Evidence:** [dom](https://html.spec.whatwg.org/multipage/dom.html), [mdn-global-attributes](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Global_attributes).

### F12 · Input applicability and categories contain conditional information

**Priority:** P1 · **State:** reconciled_structure_review_pending

The input summary has 48 physical rows: three group headings and 45 data rows. Its 15 grouped columns represent 22 input states. The content-category index has 15 rows including form-related subcategories and exceptions.

**Action:** Preserve grouped state membership, source cell text/classes and footnote links; do not flatten every Yes into unconditional permission. Review conditional category memberships and transparent content models per element.

**Closure gate:** Content-model and input-state review.

**Evidence:** [input](https://html.spec.whatwg.org/multipage/input.html), [indices](https://html.spec.whatwg.org/multipage/indices.html).

### F13 · Obsolete features have more than one authoring status

**Priority:** P1 · **State:** reconciled_structure_review_pending

The normative snapshot yields 29 obsolete/nonconforming element names, 143 obsolete attribute contexts and seven obsolete-but-conforming conditional paragraphs. These are not one interchangeable deprecated list.

**Action:** Preserve warning-only conditions separately from prohibited authoring features, including exceptions on script attributes. Keep implementation parsing support distinct from authoring permission.

**Closure gate:** Historical migration review.

**Evidence:** [obsolete](https://html.spec.whatwg.org/multipage/obsolete.html).

### F14 · Main event and interface indexes have explicit coverage limits

**Priority:** P0 · **State:** blocked_pending_inventory

The main event index omits media-element and drag-and-drop event lists. The all-interfaces list is a named-interface discovery list, not all dictionaries, callbacks, typedefs, members or processing behavior.

**Action:** Keep 49 main-event rows and 166 named-interface entries with boundary labels. Add missing event inventories and a complete agreed-depth IDL inventory before closing API coverage.

**Closure gate:** API/event inventory reconciliation.

**Evidence:** [indices](https://html.spec.whatwg.org/multipage/indices.html), [contents](https://html.spec.whatwg.org/multipage/).

### F15 · Planning artifacts cannot satisfy the campaign promise

**Priority:** P0 · **State:** blocked_publication

No chapter, worked exercise, capstone reference implementation or teaching-example test suite has been produced at this milestone. All feature coverage remains planned.

**Action:** Use this pack internally. Approve scope and complete the technical inventories before Chapter 1. Do not publish a comment-HTML offer for a complete playbook until the promised deliverable and delivery flow have been tested.

**Closure gate:** Content and delivery readiness.

### F16 · Reproducible snapshots are not a pinned upstream release

**Priority:** P1 · **State:** open_release_control

Captured sources have retrieval metadata and SHA-256 hashes. Live HTML and raw BCD main URLs can change; no upstream revision/commit is pinned for a publication release.

**Action:** Rebuild this edition from the stored snapshots. At release freeze, pin upstream revisions, review diffs, retain attribution/license notices and record actual reviewer approvals and test environments.

**Closure gate:** Release reproducibility.

**Evidence:** [indices](https://html.spec.whatwg.org/multipage/indices.html), [bcd-selectedcontent](https://raw.githubusercontent.com/mdn/browser-compat-data/main/html/elements/selectedcontent.json).

## 5. Recommended product shape and scope decision

Use two linked reading modes: a guided curriculum for learning and a generated reference for exhaustive lookup at the approved scope. Keep the proposed 74-chapter spine, but do not force every rare feature into a long tutorial. Each reference-only treatment still needs explicit ownership, accurate constraints and a stated rationale.

**Decision required before scope freeze:** does complete mean professional HTML authoring with explicit integration boundaries, or tutorial/reference treatment of every API member and algorithm in the entire HTML Standard? The latter is much larger than a normal HTML playbook. APP-I can make the boundary explicit; it cannot silently reduce the agreed promise. No exclusions have been approved.

**Proposed additions, not yet approved:** APP-I (APIs/interfaces and depth boundaries), APP-J (microsyntax/value registries) and APP-K (status/compatibility/evidence register). Embed accessible/security-aware practice throughout, not only in the final engineering part.

## 6. Proposed chapter and reference map

### I · Understanding HTML

- **CH-01** — The web platform and the role of HTML. Status: planned.

- **CH-02** — HTML's history, evolution and Living Standard. Status: planned.

- **CH-03** — How browsers interpret web documents. Status: planned.

- **CH-04** — Elements, tags, attributes and content. Status: planned.

- **CH-05** — The DOM tree and document structure. Status: planned.

- **CH-06** — Setting up a development environment and creating a first page. Status: planned.

### II · Syntax and Document Foundations

- **CH-07** — HTML document anatomy and the doctype. Status: planned.

- **CH-08** — The html, head and body elements. Status: planned.

- **CH-09** — Character encoding, Unicode and character references. Status: planned.

- **CH-10** — Nesting, void elements and optional tags. Status: planned.

- **CH-11** — Attributes, quoting, whitespace and comments. Status: planned.

- **CH-12** — Content categories and content models. Status: planned.

- **CH-13** — HTML syntax, conformance and common errors. Status: planned.

### III · Text and Content Elements

- **CH-14** — Headings, paragraphs, thematic breaks and heading-level features. Status: planned.

- **CH-15** — Inline semantics, emphasis and quotations. Status: planned.

- **CH-16** — Code, technical text and machine-readable values. Status: planned.

- **CH-17** — Links, hyperlinks, fragments and navigation. Status: planned.

- **CH-18** — Ordered, unordered and description lists. Status: planned.

- **CH-19** — Figures, captions and self-contained content. Status: planned.

- **CH-20** — Dates, times, abbreviations and document edits. Status: planned.

- **CH-21** — International text, bidirectional text and language semantics. Status: planned.

### IV · Semantic Website Architecture

- **CH-22** — Generic containers and grouping elements. Status: planned.

- **CH-23** — Semantic regions and document organization. Status: planned.

- **CH-24** — Articles, sections, headers, footers and asides. Status: planned.

- **CH-25** — Navigation, landmarks and main content. Status: planned.

- **CH-26** — Tables, captions, headers and accessible data relationships. Status: planned.

- **CH-27** — Designing complete multi-page document structures. Status: planned.

### V · Images, Audio, Video and Embedded Content

- **CH-28** — Images, alternative text and image dimensions. Status: planned.

- **CH-29** — Responsive images: picture, source, srcset and sizes. Status: planned.

- **CH-30** — Audio, video, source, captions and tracks. Status: planned.

- **CH-31** — Image maps and interactive image regions. Status: planned.

- **CH-32** — Iframes, embedded resources and sandboxing. Status: planned.

- **CH-33** — Canvas, SVG, MathML and graphics integration boundaries. Status: planned.

### VI · Forms and Native Controls

- **CH-34** — How HTML forms work. Status: planned.

- **CH-35** — Labels, fieldsets, legends and accessible grouping. Status: planned.

- **CH-36** — Text inputs, email, passwords and search. Status: planned.

- **CH-37** — Numeric, date, time, color and range inputs. Status: planned.

- **CH-38** — Checkboxes, radio buttons, files and hidden inputs. Status: planned.

- **CH-39** — Select menus, selectedcontent, options, datalists and textareas. Status: planned.

- **CH-40** — Native validation, constraints and error handling. Status: planned.

- **CH-41** — Submission methods, encoding, server integration and secure handling. Status: planned.

### VII · Interaction and Modern HTML

- **CH-42** — Buttons, commands and native interaction semantics. Status: planned.

- **CH-43** — Disclosure widgets, details and summary. Status: planned.

- **CH-44** — Dialogs, popovers, close requests and related patterns. Status: planned.

- **CH-45** — Editing, focus, selection, drag-and-drop and user interaction. Status: planned.

- **CH-46** — Templates, slots, custom elements and declarative shadow DOM. Status: planned.

- **CH-47** — Custom data attributes, microdata and structured content. Status: planned.

### VIII · Attributes and Metadata

- **CH-48** — Global attributes in depth. Status: planned.

- **CH-49** — Element-specific attributes and valid values. Status: planned.

- **CH-50** — Titles, metadata, icons and document descriptions. Status: planned.

- **CH-51** — Links, resource hints and resource relationships. Status: planned.

- **CH-52** — Loading, fetching, referrer policies, integrity, nonces and priorities. Status: planned.

- **CH-53** — Attribute reflection, defaults and browser interpretation. Status: planned.

### IX · Browser Processing and Advanced Concepts

- **CH-54** — HTML parsing and tokenization. Status: planned.

- **CH-55** — Tree construction and error recovery. Status: planned.

- **CH-56** — DOM interfaces and document lifecycle. Status: planned.

- **CH-57** — Script loading, execution, import maps and integration. Status: planned.

- **CH-58** — HTML/XML differences, XHTML and serialization. Status: planned.

- **CH-59** — Rendering behavior and HTML's relationship with CSS. Status: planned.

- **CH-60** — Web-platform APIs, communication, workers, worklets and storage: integration overview. Status: planned.

### X · Professional HTML Engineering

- **CH-61** — Accessible HTML and WCAG-oriented implementation. Status: planned.

- **CH-62** — Keyboard navigation, focus and assistive technology. Status: planned.

- **CH-63** — Security, safe embedding, trust boundaries and policy integration. Status: planned.

- **CH-64** — Performance, loading behavior and media optimization. Status: planned.

- **CH-65** — SEO, metadata and structured content. Status: planned.

- **CH-66** — Internationalization, maintainability and progressive enhancement. Status: planned.

- **CH-67** — Validation, browser testing, code review and production checklists. Status: planned.

### XI · Practical Projects

- **CH-68** — Build a well-structured personal profile. Status: planned.

- **CH-69** — Build a multi-section portfolio. Status: planned.

- **CH-70** — Create an accessible registration form. Status: planned.

- **CH-71** — Build an article and documentation page. Status: planned.

- **CH-72** — Structure a data-rich dashboard. Status: planned.

- **CH-73** — Create a responsive media gallery. Status: planned.

- **CH-74** — Capstone: a complete multi-page website with an assessment rubric. Status: planned.

### Reference appendices

- **APP-A** — Alphabetical element reference: HTML names, foreign integration and custom-element rules. Status: planned.

- **APP-B** — Global attributes, wildcard families and cross-specification ownership. Status: planned.

- **APP-C** — Element-specific attributes, conditional applicability and event-handler attributes. Status: planned.

- **APP-D** — Input states, form attributes and control-specific restrictions. Status: planned.

- **APP-E** — Content categories, transparent models and conditional memberships. Status: planned.

- **APP-F** — Obsolete features, historical syntax and migration guide. Status: planned.

- **APP-G** — Glossary, troubleshooting, exercises and explained answer keys. Status: planned.

- **APP-H** — Standards bibliography, IANA context, compatibility links and maintenance log. Status: planned.

- **APP-I** — API/interface catalogue and explicit integration-depth boundaries (proposed addition). Status: planned.

- **APP-J** — Microsyntaxes, link relationships, metadata keywords, headers and MIME types (proposed addition). Status: planned.

- **APP-K** — Feature-status, compatibility-review and test-evidence register (proposed addition). Status: planned.

## 7. Publication standard

### 1. Product and scope

Build one maintained publication with two connected reading modes: a guided beginner-to-professional curriculum and an exhaustive, searchable reference at the agreed HTML scope. Generate the documentation website and PDF from the same chapter sources. Do not maintain separately edited prose editions.

Retain 74 chapters as a provisional teaching structure, not a completeness measure. Add explicit reference inventories for APIs, value registries and compatibility evidence. HTML-defined web-platform APIs need an agreed integration depth: merely naming Worker, CanvasRenderingContext2D or Window does not document their members. Until this is resolved, never advertise complete coverage of the entire HTML Living Standard.

HTML owns a language, document processing and numerous APIs. SVG, MathML, CSS, ECMAScript, DOM, ARIA, HTTP, Fetch, CSP, SRI and Permissions Policy have separate authorities. Teach their HTML integration; explicitly declare delegated depth. A justified scope boundary is acceptable; an invisible omission is not.

### 2. Source hierarchy and claim labels

Every consequential factual assertion must be traceable to an exact section, with a review date. Discovery indexes are useful but do not replace normative definitions.

- **Standard requirement:** the actual WHATWG HTML normative definition or processing requirement. Preserve distinctions between author conformance and user-agent requirements. Use DOM, URL, Fetch or another specification where that specification owns the assertion.
- **Authoring recommendation:** a standards recommendation or explicitly labeled CTROTECH recommendation. Do not convert should into must or a house convention into a language rule.
- **Observed behavior:** a recorded browser/version/platform test or qualified implementation documentation; do not infer this from standard presence.
- **Accessibility requirement/guidance:** cite WCAG 2.2 success criteria where relevant; use WAI guidance, ARIA in HTML, HTML-AAM, WAI-ARIA and AccName for the claims they actually support. A tutorial pattern is not itself WCAG certification.
- **Compatibility metadata:** MDN Browser Compatibility Data with retrieval date and pinned release/commit for publication. Preserve flags, partial implementations, notes, removal versions and preview labels. MDN prose explains; it is not the HTML normative authority.
- **Engineering choice:** explicitly identify an optional approach and its trade-offs.

Do not use search snippets, a model's recollection or another tutorial as final evidence for a normative claim. WPT can supply useful implementation evidence; a test's existence is not proof that it passed in our tested browser versions.

### 3. Three independent status axes

Record specification/conformance status, implementation maturity and publication-review status separately. An experimental BCD label is not the same as an obsolete HTML feature. Conversely, a standard-track feature is not necessarily widely available.

Specification labels include conforming indexed HTML, foreign-vocabulary integration, autonomous-custom-element category, obsolete-but-conforming under conditions, obsolete/nonconforming for authors, and externally defined/proposal pending authority review. Implementation labels must be evidence-backed. Publication labels are planned, partial, complete, justified out-of-scope or blocked, with independent normative/example/exercise/accessibility/security/compatibility checks.

An extraction test passing only verifies that the captured records were extracted and reconciled as asserted. It does not close any teaching-material review gate.

### 4. Definition of a complete feature entry

A feature entry requires: stable ID; name and aliases; namespace and authority; normative definition URL(s); specification status; teaching owner and reference owner; semantics; permitted contexts and content; conditional exceptions; applicable attributes; values, defaults and invalid/missing-value behavior; reflection/API ties where relevant; practical examples; common mistakes; accessibility and security implications; compatibility evidence and fallback; exercises and explained solutions when pedagogically applicable; reviewer and review date.

Not every obscure feature needs an equally long tutorial, but every in-scope feature needs a deliberate treatment. A reference-only decision must say why and link to prerequisite teaching. Mark irrelevant review fields as not applicable **with a reason**, not silently omitted.

### 5. Definition of a complete chapter

Each chapter must have measurable objectives, prerequisites, terms, a concept map, purposeful examples and explanations, limitations and mistakes, accessibility/security integration, exercises with explained answers, source references and internal links. Include basic, intermediate and advanced examples where they serve the topic; do not add artificial complexity to satisfy a quota.

A completed chapter has valid example source, reviewed expected outcomes, appropriate automated/manual checks, editorial review, working cross-references and verification of every assigned coverage record. All required checks need evidence. Planned examples do not satisfy this gate.

### 6. Example rules

Show complete context when it affects validity: doctype, document language, encoding, title, MIME type, containing form/table, accessible label, resource origin or script position. An intentionally incomplete snippet must say what surrounds it. An intentionally invalid example must be visibly labeled and paired with a corrected version and an explanation of the violation.

Distinguish tag syntax from elements and the parsed DOM; HTML source from the live DOM; absent attributes from empty values; content attributes from IDL properties; boolean presence from strings; void elements from XML empty-element syntax. Explain defaults and error recovery without teaching tolerated parser behavior as recommended authoring.

Do not imply that adding a role repairs incorrect semantics, that every button needs aria-pressed, that placeholders replace labels, that client-side validation secures a server, or that a successful conformance check proves accessibility or security.

Examples must use non-sensitive, fictional data and local or clearly documented resources. Never include live credentials, untrusted unsanitized content, tracking or unnecessary external requests. Cover real trust boundaries, not generic security badges.

### 7. Testing and evidence

Maintain examples as real files, not screenshots. Record expected validity and runtime behavior in example metadata. Run a pinned Nu checker where relevant and store its version, command, output and intentional-warning rationale. Nu tests HTML conformance, not complete accessibility, security or usability.

Add parsing/DOM assertions, submission fixtures and browser tests for behavior-sensitive examples. Record browser/version, operating system, date and relevant flags. Prefer semantic behavior assertions to screenshot-only tests. Automated accessibility checks supplement keyboard, focus, names/roles/states and appropriate assistive-technology review; they do not certify WCAG conformance.

Include expected-failure fixtures for common mistakes; prove that the check detects the intended problem. Do not report a test as passed until it has executed. Do not report every-browser support from one successful run. No teaching examples have been authored or validated in this foundation edition.

### 8. Accessibility and security are cross-cutting

Integrate headings, names, labels, keyboard operation, focus, landmarks, text alternatives, form errors, tables, language and media alternatives into their original chapters. Keep dedicated accessibility chapters for synthesis rather than postponing all accessibility instruction until the end.

Likewise, explain embedding policies, sandbox boundaries, injection risks, URL/navigation implications, form submission, referrers, script/resource loading, server-side validation and authentication/authorization only where applicable. Distinguish HTML mechanisms from server and infrastructure controls. Review progressive enhancement and unsupported-feature behavior.

### 9. Exercise and answer design

Use prediction, diagnosis, repair and small builds rather than recall alone. Every question has an answer with reasoning and rejected alternatives explained where useful. Practical tasks need acceptance criteria and a runnable reference implementation. Rubrics assess semantics, conformance, accessibility, robustness and maintainability, not merely visual similarity.

Keep quiz answers and code fixtures versioned with the chapter. Do not call an answer correct just because it runs: permissive parser recovery can conceal authoring errors.

### 10. Single-source publication architecture

Proposed repository: `content/chapters/`, `content/reference/`, `examples/`, `answers/`, `data/`, `tests/`, `tools/` and `site/`. Each chapter has front matter with ID, slug, title, prerequisites, objectives, coverage IDs, sources and review state. Write prose once in a documented Markdown/MDX subset and extract code from tested example files. Reject duplicate chapter IDs, missing references and undefined coverage IDs in CI.

Use the same content graph and example versions for HTML and PDF. The website needs semantic navigation, search, visible status badges and usable keyboard behavior. The PDF needs selectable text, useful links, bookmarks, a generated contents list and an accessible export workflow. A normal PDF export is **not** automatically a tagged accessible PDF; inspect and test the chosen pipeline before promising accessibility compliance.

This foundation's HTML, PDF and workbook are planning outputs generated from the same captured data and audit source. They are not the final chapter-publishing system.

### 11. Change control and release procedure

For a release, pin the HTML Standard revision and BCD revision; retain URLs, retrieval dates, hashes, applicable licenses and attribution requirements. Reconcile refreshed element/attribute/input/category/interface/section inventories, and inspect changed definitions. Do not silently overwrite historical source snapshots.

A standards delta can add/remove features, change content models, modify values or alter processing behavior. A BCD delta can change support without a standards change. Both require reviewed updates, changelog entries and relevant test reruns. Assign an actual maintainer and review cadence before launch; a proposed cadence is not an operating maintenance service.

### 12. Readiness for the HTML lead magnet

Prepare a clearly versioned download and working delivery method before publishing a 'comment HTML' video. Test the public link from a logged-out/mobile context, test the actual manual or authorized automated DM flow, and ensure branding matches the delivered artifact. Do not promise free automation, automatic DMs or subscriber handling that has not been configured and tested. Disclose any data collected, purpose and retention.

The campaign can say 'HTML starter playbook' only if that specific resource exists and has passed its stated scope gates. Do not offer a complete beginner-to-professional reference while delivering this planning pack. Build the publication first; write the promotion around the actual finished promise.


## 8. Remaining pre-Chapter-1 gates

- Approve the revised architecture, requirement wording, API depth and external vocabulary boundaries. No hidden exclusions.

- Extract/reconcile missing value/default registries, API members at the agreed depth and separately listed media/drag events.

- Audit ARIA in HTML, WAI-ARIA, HTML-AAM, AccName, WCAG/WAI integration and externally owned attributes/policies.

- Review every individual feature definition: content-model exceptions, attribute state restrictions, parser behavior, defaults and reflection. Resolve canonical links beyond the targeted checks already captured.

- Establish a version-pinned example/Nu/browser test harness and the website/PDF single-source publishing pipeline. These are not yet built or run.

- Approve a representative chapter acceptance template and the maintenance/release process. Only then start Chapter 1.

## 9. How to use the pack

Open the offline explorer for searchable inventories, the PDF for the readable audit and the workbook for editorial tracking. inventory.json and CSV exports retain the machine-readable detail; snapshots and scripts allow an offline extraction rebuild. The publication standard and chapter template define future acceptance criteria.

The workbook is an editable tracking copy. Its Review log is for reviewer decisions, evidence paths and notes. Editing the workbook does not update inventory.json; manually reconcile approved changes into the maintained source. Rebuilding the workbook overwrites that generated copy, so preserve edited review files separately.

No external hosting, comment trigger, direct-message automation, public download endpoint, Google Drive upload or Instagram publication has been configured for this playbook.

## 10. Source and licensing register

Captured-source authority levels are distinct: WHATWG indexes/contents are discovery; normative definition pages support targeted checks; MDN prose is secondary; BCD is implementation metadata. A source being captured does not mean every assertion on it was reviewed. The manifest retains original URL, response headers, byte count and SHA-256.

WHATWG source snapshots retain their embedded source notices; consult its copyright/license page before public redistribution. MDN prose and BCD have different licensing/attribution requirements; the final public product needs an attribution and license audit. This pack is a working evidence bundle, not a publication clearance.

- **indices** — [https://html.spec.whatwg.org/multipage/indices.html](https://html.spec.whatwg.org/multipage/indices.html); capture/review date 2026-10-14; SHA-256 `099e04f3b25b48b37c6b5b7c63dc2466c6851868ead5f5c81ed6e5dc88e14444`.

- **dom** — [https://html.spec.whatwg.org/multipage/dom.html](https://html.spec.whatwg.org/multipage/dom.html); capture/review date 2026-10-14; SHA-256 `d94b359c0d9693981e79896a5ebef58a1d5cb9587b6aaf1c850c128dd9e6a9c2`.

- **obsolete** — [https://html.spec.whatwg.org/multipage/obsolete.html](https://html.spec.whatwg.org/multipage/obsolete.html); capture/review date 2026-10-14; SHA-256 `68722ca3bfa4baf5f43e14a9ac6b8fd72db3c2e465f16fd7d1a2078aa332daaf`.

- **contents** — [https://html.spec.whatwg.org/multipage/](https://html.spec.whatwg.org/multipage/); capture/review date 2026-10-14; SHA-256 `4498dd6428731fb321f2303f93b44e2828eeb23c92bdbc1ee4bad7ee8712d4e3`.

- **input** — [https://html.spec.whatwg.org/multipage/input.html](https://html.spec.whatwg.org/multipage/input.html); capture/review date 2026-10-14; SHA-256 `42e1c82cc134814892cce4a26caea437d4200c35e3d0440b9ecf971fa9dc1499`.

- **mdn-elements** — [https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements); capture/review date 2026-10-14; SHA-256 `09e7fe028ffcd63430466ce97f73051f560be2c7440528212fbebaeae0430986`.

- **mdn-global-attributes** — [https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Global_attributes](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Global_attributes); capture/review date 2026-10-14; SHA-256 `014cfde6945a45a82fd16d5b4d1e81b8fd7b90b85c11cfdaf461540a3bf9cbf0`.

- **bcd-selectedcontent** — [https://raw.githubusercontent.com/mdn/browser-compat-data/main/html/elements/selectedcontent.json](https://raw.githubusercontent.com/mdn/browser-compat-data/main/html/elements/selectedcontent.json); capture/review date 2026-10-14; SHA-256 `018dca78d45753b4dba9797da18d4313a4de20b5fdc74ff97c6785db9cbb4c1a`.

- **bcd-global-attributes** — [https://raw.githubusercontent.com/mdn/browser-compat-data/main/html/global_attributes.json](https://raw.githubusercontent.com/mdn/browser-compat-data/main/html/global_attributes.json); capture/review date 2026-10-14; SHA-256 `962149bfd14e9c779d7a349efd47c579ee48f3bd07e8d33c361432b02ff52bc6`.

- **bcd-button** — [https://raw.githubusercontent.com/mdn/browser-compat-data/main/html/elements/button.json](https://raw.githubusercontent.com/mdn/browser-compat-data/main/html/elements/button.json); capture/review date 2026-10-14; SHA-256 `716546afd4a5bfe84c9411f98629bc0385f1fbcb338375e66caa89c2b4bab1a2`.

- **bcd-geolocation** — [https://raw.githubusercontent.com/mdn/browser-compat-data/main/html/elements/geolocation.json](https://raw.githubusercontent.com/mdn/browser-compat-data/main/html/elements/geolocation.json); capture/review date 2026-10-14; SHA-256 `a927e874b4dcaa181c3b1330b6d7e1005cee1a20444db32fded6e4d4cb8bc9b2`.

- **form-elements** — [https://html.spec.whatwg.org/multipage/form-elements.html](https://html.spec.whatwg.org/multipage/form-elements.html); capture/review date 2026-10-14; SHA-256 `2008179089beb0eb6c7a2214bf0540981c0f909cde9b0cdc9fde56cc95817843`.

- **sections** — [https://html.spec.whatwg.org/multipage/sections.html](https://html.spec.whatwg.org/multipage/sections.html); capture/review date 2026-10-14; SHA-256 `a2d8e77e33e329eaa034b69f8055a30a4bd689ad427fa2be5efc5c16433a9863`.

### Required external authorities — not yet audited

- [WCAG 2.2](https://www.w3.org/TR/WCAG22/) and [WAI tutorials](https://www.w3.org/WAI/tutorials/).

- [ARIA in HTML](https://www.w3.org/TR/html-aria/), [WAI-ARIA](https://www.w3.org/TR/wai-aria-1.2/), [HTML-AAM](https://www.w3.org/TR/html-aam-1.0/) and [AccName](https://www.w3.org/TR/accname-1.2/).

- [DOM](https://dom.spec.whatwg.org/), [CSS Shadow Parts](https://drafts.csswg.org/css-shadow-parts/) and relevant Fetch/CSP/SRI/Permissions Policy definitions.

- [Nu checker documentation](https://validator.github.io/validator/) and relevant browser documentation/WPT evidence.

## 11. Release position

**Foundation snapshot reconciliation: passed for the stated captured indexes. Full coverage audit: open. Chapter drafting: not started. Public playbook readiness: not ready.** This distinction is intentional: the ledger is a control against false completeness, not a way to manufacture it.
