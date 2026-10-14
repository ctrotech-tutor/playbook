"""Editorial seed. The site/PDF build reads content/chapters.json, not this file."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
ARCH=json.loads((R.parent/'editorial/architecture.json').read_text())
TITLES=[t for p in ARCH['parts'] for t in p['chapters']]
PARTS=[p['name'].replace(' · ',' / ') for p in ARCH['parts'] for _ in p['chapters']]
BOOK=[]
def M(n,title,dek,lesson,code,explain,mistake,question,answer,source,goals):
    BOOK.append(dict(id=f'CH-{n:02}',number=n,title=title,architecture_title=TITLES[n-1],part=PARTS[n-1],dek=dek,lesson=lesson.strip(),code=code.strip(),explanation=explain.strip(),mistake=mistake,question=question,answer=answer,objectives=goals.split('|'),sources=[{'title':'HTML Living Standard: '+label,'url':'https://html.spec.whatwg.org/multipage/'+url} for label,url in source],prerequisites=[] if n==1 else [f'CH-{n-1:02}'],editorial_status='draft_for_review',technical_review='example_conformance_pending',exercise_review='editorial_answer_present_not_independently_reviewed'))

M(1,'What HTML does','Give the browser a document it can understand.',
'''A browser needs more than words and coordinates. It needs to know which words are a heading, which image needs an alternative, and which control submits a form. HTML supplies that structure. CSS controls presentation. JavaScript can change the document and respond to events.

Those responsibilities overlap in useful ways. A details element can open without your JavaScript. A required input can stop an ordinary form submission. You still need a server to decide whether a submitted value is acceptable. Native browser behavior gives you a starting point, not an application backend.

## Start with the content
Write the document before adding layout. In the example, the heading names a small lending library and the paragraph explains its purpose. The link already works with a keyboard and has a destination. If the stylesheet fails, the information remains available.

Your job is to describe what the page contains. Pick the element whose meaning fits the content, then style it. A very large paragraph does not become a heading because it looks like one.''',
'''<main>
  <h1>Neighbourhood Library</h1>
  <p>Borrow books and find a quiet place to read.</p>
  <a href="catalogue.html">Browse the catalogue</a>
</main>''',
'''The main element identifies the page's dominant content. The h1 names it. The anchor is a real hyperlink because it has an href. These choices remain useful without a framework, a stylesheet or a pointer device.''',
"Using a clickable div for navigation adds work. It needs keyboard behavior, focus handling and semantics that a hyperlink already supplies.",
"Which part of this example belongs to HTML, and which change would require CSS: renaming the heading, changing its colour, or changing the link destination?",
"The heading text and href are document content, so both are HTML changes. Colour is a presentation decision for CSS. JavaScript is unnecessary for any of these edits.",
[('the language and its scope','introduction.html#introduction')],
'Distinguish structure from presentation|Choose a hyperlink for navigation')

M(2,'Reading a Living Standard','Look up a rule without treating every browser as identical.',
'''The HTML Living Standard changes over time. A reference to HTML5 often describes the modern language informally; it does not identify a frozen collection of features you can assume every browser supports.

The Standard contains authoring requirements, browser processing rules, explanations and indexes. The index is useful for finding a feature. Its summaries are not substitutes for the feature's actual definition. Read the definition when nesting, defaults or exceptions affect your example.

## Separate three questions
Ask whether the markup conforms, whether your target browsers implement the behavior, and whether your use is accessible and appropriate. These questions need different evidence. A new element can be in the Standard while implementation remains uneven. An old presentational element can still render while being nonconforming for authors.

The example uses a normal document declaration. There is no version number to update when you use a newer conforming feature. Record the relevant source and review date in your project notes instead. Compatibility data is a dated aid, not a promise about a visitor's installed software.''',
'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Library notes</title>
</head>
<body>
  <h1>Library notes</h1>
</body>
</html>''',
'''The doctype is the short HTML doctype. It does not opt into a named annual release. The language, encoding and title solve separate document concerns.''',
"Using successful rendering as the only test of conformance. Browsers deliberately recover from many authoring errors.",
"An obsolete element displays in your browser. Is that enough evidence to recommend it in new markup?",
"No. Rendering support can exist for old content. Check the authoring requirements and use a conforming replacement that preserves the intended meaning. Then check the replacement in the browsers you support.",
[('conformance','introduction.html#conformance-requirements-for-authors'),('obsolete features','obsolete.html#obsolete')],
'Distinguish authoring rules from implementation support|Find a definition beyond the index')

M(3,'From source to page','The text file and the browser document are related, but different.',
'''The server sends bytes with a media type. For a text/html response, the browser decodes those bytes and runs the HTML parser. Parsing creates nodes in a document tree. Styles and layout then determine how that tree is presented.

Scripts can change the tree after parsing. Developer Tools usually shows the current tree, not a faithful printout of the file you saved. View Source and the Elements panel answer different questions.

## Follow one change
Our example gives a paragraph an id. A script can find the element and change its text. The original response still contains the old wording. A test that inspects the current DOM should expect the changed wording after that script has run.

The browser may also add implied elements and repair certain malformed structures during parsing. Do not take the repaired tree as permission to keep broken source. Find the authoring error, correct the source, and test again. Keep network failures separate from parsing failures: a valid document can still refer to an unavailable resource.''',
'''<p id="opening">Opening hours are being checked.</p>
<script>
  document.getElementById("opening").textContent =
    "Open Tuesday to Saturday.";
</script>''',
'''The script runs after the paragraph has been parsed because it appears after that paragraph. textContent sets text, so the replacement string is not parsed as markup.''',
"Assuming a selector can find a later element before the parser has created it. Script placement and loading behavior affect timing.",
"What will View Source show after the paragraph changes, and what will the current DOM show?",
"View Source shows the response containing the original sentence. The current DOM contains the updated text node. A later reload can produce the same change again because the script runs again.",
[('documents','dom.html#documents'),('parsing','parsing.html#parsing')],
'Describe the path from bytes to nodes|Distinguish response source from the live DOM')

M(4,'Elements, tags and attributes','Name the parts before debugging the page.',
'''An element is part of the document. Tags are syntax used to write many elements in HTML source. Most ordinary elements have a start tag, contents and an end tag. Some, such as img and input, are void elements and do not have end tags.

An attribute adds information to an element's start tag. In our link, href gives the destination and class provides a token for styling or scripting. Neither attribute changes the element into another kind of element.

## Read the whole element
The link's accessible wording comes from its text in this simple case. A class such as button does not supply button semantics. If the control navigates, keep the anchor. If it performs an action in the current interface, consider a button.

Text between tags becomes text nodes. A comment is a different node and is not displayed as normal page content. Comments are still delivered to the browser. Never store passwords, private tokens or confidential project notes in them.''',
'''<a class="catalogue-link" href="catalogue.html">
  Browse available books
</a>
<!-- The catalogue is a separate document. -->''',
'''The start tag carries two attributes. The end tag closes the anchor. Whitespace around the words can affect text nodes, but it does not create another element.''',
"Calling every piece of angle-bracket syntax an element. In particular, the doctype is a declaration, and an end tag is syntax rather than a second element.",
"Identify the element name, attribute names, attribute values and link text in the example.",
"The element name is a. The attributes are class and href, with values catalogue-link and catalogue.html. The words Browse available books are the link text. The comment is separate from the anchor.",
[('elements','syntax.html#elements-2'),('attributes','syntax.html#attributes-2')],
'Identify tags, attributes and contents|Keep confidential information out of source')

M(5,'Think in trees','Parent and child relationships explain many markup rules.',
'''The DOM is a tree of nodes. The document has an element child, html, which normally contains head and body. An element can contain text and other elements where its content model allows them.

Parent, child, sibling and descendant describe relationships, not screen positions. Two boxes that sit side by side can have very different places in the tree. A heading belongs to an article because of the document structure, not because it happens to appear above it visually.

## Inspect one branch
Here the article is a child of main. The heading and paragraph are siblings. The em element is a child of the paragraph and a descendant of the article. A selector or a DOM method operates on these relationships.

Keep the tree understandable before styling. Deep wrappers can be appropriate, but each extra layer should have a reason. Do not use the visual layout as evidence that nesting is valid: a browser can display invalidly nested source after repairing it.''',
'''<main>
  <article>
    <h1>A shelf for local writers</h1>
    <p>Bring a book by an <em>independent</em> author.</p>
  </article>
</main>''',
'''The emphasis belongs inside the sentence. Moving em around the whole article would change both the semantics and the validity question; phrasing elements cannot simply wrap arbitrary document sections.''',
"Assuming that any element may contain any other element as long as the end tags match.",
"Is em a direct child of article? Are h1 and p siblings?",
"em is not a direct child of article; p is its parent. h1 and p share article as a parent, so they are siblings. Both are descendants of main.",
[('the DOM','dom.html#dom'),('content models','dom.html#content-models')],
'Describe parent, sibling and descendant relationships|Separate visual arrangement from document structure')

M(6,'Make your first document','Use a text editor, a browser and a small feedback loop.',
'''Create a folder with index.html. Save it as UTF-8, then open it in a browser. A local file is enough for the first static document. Later, use a local HTTP server for examples that depend on fetch, modules, origin behavior or server responses.

Use an editor that lets you see the actual file contents. A rich-text document renamed with an html extension is not an HTML source file. Confirm that your operating system has not quietly saved index.html.txt.

## Check what you changed
Edit one heading, save, reload, and find the changed text. Open Developer Tools and inspect the heading. Change the document title and look at the browser tab. These separate checks establish where your output appears.

Run a conformance checker early. Fix errors in the smallest document before adding layout. Keep a copy you can return to, preferably in version control. Browser extensions can alter pages, so use a clean profile when investigating behavior you cannot explain.''',
'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Neighbourhood Library</title>
</head>
<body>
  <h1>A good place to start reading</h1>
  <p>Visit the library on Saturday.</p>
</body>
</html>''',
'''The viewport declaration supports a page sized for a device's viewport. It is not a responsive layout by itself. The page still needs CSS if its later layout should adapt to available space.''',
"Editing a different copy of the file from the one open in the browser. Check the address and the saved path before debugging the markup.",
"Change the tab title without changing the visible heading. Which element should you edit?",
"Edit title inside head. The visible heading is h1 inside body. They may use different wording because one labels the document in browser UI while the other introduces the page content.",
[('a quick introduction','introduction.html#a-quick-introduction-to-html')],
'Create a complete UTF-8 HTML document|Verify changes in the browser and a checker')

M(7,'The document shell','Give each document a predictable beginning.',
'''A complete HTML page normally declares the doctype, document language, encoding, title and body content. This small shell is worth understanding even if your framework generates it.

The doctype helps select standards-mode processing. It is not an instruction to fetch a document type definition. The html element is the document element. head holds document metadata; body holds the document's content.

## Avoid copying a shell blindly
Set lang to the language actually used by the page. Keep the character encoding declaration early in the document; the Standard requires a meta encoding declaration to be entirely within the first 1024 bytes when that mechanism is used. A server can also communicate encoding through its response headers.

Do not duplicate head or body to combine two pages. Combine their appropriate content into a single document, resolving conflicting metadata. A stylesheet, script or template system does not excuse an invalid outer structure.''',
'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Opening hours | Neighbourhood Library</title>
</head>
<body>
  <h1>Opening hours</h1>
  <p>Tuesday to Saturday, 10:00 to 17:00.</p>
</body>
</html>''',
'''The title identifies this page and its site. The heading can stay shorter. Neither substitutes for the other.''',
"Putting a second doctype and a second body inside an existing body when pasting a complete example.",
"You receive two complete HTML files and want a single page. Should you paste the second html element inside the first body?",
"No. Keep one document shell. Move the second page's relevant body content into the first body, choose the required metadata, then check heading structure, duplicate ids and links.",
[('the doctype','syntax.html#the-doctype'),('encoding declarations','semantics.html#charset')],
'Explain the job of the doctype|Combine content without duplicating document structure')

M(8,'html, head and body','Keep metadata and page content in their intended places.',
'''head is not a hidden drawer for arbitrary markup. Its content model is metadata content, with additional rules for elements such as title and base. Put a visible navigation bar in body, even if it appears at the top of the screen.

body is the main container for the document's page content. The name header refers to introductory content in body; it is not a replacement for head. A page can have a document head and several meaningful headers in its content.

## Set the page language
The lang attribute on html establishes the language for descendants that do not override it. Mark a phrase in another language on an appropriate containing element. Do not use a country code when you mean a language code. A region subtag can qualify a language where it helps, but it is optional when a general language tag is enough.

Optional-tag rules can allow some tags to be omitted in carefully defined situations. Explicit html, head and body tags are a useful convention for teaching and maintenance. Understand that this is a convention, not a claim that omission is always invalid.''',
'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Library membership</title>
</head>
<body>
  <header><p>Neighbourhood Library</p></header>
  <main><h1>Become a member</h1></main>
</body>
</html>''',
'''The header contains site introduction inside body. head contains metadata that describes the document.''',
"Using head where header was intended, or assuming that body must begin immediately with a heading and cannot contain a site header.",
"Where should a site logo link go: head, header in body, or title?",
"Put the visible logo link in body, often inside a header. title contains text for the document title, not a visible linked logo. head is for metadata.",
[('the document element','semantics.html#the-html-element'),('head','semantics.html#the-head-element'),('body','sections.html#the-body-element')],
'Place metadata and visible content correctly|Set an appropriate document language')

M(9,'Text, encoding and escaping','Make the bytes and the intended characters agree.',
'''UTF-8 represents characters as bytes. Your editor's save encoding and the document's declared encoding must agree. A declaration cannot repair bytes that were saved incorrectly.

Use literal readable text for ordinary characters when your workflow supports UTF-8. Character references are useful when source syntax would otherwise be ambiguous. Write &lt; to show a less-than sign in text, and use &amp; where an ampersand needs escaping. Escape the quote character that delimits an attribute value when it appears inside that value.

## Preserve meaning when showing code
The example displays the text <button> without creating a button. The parser consumes the character references and creates text characters. This is different from inserting untrusted strings through innerHTML, which invokes markup parsing.

A non-breaking space changes line-breaking behavior. Do not scatter it through text to imitate layout. CSS is the right place for gaps between interface elements. When you copy source between tools, check for accidental invisible characters and preserve meaningful language characters.''',
'''<p>Write <code>&lt;button&gt;</code> for an action.</p>
<p>Research &amp; reading</p>
<p title="She said &quot;welcome&quot;">A quoted greeting</p>''',
'''The code element supplies semantics for a code fragment; escaping stops the fragment from being parsed as an actual element. Both decisions matter.''',
"Escaping the same text twice. &amp;lt; displays the reference spelling &lt; rather than the intended less-than sign.",
"How would you show the literal source text <p>Hello</p> inside a code element?",
"Use <code>&lt;p&gt;Hello&lt;/p&gt;</code> in the HTML source. The browser displays the tag spelling as text. Keep the code element so that the kind of text is still identified.",
[('character references','syntax.html#character-references'),('encoding','syntax.html#character-encodings')],
'Keep saved encoding and declared encoding consistent|Escape markup when displaying source')

M(10,'Nesting and void elements','Well-formed-looking tags are only the beginning.',
'''Close nested elements in the reverse order you opened them. That keeps the source understandable, but correct nesting also depends on each element's content model. A paragraph cannot contain arbitrary flow content such as a div.

Void elements have no contents in HTML syntax. Examples include img, br, meta, link and input. Do not write an img end tag. A trailing slash on a void element is unnecessary in HTML and does not give it XML semantics.

## Choose explicit source while learning
Some end tags can be omitted under specific conditions. Closing them explicitly is often easier to review. Other end tags, such as an anchor's end tag, are not optional in the same way.

Do not use a slash on a non-void element as if it closed the element in text/html. A script element still requires an end tag. If parsing produces an unexpected tree, inspect the source around the earliest error rather than adding more closing tags at the bottom.''',
'''<p>Bring a <strong>current membership card</strong>.</p>
<img src="membership-card.svg" alt="Sample library membership card"
     width="320" height="200">
<p>Ask at the desk if you need a replacement.</p>''',
'''The strong element closes before its paragraph. The img stands on its own as a void element. Its width and height describe the intended intrinsic dimensions or aspect-ratio basis for layout, not a guarantee that CSS cannot resize it.''',
"Writing <div /> in an HTML document and expecting later content to be outside the div.",
"Why is <p><div>Notice</div></p> not a sound way to put a notice box inside a paragraph?",
"A div is not permitted paragraph content. The HTML parser can close the paragraph before it processes the div, producing a tree unlike the source suggests. Use a containing div or section with a paragraph inside it instead.",
[('elements and tag omission','syntax.html#elements-2'),('optional tags','syntax.html#optional-tags')],
'Recognize void elements|Check content rules as well as matching tags')

M(11,'Attributes and their values','Presence, an empty string and the word false are different things.',
'''Quote attribute values consistently. HTML allows unquoted values only when they satisfy its restrictions; quoting is easier to maintain when a value later gains a space or punctuation.

Boolean attributes represent their state by presence or absence. disabled="false" still supplies disabled. To leave a control enabled, omit the attribute. An enumerated attribute uses defined keywords and can have missing-value and invalid-value defaults. Do not apply boolean rules to an attribute merely because its value looks like true or false.

## Learn the value type
hidden, contenteditable and autocomplete do not all share the same value rules. Read the definition for the attribute and its particular element or state. Values such as ids, token lists, URLs and numbers each have their own syntax.

In HTML documents, attribute names on HTML elements are treated in an ASCII case-insensitive way during parsing. Lowercase names are a readable convention. Attribute values are not universally case-insensitive: an id and a URL path can be case-sensitive.''',
'''<label for="member-email">Email</label>
<input id="member-email" name="email" type="email" required>
<button type="submit" disabled>Join the waiting list</button>''',
'''required and disabled are boolean attributes. The id and for values establish a label relationship. The type keyword selects an input state, whose rules affect validation and interface behavior.''',
"Inventing a generic rule that every attribute can be turned off with the string false.",
"You find <button disabled=\"false\">Save</button>. How do you make it enabled in the initial HTML?",
"Remove disabled. The string false does not turn off a boolean attribute. If a script changes the state later, assign false to the element's disabled property or remove the attribute.",
[('boolean attributes','common-microsyntaxes.html#boolean-attributes'),('enumerated attributes','common-microsyntaxes.html#keywords-and-enumerated-attributes')],
'Distinguish boolean and enumerated attributes|Read attribute values according to their defined syntax')

M(12,'Content categories and models','Use categories to understand what can go where.',
'''The Standard groups elements into content categories such as metadata, flow, phrasing and interactive content. Categories overlap. An element can belong to several, and membership can depend on its attributes or context.

A content model describes what an element can contain. Categories make those descriptions shorter, but they do not remove additional restrictions. A button can contain phrasing content while still prohibiting interactive descendants and descendants with tabindex.

## Transparent does not mean unrestricted
An anchor has a transparent content model in relevant contexts. Its contents must fit the surrounding context, with the anchor's own restrictions still applying. Wrapping an entire card in a link does not permit putting another link or a button inside that link.

The reference includes the captured category summaries and their exceptions. Treat these as routes to the definitions, especially for media, form-related elements and transparent models. The category table contains more rows than the commonly taught core category names because it also includes form-related groupings.''',
'''<article>
  <h2><a href="book.html">The Atlas of Small Places</a></h2>
  <p>A walking guide to overlooked streets.</p>
  <button type="button">Add to reading list</button>
</article>''',
'''The navigation link and the action button are separate. Neither interactive control is nested inside the other. The article can still be styled as one visual card.''',
"Wrapping a card containing buttons in one outer anchor and assuming transparent content permits every descendant.",
"Why is a button inside an anchor a problem even if both controls can be clicked with a mouse?",
"The anchor's content restrictions disallow interactive descendants, including a button. The structure also leaves competing interactions in one region. Use separate controls with clear destinations or actions.",
[('content models','dom.html#content-models'),('categories','dom.html#kinds-of-content')],
'Use overlapping content categories|Apply extra restrictions on transparent and interactive content')

M(13,'Conformance and useful errors','Make the checker part of the feedback loop.',
'''A conformance checker can identify invalid nesting, missing required attributes and many syntax errors. It cannot decide whether your alternative text is useful, whether your page is easy to navigate, or whether a server validates a submission securely.

Check the complete document as well as small examples. The containing form, table or head can change what is permitted. Fix the earliest relevant error first because a parser recovery can cause several later messages.

## Classify what failed
A missing end tag, an unknown attribute and a broken resource URL are different problems. Some failures are conformance errors; some are network failures; some are mistakes in the intended behavior. Choose a check that can observe the failure you care about.

Keep intentionally invalid teaching examples separate from valid fixtures and record the expected error. A checker pass means the checked document passed that checker version and configuration. It is not a general quality certificate. If a new standardized feature triggers a message, compare the current definition with the checker's supported version before changing correct markup blindly.''',
'''<form action="/membership" method="post">
  <label for="full-name">Full name</label>
  <input id="full-name" name="fullName" autocomplete="name" required>
  <button type="submit">Apply for membership</button>
</form>''',
'''A conformance check can inspect the label relationship and syntax. You still need to test actual submission handling and whether the requested name field is appropriate to the service.''',
"Treating a clean checker output as proof that a page meets WCAG or has no security risks.",
"A document validates, but its submit button sends data to the wrong endpoint. Is the checker broken?",
"No. A syntactically valid action URL can be the wrong application destination. Test the request and server behavior in addition to conformance. Each check needs a defined responsibility.",
[('conformance requirements','introduction.html#conformance-requirements-for-authors')],
'Use checker output without overclaiming|Separate syntax, network and behavior failures')

M(14,'Headings and paragraphs','Make the page structure readable without its styling.',
'''A heading names the content that follows it. Use h1 through h6 to express the hierarchy you intend. For the ordinary pages in this book, one page-level h1 and properly nested subsection headings are a practical convention.

Choose heading levels for structure, not font size. CSS can make an h2 smaller or larger without changing its meaning. A section element does not automatically reset a conventional heading hierarchy to a new h1 in the way many old tutorials suggested.

## Separate paragraphs from line breaks
Use p for paragraphs. br is a line break within content where the break itself belongs, such as an address or a poem. Empty paragraphs and repeated br elements are not layout tools. hr represents a thematic break, not merely a horizontal line to decorate a page.

The Living Standard also includes headingoffset and headingreset. These require independent compatibility and accessibility review; they are not a reason to discard a clear conventional hierarchy. This edition records them in the reference and uses ordinary heading levels in its running examples.''',
'''<main>
  <h1>Membership</h1>
  <p>Membership is open to local residents.</p>
  <section>
    <h2>What to bring</h2>
    <p>Bring an address document and a form of identification.</p>
  </section>
</main>''',
'''The h2 introduces a subsection of membership. It does not depend on the browser calculating an implicit outline from section nesting.''',
"Picking h4 because its default size matches a design. That makes document structure depend on a browser stylesheet.",
"A designer wants the main heading to look small. Should you change h1 to h5?",
"Keep the heading level that matches the document structure and change its presentation with CSS. A visual size preference does not change where the heading belongs in the hierarchy.",
[('headings','sections.html#the-h1,-h2,-h3,-h4,-h5,-and-h6-elements'),('paragraphs','grouping-content.html#the-p-element')],
'Create a conventional heading hierarchy|Use paragraphs, line breaks and thematic breaks for their meanings')

M(15,'Inline meaning','Pick emphasis because of the sentence, not the browser font.',
'''em marks stress emphasis. strong marks importance, seriousness or urgency. Their default italic and bold styles are not their definitions. A book title can use cite; a short quotation can use q. Use a blockquote for a quoted section rather than a short inline quotation.

small suits side comments such as a copyright or a qualification. mark can identify text relevant to the reader's current context, such as a search match. span supplies a generic phrasing container when no more specific semantic element fits.

## Do not turn typography into semantics
The b and i elements also have defined uses beyond their default appearance. b can draw attention without conveying extra importance; i can mark text in an alternate voice or mood. u is for an explicitly rendered non-textual annotation, not a generic request to underline.

Quote and cite carefully. A cite attribute can record a source URL, but browsers do not normally expose it as a useful visible citation. Provide an ordinary visible source link when readers need to follow it. cite represents a work's title rather than a person's name.''',
'''<p><strong>Return the key before closing time.</strong></p>
<p>You may borrow <em>two</em> reference books.</p>
<p>Our reading group chose <cite>Things Fall Apart</cite>.</p>''',
'''The importance of returning the key differs from the stress on two. The novel's title names a work; it does not claim emphasis in the sentence.''',
"Using strong around every visually bold fragment, including purely decorative interface text.",
"Which element fits a short phrase that must carry stress in the sentence, and which fits an urgent warning?",
"Use em for stress emphasis and strong for an urgent or important warning. If the requirement is only a typeface change, use CSS on an appropriate existing element or a neutral span.",
[('text-level semantics','text-level-semantics.html#text-level-semantics')],
'Distinguish stress, importance and presentation|Represent titles and quotations deliberately')

M(16,'Code and technical text','Preserve the source when readers need to copy it.',
'''code identifies computer code. pre preserves the significance of whitespace in preformatted text. Combine them when indentation and line breaks matter. Escape markup characters before placing HTML source inside either element.

kbd marks user input, samp marks sample output, and var marks a variable. These meanings are useful even when a stylesheet makes them look similar. A filename or a command does not need a decorative badge to be understandable.

## Give examples enough context
State the file, command environment or containing element that an example needs. Readers should know whether they can paste a block into a document or need to supply surrounding code. A fragment that works in body may be invalid in head.

Avoid screenshots as the only version of code. Text can be copied, searched and read by assistive technology. If a code block scrolls horizontally, make the scroll container keyboard reachable and label it. Keep the example short enough to explain; put a longer working file in the downloads.''',
'''<p>Press <kbd>Ctrl</kbd> + <kbd>S</kbd> to save.</p>
<pre><code>&lt;h1&gt;Library catalogue&lt;/h1&gt;</code></pre>
<p>The server returned <samp>201 Created</samp>.</p>''',
'''The example shows HTML source as text. kbd identifies input rather than output. The status string is a sample response, not proof that this page made a request.''',
"Pasting raw <h1> markup into code and expecting it to stay visible as source.",
"Why do you still need escaping inside pre and code?",
"Neither element turns off ordinary HTML parsing of their contents. Escape the angle brackets so the parser creates text instead of an h1 element. pre changes whitespace handling, not the basic parsing rule.",
[('preformatted text','grouping-content.html#the-pre-element'),('code','text-level-semantics.html#the-code-element')],
'Distinguish code, input and output|Display copyable escaped source')

M(17,'Links that go somewhere','Let the destination explain the control.',
'''An a element with href creates a hyperlink. Give it wording that makes sense in context and a destination that does what the wording promises. A file path, a fragment and an absolute URL resolve differently.

A fragment such as #fees points to an element with a matching id in the same document. Relative URLs resolve against the document's base URL. A base element can change that resolution across the page, which makes it easy to introduce surprising navigation bugs.

## Navigation is different from an action
Use a hyperlink to go to a resource. Use a button to submit a form or perform an interface action. href="#" is not a neutral placeholder for a JavaScript button; it still has navigation behavior.

Opening a new browsing context changes the user's experience. Avoid doing it automatically without a reason. If you use target="_blank", describe the behavior where it helps and understand opener relationships. Modern anchor behavior provides implicit noopener for this target, but explicitly writing rel="noopener" can document the intention. Do not imply that this solves every trust or privacy concern.''',
'''<p><a href="catalogue.html">Browse the catalogue</a></p>
<p><a href="#fees">Read the membership fees</a></p>
<section id="fees">
  <h2>Membership fees</h2>
  <p>Ask the desk about the current membership options.</p>
</section>''',
'''The first URL is a sibling document. The second is a fragment in this document. The target id must be unique in the element's tree.''',
"Using link text such as click here repeatedly when a destination-specific phrase would be clearer.",
"Would you use an anchor or a button to open the next page of the catalogue? What about removing a book from a local reading list?",
"Use an anchor for another catalogue page. Use a button for the removal action. If the action changes server data, also design and test its request, permissions and error handling; the element choice alone does not implement those controls.",
[('the a element','text-level-semantics.html#the-a-element'),('links','links.html#links')],
'Choose links for navigation|Resolve document and fragment URLs correctly')

M(18,'Lists with a reason','Order and relationships determine the markup.',
'''Use ul for a group whose order is not significant, and ol when sequence or rank is part of the meaning. Each item is an li. A navigation menu is often a list of links, but not every group of adjacent items needs list markup.

A description list uses dl, dt and dd for name-value groups. A group can have multiple terms or multiple descriptions. It is not limited to dictionary definitions and does not require a table-like visual layout.

## Keep nested lists inside an item
A sublist belongs inside the li it expands. A list placed beside an li is not that item's nested list. Markup should explain the relationship before CSS adds indentation.

For ordered lists, start and reversed can change the numbering behavior, and an li value can set an item's ordinal value in an ol. These are useful when the displayed order has meaning. Avoid using list markers as a substitute for actual text if readers need the text outside that presentation.''',
'''<ol>
  <li>Choose a book.</li>
  <li>Check the lending period.
    <ul><li>Reference books have separate rules.</li></ul>
  </li>
  <li>Take the book to the desk.</li>
</ol>''',
'''The unordered sublist qualifies the second step. It remains inside that step's li, so the tree preserves the relationship.''',
"Putting the nested ul directly under the outer ol between two li elements.",
"Which structure fits opening hours grouped by day names: an ordered list of steps or a description list?",
"A description list is a reasonable choice for day names and their hours because the groups describe name-value relationships. A table may be better when readers need to compare a regular grid of days and multiple time ranges. An ordered list would imply a meaningful sequence of steps.",
[('lists','grouping-content.html#the-ol-element'),('description lists','grouping-content.html#the-dl-element')],
'Distinguish ordered, unordered and description lists|Nest a list under the item it expands')

M(19,'Figures and captions','Keep self-contained material with its explanation.',
'''A figure holds self-contained content that the surrounding prose can refer to as a unit. It can contain a diagram, photograph, code listing or another suitable item. figcaption supplies its caption as the first or last child when present.

Not every image needs a figure. An icon in a button is part of that control. A photograph beside a paragraph may or may not be self-contained. Decide from the content relationship, not a desire for a styled border.

## A caption and alternative text do different work
A caption explains the figure in the document. Alternative text supplies a replacement for an image according to its purpose and context. Repeating a long caption word for word as alt can add noise without helping. An image with information absent from the caption still needs that information represented appropriately.

A complex chart usually needs more than a short alt string. Provide the important conclusion and a detailed text or data alternative that readers can reach. Do not claim an image is accessible solely because alt is present.''',
'''<figure>
  <img src="floor-plan.svg"
       alt="The reading room is left of reception; the lift is opposite."
       width="640" height="360">
  <figcaption>Ground-floor facilities near the entrance.</figcaption>
</figure>''',
'''The alternative conveys the directions shown by the image. The caption identifies the figure's subject in the document. A real floor plan would need its own reviewed alternative based on its actual contents.''',
"Generating alternative text from a filename without inspecting the image or its purpose.",
"A chart caption says Monthly loans. Does repeating Monthly loans in alt communicate the chart's trend?",
"No. It only repeats the subject. Describe the meaningful information, and provide an accessible data table or fuller explanation when the chart needs one. The appropriate wording depends on the actual data and the reason the chart appears.",
[('figures','grouping-content.html#the-figure-element')],
'Choose a figure for self-contained content|Separate a caption from an image alternative')

M(20,'Dates, values and edits','Give machines a useful value without spoiling the sentence.',
'''time can pair readable date or time text with a machine-readable datetime value. Use a value that matches the defined syntax and the kind of temporal information you actually know. Do not add a timezone or a time of day just to make a date look more precise.

data associates its contents with a machine-readable value. It is useful for a product identifier or another mapping that a script or processor uses. It does not create a general validation rule for that value.

## Record edits when the change matters
ins and del mark additions and deletions. Their datetime and cite attributes can record when and why a change happened, subject to their defined rules. Provide visible context when readers need it; an attribute alone is not a usable change log.

s has a different meaning from del: it marks content that is no longer accurate or relevant, without necessarily marking a document edit. An old price can be struck through while the current price remains plainly stated. Choose the meaning before choosing the decoration.''',
'''<p>Next meeting: <time datetime="2026-11-07">7 November 2026</time>.</p>
<p>Book code: <data value="LIB-204">Local history collection</data>.</p>
<p>The desk opens at <del>09:00</del> <ins>10:00</ins>.</p>''',
'''The date supplies only a date. The collection has an explicit identifier. The changed opening time is visible in the sentence, rather than hidden in metadata.''',
"Writing an informal date such as 7/11/26 in datetime and assuming every parser will interpret it the same way.",
"You know an event date but not its time. Should you write a midnight UTC timestamp?",
"No. Use a valid date value such as 2026-11-07. A fabricated time or timezone adds information you do not have and can mislead downstream software.",
[('time','text-level-semantics.html#the-time-element'),('edits','edits.html#edits')],
'Use machine-readable dates without invented precision|Distinguish document edits from obsolete wording')

for filename in ["chapters_middle.py", "chapters_advanced.py", "chapters_professional.py"]:
    exec((R/"tools"/filename).read_text(), globals())
if __name__=='__main__':
    assert len(BOOK)==74, len(BOOK)
    (R/'content/chapters.json').write_text(json.dumps(sorted(BOOK,key=lambda x:x['number']),ensure_ascii=False,indent=2)+'\n')
