M(21,'Language and direction','Language, writing direction and pronunciation are separate concerns.',
'''Set the primary language on html, then mark language changes where they occur. A valid language tag helps software choose pronunciation, spelling and other language-sensitive behavior. It does not translate the words or determine their writing direction.

Use dir for directionality. Values such as rtl and ltr express known directions; auto lets the user agent determine direction from the content under the defined rules. For user-provided names or messages of unknown direction, isolation can stop adjacent punctuation and text from being rearranged unexpectedly.

## Work with unfamiliar text
bdi isolates a run of text from the surrounding bidirectional context. bdo overrides direction and is a more specialized tool, not the normal choice for ordinary right-to-left text. Avoid inserting directional control characters casually when markup expresses the relationship more clearly.

Ruby annotations use ruby with rt and, where appropriate, rp fallback punctuation. They have language-specific uses and should be reviewed by someone who understands the writing system. Test the actual languages your product supports, including long words, mixed scripts and names that do not fit a Western given-name/surname assumption.''',
'''<p>Readers say <span lang="yo">Ẹ káàbọ̀</span> at the entrance.</p>
<p>Reserved for <bdi dir="auto">مريم</bdi>: shelf 4.</p>''',
'''The first span identifies Yoruba text. The bdi isolates the Arabic name from the English sentence and its punctuation. Language metadata does not replace a correct translation or a test with the intended text.''',
"Using CSS direction as the only representation of document language, or assuming every non-Latin script is right-to-left.",
"A visitor submits a name whose writing direction you do not know. What is a reasonable HTML wrapper inside an English sentence?",
"Use bdi, commonly with dir=\"auto\", around the name. Keep the surrounding sentence language separate. Insert the untrusted name as text, not as untrusted HTML.",
[('language and direction','dom.html#the-lang-and-xml:lang-attributes'),('bidi isolation','text-level-semantics.html#the-bdi-element')],
'Mark language changes|Isolate mixed-direction text')

M(22,'Containers and grouping','Use a generic container when the content has no more specific grouping meaning.',
'''div is a generic flow container. span is its phrasing-level counterpart. Both are useful. The problem is replacing meaningful elements with them automatically, or adding layers with no clear purpose.

A wrapper for a layout grid may be a div. An independent article can be article. A quoted passage belongs in blockquote. Keep these choices distinct from class names such as card, row and panel, which describe your implementation rather than defining HTML semantics.

## Group for a stated reason
Start with the text and controls, then add a wrapper only when layout, scripting or a content relationship needs one. A single element can carry several class tokens. You do not need a separate div for every CSS property.

Do not add a role to every generic container. Many wrappers should remain semantically neutral. Adding unnecessary landmarks or groups can make an interface harder to navigate with assistive technology. When you do add an explicit accessible group, give it an appropriate purpose and name and test that relationship.''',
'''<div class="contact-grid">
  <section aria-labelledby="visit-title">
    <h2 id="visit-title">Visit the library</h2>
    <p>Ask at reception for directions.</p>
  </section>
  <section aria-labelledby="call-title">
    <h2 id="call-title">Call the desk</h2>
    <p><a href="tel:+2341000000000">Call our example number</a></p>
  </section>
</div>''',
'''The outer div is a layout wrapper. The named sections carry the content organization. The telephone number is fictional and must be replaced before publishing a real contact page.''',
"Naming a div class=\"section\" and assuming it now has section semantics.",
"A wrapper exists only to arrange two existing sections in a grid. Does it need to become a third section?",
"No. A generic div is appropriate for the layout wrapper. Another section would imply another thematic grouping and should have a content reason.",
[('div','grouping-content.html#the-div-element')],
'Use generic wrappers deliberately|Avoid adding semantics without a content reason')

M(23,'Sections that have a subject','A section should explain the document, not a spacing requirement.',
'''section represents a thematic grouping, normally with a heading. A chapter's requirements, an article's background and a service page's eligibility rules can be sections. A border or a margin does not establish a theme.

A heading can be enough to structure a straightforward document without wrapping every subsection in section. Choose wrappers when they clarify grouping or are needed for the document's relationships. Keep the conventional heading hierarchy readable either way.

## Name important regions
A section with an accessible name can become a region landmark in relevant accessibility mappings. Name a region when users benefit from navigating to it, rather than naming every small block. aria-labelledby can reference an existing visible heading.

Source order should remain understandable when layout is removed. Moving columns with CSS does not change the DOM reading order. Review both the visible result and the underlying sequence, especially when the page has multiple related sections.''',
'''<section aria-labelledby="eligibility">
  <h2 id="eligibility">Who can join</h2>
  <p>Membership options depend on the service you need.</p>
  <h3>Young readers</h3>
  <p>A guardian can help complete the application.</p>
</section>''',
'''The section has a theme and a visible heading used as its name. The h3 is a subsection under the h2, not a visual size instruction.''',
"Replacing every div with section as a general cleanup step.",
"A block exists solely to add a background colour around two unrelated widgets. Should it automatically be a section?",
"No. A div may be the more accurate wrapper. Use section when the content forms a thematic grouping, usually introduced by a heading.",
[('section','sections.html#the-section-element')],
'Identify a thematic grouping|Name useful regions without excessive landmarks')

M(24,'Articles and supporting content','Decide what can stand on its own.',
'''article represents a complete or self-contained composition that could be distributed or reused independently in principle. A news story, a forum post or a self-contained review can qualify. An article can contain its own header, footer and sections.

aside holds content tangentially related to its surrounding content. The element does not mean right column. Related background could appear beneath the article on a phone and still be an aside. address provides contact information for its nearest relevant article or body ancestor; it is not a generic postal-address styling element.

## Reuse header and footer carefully
header is introductory or navigational material for its relevant context. footer can contain authorship, related links or other footer information. A footer does not need to sit at the bottom of a viewport.

Keep a page's repeated site header separate from an article's own introduction. If you include dates, author details or related reading, make their relationship clear from the surrounding structure and text. Do not select article merely because a card has a title; ask whether the content is a composition in its own right.''',
'''<article>
  <header>
    <h2>A reading room after school</h2>
    <p>Library programme notes</p>
  </header>
  <p>The room is available for supervised study.</p>
  <footer><p>Contact the library desk for current sessions.</p></footer>
</article>''',
'''The article includes its own introduction and footer. Their meaning belongs to this composition; a page may also have a separate site-wide header and footer.''',
"Using aside because a design puts something on the right, even when it contains essential main content.",
"Is the only set of instructions for submitting an application appropriate in an aside?",
"Usually not. Those instructions are part of the main task, not tangential content. Put essential instructions with the form or the relevant main section.",
[('articles','sections.html#the-article-element'),('aside','sections.html#the-aside-element'),('address','sections.html#the-address-element')],
'Distinguish standalone and tangential content|Use contextual headers and footers')

M(25,'Navigation and main content','Give recurring page regions clear jobs.',
'''main represents the dominant content of the document body. A normal visible page should not expose several competing main regions. Repeated site navigation and the general site footer ordinarily sit outside main.

nav identifies a major navigation section. Use it for the principal site menu or a substantial table of contents, not every isolated link. If several navigation regions need distinguishing, give them concise names such as Primary and On this page.

## Make repeated content easy to pass
A skip link near the beginning can take keyboard users to main content. Its target needs a unique id and should be tested in the browsers you support. Keep the link visible on focus rather than hiding it permanently.

The search element groups controls or content used for searching or filtering. It does not implement a search service by itself. A form inside it can submit a query to a real endpoint. Keep the form's label and response behavior usable without relying on a decorative magnifying-glass icon.''',
'''<a href="#main-content">Skip to main content</a>
<nav aria-label="Primary">
  <a href="index.html">Home</a>
  <a href="catalogue.html">Catalogue</a>
</nav>
<main id="main-content" tabindex="-1">
  <h1>Library services</h1>
  <p>Choose a service from the catalogue.</p>
</main>''',
'''The skip destination is programmatically focusable without adding it to ordinary sequential keyboard navigation. Test actual focus and scrolling rather than assuming the fragment provides the full intended experience everywhere.''',
"Giving several visible main elements different class names and treating them as layout columns.",
"How would you distinguish a site menu from a chapter table of contents for landmark navigation?",
"Use separate nav regions and name them, for example Primary and On this page. Keep names concise and avoid repeating the word navigation when the role already communicates it.",
[('main','grouping-content.html#the-main-element'),('navigation','sections.html#the-nav-element'),('search','grouping-content.html#the-search-element')],
'Create a clear main region|Distinguish navigation regions and test a skip link')

M(26,'Tables that explain the data','Use a table when the relationships run in rows and columns.',
'''A data table relates cells along two axes. Use table, tr and the appropriate th or td cells. A caption identifies the table. thead, tbody and tfoot can group rows, but grouping alone does not create header associations for every complex layout.

For a simple table, use scope="col" on column headers and scope="row" on row headers where appropriate. More complex tables can need explicit id and headers relationships. Simplifying the data layout is often easier for readers than making a deeply spanned table navigable.

## Preserve the relationships on small screens
A wide table can live in a labelled, keyboard-reachable scrolling region. Do not replace it with a screenshot. If you change its visual layout, test that header relationships and reading order still make sense.

rowspan and colspan change the cell grid. Incorrect spans can make a table model hard to reason about even when the display appears close enough. Do not use obsolete presentational attributes to recreate an old layout system. Use CSS for table styling and keep HTML focused on the data.''',
'''<table>
  <caption>Lending periods</caption>
  <thead><tr><th scope="col">Collection</th><th scope="col">Days</th></tr></thead>
  <tbody>
    <tr><th scope="row">General lending</th><td>14</td></tr>
    <tr><th scope="row">Reference desk copies</th><td>0</td></tr>
  </tbody>
</table>''',
'''Each value has a collection row header and a Days column header. The numbers are fictional teaching data, not actual library policy.''',
"Using a table for an entire page layout, or using bold td cells where actual th headers are required.",
"Which two headers should describe the value 14 in this table?",
"General lending and Days. The row header supplies the category and the column header supplies the quantity. The caption identifies the table as lending-period data.",
[('tables','tables.html#tables')],
'Build a simple data table with headers|Recognize when a complex table needs stronger associations')

M(27,'Plan a small site','Page structure should survive the trip between documents.',
'''Before writing a multi-page site, list the pages and the task each page supports. Give every document a distinct title and a useful main heading. Repeated navigation should remain consistent without making every page's content identical.

Use relative links deliberately. A path from pages/contact.html to the home page differs from the same path in index.html. A root-relative path beginning with a slash can break when the site is hosted under a repository subpath on GitHub Pages.

## Work from a content map
For the library, start with Home, Catalogue, Membership and Contact. Keep policy wording in one maintained location and link to it. If pages repeat the same structure, use a build template rather than manually copying it indefinitely.

A navigation link with aria-current="page" identifies the current page. Keep that state correct on each document. Do not rely only on colour to mark it visually. Test every relative path from the built output and from the eventual deployment base path.''',
'''<nav aria-label="Primary">
  <a href="index.html">Home</a>
  <a href="catalogue.html" aria-current="page">Catalogue</a>
  <a href="membership.html">Membership</a>
  <a href="contact.html">Contact</a>
</nav>''',
'''The current-page state belongs to the catalogue link on this page. A shared template needs page-specific information to put that state on the right link.''',
"Assuming a site that works at localhost / will work unchanged at /repository-name/ when links begin with a slash.",
"From pages/contact.html, what relative path reaches index.html one directory above?",
"Use ../index.html. The double-dot segment moves to the parent directory. Check the built link rather than guessing from the source template path.",
[('URLs','urls-and-fetching.html#urls'),('hyperlinks','links.html#hyperlink')],
'Assign a purpose to each page|Test paths under a deployment subdirectory')

M(28,'Images with a purpose','The alternative depends on why the image is there.',
'''An img embeds an image. Its src identifies a resource; alt supplies a text alternative according to the image's purpose. Useful alternative text requires the actual image and its context. A filename or a generic image description is not enough evidence.

For a purely decorative image, alt="" can keep it out of the ordinary text alternative. Do not omit alt as a casual way to say decorative. A functional image in a link needs an alternative that communicates the link's purpose if no other accessible wording provides it.

## Reserve the space
Provide width and height when you know the intended image dimensions or ratio. CSS can still size the rendered image responsively. Reserving an aspect ratio helps avoid layout movement as the resource loads.

Use loading="lazy" for suitable off-screen images, not automatically for the likely largest above-the-fold image. decoding and fetchpriority are hints with defined behavior and implementation limits. Measure before claiming a performance improvement. A broken src and a valid alt are different tests: an alternative does not make a missing image resource successful.''',
'''<img src="reading-room.jpg"
     alt="Four study desks beside the reading room windows"
     width="1200" height="800"
     loading="lazy">''',
'''This teaching image needs a real file with matching content and dimensions before use. The wording describes its supposed informational purpose; it is not a universal alt string to reuse for any photograph.''',
"Writing alt=\"image\" or alt=\"photo\" while leaving out the information the image contributes.",
"An image repeats the adjacent text label inside the same link and adds no other information. What alt value may be appropriate?",
"An empty alt can avoid repeating the link label, provided the visible text already supplies the required name and the image is genuinely redundant. Review the complete link and context rather than applying this to all linked images.",
[('images','embedded-content.html#the-img-element')],
'Choose alternatives from purpose and context|Use dimensions and loading hints deliberately')

M(29,'Responsive image choices','Offer candidates without pretending the browser follows a simple width switch.',
'''srcset gives the browser image candidates. Width descriptors describe candidate resource widths; sizes describes the expected rendered slot width for selecting among width candidates. A misleading sizes value can cause an unnecessarily large or blurry choice.

picture is useful for art direction or format alternatives. Its source elements appear before the fallback img. The img remains required for the actual image and its alternative text. A source inside picture has rules different from a source inside audio or video.

## Match the markup to the layout
If the slot is full width on small screens and half the viewport on wider screens, describe that relationship accurately. Keep a src fallback and test actual selections in the network panel at different viewport sizes and device pixel ratios.

Do not write a fixed candidate table and promise a particular resource in every browser condition. Selection can account for implementation and device considerations. For art direction, inspect that each crop still communicates the intended content and that the single alternative text remains appropriate.''',
'''<img src="room-800.jpg"
     srcset="room-400.jpg 400w, room-800.jpg 800w, room-1200.jpg 1200w"
     sizes="(max-width: 40rem) 100vw, 50vw"
     alt="The library reading room"
     width="1200" height="800">''',
'''The candidates must exist and have the stated widths. sizes describes a layout assumption; change it when the actual CSS slot no longer follows that assumption.''',
"Using width descriptors with an inaccurate sizes value, or believing srcset is a guaranteed breakpoint-to-file mapping.",
"When is picture more appropriate than simply adding more width candidates to one img?",
"Use picture when the source itself should change, such as a different crop for a narrow layout or a supported format alternative. Use width candidates when the same image composition is available at different resource widths.",
[('responsive images','images.html#images'),('picture','embedded-content.html#the-picture-element')],
'Describe candidate widths and slot size|Separate resolution switching from art direction')

M(30,'Audio, video and tracks','Playable media needs controls and usable alternatives.',
'''audio and video embed media. Provide controls unless an appropriate alternative interface supplies the required operation. Autoplay is subject to browser policies and user choices; adding autoplay is not a guarantee that playback begins.

source provides alternate media resources with relevant type information. track supplies timed text such as captions, subtitles or descriptions using a supported format, commonly WebVTT. Captions and subtitles serve different purposes, so choose the kind accurately.

## Plan the alternative before publishing
A transcript, captions and an audio description each address different access needs. The correct combination depends on the media and the information it conveys. A decorative silent clip and an instructional interview do not have identical requirements.

Include a poster for suitable video content and choose preload with an understanding that it is a hint. Third-party players add privacy, performance and embedding-policy concerns. Test keyboard playback controls, caption selection, mobile behavior and fallback links with the actual resources. Placeholder filenames prove nothing about media decoding or caption accuracy.''',
'''<video controls width="640" height="360" preload="metadata"
       poster="library-tour-poster.jpg">
  <source src="library-tour.mp4" type="video/mp4">
  <track kind="captions" src="library-tour.en.vtt" srclang="en"
         label="English" default>
  <p><a href="library-tour.mp4">Download the library tour</a>.</p>
</video>
<p><a href="tour-transcript.html">Read the tour transcript</a></p>''',
'''The track refers to a real caption file that must be written and checked against the media. The transcript link is available outside the video fallback content, so it remains visible in supporting browsers.''',
"Treating auto-generated captions as reviewed simply because a track file loads.",
"Why put the transcript link outside the video element as well as providing fallback content?",
"Fallback children are not a reliable always-visible location in browsers that support video. An ordinary external paragraph gives every reader a discoverable transcript link.",
[('media','media.html#media-elements'),('tracks','media.html#the-track-element')],
'Provide controls and intentional loading hints|Distinguish timed text and transcript needs')

M(31,'Image maps','Coordinate-based hotspots need an equivalent way to navigate.',
'''An image map associates areas of an image with hyperlinks. img uses usemap to refer to a map. area supplies a shape, coordinates, destination and appropriate alternative text for each linked region.

These controls are tied to the image's coordinate system. A design that resizes or changes the image needs careful testing. For many interfaces, ordinary links beside a diagram are easier to maintain and understand.

## Explain the destinations
Give each linked area an alt that communicates its purpose. A geographic or building diagram should not require readers to identify a shape visually before they can follow a link. Provide visible text links when they make the choices clearer.

Check keyboard focus, activation and the relationship between the displayed image and the hotspot geometry. The existence of an area element does not prove that a visitor can find the right destination or that the coordinate mapping still matches a responsive design.''',
'''<img src="library-floor.png" alt="Library floor plan"
     usemap="#facilities" width="600" height="400">
<map name="facilities">
  <area shape="rect" coords="20,20,200,140" href="reading-room.html"
        alt="Reading room">
</map>
<p><a href="reading-room.html">Reading room details</a></p>''',
'''The usemap fragment matches the map name. The coordinates are illustrative and need to be measured against the actual 600 by 400 image.''',
"Copying hotspot coordinates to a different image and assuming the clickable regions still match.",
"What needs to change when a replacement floor-plan image moves the reading room to another location?",
"Review the area geometry against the new image, update coordinates and alternatives as necessary, and retest navigation. Also inspect the visible link wording and any directions that referred to the old layout.",
[('image maps','image-maps.html#image-maps')],
'Connect a map and its areas|Review geometry and alternatives against the actual image')

M(32,'Embedding another document','An iframe introduces another browsing context and another trust decision.',
'''iframe embeds another document. Give it a useful title so readers can identify the embedded content. A title does not fix the embedded document's own accessibility problems.

sandbox restricts capabilities. The tokens you add restore particular capabilities, so start from the actual requirements and grant as little as the integration needs. Combining allow-scripts with allow-same-origin can weaken the intended isolation for same-origin content. Do not describe sandbox as a universal security wrapper.

## Consider the resource owner
Third-party embeds may load tracking, cookies, scripts and further resources. Review privacy, origin policy, referrer policy and the allow attribute's Permissions Policy integration. A provider's sample embed code is a starting point, not a completed review.

object and embed serve other embedding cases and bring their own fallback and implementation concerns. param is obsolete for authoring in the captured Standard and belongs in migration guidance. Do not add it to new object examples because an old tutorial used it.''',
'''<iframe src="preview.html" title="Preview of the library notice"
        sandbox="" loading="lazy" referrerpolicy="no-referrer"
        width="640" height="360"></iframe>''',
'''An empty sandbox imposes restrictions without opting capabilities back in. This example needs a local preview.html and does not support a third-party widget that requires scripts or forms.''',
"Adding every sandbox permission until an embed works, then assuming the original security boundary remains intact.",
"A widget needs only static text and images. Should you add allow-scripts and allow-same-origin by default?",
"No. Do not grant capabilities without a demonstrated need. Test the actual static resource under the intended restrictions and document any permissions you choose to add.",
[('iframe','iframe-embed-object.html#the-iframe-element')],
'Identify an embedding trust boundary|Choose sandbox permissions from actual requirements')

M(33,'Canvas, SVG and MathML','Graphics need a document-level alternative strategy.',
'''canvas provides a bitmap drawing surface controlled through APIs. Drawing pixels does not automatically produce semantic headings, text or controls in the accessibility tree. Fallback content and a usable alternative interface need deliberate design.

SVG and MathML are foreign vocabularies that can be integrated into an HTML document. Their own element vocabularies and rules come from their respective specifications. HTML parsing and integration rules still matter at the boundary.

## Use the right representation
For a simple diagram, an SVG with a title and a text explanation can be more maintainable than a canvas rendering. For a data chart, an accessible table may communicate the exact values better than an image alone. For meaningful mathematical notation, MathML can express structure that a screenshot loses.

This chapter introduces the HTML integration. A complete Canvas 2D or SVG API reference requires separate member-level documentation and tests. Do not infer that a graphic is accessible merely because it has a title element. Review its purpose, interactions and the information the alternative actually supplies.''',
'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 100"
     role="img" aria-labelledby="route-title route-desc">
  <title id="route-title">Route to the reading room</title>
  <desc id="route-desc">Reception connects directly to the reading room.</desc>
  <path d="M40 50 H280" stroke="currentColor" stroke-width="4"/>
  <circle cx="40" cy="50" r="10" fill="currentColor"/>
  <circle cx="280" cy="50" r="10" fill="currentColor"/>
</svg>''',
'''The graphic has a short title and a description of the relationship. The visible diagram is intentionally simple. A real route plan with turns or hazards would need a more complete alternative.''',
"Replacing an interactive chart with canvas pixels while removing all operable controls and data relationships.",
"Your canvas chart shows exact lending totals. What alternative lets readers inspect those values without interpreting pixels?",
"Provide a text or data-table representation with the actual values and labels. Keep it synchronized with the chart data. If the chart has controls, those also need an accessible operable interface.",
[('canvas','canvas.html#the-canvas-element'),('foreign elements','syntax.html#foreign-elements')],
'Distinguish bitmap drawing from document semantics|Describe HTML integration boundaries for foreign content')

M(34,'How forms send data','Start with the request, then choose the controls.',
'''A form collects successful control data and submits it according to its action, method and encoding rules. A visible input without a name usually does not contribute the expected name-value entry. An id connects labels and references; it is not the submission key.

GET commonly expresses retrieval by placing the encoded query in the URL. POST sends a request body under the selected encoding. Neither method provides encryption by itself. Use HTTPS for transport protection where appropriate and implement the server's validation, permissions and storage handling.

## Make the simple path work
A search form can submit without JavaScript. Build that path first when the service supports it. Scripts can enhance the experience without becoming the only way to reach the result.

Controls outside a form can be associated through a form attribute when their element supports it. Avoid relying on visual proximity as a submission relationship. Check actual submitted entries, including unchecked controls, disabled fields and the button used to submit. A browser preview without a backend cannot prove a successful application workflow.''',
'''<form action="catalogue.html" method="get">
  <label for="query">Search the catalogue</label>
  <input id="query" name="q" type="search">
  <button type="submit">Search</button>
</form>''',
'''The query key is q because that is the name. A real catalogue endpoint must read the query and return results; a static catalogue file does not implement that search service automatically.''',
"Assuming that giving a control an id is enough to send its value under that key.",
"Why might a filled input appear on screen but be absent from the submitted entry list?",
"It may lack a name, be disabled, be outside the relevant form without an association, or fall under another exclusion rule. Inspect the actual control state and form data rather than the visual layout.",
[('forms','forms.html#forms'),('submission','form-control-infrastructure.html#form-submission-2')],
'Distinguish name from id|Explain a form request without inventing a backend')

M(35,'Labels and groups','People should know what to enter before making a mistake.',
'''A label supplies the visible prompt for a form control. An explicit label uses for to reference the control's id. Nesting an appropriate control inside its label can also establish the association under the defined rules.

A placeholder is not a durable label. It can disappear as soon as someone types and often has poor contrast or confusing wording. Use supporting text for instructions, formatting rules and examples, then connect it with aria-describedby where that relationship helps.

## Group a shared question
fieldset and legend can express a group such as contact preference or membership type. Each radio still needs its own label. Keep the legend short enough that repeated announcements remain manageable.

Do not place essential instructions only in title or in a tooltip that requires a pointer. Write the instructions visibly. If a field is required, communicate that meaning consistently and explain the service's expectations. Required does not mean the requested information is necessary; review the form's data needs before adding fields.''',
'''<fieldset>
  <legend>How should we contact you?</legend>
  <label><input type="radio" name="contact" value="email"> Email</label>
  <label><input type="radio" name="contact" value="phone"> Phone</label>
</fieldset>''',
'''The shared name creates the radio group for submission and selection behavior. The legend supplies the common question. Each label names its own option.''',
"Using two separate names for radio options that should be mutually exclusive.",
"Why does a legend not remove the need to label each radio button?",
"The legend names the group question. Each radio still needs to identify its particular answer, such as Email or Phone. The reader needs both pieces of information.",
[('labels','forms.html#the-label-element'),('fieldset','form-elements.html#the-fieldset-element')],
'Associate visible labels with controls|Group related choices with a fieldset and legend')

M(36,'Text, email and passwords','Choose a state for the data, not just the keyboard.',
'''input type="text" is the general single-line text state. email and url have their own syntax and validation behavior. search can supply search-oriented interface behavior. password obscures the displayed value but does not encrypt it, protect it from scripts on the page or secure its eventual storage.

Use autocomplete tokens that describe the field's purpose. An existing-password field and a new-password field are different. Permit password managers and pasting rather than introducing unnecessary obstacles.

## Do not promise more validation than you have
An email input checks its defined syntax, not whether the address belongs to someone or can receive messages. A service that needs ownership verification must implement a separate confirmation process.

inputmode is a hint about input mechanisms, not a data validator. A numeric keyboard hint does not turn a text input into an integer or stop pasted characters. Pick constraints from the service's actual requirements, and keep server-side validation independent from the client interface.''',
'''<label for="join-email">Email address</label>
<input id="join-email" name="email" type="email" autocomplete="email"
       aria-describedby="email-help" required>
<p id="email-help">We use this address to contact you about your application.</p>''',
'''The helper describes this fictional form's intended use. Replace it with the actual service policy before collecting real addresses. The control cannot prove that a user controls the supplied mailbox.''',
"Calling a password secure because its characters appear as dots, or disabling paste to discourage password managers.",
"Will type=\"email\" prove that an address can receive your confirmation message?",
"No. It applies the email state's syntax rules. Message delivery and ownership are application concerns that need their own process and error handling.",
[('input states','input.html#states-of-the-type-attribute')],
'Choose a text-related input state|Distinguish syntax validation from verification')

M(37,'Numbers, dates and colour','A control can normalize a value without deciding what it means.',
'''number fits quantities where numeric operations make sense. Do not use it for every string made of digits. A membership identifier or postal code may need leading zeros, nonnumeric characters or a format that should not change.

min, max and step affect constraints for relevant input states. A range control suits selecting within a range when approximate adjustment is appropriate. Give the value a meaningful visible context; a bare slider can leave readers unsure what they are choosing.

## Dates need a data model
date supplies a date without a timezone. datetime-local supplies a local date and time, also without an offset or timezone identifier. An appointment service needs a clear policy for interpreting that value. The displayed picker can vary across browsers while the submitted value follows defined syntax.

Colour controls and the newer alpha/colorspace attributes need their own implementation review. Do not assume every browser presents the same picker or supports every standardized extension. Keep a usable alternative when exact colour input is important.''',
'''<label for="copies">Number of copies</label>
<input id="copies" name="copies" type="number" min="1" max="5" step="1">
<label for="visit-date">Preferred visit date</label>
<input id="visit-date" name="visitDate" type="date">''',
'''The quantity has integer steps within a range. The preferred date is not an instant on a global timeline and needs application interpretation before it becomes a scheduled event.''',
"Using number for a phone number and losing formatting or leading-zero expectations.",
"Why is a phone number often better represented by type=\"tel\" than type=\"number\"?",
"A phone number is an identifier with possible leading zeros, plus signs and formatting conventions. It is not a quantity to increment or average. tel can offer a useful input mechanism without pretending to validate every international number.",
[('numeric and temporal controls','input.html#states-of-the-type-attribute')],
'Distinguish quantities from numeric-looking identifiers|Interpret local dates without inventing timezones')

M(38,'Choices, files and hidden values','Submission depends on the control state.',
'''Checkboxes express independent choices. Radios with a shared name express a mutually exclusive selection. A checked checkbox or radio contributes its value under the defined entry-list rules; an unchecked one normally contributes no entry. Plan that absence on the server.

A file input lets a user choose files. accept is a hint to the chooser, not proof that a file is safe or of the declared type. File size, content, storage name and permissions need server-side checks. Do not serve uploaded files as executable content by accident.

## Hidden is not private
A hidden input participates in form submission without an ordinary visible control. Its value remains in the document and can be changed by a visitor. A server must not trust a hidden price, role or authorization decision merely because the page supplied it.

Likewise, readonly and disabled are different states for supporting controls. A readonly text control can still contribute its value; a disabled control is generally excluded from the entry list. Neither state is a substitute for enforcing business rules on the server.''',
'''<label>
  <input type="checkbox" name="updates" value="yes">
  Email me the reading-group schedule
</label>
<label for="attachment">Supporting document</label>
<input id="attachment" name="attachment" type="file" accept=".pdf">
<input type="hidden" name="formVersion" value="1">''',
'''The hidden value is a routing hint for the application, not a trusted permission. A surrounding file-upload form needs the appropriate multipart encoding and a real upload handler.''',
"Expecting an unchecked checkbox to submit the literal value false.",
"How should a server interpret the absence of an optional updates checkbox?",
"Apply the documented default for the field, commonly not opted in. Do not infer consent from a missing value. Validate any submitted value as well, since clients can send requests without using the page.",
[('checkboxes','input.html#checkbox-state-(type=checkbox)'),('file upload','input.html#file-upload-state-(type=file)'),('hidden state','input.html#hidden-state-(type=hidden)')],
'Predict submitted entries for checked controls|Treat files and hidden values as untrusted input')

M(39,'Menus and longer text','Choose the control that fits the number and kind of answers.',
'''select represents a choice among option elements, with optgroup available to group related choices. A native select carries behavior that a custom visual menu would otherwise need to recreate. Use a visible label and make any initial prompt consistent with required-selection rules.

textarea is for multiline text. Its initial value comes from its text content, not a value attribute. A datalist can supply suggestions for an associated input, but suggestions do not normally restrict the user to the listed values.

## Customizable selects need extra review
The Living Standard includes selectedcontent and newer customizable-select behavior. Their permitted structure and browser support need separate attention. Keep a conventional select usable as the baseline rather than assuming a decorative demonstration proves full keyboard and assistive-technology support.

multiple changes both the interface and submission expectations for a select. Do not use a multiple list solely to imitate the visual height of a different widget. Explain how to choose and how the service interprets several selected values.''',
'''<label for="branch">Preferred branch</label>
<select id="branch" name="branch" required>
  <option value="">Choose a branch</option>
  <option value="central">Central</option>
  <option value="east">East</option>
</select>
<label for="request">What would you like to read?</label>
<textarea id="request" name="request" rows="4"></textarea>''',
'''This is a conventional select baseline. Its empty initial option works with the required single-select context shown here. Check the detailed placeholder-label rules before changing the structure.''',
"Assuming datalist creates a strict allowed-value list or that textarea uses value like an input.",
"A field must accept only Central or East. Does an input with datalist enforce that restriction?",
"No. A datalist provides suggestions. Use a suitable select for this choice and validate the submitted value on the server. A client can send any value regardless of the visible controls.",
[('select','form-elements.html#the-select-element'),('selectedcontent','form-elements.html#the-selectedcontent-element'),('textarea','form-elements.html#the-textarea-element')],
'Use select, datalist and textarea intentionally|Keep a native baseline for newer select customization')

M(40,'Validation people can recover from','An error message should help someone finish the task.',
'''Native constraints include required, appropriate type rules and state-specific min, max, step, pattern and length restrictions. Their applicability differs by input state. A constraint in the wrong state may do nothing.

Constraint validation helps guide ordinary interaction. It does not secure a request. A server must validate the submitted data, enforce permissions and return useful errors even when JavaScript or browser validation has been bypassed.

## Keep the correction near the field
When application validation finds an error, identify the field and explain how to fix it. Preserve the submitted non-sensitive values when appropriate. Connect useful error text with aria-describedby and update aria-invalid when the application knows the value is invalid. Do not mark a field invalid before there is a reason to do so.

setCustomValidity can add an application message to supporting controls; a nonempty message keeps the control invalid until cleared. A mismatch between custom validity and visible errors can trap someone in a form. Test correction, not just failure. Native error UI varies between browsers, so do not base instructions on one screenshot.''',
'''<label for="card-number">Membership number</label>
<input id="card-number" name="cardNumber" inputmode="numeric"
       pattern="[0-9]{6}" aria-describedby="card-format" required>
<p id="card-format">Enter the six digits printed on your card.</p>''',
'''The pattern applies to this text-state input. inputmode is a keyboard hint. The six-digit rule is fictional teaching policy and needs a matching server-side rule in a real service.''',
"Adding a pattern without visible formatting guidance, or showing a generic Something went wrong message for a correctable field error.",
"After setting a custom validity message, a script sees the corrected value. What must it do to let the field become valid?",
"Clear the custom message with setCustomValidity(\"\") when the custom condition passes. Other native constraints may still apply, so inspect validity rather than assuming clearing one message proves every rule passed.",
[('constraint validation','form-control-infrastructure.html#the-constraint-validation-api')],
'Apply state-specific constraints|Design and test the correction path')

M(41,'Submission and server boundaries','A finished form includes what happens after the request.',
'''Form submission produces an entry list and a request under defined rules. application/x-www-form-urlencoded is the common default encoding. File uploads through a conventional POST form need multipart/form-data. Do not choose text/plain as a general production data format merely because it looks readable.

A submit button can override supported submission attributes for that submission. The button used can also contribute its own name and value. Test these details when one form supports several actions.

## Protect and explain the result
Use server-side validation, appropriate authorization and protections suited to the application, including CSRF defenses where the authentication and request model need them. HTTPS protects transport; it does not decide whether the requester may change a record.

A successful HTTP response is not necessarily a successful business operation. Show whether the application accepted, rejected or queued the action, and explain the next step. Handle retries and duplicate submissions according to the service's data model. Static GitHub Pages hosts HTML assets but does not provide a form-processing backend by itself.''',
'''<form action="/applications" method="post" enctype="multipart/form-data">
  <label for="proof">Address document</label>
  <input id="proof" name="proof" type="file" required>
  <button type="submit" name="action" value="apply">Send application</button>
</form>''',
'''The endpoint is illustrative and is not implemented by this static book. A real service needs a handler, storage rules, privacy information and testable success and failure states.''',
"Claiming a contact or application form works because the browser renders the fields and button.",
"What else is required before this form can be advertised as accepting real applications?",
"A working endpoint, validated and authorized handling, appropriate upload limits and storage controls, a clear privacy policy, and tested user-visible results for success, error and retry cases. Confirm deployment and transport behavior too.",
[('form submission','form-control-infrastructure.html#form-submission-2')],
'Choose an encoding for the actual data|Separate a static form interface from its service')
