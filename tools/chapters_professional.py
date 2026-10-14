M(61,'Accessibility starts in the markup','Semantic HTML helps, but it does not certify the whole experience.',
'''Use native elements that fit the task, then review the name, role, state and behavior actually exposed to users. A button needs an understandable name and an operable action. A heading needs a useful position in the document hierarchy. A table needs its data relationships.

ARIA can supplement semantics where needed. It can also introduce wrong or conflicting information. Follow ARIA in HTML restrictions rather than adding roles to every element. Prefer an existing visible label through a native label relationship or a suitable reference before inventing an unrelated hidden name.

## Review the entire task
A successful automated scan does not demonstrate WCAG conformance. Test keyboard operation, visible focus, text alternatives, error correction, zoom, reflow and appropriate assistive-technology behavior. Include the actual data and content states, not just a polished empty page.

WCAG describes requirements at the level of the delivered experience. HTML-AAM, AccName, WAI-ARIA and ARIA in HTML help answer more specific mapping and authoring questions. This edition links to them but has not completed an independent accessibility audit. Record that limitation instead of turning a few semantic examples into a certification badge.''',
'''<form action="catalogue.html" method="get">
  <label for="accessible-search">Search books by title</label>
  <input id="accessible-search" name="q" type="search">
  <button type="submit">Search books</button>
</form>''',
'''The visible label, control relationship and button text support an understandable task. You still need a functioning search response, usable focus styles and tested result/error states in the real service.''',
"Adding an aria-label that contradicts the visible wording, or describing role-based automated tests as a complete accessibility review.",
"A scanner reports no issues. What should you do before claiming that the search experience is accessible?",
"Complete the relevant manual and assistive-technology checks across the actual task and states, assess applicable WCAG requirements, and document results and limitations. A scanner result is one piece of evidence.",
[('HTML semantics and ARIA','dom.html#wai-aria')],
'Use native semantics with accurate names|Separate automated checks from accessibility conformance')

M(62,'Keyboard and focus review','Follow the task without touching the mouse.',
'''Begin at the top of the page and use Tab, Shift+Tab, Enter, Space and the keys appropriate to each native control. Confirm that every needed action is reachable, the order is sensible and focus remains visible.

Do not require hover to reveal the only route to an action. A control that appears on pointer hover should have an equivalent usable focus or interaction path. Keep focus indications strong enough to locate rather than removing outlines without a replacement.

## Check transitions, not just tab stops
Open and close a dialog. Submit an invalid form. Remove a focused list item. Load more results. These transitions need deliberate focus and feedback behavior. Moving focus on every update can be as disruptive as losing it.

A disabled control and an aria-disabled control do not automatically behave the same way. ARIA communicates semantics but does not implement all interaction restrictions. Choose the appropriate element/state and test the actual behavior.

Record the browser, operating system and assistive technology used. A successful keyboard pass in one environment is useful evidence, not a claim about all combinations.''',
'''<a href="#keyboard-main" class="skip-link">Skip to main content</a>
<main id="keyboard-main" tabindex="-1">
  <h1>Reading list</h1>
  <button type="button">Add a book</button>
</main>''',
'''This is a starting structure. The stylesheet must keep the skip link discoverable on focus, and the Add a book action still needs its implementation and focus plan.''',
"Setting a positive tabindex sequence to match a visual layout instead of fixing the source order.",
"After deleting the focused row in a list, where should focus go?",
"There is no universal target. Choose a predictable nearby control or a relevant list heading based on the task, then test the behavior. Do not let focus disappear into the document body accidentally.",
[('focus model','interaction.html#focus')],
'Run a task-based keyboard check|Plan focus after dynamic changes')

M(63,'Trust boundaries','Treat browser input as something the server must verify.',
'''A browser can display constraints and hidden values, but a requester can send a different request. Validate on the server, enforce the relevant authentication and authorization rules, and apply abuse controls appropriate to the service.

For content insertion, distinguish plain text from accepted markup. textContent fits text. Markup acceptance needs a maintained, context-appropriate sanitization strategy. A handmade list of forbidden strings is not a dependable general sanitizer.

## Review each boundary
A form crosses into a server handler. An iframe crosses into another document. A script can introduce a remote execution dependency. A file upload crosses into storage and later retrieval. Document the expected origin, allowed capabilities and validation for each boundary.

Security policies and headers belong to the deployment as well as the document. CSP, CORS, SRI, referrer policy and Permissions Policy address different concerns. Do not describe any one of them as a complete defense. Test the intended failure behavior, and never place private API credentials in HTML, client JavaScript, data attributes or a downloadable environment file.''',
'''<p id="reader-comment"></p>
<script>
  const commentFromAReader = "A useful guide <script>example</scr" + "ipt>";
  document.getElementById("reader-comment").textContent = commentFromAReader;
</script>''',
'''The comment is rendered as text. Splitting the closing script spelling here avoids accidentally terminating the surrounding HTML script element. Real serialization should use a reviewed data-embedding strategy.''',
"Thinking that a value is trusted because it originated in a hidden input or a front-end build variable.",
"Why must the server ignore a submitted role=\"admin\" value when deciding a requester's permissions?",
"The requester controls submitted data. Authorization must use trusted server-side identity and permission information, not a role string supplied by the client.",
[('security introduction','introduction.html#security-and-privacy')],
'Identify client-controlled data|Choose controls for specific trust boundaries')

M(64,'Performance without folklore','Find the slow resource before adding an optimization.',
'''HTML influences resource discovery and loading. An early stylesheet link, a delayed image source, script loading attributes and image candidates can affect the page's critical work. Measure the actual page on representative conditions before prescribing changes.

Provide image dimensions and appropriate resources. Keep likely important above-the-fold media from being needlessly delayed. Lazy loading is useful when deferring a resource is appropriate; it is not a rule to apply to every image.

## Test a before and an after
Record the page version, device or emulation, network conditions and measurement method. Repeat enough to recognize variation. Do not invent percentage improvements or treat one warm-cache result as a stable performance guarantee.

A fast initial response can coexist with a slow interaction. Loading less script helps only when it addresses actual work. Keep the underlying document usable while enhancements load. Review the network waterfall and interaction path together rather than optimizing a score in isolation.''',
'''<img src="library-entrance.jpg" alt="The library entrance beside the reception desk"
     width="1440" height="960" fetchpriority="high">''',
'''A high priority hint can be appropriate for an important image, but only when the page and measured loading behavior justify it. This filename is an illustrative resource, not an image included in the example sandbox.''',
"Claiming that fetchpriority=\"high\" on every image makes the page faster.",
"What evidence should accompany a claim that an HTML loading change improved performance?",
"A recorded before/after measurement under stated comparable conditions, with the tested page version and enough detail to reproduce it. Explain variability and avoid generalizing beyond the measured scenario.",
[('fetch priority','urls-and-fetching.html#fetch-priority-attributes'),('lazy loading','urls-and-fetching.html#lazy-loading-attributes')],
'Relate HTML loading choices to real resources|Report measured results with their conditions')

M(65,'Findable and shareable pages','Describe the page accurately before chasing a search treatment.',
'''Use descriptive titles, meaningful headings and links, useful body content and accurate metadata. A crawler cannot discover a resource through a private thought or a button whose only destination exists in opaque application state.

Canonical URLs should identify the intended canonical document, not point every page to the home page. Alternate-language relationships need correct URLs and language relationships. Structured data should match the visible content and an actual supported vocabulary.

## Keep promises narrow
A meta description can help summarize a page but does not force a search snippet. Structured data does not guarantee a rich result. Social-card previews depend on platform behavior, caching and the accessible resource URLs.

Test the deployed output, not only templates. A robots restriction, a wrong status code, an inaccessible asset or a repository subpath error can undo otherwise tidy head markup. Do not add a measurement claim or an SEO guarantee to sales copy without actual evidence.''',
'''<article>
  <h1>How to renew your library membership</h1>
  <p>Check the documents you need before visiting the desk.</p>
  <a href="membership-documents.html">Documents accepted for renewal</a>
</article>''',
'''The heading and link describe a specific task. The actual accepted-document page must exist and give current information. HTML alone does not ensure indexing or ranking.''',
"Using the same generic summary and title on every page, then adding unsupported ranking claims.",
"Does a valid canonical link prove that a search engine will choose your preferred URL?",
"No. It supplies a signal that consumers interpret under their own rules. Keep the signal accurate and consistent with redirects, links and actual content, then inspect the deployed behavior.",
[('document metadata','semantics.html#document-metadata'),('link types','links.html#linkTypes')],
'Write task-specific titles and links|Qualify metadata and search-consumer claims')

M(66,'Maintainable HTML','A useful baseline makes later changes less fragile.',
'''Keep the content, relationships and primary task available before adding optional enhancements where the service permits it. Progressive enhancement is a design approach, not a promise that every application can offer identical behavior without scripting.

Use consistent naming, a small number of clear components and maintained sources for repeated structures. Avoid editing separate website and PDF copies of the same explanation. A single-source build reduces drift, but the generated outputs still need independent checks.

## Plan for changed content
Test a long name, a translated label, no results, a server error and more content than the design screenshot contained. A layout that only works with one short English phrase is not ready for real users.

Keep source review dates, compatibility notes and meaningful changelog entries. A Living Standard and browser implementations can change independently. Assign an actual maintainer before promising updates. Do not advertise an automated maintenance process that has not been configured.''',
'''<form action="catalogue.html" method="get">
  <label for="baseline-query">Title or author</label>
  <input id="baseline-query" name="q" type="search">
  <button type="submit">Search catalogue</button>
</form>
<p><a href="all-books.html">Browse the complete list instead</a></p>''',
'''A real endpoint can support a conventional form submission. A script may add in-page results, while the browse link provides another route. A static file with no query handler is not automatically that endpoint.''',
"Calling a page progressively enhanced when every visible route silently depends on one script succeeding.",
"What content states should you test besides the short, successful example shown in a design file?",
"Include empty, loading, error, long-content, translated and high-density states as relevant to the task. Test the actual interaction and recovery path, not just their appearance.",
[('extensibility and authoring','introduction.html#extensibility')],
'Keep a useful baseline where feasible|Review content variation and maintenance responsibilities')

M(67,'A release checklist that means something','An unchecked box is an open task, not a smaller font.',
'''Check the built documents with a recorded checker version. Test internal links and referenced assets under the real deployment base path. Inspect the browser console and run behavior tests for the examples that make behavior claims.

Review keyboard navigation, focus, names, text alternatives, form errors, reflow and relevant assistive-technology use. Record what was tested and what was not. Security and accessibility reviews need named responsibilities and evidence rather than decorative badges.

## Separate authoring from approval
An answer being written does not mean it has been independently checked. A chapter existing does not mean every assigned feature is fully documented. Keep drafting, example conformance, browser behavior, compatibility and editorial approval as separate states.

For publication, verify the PDF's text, links, navigation and accessibility workflow; do not call an untagged export an accessible PDF. Check downloads in a logged-out browser and test the promised delivery method. This review edition is for that inspection, not a claim that every whole-Standard coverage gate has closed.''',
'''<section aria-labelledby="release-heading">
  <h2 id="release-heading">Before publishing</h2>
  <ul>
    <li>Validate the built documents and record the output.</li>
    <li>Test the main tasks with a keyboard.</li>
    <li>Check paths under the deployment subdirectory.</li>
    <li>Record remaining content and technical review work.</li>
  </ul>
</section>''',
'''This is a visible checklist, not an assertion that its tasks passed. A project should link each claimed result to the relevant command output, environment or review note.''',
"Renaming a draft final and carrying its unchecked review states into the release unchanged.",
"What should you do if examples validate but the API-member inventory is incomplete?",
"Report the example result separately, keep API coverage open, and limit the publication promise or complete the missing inventory before making the broader claim. One passing check cannot close unrelated work.",
[('conformance','introduction.html#conformance-requirements')],
'Keep independent review states|Tie release claims to specific evidence')

PROJECTS=[
(68,'Build a personal profile','A complete first document with an honest scope.',
'''Build a profile for a fictional library volunteer. Include the person's name, a short introduction, relevant experience and a way to navigate to a contact section. Use fictional contact details and make that clear in the source notes.

Start with a complete document shell. Give the page a useful title, a language and one clear main heading. Group experience under an appropriate subsection heading. A profile image is optional; if you use one, choose and review its alternative from the image's purpose.

## Acceptance criteria
The document must pass the chosen conformance check, preserve a sensible reading order without CSS and use real links for navigation. A visible contact heading must remain understandable on its own. Do not add fabricated qualifications or testimonials to make the sample sound established.

Open the downloadable reference project only after attempting your version. Compare the semantics and relationships rather than copying its colours. The supplied project is static; it does not send messages or collect visitor data.''',
'''<main>
  <h1>Ada, library volunteer</h1>
  <p>I help readers find their next book.</p>
  <a href="#contact">Contact information</a>
  <section><h2>At the library</h2><p>Reading-group support and catalogue help.</p></section>
  <section id="contact"><h2>Contact information</h2><p>Ask at the desk for the volunteer coordinator.</p></section>
</main>''',
"What makes the fragment link a genuine navigation feature rather than a decorative button?",
'It has an href that points to the unique contact id. The destination contains the promised contact information. Test the fragment and reading order in the built document.'),
(69,'Build a portfolio','Organize several pieces of work without inventing a career.',
'''Build a portfolio for a fictional front-end learner. Include an introduction, two project descriptions and a contact route. State what each sample actually does. A static form interface must not be described as a deployed application service.

Choose whether each project description stands as an article or fits under a simpler section heading. Link text should identify the project or destination. Keep navigation consistent between the home page and a project page.

## Acceptance criteria
Use distinct page titles, correct relative links, useful headings and visible current-page navigation where relevant. Explain project limitations in ordinary prose. Keep code screenshots optional, with text and links that still communicate the work.

The downloadable version includes a second document so you can test navigation under a repository subpath. Check both directions. A successful trip from the home page to a project is only half of the link test.''',
'''<section aria-labelledby="work-title">
  <h2 id="work-title">Selected work</h2>
  <article><h3>Library notice board</h3><p>A static page for public notices.</p>
    <a href="project.html">Read about the notice board</a></article>
</section>''',
"What should the portfolio say about a contact form that has no processing endpoint?",
'It should identify the form as an interface demonstration or omit it in favour of an actual contact route. Do not tell readers it delivers messages.'),
(70,'Build a registration form','Make the correction path as clear as the happy path.',
'''Build an application form for a fictional reading group. Ask only for a name, email address and session choice. Add a visible privacy/use explanation suited to the demonstration, not a claim about a real service.

Use labels, an appropriate email state, an autocomplete purpose and a labelled select. Required fields need visible guidance and appropriate native constraints. Include a conventional submit control and explain that a static reference file has no application backend.

## Acceptance criteria
The interface needs a sensible keyboard order and readable instructions. It must not claim a submitted application was accepted unless an actual handler reports that result. In the supplied reference, JavaScript intercepts submission and explicitly says it is a local demonstration. The no-script path must disclose the limitation too.

Review the request design separately before adapting this into a live service. Client validation, a success-looking animation and a disabled button do not provide server validation or authorization.''',
'''<form action="#registration-note" method="get">
  <label for="project-name">Name</label>
  <input id="project-name" name="name" autocomplete="name" required>
  <label for="project-email">Email</label>
  <input id="project-email" name="email" type="email" autocomplete="email" required>
  <button type="submit">Check this demonstration</button>
</form>
<p id="registration-note">Demonstration only. No application service is connected.</p>''',
"Why should a real application not send personal registration details in a GET query just because this demo uses a simple local action?",
'URLs can be retained or exposed through history, logs and other contexts. Design the live service with appropriate transport, method, privacy, validation and storage controls. The static demonstration is not a live collection endpoint.'),
(71,'Build an article page','Make long content navigable without turning every paragraph into a card.',
'''Build a documentation article called How lending works. Include a page title, introduction, an on-page contents list, three meaningful sections and an update date. Use time only when you can supply the appropriate machine-readable value.

The contents links must point to unique section ids. Keep heading levels consistent. An aside can hold genuinely supporting material, such as a definition of an unfamiliar term, but not the only copy of essential renewal instructions.

## Acceptance criteria
The article must remain readable without its layout stylesheet. A keyboard user should reach the contents links and follow them. Code examples, if present, must be text rather than screenshot-only information. Do not add a fictional expert quotation for atmosphere.

Use the reference project to inspect document structure, then improve the content for a real service. A guide is only useful while its instructions match the service it describes.''',
'''<article>
  <h1>How lending works</h1>
  <nav aria-label="On this page"><a href="#borrowing">Borrowing</a></nav>
  <section id="borrowing"><h2>Borrowing</h2><p>Ask at the desk about the current lending policy.</p></section>
</article>''',
"What should happen when the label Borrowing in the contents is activated?",
'It should reach the matching borrowing section in the same document. Test that the id exists exactly once and that the landing content matches the label.'),
(72,'Build a data dashboard','Keep every displayed number understandable.',
'''Build a static dashboard with fictional lending data. Include a period label, a small summary and a data table. Label the data as fictional so it cannot be mistaken for evidence about the real library.

Every quantity needs a unit or context. A number card saying 42 does not say whether it means books, readers, days or percent. Use table headers for comparisons and a caption that identifies the dataset.

## Acceptance criteria
The table must preserve row/column relationships and have a usable small-screen strategy. A graphical summary is optional and must have a meaningful equivalent. Do not communicate a status only through colour.

The reference project has no live data feed. It demonstrates structure and a clearly labelled static dataset. If you later connect a service, add timestamps, loading/error states and data-source explanations that reflect the actual implementation.''',
'''<table>
  <caption>Fictional loans by collection, October sample</caption>
  <thead><tr><th scope="col">Collection</th><th scope="col">Loans</th></tr></thead>
  <tbody><tr><th scope="row">Fiction</th><td>42</td></tr>
  <tr><th scope="row">Local history</th><td>18</td></tr></tbody>
</table>''',
"What is missing from a dashboard card that displays only 42?",
'A label, unit and time/context sufficient to interpret the number. If it is a change or percentage, the comparison basis must also be clear. Do not make the reader infer these from colour or position.'),
(73,'Build a media gallery','Give the images a structure and a loading plan.',
'''Build a small gallery of three self-contained illustrations. The downloadable reference uses simple locally included SVG drawings rather than claiming to include photographs of a real place. Inspect each file before writing its alternative.

Use a list when the gallery is a collection of items. A figure and caption can keep each illustration with its description. Decide whether the image repeats a caption or contributes additional information and write alt accordingly.

## Acceptance criteria
All resources must resolve offline from the downloaded folder. Images need intentional dimensions. Links, if present, should name their destinations. Keep a clear heading and avoid loading delays for the first important visible image without a reason.

Resize the page and test the image/text relationships. The gallery is not complete because every image has some alt string; the alternatives must match what the actual images and task require.''',
'''<ul>
  <li><figure>
    <img src="shelves.svg" alt="Three rows of books on a shelf" width="640" height="400">
    <figcaption>A study in organising a small collection.</figcaption>
  </figure></li>
</ul>''',
"Why should you inspect the included SVGs instead of trusting their filenames when writing alt?",
'A filename does not establish the meaningful visible content or its role in the page. The alternative should represent the actual image in context, including whether the caption already supplies some information.'),
(74,'Capstone: the library site','Bring the document, forms, data and navigation into one reviewable project.',
'''Build a multi-page library site with Home, Catalogue, Membership and Visit pages. This capstone is a static reference implementation, not a live lending system. Use that limitation in its public copy rather than implying real reservations or accepted applications.

Reuse a consistent document shell and navigation. Give each page its own title, main heading and current-page state. Include a catalogue table or list, a clearly identified demonstration form and an accessible visit/contact structure.

## Review against the rubric
Award up to four points each for document structure, semantic choice, keyboard/focus behavior, labels and errors, content clarity, resource/path reliability and maintainability. A score is a review aid, not a WCAG or security certification. Record a concrete observation for each awarded point.

Test every page at the repository subpath as well as locally. Check back navigation, fragment links, file downloads and the no-script form explanation. Use the example source and release checklist to document what passed and what still needs work. A real deployment needs an actual service design before it can accept private member data.''',
'''<main>
  <h1>Neighbourhood Library</h1>
  <p>A static reference site for learning HTML.</p>
  <a href="catalogue.html">Explore the example catalogue</a>
  <p>No books can be reserved and no applications are collected on this site.</p>
</main>''',
"What changes before this capstone can become a real membership service?",
'Implement and test the server workflow, appropriate authentication/authorization, input and upload handling as needed, privacy and retention rules, transport and deployment policies, and honest user-visible results. Re-review the final experience for accessibility and security.')]

for n,title,dek,lesson,code,q,a in PROJECTS:
    M(n,title,dek,lesson,code,'The fragment shows the core relationship. Download the complete reference project for its document shell, local assets and implementation notes. Compare your work against the acceptance criteria before reading the reference answer.',
      'Treating a static reference project as a connected production service.',q,a,[('authoring requirements','introduction.html#conformance-requirements-for-authors')],
      'Build the described project|Evaluate it against explicit acceptance criteria')
    BOOK[-1]['project_slug']={68:'profile',69:'portfolio',70:'registration',71:'article',72:'dashboard',73:'gallery',74:'capstone'}[n]
