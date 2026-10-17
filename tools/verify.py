#!/usr/bin/env python3
"""Executed publication checks, deliberately narrower than whole-book approval."""
from pathlib import Path
from datetime import datetime,timezone
from urllib.parse import urlparse,unquote,urlsplit
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from threading import Thread
from playwright.sync_api import sync_playwright,expect
from bs4 import BeautifulSoup
import collections,functools,hashlib,json,os,re,subprocess,zipfile
import pymupdf
from fingerprint import publication_fingerprint
from check_syntax import check as check_syntax
R=Path(__file__).resolve().parents[1];SITE=R/'build/site';CACHE=R/'.cache';CACHE.mkdir(exist_ok=True)
book=json.loads((R/'content/chapters.json').read_text());meta=json.loads((R/'content/publication.json').read_text());results=[]
def passed(check,scope,**details):results.append({'check':check,'result':'PASS','scope':scope,**details})

class Handler(SimpleHTTPRequestHandler):
    def translate_path(self,path):
        clean=urlsplit(path).path
        if clean.startswith('/review-repo/'):clean=clean[len('/review-repo/'):]
        else:clean=clean.lstrip('/')
        return str(SITE/clean)
    def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),Handler);thread=Thread(target=server.serve_forever,daemon=True);thread.start()
base=f'http://127.0.0.1:{server.server_port}/review-repo/'

# Full built-doc conformance. The caller installs a known Nu version separately.
jar=CACHE/'vnu/vnu.jar'
assert jar.exists(),'Install the recorded Nu jar before running full verification.'
assert hashlib.sha256(jar.read_bytes()).hexdigest()==json.loads((R/'tests/nu-download-provenance.json').read_text())['sha256'],'Nu checker does not match the recorded provenance.'
version=subprocess.check_output(['java','-jar',str(jar),'--version'],text=True).strip()
cmd=['java','-Dnu.validator.servlet.allow-forbidden-hosts=true','-Xss4m','-jar',str(jar),'--format','json','--skip-non-html']+[base+p.relative_to(SITE).as_posix() for p in sorted(SITE.rglob('*.html'))]
nu=subprocess.run(cmd,capture_output=True,text=True,timeout=180);raw=nu.stderr or nu.stdout
(R/'tests/nu-full-result.json').write_text(raw);nu_json=json.loads(raw)
assert nu.returncode==0 and not nu_json.get('messages'),raw[:3000]
count=len(list(SITE.rglob('*.html')))
passed('Built HTML conformance',f'{count} HTTP-served built documents, including 74 wrapped examples and all seven project folders; Nu {version}.',version=version,files=count,messages=0,jar_sha256=hashlib.sha256(jar.read_bytes()).hexdigest())
negative=R/'tests/fixtures/invalid-interactive-nesting.html';negative.parent.mkdir(exist_ok=True)
negative.write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Expected invalid fixture</title></head><body><h1>Expected failure</h1><button type="button"><a href="next.html">Nested link</a></button></body></html>')
fail=subprocess.run(['java','-Xss4m','-jar',str(jar),'--format','json',str(negative)],capture_output=True,text=True,timeout=60)
failure=json.loads(fail.stderr or fail.stdout);assert fail.returncode!=0 and any(x.get('type')=='error' for x in failure['messages'])
(R/'tests/nu-expected-failure.json').write_text(json.dumps(failure,indent=2));passed('Expected-failure check','The same checker rejects the deliberately invalid interactive-nesting fixture.')

# Source structure and complete static graph. Standalone media/resource examples intentionally
# refer to resources the reader must supply; they are not treated as functioning asset demos.
assert [c['number'] for c in book]==list(range(1,75))
for c in book:
    for f in ['title','dek','lesson','code','explanation','mistake','question','answer','objectives','sources']:assert c.get(f),(c['id'],f)
    assert '\u2014' not in json.dumps(c,ensure_ascii=False),c['id']
    assert not re.search(r'\b(TODO|TBD|lorem ipsum)\b',c['lesson'],re.I),c['id']
    assert c['editorial_status']=='draft_for_review'
passed('Manuscript structure','74 populated chapter records with open independent review, 74 explained exercises, no em dashes in authored chapter data; no independent answer correctness approval is implied.',chapters=74,exercises=74)
link_errors=[];checked_links=0;docs={}
for p in SITE.rglob('*.html'):docs[p.resolve()]=BeautifulSoup(p.read_text(),'html5lib')
for path,soup in docs.items():
    if 'examples' in path.relative_to(SITE.resolve()).parts:continue
    ids=[x['id'] for x in soup.select('[id]')];assert len(ids)==len(set(ids)),str(path)
    for node,attr in [(n,'href') for n in soup.select('[href]')]+[(n,'src') for n in soup.select('[src]')]:
        url=node.get(attr,'');u=urlparse(url)
        if u.scheme or url.startswith('//') or not url:continue
        if url.startswith('/'):link_errors.append((str(path),url,'root-relative path'));continue
        target=(path.parent/unquote(u.path)).resolve() if u.path else path
        if target.is_dir():target/= 'index.html'
        checked_links+=1
        if not target.exists():link_errors.append((str(path),url,'missing file'))
        elif u.fragment and target.suffix=='.html' and target in docs and not docs[target].find(id=unquote(u.fragment)):link_errors.append((str(path),url,'missing fragment'))
assert not link_errors,link_errors[:20]
passed('Internal links and assets',f'{checked_links} relative destinations checked across book/reference/project pages. Standalone media examples are excluded from resource-existence claims.',destinations=checked_links)
for zpath in (SITE/'downloads').glob('project-*.zip'):
    with zipfile.ZipFile(zpath) as z:assert z.testzip() is None;assert any(n.endswith('index.html') for n in z.namelist())
assert len(list((SITE/'downloads').glob('project-*.zip')))==7
passed('Project downloads','All seven ZIPs pass integrity checks and contain a standalone index document.')

pdf=pymupdf.open(R/'deliverables/ctrotech-html-playbook.pdf');assert pdf.metadata['author']==meta['author'];alltext=' '.join(page.get_text() for page in pdf)
for c in book:assert c['title'] in alltext or re.sub(r'\s+',' ',c['title']) in re.sub(r'\s+',' ',alltext),c['title']
assert len(pdf.get_toc())>=74
guide=json.loads((R/'content/reading-guide.json').read_text())
normal=lambda value:re.sub(r'\s+',' ',value).strip()
guide_html=BeautifulSoup((SITE/'start.html').read_text(),'html.parser').get_text(' ',strip=True)
for value in [guide['intro'],guide['formats'],guide['sources'],guide['scope'],guide['corrections']]+[r['text'] for r in guide['routes']]+[r['text'] for r in guide['practice']]+guide['edition_notes']:
    assert normal(value.replace('`','')) in normal(guide_html),value
    assert re.sub(r'\s+','',value.replace('`','')) in re.sub(r'\s+','',alltext),value
assert any(row[1]=='Start here: a reading guide' for row in pdf.get_toc())
passed('Reading guide and edition consistency','Shared reading routes, practice routine, scope, corrections and edition notes appear in both HTML and selectable PDF text. Independent review states are unchanged.')
syntax=check_syntax()
(R/'tests/syntax-verification.json').write_text(json.dumps(syntax,indent=2)+'\n')
passed('Syntax and author credits','74 selectable, token-coloured PDF examples; exact website/code downloads; author credit and PDF metadata. Token contrast and synthetic multi-page wrapping checked; this is not an accessibility certification.',**syntax)

outliers=[]
for n,page in enumerate(pdf):
    for block in page.get_text('blocks'):
        if block[0]<30 or block[2]>page.rect.width-25 or block[3]>page.rect.height-17:outliers.append((n+1,block[:4],block[4][:100]))
assert not outliers,outliers[:10]
from pdf import verify_primary_pdf
verify_primary_pdf(R)
passed('PDF integrity and text layout',f'{len(pdf)} pages; all chapter titles found; {len(pdf.get_toc())} bookmarks; text bounds checked. Semantically tagged; the separate exact-artifact PDF/UA-1 validation report is checked. Not independently accessibility-audited.',pages=len(pdf),bookmarks=len(pdf.get_toc()))

# Serve beneath a repository prefix to test GitHub Pages path behavior.
errors=[];failures=[];network=[];browser_rows=[]
try:
    with sync_playwright() as p:
        browser=p.chromium.launch(args=['--no-sandbox']);browser_version=browser.version
        ctx=browser.new_context(viewport={'width':1440,'height':1100},permissions=['clipboard-read','clipboard-write'])
        page=ctx.new_page();page.on('pageerror',lambda x:errors.append(str(x)));page.on('response',lambda r:failures.append(r.url) if r.status>=400 else None);page.on('request',lambda r:network.append(r.url) if r.url.startswith('http') and not r.url.startswith(base) else None)
        page.goto(base,wait_until='networkidle');page.evaluate('document.fonts.ready');assert page.title().startswith('The book');assert meta['author'] in page.locator('.author-line').inner_text();assert page.locator('meta[name=author]').get_attribute('content')==meta['author']
        page.keyboard.press('Tab');assert page.locator(':focus').inner_text()=='Skip to main content';browser_rows.append('Skip link is first keyboard destination')
        page.keyboard.press('Control+k');assert page.locator('#search-dialog').is_visible();page.locator('#book-search').fill('selectedcontent');assert page.locator('#search-results li').count()>0
        page.keyboard.press('Escape');page.locator('#search-dialog').wait_for(state='hidden');browser_rows.append('Keyboard search opens, finds content and closes with Escape')
        page.screenshot(path=str(CACHE/'home-desktop.png'),full_page=False)
        page.goto(base+'chapters/34.html',wait_until='networkidle');assert page.locator('[aria-current=page]').count()==1
        page.locator('[data-mark-read]').click();assert page.locator('[data-mark-read]').get_attribute('aria-pressed')=='true'
        page.reload();assert page.locator('[data-mark-read]').get_attribute('aria-pressed')=='true';browser_rows.append('Reading progress persists across reload')
        page.locator('[data-theme-toggle]:visible').click();assert page.locator('body').get_attribute('data-theme')=='night';page.reload();assert page.locator('body').get_attribute('data-theme')=='night';page.locator('[data-theme-toggle]:visible').click();browser_rows.append('Theme preference persists without an account')
        page.locator('[data-copy]').click();expect(page.locator('[data-copy]')).to_have_text(re.compile('Copied|Select and copy'));assert page.evaluate('navigator.clipboard.readText()')==book[33]['code'];browser_rows.append('Copy control copies the exact canonical code to the clipboard')
        page.locator('[data-open-lab]').click();assert page.locator('#lab-dialog').is_visible();page.locator('#lab-code').fill('<!doctype html><html lang="en"><title>Test</title><h1>Edited locally</h1></html>');page.locator('#lab-run').click();frame=page.frame_locator('#lab-output');expect(frame.locator('h1')).to_have_text('Edited locally');assert page.locator('#lab-output').get_attribute('sandbox')=='allow-scripts';page.locator('[data-close-dialog="lab-dialog"]').click();browser_rows.append('Editable example renders in a script-only isolated sandbox')
        page.evaluate('window.scrollTo(0,0)');page.screenshot(path=str(CACHE/'chapter-desktop.png'),full_page=False)
        page.goto(base+'reference/elements.html',wait_until='networkidle');page.locator('#reference-search').fill('selectedcontent');assert page.locator('[data-reference-entry]:visible').count()==1;browser_rows.append('Element reference filters to the requested feature')
        page.goto(base+'projects/registration/index.html',wait_until='networkidle');posted=[];page.on('request',lambda r:posted.append(r.method) if r.method=='POST' else None)
        page.locator('#demo-name').fill('Example Reader');page.locator('#demo-email').fill('reader@example.invalid');page.locator('#demo-session').select_option('morning');page.locator('button[type=submit]').click();assert 'No application was sent' in page.locator('#demo-result').inner_text();assert not posted;browser_rows.append('Demonstration form validates locally without POST or collection')
        for example,selector,expected in [(3,'#opening','Open Tuesday to Saturday.'),(46,'#book-results h2','Local histories'),(56,'#status-message','Catalogue view ready.'),(63,'#reader-comment','<script>')]:
            # Example 3 is file-free; these examples make no resource requests.
            page.goto(base+f'examples/{example:02}.html',wait_until='load');assert expected in page.locator(selector).inner_text()
        page.goto(base+'examples/44.html',wait_until='load');page.locator('#open-help').click();assert page.locator('#help-dialog').evaluate('(d)=>d.open');page.locator('#help-dialog button').click();assert not page.locator('#help-dialog').evaluate('(d)=>d.open');browser_rows.append('Selected live examples: DOM updates, templates, lifecycle, text insertion and native dialog close path')
        page.goto(base+'examples/21.html');assert page.locator('bdi').inner_text()=='مريم';browser_rows.append('Numeric character references render the intended Arabic name inside bdi')
        page.goto(base+'examples/53.html');assert page.locator('#nickname').input_value()=='Ada';assert page.locator('#nickname').get_attribute('value')=='Guest';browser_rows.append('Input current-value/default-attribute distinction executed')
        page.goto(base+'chapters/44.html',wait_until='networkidle');page.screenshot(path=str(CACHE/'syntax-desktop.png'),full_page=True)
        page.set_viewport_size({'width':390,'height':844});overflow=[]
        mobile_paths=['author.html','index.html','contents.html','projects.html','about.html','reference/index.html','reference/attributes.html','reference/sources.html']+[f'chapters/{n:02}.html' for n in range(1,75)]
        for path in mobile_paths:
            page.goto(base+path,wait_until='load')
            if page.evaluate('document.documentElement.scrollWidth>innerWidth+1'):overflow.append(path)
        assert not overflow,overflow
        page.goto(base+'chapters/34.html');page.locator('[data-chapters-toggle]').click();assert page.locator('#chapter-navigation').is_visible();assert page.locator('[data-chapters-toggle]').get_attribute('aria-expanded')=='true';page.locator('[data-chapters-toggle]').click();browser_rows.append('Mobile chapter navigation opens and closes with represented state')
        page.evaluate('window.scrollTo(0,0)');page.screenshot(path=str(CACHE/'chapter-mobile.png'),full_page=False)
        page.goto(base+'author.html',wait_until='networkidle');page.screenshot(path=str(CACHE/'author-mobile.png'),full_page=False)
        page.goto(base,wait_until='networkidle');page.screenshot(path=str(CACHE/'home-mobile.png'),full_page=False)
        browser_rows.append(f'No page-level horizontal overflow at 390px across {len(mobile_paths)} representative/all-chapter pages')
        assert not errors,errors;assert not failures,failures;assert not network,network
        browser_rows.append('No JavaScript errors, failed main-site requests or third-party requests in this test sequence')
        browser.close()
finally:server.shutdown();server.server_close()
passed('Browser smoke tests',f'{len(browser_rows)} checks using Chromium {browser_version}; desktop and 390px mobile, served under /review-repo/. No general cross-browser or assistive-technology claim.',details=browser_rows,browser_version=browser_version)
citations=json.loads((R/'tests/citation-checks.json').read_text());assert citations['checked']==citations['passed'];passed('Citation targets',f'{citations["passed"]} HTTP/document/fragment targets resolved. This verifies links, not the correctness of every cited assertion.')
output={'publication_fingerprint':publication_fingerprint(R),'edition':meta['edition'],'review_date':datetime.now(timezone.utc).date().isoformat(),'state':'Executed checks passed; independent content and whole-Standard coverage approval remain open','results':results,'not_certified':['Independent technical or answer-key correctness','Whole-Standard API/member/value completeness','Universal browser compatibility','WCAG conformance or complete assistive-technology behavior','Complete security review','Independent PDF accessibility and actual assistive-technology approval','Legal certification or hosted deployment verification of this rebuilt edition']}
(R/'tests/release-evidence.json').write_text(json.dumps(output,indent=2)+'\n')
print(json.dumps(output,indent=2))
