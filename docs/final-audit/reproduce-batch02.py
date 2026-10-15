"""Run from the installed candidate checkout after tools/build.py --pdf.
Tests DOM behavior, not assistive-technology output or comprehensive feature coverage.
"""
from pathlib import Path
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from threading import Thread
from urllib.parse import urlsplit
import functools, hashlib, json, subprocess, sys
from playwright.sync_api import sync_playwright
R=Path.cwd(); O=Path(__file__).resolve().parent
sys.path.insert(0,str(R/'tools'))
from fingerprint import publication_fingerprint
F=O/'batch02-fixtures'; F.mkdir(exist_ok=True)
def fixture(name,body,head=''):
    p=F/(name+'.html')
    p.write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Audit '+name+'</title>'+head+'</head><body>'+body+'</body></html>')
    return p
fixture('text','<hgroup><h1>Library membership</h1><p>A place for every reader</p></hgroup><p>A <dfn>loan period</dfn> is the time before an item is due back.</p><p>Hypertext Markup Language (<abbr title="Hypertext Markup Language">HTML</abbr>)</p><p><var>x</var><sup>2</sup>; H<sub>2</sub>O</p><pre id="direct">\nfirst\nsecond</pre><pre id="nested"><code>\nfirst</code></pre><p id="break">catalogue<wbr>reference</p><p><bdi>مريم</bdi></p><p><bdo dir="rtl">abc</bdo></p><p><ruby>漢<rp>(</rp><rt>かん</rt><rp>)</rp></ruby></p>')
fixture('base','<h1>Resolution test</h1><a id="fragment" href="#fees">Fees</a><a id="relative" href="../index.html">Book</a><a id="root" href="/index.html">Origin</a><p id="fees">Current document fees</p>','<base href="https://example.invalid/book/pages/contact.html">')
fixture('lists','<h1>Commands and descriptions</h1><menu><li><button type="button">Copy</button></li><li><button type="button">Paste</button></li></menu><dl><div><dt>Saturday</dt><dd><p>10:00 to 14:00</p><p>Desk closes at 13:45.</p></dd></div></dl><ol reversed><li>First</li><li value="7">Second</li><li>Third</li></ol>')
fixture('table','<h1>Lending</h1><table><caption>Periods</caption><colgroup><col><col></colgroup><thead><tr><th id="collection" scope="col">Collection</th><th id="days" scope="col">Days</th></tr></thead><tbody><tr><th id="general" scope="row" rowspan="0">General</th><td headers="general days">14</td></tr><tr><td id="renewal" headers="general days">7</td></tr></tbody></table>')
fixture('heading-offset','<h1>Title</h1><h2>Overview</h2><section headingoffset="1"><h2>Offset subsection</h2><div headingreset><h2>Reset subsection</h2></div></section>')
# Deliberate invalid authoring examples are isolated, never shipped as manuscript examples.
fixture('invalid-edit','<h1>Invalid edit timestamp</h1><p><ins datetime="10:00">New opening time</ins></p>')
fixture('invalid-columns','<h1>Invalid column group</h1><table><colgroup span="2"><col></colgroup><tr><th scope="col">One</th><th scope="col">Two</th></tr><tr><td>A</td><td>B</td></tr></table>')
class Handler(SimpleHTTPRequestHandler):
    def translate_path(self,path):
        p=urlsplit(path).path
        if p.startswith('/fixtures/'):return str(F/p.removeprefix('/fixtures/'))
        return str(R/'build/site'/p.lstrip('/'))
    def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
Thread(target=server.serve_forever,daemon=True).start()
base='http://127.0.0.1:'+str(server.server_port)
rows=[]
try:
 with sync_playwright() as pw:
  for engine in ['chromium','firefox','webkit']:
   browser=getattr(pw,engine).launch(args=['--no-sandbox'] if engine=='chromium' else [])
   page=browser.new_page(); checked=[]
   for n in range(14,28):
    response=page.goto(base+f'/examples/{n:02}.html',wait_until='load');assert response.status==200
    assert page.locator('html').get_attribute('lang')=='en'
    assert page.locator('body').inner_text().strip()
    checked.append(n)
    if n==17:
     page.get_by_role('link',name='Read the membership fees').click()
     assert page.url.endswith('#fees') and page.locator('#fees').count()==1
    if n==19:
     page.wait_for_function('()=>document.querySelector("img").complete');assert page.locator('img').evaluate('(x)=>x.naturalWidth===640 && x.naturalHeight===360')
    if n==21:assert page.locator('bdi').inner_text()=='مريم'
    if n==22:assert page.locator('a[href^="tel:"]').count()==0
    if n==25:
     page.get_by_role('link',name='Skip to main content').focus();page.keyboard.press('Enter')
     assert page.evaluate('document.activeElement.id')=='main-content'
    if n==26:
     assert page.locator('#period-days').inner_text()=='Days'
     assert page.locator('#collection-general').inner_text()=='General lending'
   page.goto(base+'/fixtures/text.html')
   assert page.locator('#direct').text_content()=='first\nsecond'
   assert page.locator('#nested').text_content()=='\nfirst'
   assert page.locator('#break').text_content()=='cataloguereference'
   assert page.locator('bdi').evaluate('(e)=>getComputedStyle(e).direction')=='rtl'
   assert page.locator('bdo').evaluate('(e)=>getComputedStyle(e).direction')=='rtl'
   assert page.locator('ruby rt').text_content()=='かん'
   page.goto(base+'/fixtures/base.html')
   urls=page.locator('a').evaluate_all('(a)=>a.map(x=>({raw:x.getAttribute("href"),resolved:x.href}))')
   assert [v['resolved'] for v in urls]==['https://example.invalid/book/pages/contact.html#fees','https://example.invalid/book/index.html','https://example.invalid/index.html']
   page.goto(base+'/fixtures/lists.html')
   assert page.locator('menu > li > button').count()==2
   assert page.locator('dl > div > dd p').count()==2
   assert page.locator('ol').evaluate('(x)=>x.reversed') is True
   assert page.locator('ol li').nth(1).evaluate('(x)=>x.value')==7
   page.goto(base+'/fixtures/table.html')
   table=page.evaluate('''()=>({rowSpan:document.querySelector('#general').rowSpan,index:document.querySelector('#renewal').cellIndex,headers:[...document.querySelectorAll('td[headers]')].map(x=>x.headers.split(/\\s+/).every(id=>{const h=document.getElementById(id);return h?.localName==='th'&&h.closest('table')===x.closest('table')}))})''')
   assert table=={'rowSpan':0,'index':0,'headers':[True,True]}
   page.goto(base+'/fixtures/heading-offset.html')
   reflection=page.evaluate('''()=>({headingOffsetProperty:'headingOffset' in HTMLElement.prototype,headingResetProperty:'headingReset' in HTMLElement.prototype,sourceAttributesRetained:document.querySelector('section').getAttribute('headingoffset')==='1'})''')
   ax=None
   if engine=='chromium':
    session=page.context.new_cdp_session(page)
    nodes=session.send('Accessibility.getFullAXTree')['nodes']
    ax=[{'name':v.get('name',{}).get('value'),'level':next((p['value'].get('value') for p in v.get('properties',[]) if p['name']=='level'),None)} for v in nodes if v.get('role',{}).get('value')=='heading']
   # Do not assert cross-browser outline support from DOM reflection or Playwright's own role algorithm.
   reflow=[]
   page.set_viewport_size({'width':320,'height':800})
   for n in range(14,28):
    page.goto(base+f'/chapters/{n:02}.html',wait_until='load')
    assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+1'),(engine,n)
    assert page.locator('[data-open-lab]').count()==1
    reflow.append(n)
   rows.append({'engine':engine,'version':browser.version,'primary_examples_loaded':checked,'chapter_reflow_at_320px':reflow,'assertions':['native fragment navigation','native skip-link focus','Arabic character-reference text','absence of dialable teaching placeholder','pre immediate-newline stripping versus nested code','wbr does not insert text','bdi automatic RTL and bdo explicit RTL CSS direction','ruby annotation DOM text','base/relative/root href resolution','command/list-group DOM shape and list IDL values','rowspan zero reflection, headers same-table targets and cellIndex'], 'chapter19_image':'Supplied original fictional SVG loaded at 640 by 360; visual/alternative comparison is a same-agent check, not independent image-accessibility approval.','heading_offset_observation':reflection,'chromium_cdp_heading_levels':ax,'heading_offset_scope':'Reflection and Chromium CDP observations only. Firefox/WebKit accessibility trees, OS assistive technology and full offset algorithm coverage were not tested.'})
   browser.close()
finally:server.shutdown();server.server_close()
jar=R/'.cache/vnu/vnu.jar';nu=[]
for p in sorted(F.glob('*.html')):
 proc=subprocess.run(['java','-Xss4m','-jar',str(jar),'--format','json',str(p)],capture_output=True,text=True,timeout=60)
 output=json.loads(proc.stderr or proc.stdout)
 errors=[m for m in output.get('messages',[]) if m.get('type')=='error']
 expected_invalid=p.name.startswith('invalid-')
 assert bool(errors)==expected_invalid,(p.name,output)
 nu.append({'fixture':p.name,'expected_invalid':expected_invalid,'exit_code':proc.returncode,'messages':output.get('messages',[]),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
report={'date':'2026-10-15','candidate_fingerprint':publication_fingerprint(R),'result':'PASS','browsers':rows,'fixture_conformance':nu,'limits':['No independent exercise-key review','No OS assistive-technology run','No universal compatibility claim','No manual linguistic review','No exhaustive API conversion/exception/default coverage','No independent review of CH19 image/alternative','These fixtures do not replace a full security or accessible-PDF review']}
(O/'batch02-browser-checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('PASS: CH14–27 scoped DOM/navigation/reflow checks in three engines; five conforming and two expected-invalid fixtures.')
