#!/usr/bin/env python3
"""Build the static reading publication. No network access; no framework or CDN runtime."""
from pathlib import Path
from html import escape
from urllib.parse import urlparse
import argparse, hashlib, json, re, shutil, textwrap, zipfile
from collections import defaultdict
from fingerprint import publication_fingerprint,input_manifest
from pygments import highlight
from pygments.lexers import HtmlLexer
from pygments.formatters import HtmlFormatter
R=Path(__file__).resolve().parents[1];SITE=R/'build/site'
BOOK=json.loads((R/'content/chapters.json').read_text())
META=json.loads((R/'content/publication.json').read_text())
GUIDE=json.loads((R/'content/reading-guide.json').read_text())
INV=json.loads((R/'content/reference-snapshot.json').read_text())['inventories']
SOURCES=json.loads((R/'content/source-manifest.json').read_text())
PARTS=defaultdict(list)
for c in BOOK:PARTS[c['part']].append(c)
def clean(s):return str(s).replace('\u2014',', ').replace('\u2013','-')
def e(s):return escape(clean(s),quote=True)
def inline(s):
    s=e(s);s=re.sub(r'`([^`]+)`',r'<code>\1</code>',s);return s

def prose(s):
    out=[]
    for part in s.strip().split('\n\n'):
        if part.startswith('## '):
            lines=part.split('\n',1);heading=lines[0][3:];out.append('<h2>'+inline(heading)+'</h2>')
            if len(lines)>1:out.append('<p>'+inline(lines[1])+'</p>')
        else:out.append('<p>'+inline(part)+'</p>')
    return '\n'.join(out)

def write(path,html):
    p=SITE/path;p.parent.mkdir(exist_ok=True,parents=True)
    if str(path).endswith('.html'):
        html=html.replace('<head>','<head><meta name="author" content="'+e(META['author'])+'">',1)
        if not str(path).startswith('examples/'):
            html=html.replace('Review edition 0.1',e(META['edition_label'])).replace('Review edition',e(META['edition_label']))
            html=html.replace('<span>EDITION<br>0.1</span>','<span>EDITION<br>'+e(META['edition'].replace('-rc',' RC'))+'</span>')
    p.write_text(html)

def shell(title,content,base='',description='',reader=False):
    search='''<dialog id="search-dialog" class="search-dialog" aria-labelledby="search-title"><div class="dialog-top"><h2 id="search-title">Find a page or feature</h2><button type="button" data-close-dialog="search-dialog" aria-label="Close search">Close</button></div><div class="search-input-wrap"><label for="book-search">Search chapters and reference entries</label><input id="book-search" type="search" placeholder="Try forms, selectedcontent, focus..." autocomplete="off"></div><p class="search-status" id="search-status" role="status"></p><ul class="search-results" id="search-results"></ul></dialog>'''
    foot=f'''<footer class="wrap"><div class="footbar"><div>CTROTECH / HTML Playbook<br>© {META["copyright_year"]} {e(META["author"])}<br>{e(META["edition_label"])}</div><div><a href="{base}start.html">Start here</a><a href="{base}author.html">Author and credits</a><a href="{base}about.html">About this edition</a><a href="{base}reference/status.html">Scope and checks</a><a href="{base}downloads/ctrotech-html-playbook.pdf">Download PDF</a></div></div></footer>'''
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; font-src 'self'; img-src 'self' data:; connect-src 'none'; frame-src about:; object-src 'none'; base-uri 'self'; form-action 'none'"><meta name="description" content="{e(description or 'A source-linked HTML curriculum, practice companion and captured reference from CTROTECH.')}"><meta name="theme-color" content="#234d42"><title>{e(title)} | CTROTECH HTML Playbook</title><link rel="icon" href="{base}assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="{base}assets/site.css"><script src="{base}assets/search.js" defer></script><script src="{base}assets/site.js" defer></script></head><body data-base="{base}"><a class="skip" href="#main">Skip to main content</a><header class="topbar"><div class="wrap topinner"><a class="brand" href="{base}index.html"><span class="brand-mark" aria-hidden="true">CT</span><span>CTROTECH<small>HTML Playbook</small></span></a><nav class="toplinks" aria-label="Primary"><a href="{base}contents.html">Read the book</a><a href="{base}reference/index.html">Reference</a><a href="{base}projects.html">Projects</a><button type="button" class="search-trigger" data-open-search>Search <kbd aria-hidden="true">⌘ K</kbd></button></nav></div></header>{'<div class="progress-track" aria-hidden="true"><div class="progress-fill"></div></div>' if reader else ''}{content}{foot}{search}<p id="ui-status" role="status" style="position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%);white-space:nowrap"></p></body></html>'''

def parts_html(open_all=False):
    out=[]
    for part,chapters in PARTS.items():
        name=part.split(' / ',1)[1]
        out.append(f'<details class="part-item" {"open" if open_all else ""}><summary><span class="part-label">{e(name)}</span><span class="part-count">{chapters[0]["number"]:02}-{chapters[-1]["number"]:02} +</span></summary><ol class="chapter-list">'+''.join(f'<li><a href="chapters/{c["number"]:02}.html"><span class="number">{c["number"]:02}</span>{e(c["title"])}</a></li>' for c in chapters)+'</ol></details>')
    return '<div class="part-list">'+''.join(out)+'</div>'

NOTICE='<div class="review-note"><p><strong>About this edition.</strong> A practical reading curriculum with a captured, source-linked reference. It is not a completed whole-Standard behavioral audit. <a href="about.html#edition-scope">Read the scope and review notes</a>.</p></div>'

def home():
    content='''<main id="main" class="wrap"><section class="hero" aria-labelledby="home-title"><div><p class="eyebrow"><span class="dot"></span>Field guide 001 / October 2026</p><h1 id="home-title">The HTML<br>Playbook.</h1><p class="intro">Write pages you can explain. A practical guide to HTML, from your first document to forms, browser behavior and a site worth maintaining.</p><p class="author-line">By <a href="author.html">__AUTHOR__</a> <span>/ CTROTECH</span></p><div class="hero-actions"><a class="button primary" href="chapters/01.html">Start reading <span aria-hidden="true">↗</span></a><a class="button" href="downloads/ctrotech-html-playbook.pdf">Get the PDF</a></div><p class="hero-foot">Read at your own pace. No account, email gate or analytics. <a href="start.html">Find your reading path</a>. <a href="downloads/code-examples.zip" download>Get all 74 code files</a>.</p></div><div class="book-art" role="img" aria-label="HTML Playbook, CTROTECH October 2026 reading edition"><div class="cover-meta"><span>CTROTECH<br>FIELD GUIDE / 001</span><span>EDITION<br>0.1</span></div><div class="cover-title">HTML</div><div class="cover-caption">A working knowledge of the web.</div><div class="cover-rule"></div><div class="cover-code"><span class="c">&lt;main&gt;</span>
  &lt;h1&gt;Make the meaning clear.&lt;/h1&gt;
  &lt;p&gt;Start with the document.&lt;/p&gt;
<span class="c">&lt;/main&gt;</span></div><div class="cover-bottom"><span>LEARN / LOOK UP / BUILD</span><span>2026</span></div></div></section><div class="facts"><div><b>74</b><span>chapters to work through</span></div><div><b>113</b><span>HTML element entries</span></div><div><b>74</b><span>explained exercises</span></div><div><b>7</b><span>reference projects</span></div></div><section><div class="section-head"><div><p class="eyebrow">Choose a starting point</p><h2>Where are you building from?</h2></div><p>Follow the chapters in order, or go straight to the problem on your desk.</p></div><div class="path-grid">'''
    for num,title,desc in [(1,'Your first page','Understand the document, tags and the browser tree.'),(28,'Images and media','Choose resources, alternatives and loading behavior.'),(34,'Forms that make sense','Work through labels, choices, constraints and submission.'),(61,'Before you publish','Review keyboard use, trust boundaries and release evidence.')]:
        content+=f'<a class="path-card" href="chapters/{num:02}.html"><span class="path-num">CHAPTER {num:02}</span><h3>{title}</h3><p>{desc}</p><span class="arrow" aria-hidden="true">↗</span></a>'
    content+='</div></section><section><div class="section-head"><div><p class="eyebrow">The reading path</p><h2>A document first. A site next.</h2></div><a href="contents.html">See every chapter</a></div>'+parts_html()+ '</section>'+NOTICE+'</main>'
    content=content.replace('__AUTHOR__',e(META['author']))
    write('index.html',shell('The book',content))
    write('contents.html',shell('Contents','<main id="main" class="wrap"><div class="page-heading"><p class="eyebrow">The reading path and reference</p><h1>Contents</h1><p>Begin with the document model, then build toward a multi-page site. Every chapter includes an example and an exercise with an explained answer.</p></div>'+NOTICE+parts_html(True)+'</main>'))


def standalone(c):
    code=c['code']
    if code.lower().startswith('<!doctype'):return code+'\n'
    extra=code if c['number']==51 else ''
    body='' if c['number']==51 else code
    if not re.search(r'<h1(?:\s|>)', body, re.I):body='<h1>'+e(c['title'])+': example</h1>\n'+body
    return f'<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1">\n<title>{e(c["title"])}: example</title>\n{extra}\n</head>\n<body>\n{body}\n</body>\n</html>\n'


def chapter(c):
    n=c['number'];base='../'
    nav='<aside class="reader-nav" id="chapter-navigation"><div class="nav-top"><a href="../contents.html">All chapters</a><span data-reading-count>0 / 74 read</span></div>'
    for part,chapters in PARTS.items():
        nav+=f'<details {"open" if c["part"]==part else ""}><summary>{e(part.split(" / ",1)[1])}</summary><ul>'
        nav+=''.join(f'<li><a href="{ch["number"]:02}.html" {"aria-current=page" if ch["number"]==n else ""}><span>{ch["number"]:02}</span>{e(ch["title"])}</a></li>' for ch in chapters)+'</ul></details>'
    nav+='</aside>'
    count=len(re.findall(r'\b\w+\b',c['lesson']+' '+c['explanation']+' '+c['answer']));minutes=max(2,round(count/180))
    code=highlight(c['code'],HtmlLexer(ensurenl=False,stripnl=False),HtmlFormatter(nowrap=True))
    if not c['code'].endswith('\n'):code=code.removesuffix('\n')
    write(f'code/{n:02}.html.txt',c['code'])
    lab='''<dialog id="lab-dialog" class="lab-dialog" aria-labelledby="lab-title"><div class="dialog-top"><h2 id="lab-title">Try the markup</h2><button type="button" data-close-dialog="lab-dialog">Close example</button></div><div class="lab-content"><textarea id="lab-code" aria-label="HTML source editor" spellcheck="false"></textarea><iframe id="lab-output" title="Isolated HTML example" sandbox="allow-scripts"></iframe></div><div class="lab-footer"><button type="button" id="lab-run">Run changes</button><button type="button" id="lab-reset">Reset</button><span>Isolated preview. Parent DOM access and form submissions are blocked; resource loading is restricted. Never paste secrets or run code you do not trust.</span></div></dialog>'''
    text=f'<div class="reader-shell"><div class="mobile-chapters"><button type="button" data-chapters-toggle aria-expanded="false" aria-controls="chapter-navigation">Chapters</button><span data-reading-count>0 / 74 read</span></div>{nav}<div><main id="main" class="reader"><article><div class="breadcrumbs"><a href="../contents.html">The book</a> / {e(c["part"].split(" / ",1)[1])}</div><p class="eyebrow">Chapter {n:02}</p><h1>{e(c["title"])}</h1><p class="dek">{e(c["dek"])}</p><div class="chapter-meta"><span>{minutes} MIN READ + PRACTICE</span><span>SOURCE-LINKED PRACTICE</span><span>OCTOBER 2026</span></div><div class="mobile-reading-tools" role="group" aria-label="Reading settings"><button type="button" data-font-size="17" aria-label="Smaller reading text">A−</button><button type="button" data-font-size="19" aria-label="Default reading text">A</button><button type="button" data-font-size="21" aria-label="Larger reading text">A+</button><button type="button" data-theme-toggle>Night theme</button></div><div class="objectives"><strong>By the end of this chapter</strong><ul>'+''.join('<li>'+e(g)+'</li>' for g in c['objectives'])+'</ul></div><div class="prose">'+prose(c['lesson'])
    text+=f'<h2 id="example">The example</h2><div class="codebox"><div class="code-head"><span>{"HTML + JavaScript" if "<script" in c["code"].lower() else "HTML"} / example {n:02}</span><button type="button" data-copy="chapter-code">Copy</button></div><pre tabindex="0" role="region" aria-label="Scrollable HTML example"><code id="chapter-code">{code}</code></pre></div><div class="example-actions"><button type="button" data-open-lab>Try the markup</button><a href="../code/{n:02}.html.txt" download="example-{n:02}.html">Download exact code</a><small>Sandbox restrictions apply.</small></div>'+prose(c['explanation'])
    if c.get('project_slug'):text+=f'<p><a class="button primary" href="../downloads/project-{c["project_slug"]}.zip">Download the complete reference project</a></p>'
    text+='<div class="callout"><strong>A mistake to watch for</strong>'+inline(c['mistake'])+'</div><section class="exercise" aria-labelledby="exercise-title"><p class="eyebrow">Your turn</p><h2 id="exercise-title">Check your understanding</h2><p>'+inline(c['question'])+'</p><details><summary>Read the explained answer</summary><p>'+inline(c['answer'])+'</p></details></section>'
    text+='<h2 id="sources">Read the source</h2><ul class="source-list">'+''.join(f'<li><a href="{e(s["url"])}" target="_blank" rel="noopener noreferrer">{e(s["title"])}</a></li>' for s in c['sources'])+'</ul></div><div class="chapter-end"><button type="button" class="complete-button" data-mark-read="'+c['id']+'" aria-pressed="false">Mark this chapter as read</button><p class="small-note">Reading progress stays in this browser. It is not a course certificate or a technical-review status.</p></div><nav class="page-turn" aria-label="Chapter navigation">'
    if n>1:text+=f'<a href="{n-1:02}.html"><small>PREVIOUS / {n-1:02}</small>{e(BOOK[n-2]["title"])}</a>'
    else:text+='<a href="../contents.html"><small>THE BOOK</small>Back to contents</a>'
    if n<74:text+=f'<a href="{n+1:02}.html"><small>NEXT / {n+1:02}</small>{e(BOOK[n]["title"])}</a>'
    else:text+='<a href="../reference/status.html"><small>AFTER THE CAPSTONE</small>Review and release checklist</a>'
    text+='</nav></article></main></div><aside class="on-page" aria-label="On this page"><p class="eyebrow">In this chapter</p><a href="#example">The example</a><a href="#exercise-title">Your turn</a><a href="#sources">Sources</a><div class="reading-tools"><p class="eyebrow">Reading settings</p><div><button type="button" data-font-size="17" aria-label="Smaller reading text">A−</button> <button type="button" data-font-size="19" aria-label="Default reading text">A</button> <button type="button" data-font-size="21" aria-label="Larger reading text">A+</button></div><button type="button" data-theme-toggle>Night theme</button></div></aside></div><textarea id="example-source" hidden>'+e(standalone(c))+'</textarea>'+lab
    write(f'chapters/{n:02}.html',shell(c['title'],text,base=base,description=c['dek'],reader=True));write(f'examples/{n:02}.html',standalone(c))

REFS=[('elements','Elements','All 113 named built-in HTML elements from the captured conforming index.',['elements']),('attributes','Attributes','Context-specific attributes and event-handler records.',['attributes','event_handler_attributes']),('globals','Global attributes','Named global attributes and cross-specification boundaries.',['global_attributes','global_attribute_families']),('inputs','Input states','The 22 input states and their defined control roles.',['input_states']),('categories','Content models','Category membership and exceptions from the discovery index.',['content_categories']),('obsolete','Obsolete features','Historical authoring restrictions and migration guidance.',['obsolete_elements','obsolete_attributes','obsolete_conforming_conditions']),('apis','API catalogue','166 named interface routes. Member-level documentation is still incomplete.',['interfaces'])]

def ref_card(r,category):
    name=r['name'];tag=r['id'].split(':')[0];description=r.get('description') or r.get('scope') or r.get('condition') or r.get('migration_guidance') or r.get('inventory_boundary') or r.get('state','')
    if len(description)>1200:description=description[:1200]+' See the normative source for the complete condition.'
    details=''
    for key,label in [('categories','Categories'),('parents','Parent summary'),('children','Content summary'),('attributes','Attribute summary'),('applicability_summary','Applies to'),('value_summary','Value summary'),('ownership','Owning specification'),('elements_summary','Members'),('exceptions_summary','Exceptions'),('data_type','Data'),('control_type','Control')]:
        if r.get(key):details+=f'<dt>{label}</dt><dd>{inline(r[key])}</dd>'
    url=r.get('definition_url') or next(iter(r.get('definition_urls',[])),None) or r['source_url']
    owners=[]
    for owner in r.get('owner_chapters',[]):
        if owner.startswith('CH-'):owners.append(f'<a href="../chapters/{int(owner[3:]):02}.html">Chapter {int(owner[3:]):02}</a>')
    anchor=r['id'].replace(':','-')
    return f'<article class="ref-card" id="{e(anchor)}" data-reference-entry data-category="{e(category)}" data-search="{e((name+" "+description+" "+str(r.get("applicability_summary",""))).lower())}"><h2>{e("<"+name+">" if tag in ["element","obsolete-element"] else name)}</h2><span class="badge">{e(tag)}</span><p>{inline(description)}</p><dl>{details}</dl><div class="ref-links"><a href="{e(url)}" target="_blank" rel="noopener noreferrer">Normative source / discovery route</a>{" ".join(owners)}</div></article>'


def references():
    cards=''.join(f'<a class="path-card" href="{slug}.html"><span class="path-num">LOOKUP / {i:02}</span><h2>{title}</h2><p>{desc}</p></a>' for i,(slug,title,desc,_) in enumerate(REFS,1))
    write('reference/index.html',shell('Reference','<main id="main" class="wrap"><div class="page-heading"><p class="eyebrow">Keep this beside the editor</p><h1>The reference desk.</h1><p>Look up a feature, then follow its definition when context, defaults or exceptions matter.</p></div><div class="review-note">These entries are derived from the captured specification indexes. They are not independently reviewed replacements for every normative definition. Counts refer to this snapshot, not timeless language totals.</div><div class="path-grid reference-menu">'+cards+'</div><div class="reference-body"><h2>More useful pages</h2><ul><li><a href="api-members.html">API members and declarations</a></li><li><a href="keywords.html">Keywords, states and events</a></li><li><a href="answers.html">Exercise answers</a></li><li><a href="glossary.html">Glossary</a></li><li><a href="values.html">Value and microsyntax starting points</a></li><li><a href="sources.html">Source and attribution register</a></li><li><a href="status.html">Review evidence and remaining work</a></li></ul></div></main>',base='../'))
    for slug,title,desc,keys in REFS:
        entries=[]
        for key in keys:entries.extend((r,key) for r in INV[key])
        if slug=='elements':entries.extend((r,'integration') for r in INV['integration_entries'])
        filters='<option value="all">All groups</option>'+''.join(f'<option value="{key}">{e(key.replace("_"," "))}</option>' for key in dict.fromkeys(k for _,k in entries))
        text=f'<main id="main" class="wrap"><div class="page-heading"><p class="eyebrow"><a href="index.html">Reference desk</a></p><h1>{title}</h1><p>{desc}</p></div><div class="review-note">Index-derived review reference. Parent/content summaries, asterisks and conditional applicability need the linked full definition. A listed feature is not necessarily widely supported. The API member register is separate; expanded behavioral coverage is not complete.</div><div class="reference-controls"><label>Find a feature<input id="reference-search" type="search" placeholder="Search by name or meaning"></label><label>Group<select id="reference-filter">{filters}</select></label></div><p class="small-note" id="reference-count" role="status">{len(entries)} entries</p><div class="reference-grid">'+''.join(ref_card(r,key) for r,key in entries)+'</div></main>'
        write('reference/'+slug+'.html',shell(title,text,base='../'))
    answers='<main id="main" class="wrap"><div class="page-heading"><p class="eyebrow">Practice companion</p><h1>Explained answers</h1><p>Attempt the exercise before opening its answer. These are editorial answers awaiting independent review, not a marked assessment.</p></div><div class="reference-body">'
    for c in BOOK:answers+=f'<section id="answer-{c["number"]:02}"><h2><a href="../chapters/{c["number"]:02}.html">{c["number"]:02}. {e(c["title"])}</a></h2><p>{inline(c["question"])}</p><details><summary>Read the answer</summary><p>{inline(c["answer"])}</p></details></section>'
    write('reference/answers.html',shell('Exercise answers',answers+'</div></main>',base='../'))
    glossary=json.loads((R/'content/glossary.json').read_text())
    content='<main id="main" class="wrap"><div class="page-heading"><p class="eyebrow">A shared vocabulary</p><h1>Glossary</h1></div><div class="reference-body"><dl>'+''.join(f'<dt id="{e(k.lower().replace(" ","-"))}"><strong>{e(k)}</strong></dt><dd><p>{inline(v)}</p></dd>' for k,v in glossary.items())+'</dl></div></main>'
    write('reference/glossary.html',shell('Glossary',content,base='../'))
    registry=json.loads((R/'content/value-routes.json').read_text())
    content='<main id="main" class="wrap"><div class="page-heading"><p class="eyebrow">Value syntax is part of the language</p><h1>Values and microsyntaxes</h1><p>A starting map to the definitions. This is not yet a complete value, keyword and default registry.</p></div><div class="reference-body"><ul>'+''.join(f'<li><a href="{e(r["url"])}">{e(r["title"])}</a>: {e(r["note"])}</li>' for r in registry)+'</ul></div></main>'
    write('reference/values.html',shell('Values and microsyntaxes',content,base='../'))
    source_html='<main id="main" class="wrap"><div class="page-heading"><p class="eyebrow">Sources and attribution</p><h1>Follow the rule to its source.</h1><p>HTML definitions come from WHATWG. Compatibility metadata, accessibility guidance and editorial advice have separate roles.</p></div><div class="reference-body"><h2>Captured foundation sources</h2><p>Reference summaries are derived from the retained WHATWG HTML indexes and definition pages. See the <a href="https://whatwg.org/ipr-policy#copyright-license-grant">WHATWG copyright and license terms</a>. The foundation snapshot is dated 14 October 2026. Copyright © WHATWG (Apple, Google, Mozilla, Microsoft). Captured summaries and declarations have been extracted, arranged and linked for this publication; no endorsement is implied. The supplied <a href="../assets/WHATWG-LICENSE.txt">WHATWG license notice</a> preserves the Creative Commons Attribution 4.0 terms and BSD 3-Clause source-code terms. Webref extraction software is covered by its <a href="../assets/webref-MIT.txt">MIT notice</a>. Selected Browser Compatibility Data retains its <a href="../assets/BCD-LICENSE.txt">upstream notice</a>. A captured URL is not proof that every assertion has received normative review.</p><ul>'
    source_html+=''.join(f'<li><a href="{e(s["url"])}">{e(s["id"])}</a><br><span class="small-note">SHA-256: {s["sha256"]}</span></li>' for s in SOURCES)+'</ul><h2>Accessibility authorities</h2><ul><li><a href="https://www.w3.org/TR/WCAG22/">WCAG 2.2</a></li><li><a href="https://www.w3.org/TR/html-aria/">ARIA in HTML</a></li><li><a href="https://www.w3.org/TR/html-aam-1.0/">HTML accessibility mappings</a></li><li><a href="https://www.w3.org/TR/accname-1.2/">Accessible name and description computation</a></li><li><a href="https://www.w3.org/WAI/tutorials/">WAI tutorials</a></li></ul><h2>Writing and type</h2><p>The editorial process used the <a href="https://github.com/blader/humanizer">Humanizer skill</a> as style guidance. That does not make the manuscript human-authored or guarantee a detector result. Technical terms, examples and evidence take priority over style heuristics.</p><p>Instrument Serif is served locally under the SIL Open Font License. Its license is included at <a href="../assets/fonts/OFL.txt">assets/fonts/OFL.txt</a>. Other text uses system fonts.</p><p>This is an AI-assisted reading edition published by CTROTECH. Source and font notices are supplied with the edition. Original editorial rights are reserved unless the author selects different terms; upstream rights are not overridden. Expanded behavioral coverage and independent review remain open.</p></div></main>'
    write('reference/sources.html',shell('Sources and attribution',source_html,base='../'))


def status_page():
    evidence_path=R/'tests/release-evidence.json'
    evidence=json.loads(evidence_path.read_text()) if evidence_path.exists() else {'state':'Checks not run yet','results':[]}
    if evidence.get('publication_fingerprint')!=publication_fingerprint(R):evidence={'state':'No current evidence: content or build inputs changed after the recorded checks. Re-run verification.','results':[]}
    deployment_path=R/'tests/seo-verification.json'
    if deployment_path.exists():
        deployment=json.loads(deployment_path.read_text())
        if deployment.get('publication_fingerprint')==publication_fingerprint(R) and deployment.get('result')=='PASS':
            for row in deployment['checks']:
                scope='Generated artifacts/local HTTPS fixtures, not a hosted Vercel deployment. No ranking or independent content approval is implied.'
                if 'html_documents' in row:scope=f'{row["html_documents"]} output HTML documents; {row["indexed_pages"]} intended search landing pages in the synthetic production-origin test. Real canonical origins are resolved at deployment.'
                elif 'browsers' in row:scope='Local HTTPS flows in '+', '.join(b['engine']+' '+b['version'] for b in row['browsers'])+'. Not real-device or universal browser certification.'
                elif 'axe_version' in row:scope=f'{row["pages"]} representative pages, axe {row["axe_version"]}, zero automated violations. This is not WCAG or assistive-technology approval.'
                evidence['results'].append({'check':row['check'],'result':row['result'],'scope':scope})
    rows=''.join(f'<tr><th scope="row">{e(r["check"])}</th><td>{e(r["result"])}</td><td>{e(r["scope"])}</td></tr>' for r in evidence.get('results',[]))
    content='<main id="main" class="wrap"><div class="page-heading"><p class="eyebrow">Release evidence</p><h1>Checks, coverage and known limits.</h1><p>This page records executed checks, captured reference coverage and the work still open. Technical or independent approval is not inferred from a successful build.</p></div><div class="reference-body"><h2>Review position</h2><p>All 74 chapters have prose, one example and an explained exercise. The internal technical and answer-key review states remain open. Seven static projects and the index-derived reference are included. This is not a completed whole-Standard, member-level reference and has not received independent technical, accessibility, security or answer-key approval.</p><h2>Recorded build checks</h2><p>'+e(evidence['state'])+'</p><div class="reference-table"><table><caption>Build evidence for this reading edition</caption><thead><tr><th scope="col">Check</th><th scope="col">Result</th><th scope="col">What it covers</th></tr></thead><tbody>'+rows+'</tbody></table></div><h2>Work continuing beyond this edition</h2><ul><li>Independent chapter and explained-answer review against the actual normative definitions.</li><li>Expanded API behavior, algorithms, conversions and exceptions at the promised depth. The separate declaration register does not replace these explanations.</li><li>Complete keyword/value/default registries and excluded media/drag event inventories.</li><li>Full ARIA restrictions and accessibility mapping reconciliation.</li><li>Cross-browser and relevant assistive-technology checks, plus a security review of the delivered experience.</li><li>A tagged, accessibility-reviewed PDF workflow. The supplied PDF has selectable text, links and bookmarks, but is not claimed to be a tagged accessible PDF.</li><li>Remaining source attribution and technical approval. Hosting success does not close these content reviews.</li></ul><p>Browser smoke tests exercise this site and selected examples. They do not establish universal browser support. Nu tests document conformance for its recorded version, not complete accessibility or security.</p><h2>Your local data</h2><p>Theme, reading text size and marked chapters can be stored in this browser. No analytics or account service is included. <button type="button" data-clear-progress>Clear reading progress</button></p></div></main>'
    write('reference/status.html',shell('Review status',content,base='../'))


def reading_guide():
    content='<main id="main" class="wrap"><div class="page-heading"><p class="eyebrow">Read, test, explain</p><h1>Start here.</h1><p>'+inline(GUIDE['intro'])+'</p></div><div class="reference-body"><h2>Choose your route</h2>'
    for route in GUIDE['routes']:
        content+='<h3>'+e(route['title'])+'</h3><p>'+inline(route['text'])+'</p>'
        if route['chapters']:content+='<ul>'+''.join('<li><a href="chapters/'+f'{n:02}'+'.html">'+f'{n:02}'+'. '+e(BOOK[n-1]['title'])+'</a></li>' for n in route['chapters'])+'</ul>'
        else:content+='<p><a href="reference/index.html">Open the reference desk</a> or <a href="reference/api-members.html">browse the declaration register</a>.</p>'
    content+='<h2>One useful practice loop</h2><ol>'+''.join('<li><h3>'+e(step['title'])+'</h3><p>'+inline(step['text'])+'</p></li>' for step in GUIDE['practice'])+'</ol>'
    content+='<h2>Website, PDF and code</h2><p>'+inline(GUIDE['formats'])+'</p><p><a href="downloads/ctrotech-html-playbook.pdf">Download the PDF</a> · <a href="downloads/code-examples.zip" download>Get exact chapter code</a> · <a href="projects.html">Explore the seven projects</a></p><h2>Know what a source tells you</h2><p>'+inline(GUIDE['sources'])+'</p><h2>Scope of this edition</h2><p>'+inline(GUIDE['scope'])+'</p><h2 id="corrections">Help correct the book</h2><p>'+inline(GUIDE['corrections'])+'</p><p><a href="'+e(META['corrections_url'])+'">Report a content correction on GitHub</a>.</p><h2 id="edition-notes">October 2026 edition notes</h2><ul>'+''.join('<li>'+inline(note)+'</li>' for note in GUIDE['edition_notes'])+'</ul></div></main>'
    write('start.html',shell('Start here',content))


def about():
    content='<main id="main" class="wrap"><div class="page-heading"><p class="eyebrow">About the book</p><h1>Learn the document.<br>Then learn the edge cases.</h1><p>For people who want to explain their markup, not just copy a page that happens to render.</p></div><div class="reference-body"><h2>How to read it</h2><p>Follow the chapters for the curriculum. Each has objectives, an example, a mistake to consider and an exercise with an explained answer. <a href="start.html">Use the reading guide</a> to choose a route and a practice routine. Open the projects when you want a complete static folder to inspect.</p><h2>The writing standard</h2><p>The book uses plain language without treating browser behavior as simpler than it is. Standards requirements, authoring advice and implementation limits have different roles. Examples have a purpose and source links for further checking. Preparation was AI-assisted; the <a href="author.html">publication credits</a> record the author and preparation details.</p><h2 id="edition-scope">What this edition is</h2><p>'+inline(GUIDE['scope'])+'</p><p>The reference preserves captured element and attribute summaries, declaration signatures and source routes. A signature is not an explanation of every algorithm, exception or inherited member. The <a href="reference/status.html">scope and checks page</a> separates executed checks from the reviews still open.</p><h2>Website and PDF</h2><p>'+inline(GUIDE['formats'])+'</p><p>Syntax colouring helps distinguish parts of the source; it does not prove correctness. Wrapped examples are browser demonstrations, not application backends. External media examples require their own actual resources.</p><h2>Publication and corrections</h2><p>The maintained source is versioned in the <a href="https://github.com/ctrotech-tutor/playbook">author’s GitHub repository</a>. The public reading site is <a href="'+e(META['public_site_url'])+'">ctrobook.vercel.app</a>, served through Vercel. The author confirmed successful delivery on 14 October 2026; later editions still need their own deployment.</p><p><a href="start.html#edition-notes">Read the edition notes</a> or <a href="start.html#corrections">report a correction</a>. Public feedback must not contain private data or credentials.</p></div></main>'
    write('about.html',shell('About the book',content))


def author_page():
    content='<main id="main" class="wrap"><div class="page-heading"><p class="eyebrow">Author and publication credits</p><h1>'+e(META['author'])+'</h1><p>Author of <cite>'+e(META['title'])+'</cite>, published under the '+e(META['imprint'])+' brand.</p></div><div class="reference-body"><h2>The publication</h2><p>The book follows HTML from document structure to forms, browser behavior and multi-page projects. Its website and PDF use the same maintained chapter source.</p><h2>Edition and rights</h2><p>'+e(META['edition_label'])+' / 14 October 2026.</p><p>'+e(META['copyright_notice'])+'</p><p>'+e(META['reuse_license'])+'</p><h2>Credits</h2><p>Author: '+e(META['author'])+'. Publication brand: '+e(META['imprint'])+'. Syntax colouring is generated from Pygments tokens. The PDF keeps source code as selectable text, not screenshots.</p><p>Instrument Serif is included under the <a href="assets/fonts/OFL.txt">SIL Open Font License</a>. The PDF embeds DejaVu fonts; their <a href="assets/fonts/DejaVu-COPYRIGHT.txt">copyright and license notice</a> is included in the companion files and attached to the PDF. Reference material and external guidance retain their own source rights. See the <a href="reference/sources.html">source and attribution register</a>.</p><h2>Preparation and review</h2><p>'+e(META['preparation_note'])+'</p><p>The author has approved the visual direction. Full technical and coverage approval is a separate step. The <a href="reference/status.html">status page</a> records what has been tested and what remains open.</p></div></main>'
    write('author.html',shell('Author and credits',content))


def projects_page():
    text='<main id="main" class="wrap"><div class="page-heading"><p class="eyebrow">Build, compare, revise</p><h1>Seven projects.<br>Actual folders to inspect.</h1><p>Static reference implementations with local assets and explicit limitations. None is connected to a lending or application service.</p></div><div class="project-grid">'
    for c in BOOK[67:]:
        slug=c['project_slug'];text+=f'<article class="project-card"><p class="eyebrow">PROJECT {c["number"]-67:02} / CHAPTER {c["number"]}</p><h2>{e(c["title"].replace("Build ","").replace("Capstone: ",""))}</h2><p>{e(c["dek"])}</p><p><a href="chapters/{c["number"]:02}.html">Read the brief and rubric</a></p><a class="button" href="projects/{slug}/index.html">Open reference</a> <a class="button" href="downloads/project-{slug}.zip">Download files</a></article>'
    write('projects.html',shell('Reference projects',text+'</div></main>'))


def search_data():
    entries=[dict(title=f'{c["number"]:02}. {c["title"]}',text=c['dek']+' '+c['lesson']+' '+c['code'],path=f'chapters/{c["number"]:02}.html',kind='CHAPTER') for c in BOOK]
    entries.append(dict(title='Start here: reading guide and edition notes',text=GUIDE['intro']+' '+GUIDE['corrections'],path='start.html',kind='GUIDE'))
    for slug,title,_,keys in REFS:
        for key in keys:
            for r in INV[key]:entries.append(dict(title=r['name']+' / '+title,text=clean(r.get('description',r.get('scope',''))),path=f'reference/{slug}.html#{r["id"].replace(":","-")}',kind='REFERENCE'))
    api=json.loads((R/'content/api-register.json').read_text())
    for row in api['records']:entries.append(dict(title=row['name'],text=' '.join(m['name'] for m in row['members'])+' '+row['type'],path='reference/api/'+re.sub(r'[^a-z0-9]+','-',row['name'].lower()).strip('-')+'.html',kind='API'))
    for index,row in enumerate(api['keyword_records'],1):entries.append(dict(title=' / '.join(row['names'])+' / '+row['type'],text=' '.join(row['contexts'])+' '+row['section'],path='reference/keywords.html#'+row['id']+'-'+str(index),kind='DEFINITION'))
    write('assets/search.js','window.BOOK_SEARCH = '+json.dumps(entries,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')+';\n')


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--pdf',action='store_true');args=parser.parse_args()
    SITE.mkdir(parents=True,exist_ok=True)
    shutil.copytree(R/'assets',SITE/'assets',dirs_exist_ok=True)
    (SITE/'downloads').mkdir(exist_ok=True)
    with zipfile.ZipFile(SITE/'downloads/code-examples.zip','w',zipfile.ZIP_DEFLATED) as archive:
        for c in BOOK:archive.writestr(f'example-{c["number"]:02}.html',c['code'].encode('utf-8'))
        archive.writestr('README.md',f'# CTROTECH / Exact chapter code\n\nBy {META["author"]}. {META["edition_label"]}.\n\nThese 74 files preserve the exact UTF-8 code in content/chapters.json. Some are HTML fragments. Insert fragments in a complete UTF-8 HTML document before running them. External media, modules and server handlers may be reader-supplied; read the chapter explanation. File numbering matches chapter numbering. Wrapped browser examples and the seven complete projects are separate downloads.\n\n{META["copyright_notice"]}\n{META["reuse_license"]}\n')
    write('.nojekyll','');write('assets/favicon.svg','<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="8" fill="#234d42"/><text x="32" y="41" text-anchor="middle" fill="#faf8f1" font-size="26" font-family="monospace">CT</text></svg>')
    home();[chapter(c) for c in BOOK];references();
    from api_reference import build_api
    build_api(R,write,shell)
    about();reading_guide();author_page();search_data();status_page()
    from projects import build_projects
    build_projects(R,SITE);projects_page()
    if args.pdf:
        from pdf import build_pdf
        build_pdf(R,SITE,BOOK,INV)
    elif (R/'deliverables/ctrotech-html-playbook.pdf').exists():shutil.copy2(R/'deliverables/ctrotech-html-playbook.pdf',SITE/'downloads/ctrotech-html-playbook.pdf')
    write('build-inputs.json',json.dumps(input_manifest(R),indent=2)+'\n')
    print(f'Built {len(list(SITE.rglob("*.html")))} HTML files from {len(BOOK)} chapters.')
if __name__=='__main__':main()
