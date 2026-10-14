M(42,'Buttons and commands','A button should say what will happen.',
'''Use button for an action. Give it a clear name and choose type deliberately. A button associated with a form can submit by default in relevant states, so write type="button" for a local interface action and type="submit" for an intended submission.

A toggle button needs a represented state when the interaction is a persistent toggle. aria-pressed is appropriate for that pattern, not for every button that can be clicked. Keep the state synchronized with the result.

## Prefer a native action when it fits
The Standard includes command and commandfor for invoker commands, including relationships to dialogs and popovers under their defined rules. This can reduce script, but each command and target needs current compatibility review. Custom command names and their handling do not become application behavior automatically.

Avoid nesting another interactive control inside a button. An icon can accompany text, but a tooltip should not be the only way to discover an otherwise unnamed action. Disabled buttons are also a communication decision: if someone needs to know why they cannot continue, provide that explanation outside the unavailable control.''',
'''<form action="catalogue.html" method="get">
  <label for="button-query">Book title</label>
  <input id="button-query" name="q" type="search">
  <button type="submit">Find books</button>
  <button type="reset">Clear the search</button>
</form>''',
'''The two types deliberately perform different native form operations. A reset button is shown to explain the behavior; decide whether clearing work is helpful enough to include in a real form.''',
"Leaving a local interaction button without a type inside a form, then being surprised by submission.",
"Does a button that opens a dialog always need aria-pressed?",
"No. aria-pressed represents a toggle-button state. A dialog opener is not automatically a toggle button. Give it an appropriate name and implement the dialog interaction and focus behavior correctly.",
[('button','form-elements.html#the-button-element')],
'Choose a button type deliberately|Distinguish actions from persistent toggles')

M(43,'Disclosure with details','Use a native disclosure before rebuilding one.',
'''details represents a disclosure. Its first summary supplies the label. The open attribute controls whether the contents are shown. This is a boolean attribute, so open="false" is still open.

A disclosure suits supplementary information that can reasonably remain collapsed. Do not hide the only instruction someone needs to complete a required field or understand a price behind an obscure label.

## Keep the summary useful
Write the summary as a question or a short description of the hidden information. Clicking it and keyboard activation should work without your own click handler. Avoid putting competing interactive controls in a summary without a specific reviewed reason.

The name attribute can associate details elements in an exclusive group under its defined behavior. Compatibility still matters. A group of disclosures is not automatically a tab interface or a full application accordion with every optional keyboard interaction from another pattern.

Test the disclosure with a keyboard and inspect whether its content is understandable when expanded. If you add animation, respect reduced-motion preferences and avoid delaying access to the actual information.''',
'''<details>
  <summary>Can I renew a borrowed book?</summary>
  <p>Ask the desk before the due date. Some collections have separate rules.</p>
</details>''',
'''The summary remains the control. The paragraph is ordinary document content when the disclosure is open. The library rule is an illustrative example, not a real lending policy.''',
"Adding role=\"button\" and a second keyboard listener to a summary, creating duplicate or conflicting behavior.",
"How do you make this disclosure initially expanded, and how do you make it initially collapsed?",
"Add open to details for an initially expanded disclosure. Omit open for the collapsed state. The string false is not a way to turn off the boolean attribute.",
[('details and summary','interactive-elements.html#the-details-element')],
'Use a native disclosure|Control a boolean open state correctly')

M(44,'Dialogs and popovers','Choose the interaction before choosing the container.',
'''A dialog can be shown modally with showModal or non-modally with show. A modal dialog changes interaction with the rest of the page. Opening it requires an intentional focus destination, a usable close path and sensible focus restoration when it closes.

Writing open in source displays a dialog in its non-modal open state; it does not reproduce every part of showModal. Use the dialog API or an appropriately supported invoker relationship for the intended behavior.

## A popover is not automatically a dialog
popover controls display and dismissal behavior for a popover element. It does not assign the semantics of a menu, dialog or tooltip. Choose markup and accessibility behavior for the actual content. The auto, manual and newer hint behaviors need their own defined handling and compatibility review.

closedby and declarative commands are newer parts of this area. Keep a compatible close mechanism and test Escape, focus, pointer dismissal and small-screen scrolling. Avoid using a modal merely to deliver a short message that could be shown in the page.''',
'''<button type="button" id="open-help">Membership help</button>
<dialog id="help-dialog" aria-labelledby="help-title">
  <h2 id="help-title">Membership help</h2>
  <p>Ask at the desk if you cannot supply an address document.</p>
  <form method="dialog"><button>Close help</button></form>
</dialog>
<script>
  const help = document.getElementById("help-dialog");
  document.getElementById("open-help").addEventListener("click", () => {
    help.showModal();
  });
</script>''',
'''The close button submits the method="dialog" form, closing the dialog rather than posting to a server. Test the actual focus behavior and decide whether a more specific initial focus target is needed for longer content.''',
"Assuming that adding the popover attribute supplies menu keyboard navigation or a dialog role.",
"Why is toggling the dialog open attribute not equivalent to calling showModal?",
"showModal establishes modal behavior, including its relationship with the top layer and the rest of the page. The open attribute alone shows an open dialog without that same modal operation.",
[('dialog','interactive-elements.html#the-dialog-element'),('popovers','popover.html#the-popover-attribute')],
'Distinguish modal dialog and popover behavior|Provide a keyboard-usable close path')

M(45,'Focus, editing and dragging','An interaction needs a path that does not depend on a pointer.',
'''Focusable and sequentially focusable are related but distinct. tabindex="0" can place an otherwise suitable element in sequential focus order. tabindex="-1" commonly allows programmatic focus without adding an ordinary tab stop. Positive tabindex values create a separate ordering problem and are usually best avoided.

contenteditable enables editing under its defined states. It does not provide a complete rich-text editor, accessible toolbar, sanitation pipeline or save system. Editing behavior and supported input methods need real-device testing.

## Offer alternatives to dragging
draggable participates in the drag-and-drop model. A drag gesture should not be the only way to perform an important operation. Provide buttons or another keyboard-usable mechanism for moving an item, and keep the outcome understandable.

Use focus to support a task, not to surprise someone whenever content changes. When removing a focused item, decide where focus goes next. Avoid trapping focus in a non-modal widget. Mobile input, speech control and assistive technology can expose assumptions that mouse-only testing misses.''',
'''<section aria-labelledby="list-title">
  <h2 id="list-title" tabindex="-1">Your reading list</h2>
  <ol><li>Local histories <button type="button">Move up</button></li></ol>
</section>''',
'''The heading can be a deliberate programmatic focus destination. The button demonstrates an alternative to a drag action, but its actual reordering logic is not implemented in this fragment.''',
"Adding tabindex=\"0\" to every paragraph and wrapper, making keyboard navigation unnecessarily long.",
"An item can only be moved by dragging. What should you add before treating the interaction as broadly usable?",
"Provide an operable non-drag mechanism, such as Move up and Move down controls, then implement focus management and meaningful feedback for the result. Test with a keyboard and the actual input methods you support.",
[('focus','interaction.html#focus'),('drag and drop','dnd.html#dnd')],
'Explain sequential and programmatic focus|Provide a non-drag path for important actions')

M(46,'Templates and component boundaries','A template stores a fragment without rendering it as ordinary page content.',
'''template holds inert template contents that a script can clone and insert. Its content is a DocumentFragment. Querying the template element's ordinary descendants is not the same as querying its content fragment.

slot is a placeholder within a shadow tree for assigned content. The slot attribute on an element identifies the named slot it should be assigned to under the relevant rules. This attribute is different from a slot element.

## Separate the pieces of a component
Autonomous custom elements use valid custom-element names, including the required hyphen and other naming restrictions, and are defined through the custom-elements machinery. A custom tag name alone does not register a working component. Customized built-in elements have separate is behavior and implementation considerations.

Declarative shadow DOM uses supported template shadowroot attributes to establish a shadow root during parsing under defined conditions. The evolving set includes mode, focus, cloning, serialization and registry-related controls. Review each independently. A shadow boundary is not a security sandbox or an excuse to ignore accessible names and keyboard behavior.''',
'''<template id="book-template">
  <article class="book">
    <h2></h2>
    <p></p>
  </article>
</template>
<div id="book-results"></div>
<script>
  const template = document.getElementById("book-template");
  const card = template.content.cloneNode(true);
  card.querySelector("h2").textContent = "Local histories";
  card.querySelector("p").textContent = "A collection of neighbourhood stories.";
  document.getElementById("book-results").append(card);
</script>''',
'''The example clones template content and inserts plain text into it. This is a template example, not a registered custom element or a shadow tree.''',
"Treating a shadow root as protection against hostile same-page code, or treating a template string as safely sanitized HTML.",
"Why does the script use template.content rather than expecting the article to be a normal child rendered in the page?",
"Template contents are held in a separate fragment and are not rendered as ordinary template children. Clone that fragment, fill it safely and insert it where the page should display it.",
[('template','scripting.html#the-template-element'),('custom elements','custom-elements.html#custom-elements')],
'Clone inert template content|Distinguish templates, slots and custom-element registration')

M(47,'Custom data and structured data','Store page-specific values without inventing semantics.',
'''data-* attributes store page-specific data where no more appropriate attribute fits. Scripts can access them through dataset with the defined name conversion. Values are strings; a value such as "false" is not automatically a false boolean.

Custom data is visible in the document. Do not place credentials or trusted authorization decisions there. A visitor can inspect and change it. Do not use a data attribute as a substitute for a real href, label or disabled state when the platform already defines one.

## Microdata serves a different purpose
itemscope, itemtype, itemprop, itemid and itemref participate in microdata. A vocabulary supplies meaning to properties; arbitrary names do not create a recognized public schema. Search and other consumers have their own supported formats and policies.

Keep visible content and structured annotations consistent. Do not claim that adding structured data guarantees a search result treatment. Choose a supported vocabulary and validate both its syntax and the content it represents using the relevant consumer's current documentation.''',
'''<button type="button" data-book-id="LIB-204" id="save-book">
  Save Local histories
</button>
<script>
  const saveButton = document.getElementById("save-book");
  const bookId = saveButton.dataset.bookId;
  // Use bookId as an identifier, never as an authorization decision.
</script>''',
'''The conversion is from data-book-id to dataset.bookId. Reading an identifier does not save anything; a real action still needs its implementation and feedback.''',
"Adding data-disabled=\"true\" and expecting native disabled behavior.",
"What JavaScript type do you get from element.dataset.count when the source has data-count=\"3\"?",
"You get the string \"3\". Convert and validate it deliberately if your application needs a number. Do not trust the value merely because it appeared in your own initial markup.",
[('custom data','dom.html#embedding-custom-non-visible-data-with-the-data-*-attributes'),('microdata','microdata.html#microdata')],
'Read custom data with explicit type handling|Distinguish page-specific data from public structured annotations')

M(48,'Global attributes in context','Global availability does not make every use a good idea.',
'''The global attributes section lists attributes common to HTML elements. DOM also owns requirements for id, class and slot. Other attributes and families integrate specifications such as ARIA and CSS Shadow Parts. Keep ownership and namespace boundaries clear.

An id must satisfy its defined authoring constraints and be unique among ids in the element's tree. class is a set of tokens. title supplies advisory information, but it is not a dependable sole label or instruction because exposure varies with device and interaction.

## Hidden and inert differ
hidden participates in rendering and relevance rules, including its until-found state in supporting implementations. inert prevents interaction and affects focus and accessibility exposure under its rules. Neither is simply a synonym for a CSS property.

Use lang and dir for their own meanings. accesskey can conflict with browser, operating-system or assistive-technology commands, so do not invent a keyboard shortcut scheme casually. Newer autocorrect, writingsuggestions and heading-level attributes need compatibility review. The reference keeps them visible rather than silently dropping them because they are unfamiliar.''',
'''<section id="renewal" class="notice compact" lang="en">
  <h2>Renew your membership</h2>
  <p>Use the same name as your current library card.</p>
</section>''',
'''id is a stable reference target. The two classes are separate tokens, not two independent class attributes. The section's language is explicit here even though it may already inherit English from html.''',
"Relying on title as the only label for an icon-only control or the only explanation of a field error.",
"Can two unrelated controls safely share an id just because they are on different visual panels?",
"Not within the same element tree. Visual separation does not establish a new id scope. Use unique ids and update all for, fragment and ARIA references consistently.",
[('global attributes','dom.html#global-attributes')],
'Apply global attributes with their own constraints|Keep id relationships unique and meaningful')

M(49,'Element-specific attributes','The same spelling can have different rules.',
'''An attribute name is not a complete definition. type means different things on input, button, script and other elements. value differs between a text input, an option and a progress element. Read the element and state alongside the name.

The reference retains contextual rows rather than merging everything into one alphabetical name list. An input's type can determine whether min, maxlength or another constraint applies. A parser accepting an attribute does not make the use conforming or effective.

## Check the default as well as the explicit value
Missing-value defaults and invalid-value defaults can differ. Enumerated attributes have defined keywords and states. Boolean attributes depend on presence. Token lists have their own constraints. When a script reflects an attribute through a property, the property can normalize or interpret it rather than exposing the raw source string.

For a new attribute, verify its canonical definition, supported elements, permitted values, side effects and implementation data. Preserve compatibility notes and fallback behavior. Do not infer support merely because getAttribute returns the text you set; the DOM can store unknown attributes too.''',
'''<label for="age-years">Age in years</label>
<input id="age-years" name="age" type="number" min="0" max="120">
<label for="reader-name">Reader name</label>
<input id="reader-name" name="readerName" type="text" maxlength="100">''',
'''The numeric bounds suit the number state. The text length constraint suits the text state. These are illustrative service limits, not universal requirements for personal data.''',
"Adding maxlength to a number input and assuming it enforces the number of digits.",
"Why does reading an unfamiliar attribute with getAttribute fail to prove native support?",
"getAttribute reads stored attribute text. It does not demonstrate that the browser implements the attribute's specified behavior. Test the behavior and consult dated implementation evidence.",
[('attribute index','indices.html#attributes-3'),('input applicability','input.html#input-type-attr-summary')],
'Interpret attributes in element and state context|Distinguish stored markup from implemented behavior')

M(50,'Metadata readers encounter','A good title helps someone find the right tab again.',
'''title identifies the document in browser UI and other contexts. Make it specific enough to distinguish this page from the rest of the site. A visible h1 and the document title have related but separate jobs.

meta can declare encoding or named metadata. A description is useful page-summary metadata, but its presence does not guarantee that a search engine will display it. Do not promise rankings from a tag.

## Keep head deliberate
Use link for supported resource relationships such as stylesheets and icons. A favicon is not the same as a visible logo. style holds embedded CSS when permitted. base changes URL resolution and target defaults, so use it only when you understand the effects on every relative reference.

Metadata names and link types have defined or registered meanings. Do not invent a plausible name and assume a consumer understands it. Social sharing formats also need their own current documentation. Keep canonical URLs accurate, and avoid adding several conflicting declarations through independently configured tools.''',
'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="description" content="Find opening hours and contact details for the library.">
  <title>Visit and contact | Neighbourhood Library</title>
</head>
<body><h1>Visit and contact</h1></body>
</html>''',
'''The description summarizes this particular page. It makes no claim about search ranking or the exact snippet a service will show.''',
"Giving every page the same title, or treating a meta description as a guaranteed search-result advertisement.",
"Which title better identifies the contact page: Welcome or Visit and contact | Neighbourhood Library?",
"The second identifies both the page purpose and the site. It remains useful in a tab list, bookmark collection or history entry where surrounding page content is absent.",
[('metadata','semantics.html#document-metadata')],
'Write a specific document title|Describe metadata without search-result guarantees')

M(51,'Resource relationships','rel tells consumers how a link relates to its context.',
'''A link relation gives a relationship meaning rather than merely a destination. link rel="stylesheet" requests a stylesheet relationship. An anchor's rel can annotate a hyperlink. Their allowed contexts and effects depend on the particular link type.

preload, preconnect and related hints should correspond to a real loading need. A preload has request details such as as and, when relevant, type or crossorigin. A mismatch with the eventual request can waste work rather than helping.

## Avoid hints by habit
Measure the loading problem before adding hints. A preconnect to a third party can create network and privacy costs even when the visitor never uses that service. A resource hint is not proof of a faster page.

Canonical, alternate, author and other relations have defined uses and consumer expectations. Keep the reference's link-type inventory separate from a list of attribute names. The rel attribute's existence does not enumerate all its possible relationship tokens or guarantee a particular consumer's action.''',
'''<link rel="stylesheet" href="styles.css">
<link rel="icon" href="favicon.svg" type="image/svg+xml">''',
'''These are head-context resource relationships. The resource files must exist at the resolved URLs. The example is displayed as source; the book's sandbox blocks external resource loading.''',
"Preloading every image, font and script on a page without checking which resources are actually needed early.",
"Why might a preload download fail to benefit the later resource request?",
"Its request parameters can differ from the later request, the resource may be unused, or the early work may contend with something more important. Inspect actual network behavior and request matching.",
[('link types','links.html#linkTypes'),('link element','semantics.html#the-link-element')],
'Read rel as a defined relationship|Evaluate hints using actual requests')

M(52,'Loading and policy attributes','A hint and a security policy do not do the same job.',
'''loading and fetchpriority influence eligible loading decisions. They are not strict scheduling commands. crossorigin participates in the resource's fetching and CORS behavior; it does not grant your server permission to expose private data.

integrity integrates Subresource Integrity for supported resource uses. The hash must match the actual bytes, and cross-origin requirements matter. A placeholder digest is not a security control. nonce participates in a Content Security Policy arrangement and should be generated and delivered according to that policy's requirements.

## Follow the actual authority
HTML defines where these attributes integrate, while Fetch, CORS, CSP, Referrer Policy and SRI own important parts of their behavior. Read the relevant specification and deployment documentation for a security assertion.

referrerpolicy controls referrer information according to the defined policy, not all information a remote service can learn. Avoid presenting one attribute as a complete privacy solution. Test response headers and real requests as well as the source markup.''',
'''<a href="https://example.org/reading-list" referrerpolicy="no-referrer">
  Read the example partner's list
</a>''',
'''The example demonstrates a referrer policy on a hyperlink. It does not remove the network request, hide the destination from the visitor's network, or imply a relationship with an actual partner.''',
"Copying a static nonce into every deployment and describing it as a complete CSP configuration.",
"Can adding crossorigin make a remote server return private data to your script when that server does not allow the origin?",
"No. The server's CORS policy and the request mode and credentials behavior still apply. The attribute is part of a fetching configuration, not a bypass for a server's access policy.",
[('CORS settings','urls-and-fetching.html#cors-settings-attributes'),('nonce','urls-and-fetching.html#attr-nonce')],
'Distinguish loading hints from policy enforcement|Trace integration claims to the owning specification')

M(53,'Attributes and properties','Source text, defaults and current state can diverge.',
'''getAttribute reads an attribute's text or returns null when absent. A corresponding DOM property can expose a parsed, normalized or stateful value. Do not assume they always remain equal.

For a text input, the value attribute is associated with its default value, while the value property describes the current value under the control's rules. User edits can change the current value without rewriting the source attribute. checked and defaultChecked have a related distinction for appropriate controls.

## Read the right layer
Boolean reflection commonly maps property true to attribute presence and false to absence. URL properties can return resolved absolute URLs while the attribute contains a relative string. Numeric reflection has its own rules, defaults and limits.

When debugging, ask whether the question concerns the original source, the current attribute, or the current control state. Reset behavior, script assignment and user interaction can affect different layers. Avoid a generic helper that treats every attribute and property as interchangeable strings.''',
'''<label for="nickname">Reading-group name</label>
<input id="nickname" name="nickname" value="Guest">
<script>
  const field = document.getElementById("nickname");
  field.value = "Ada";
  console.log(field.value);                 // Ada
  console.log(field.getAttribute("value")); // Guest
</script>''',
'''The script changes the current input value. The attribute retains Guest in this example. This is a specific input-state behavior, not a universal rule for every property named value.''',
"Using getAttribute(\"value\") to read a text field after the user has edited it.",
"Which should an ordinary script read for the current text input value after editing?",
"Read the input's value property. If you need the default value or the raw attribute, ask for that specifically instead of assuming it equals the current state.",
[('reflection','common-dom-interfaces.html#reflecting-content-attributes-in-idl-attributes'),('input value','input.html#dom-input-value')],
'Distinguish raw attributes and current state|Read the correct layer when debugging controls')

M(54,'How parsing starts','The parser has states, not a general find-and-replace rule.',
'''HTML parsing includes tokenization and tree construction. The tokenizer recognizes text, tags, attributes, comments and other tokens while its state affects how characters are interpreted. A less-than sign inside an ordinary text context does not have the same surrounding rules as text in script or style.

Character references are consumed in the contexts defined by the parser. An apparent tag inside a JavaScript string can still interact with the HTML script-data rules, which is why serializing arbitrary data into inline script needs careful escaping and a reviewed approach.

## Do not sanitize with a tag regex
Untrusted HTML needs a context-appropriate safe handling strategy. Plain text should usually be inserted as text. If a product truly accepts markup, use a maintained sanitizer configured for the allowed content and review how it interacts with the destination.

Encoding for one context does not automatically encode for another. An HTML attribute, JavaScript string, URL and CSS value have different grammar. The examples here are educational text; they are not a complete sanitizer implementation.''',
'''<p id="message"></p>
<script>
  const submittedText = "<strong>Recommended</strong>";
  document.getElementById("message").textContent = submittedText;
</script>''',
'''The literal string appears as text because the script assigns textContent. It does not create a strong element. Use this route when the product accepts text rather than markup.''',
"Assuming that stripping text between angle brackets with a regular expression produces safe HTML.",
"If a comment field is intended to accept plain text, why use textContent rather than innerHTML?",
"textContent creates text without interpreting the submitted string as markup. innerHTML parses markup and can introduce dangerous behavior if the data is not handled with a correct sanitization strategy.",
[('tokenization','parsing.html#tokenization'),('dynamic insertion','dynamic-markup-insertion.html#dynamic-markup-insertion')],
'Describe tokenizer context|Choose text insertion for plain untrusted text')

M(55,'Tree construction and recovery','Inspect what the browser built, then fix the source.',
'''The tree builder processes tokens using insertion modes and special rules. Table parsing, implied end tags and misnested formatting are examples where a browser can build a tree that differs from an author's naive reading of the source.

Error recovery is specified so browsers can process existing pages consistently. It is not a list of recommended authoring shortcuts. A source file can appear usable while the parsed relationships break labels, selectors or accessibility semantics.

## Make a small failing case
Reduce unexpected markup to the shortest document that still produces the surprising tree. Compare View Source with the live DOM. Remove scripts and extensions that might be modifying the result before blaming parsing.

Keep invalid examples explicitly labelled. When a checker reports a problem, record the intended correction and verify the resulting tree. Add a regression test for the relationship that mattered, not just a screenshot of the page.''',
'''<div class="notice">
  <p>Applications are open.</p>
  <section>
    <h2>How to apply</h2>
    <p>Collect a form at the desk.</p>
  </section>
</div>''',
'''This corrected structure keeps the section outside the paragraph. A paragraph cannot be used as a generic container for the whole notice, even if recovery makes the output look plausible.''',
"Testing a CSS selector against the intended source hierarchy rather than the hierarchy the parser actually created.",
"How should you investigate a table row that appears in an unexpected place in Developer Tools?",
"Create a reduced complete document, inspect its actual DOM and check the source against table content rules. Parsing can relocate or imply nodes. Verify the correction with a checker and a DOM assertion.",
[('tree construction','parsing.html#tree-construction')],
'Observe a repaired tree without recommending invalid source|Reduce parsing bugs to a testable fixture')

M(56,'The document lifecycle','Wait for the condition your code actually needs.',
'''The document moves through loading states. DOMContentLoaded relates to parsing and eligible deferred/module script execution. The load event waits for the document's relevant dependent resources. Neither event proves that every later asynchronous operation has completed.

A script placed after a target element can often use that element immediately. A deferred external classic script runs after parsing under its ordering rules. Code that can run after DOMContentLoaded has already fired may need to inspect readyState before deciding whether to attach a listener.

## Separate readiness from data
A catalogue fetch completing is an application condition, not the same as the initial DOM being ready. Give the result area explicit loading, empty, error and success states where needed. Do not leave a spinner indefinitely because a request failed.

Document navigation, visibility changes, page restoration and the back-forward cache introduce further lifecycle cases. Avoid using unload as a dependable save system. Design persistence and recovery around the actual platform behavior and test reload and back navigation.''',
'''<p id="status-message">Preparing the catalogue view.</p>
<script>
  function initialize() {
    document.getElementById("status-message").textContent = "Catalogue view ready.";
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initialize, { once: true });
  } else {
    initialize();
  }
</script>''',
'''This pattern handles running before or after initial parsing has finished. It announces only that this local view initialization ran, not that remote catalogue data was fetched.''',
"Waiting for load for every DOM task, or assuming DOMContentLoaded waits for every image and application request.",
"What should your code wait for before rendering data from a specific fetch request?",
"Wait for that request and its response processing, then render or show its error state. Document readiness alone does not prove the data is available.",
[('document readiness','dom.html#current-document-readiness'),('stop parsing','parsing.html#the-end')],
'Choose a readiness condition|Separate document lifecycle from application data loading')

M(57,'Scripts and execution','Order, dependencies and origin rules affect the result.',
'''An ordinary external classic script without async or defer can block parsing while it is fetched and executed. defer allows eligible external classic scripts to run after parsing, preserving their deferred execution order. async allows independent loading and execution without that dependency ordering guarantee.

Module scripts have their own loading, dependency, scope and CORS behavior. They are deferred by default in the usual parser-inserted case. Do not assume that adding type="module" to an existing global script preserves every behavior.

## Give dependency rules a home
If one script relies on another, represent the dependency through an appropriate module graph or a deliberately ordered loading strategy. Import maps define supported module-specifier mappings under their own processing rules. Newer script types, including speculation rules, need their own review.

noscript provides content for defined scripting-disabled cases. It is not a catch-all for script download failures or runtime exceptions. A progressively enhanced page should keep useful content and a clear failure path even when one script fails.''',
'''<script src="catalogue.js" defer></script>
<noscript>
  <p>The complete book list is available on the <a href="catalogue.html">catalogue page</a>.</p>
</noscript>''',
'''The file catalogue.js must exist and implement its behavior. The noscript fallback concerns disabled scripting; a failed request for catalogue.js still needs a resilient baseline or another failure strategy.''',
"Using async on two dependent classic scripts and relying on their tag order for execution order.",
"Would noscript automatically display when a script downloads successfully but throws an exception?",
"No. Scripting remains enabled. Handle the failure in the application design and keep a useful underlying document instead of relying on noscript for runtime errors.",
[('script','scripting.html#the-script-element'),('noscript','scripting.html#the-noscript-element')],
'Choose a loading strategy for dependencies|Distinguish disabled scripting from script failure')

M(58,'HTML and XML serialization','The media type changes the parser and its rules.',
'''HTML syntax and XML syntax are not interchangeable decorations around the same file. A response's media type determines the relevant processing path. Renaming a file or adding an XHTML-looking namespace does not make a text/html response use XML parsing.

In HTML, element and attribute processing includes defined case handling and error recovery. XML has different well-formedness, namespace and case rules. An XML parse error is not handled like an ordinary recoverable HTML authoring error.

## Do not infer a mode from a slash
A trailing slash on br in HTML is not the XML mechanism applied to every element. A non-void HTML element still needs its end tag. Conversely, XML serialization has its own namespace and empty-element rules.

If you intentionally serve application/xhtml+xml, test the actual HTTP Content-Type and XML requirements. For normal HTML authoring in this book, use the short HTML doctype, UTF-8 and text/html. Preserve namespace-sensitive behavior when integrating SVG or MathML.''',
'''<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><title>HTML serialization</title></head>
<body><p>Neighbourhood Library<br>Reading room entrance</p></body>
</html>''',
'''This is intended as text/html. The br element is void and does not have an end tag. A local browser file test is not proof of the headers used by a deployed server.''',
"Adding xmlns to html and assuming it switches the HTML parser to XML mode.",
"Which matters more for choosing the HTML or XML parsing path: an XHTML-looking source style or the actual response media type?",
"The actual processing context and response media type matter. Confirm the server behavior and follow the rules for that syntax; visual resemblance to XHTML is insufficient.",
[('XML syntax','xhtml.html#the-xhtml-syntax'),('HTML syntax','syntax.html#syntax')],
'Distinguish HTML and XML processing|Test the media type rather than guessing from source style')

M(59,'HTML and rendering','Default styles are a starting point, not the meaning.',
'''Browsers have default rendering rules and styles. A heading often appears bold and large; an anchor often appears underlined. Those defaults make an unstyled document usable, but they do not define every semantic or accessibility behavior.

Changing display can alter layout without changing the element's underlying HTML definition. It can also interact with accessibility mappings and implementation quirks. Test the actual result rather than assuming a CSS property is semantically harmless everywhere.

## Keep reading order deliberate
Layout can visually reorder items while the DOM order stays the same. A keyboard or screen reader may encounter a sequence unlike the visual arrangement. Put the logical order in HTML and use layout to adapt it without creating competing stories.

Use HTML attributes with their intended behavior rather than recreating them through presentation alone. CSS hiding, hidden and inert have different consequences. Contrast, focus visibility, reflow and zoom are also part of the usable page, even though their implementation often lives in CSS.''',
'''<article>
  <h1>Visit the reading room</h1>
  <p>Check the current opening hours before travelling.</p>
  <a href="opening-hours.html">Read the opening hours</a>
</article>''',
'''The source remains a sensible reading sequence before layout. Styling should not move the link ahead of its context solely to match a decorative composition.''',
"Choosing an element because its browser default margin looks right, then compensating for the wrong semantics with ARIA.",
"Can CSS make an h2 look larger than an h1 without changing their heading levels?",
"Yes. Presentation and heading rank are different. Keep the semantic hierarchy appropriate and use CSS for the visual scale, then check that the overall design still communicates the structure.",
[('rendering','rendering.html#rendering')],
'Distinguish default appearance from meaning|Keep source and interaction order understandable')

M(60,'Where the wider APIs begin','Know the boundary before calling the reference exhaustive.',
'''The HTML Standard includes more than markup. It defines navigation and history behavior, messaging, workers, worklets, storage, event loops and many interfaces. A language guide can introduce their integration, but a named-interface list does not document every member or algorithm.

localStorage is synchronous, origin-scoped storage with its own access and failure behavior. It is not a suitable place for secrets simply because it is local. Workers run script in a different execution environment, not a second DOM you can manipulate directly. Messaging needs explicit origin and data validation where relevant.

## Treat integration as a design decision
A history update needs a corresponding content and navigation strategy. A cross-document message needs an expected sender and validated payload. A background task needs cancellation and failure handling. These responsibilities do not disappear because the API call is short.

The API catalogue in this review edition routes to 166 named interfaces from the captured index. It does not claim member-level completeness. That remaining work is recorded in the release checklist; a finished whole-Standard reference needs a larger inventory and review than this chapter provides.''',
'''<button type="button" id="save-preference">Remember compact view</button>
<p id="preference-result" role="status"></p>
<script>
  document.getElementById("save-preference").addEventListener("click", () => {
    const result = document.getElementById("preference-result");
    try {
      localStorage.setItem("library.view", "compact");
      result.textContent = "Preference saved in this browser.";
    } catch {
      result.textContent = "This browser could not save the preference.";
    }
  });
</script>''',
'''Storage can be unavailable or fail. The book's isolated example sandbox may not allow localStorage, so the failure path is intentional. No data is sent to a server.''',
"Calling a reference complete because every interface name appears somewhere in it.",
"Why does the example catch a storage failure rather than assuming localStorage is always writable?",
"Access restrictions, browser settings and storage failures can prevent writing. A preference control should remain usable and explain the actual result. Do not report a successful save when the write failed.",
[('web application APIs','webappapis.html#webappapis'),('web storage','webstorage.html#webstorage')],
'Identify wider API responsibilities|Keep API integration separate from member-level completeness')
