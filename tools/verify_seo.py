#!/usr/bin/env python3
"""Validate the actual Vercel output, deployment modes and selected browser flows.
Local header/routing emulation is not a hosted Vercel deployment test.
"""
from pathlib import Path
from urllib.parse import urlparse,unquote
from xml.etree import ElementTree as ET
from playwright.sync_api import sync_playwright,expect
from bs4 import BeautifulSoup
import hashlib,json,os,re,select,subprocess,time,functools,sys
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from threading import Thread
from fingerprint import publication_fingerprint
R=Path(__file__).resolve().parents[1];D=R/'dist';NODE=os.environ.get('NODE_BINARY','node')
META=json.loads((R/'content/publication.json').read_text());BOOK=json.loads((R/'content/chapters.json').read_text());API=json.loads((R/'content/api-register.json').read_text())
report={'publication_fingerprint':publication_fingerprint(R),'scope':'Generated SEO, static routing/header emulation, selected desktop/mobile browser flows and automated accessibility checks. Not a real Vercel deployment, independent content review or WCAG certification.','node':subprocess.check_output([NODE,'--version'],text=True).strip(),'checks':[]}
def passed(name,**details):report['checks'].append({'check':name,'result':'PASS',**details})
def build(mode,origin='',extra=None,fail=False):
    env=os.environ.copy()
    for key in ['SITE_URL','VERCEL_ENV','VERCEL_PROJECT_PRODUCTION_URL','DEPLOY_ENV','GOOGLE_SITE_VERIFICATION','BING_SITE_VERIFICATION','YANDEX_SITE_VERIFICATION','PINTEREST_SITE_VERIFICATION','INDEXNOW_KEY']:env.pop(key,None)
    env.update(DEPLOY_ENV=mode,SEO_TEST_MODE='1')
    if origin:env['SITE_URL']=origin
    env.update(extra or {})
    p=subprocess.run([NODE,'deploy/build.mjs'],cwd=R,env=env,text=True,capture_output=True,timeout=90)
    if fail:assert p.returncode!=0,p.stdout
    else:assert p.returncode==0,p.stdout+p.stderr
    return p
build('production',fail=True);build('production','http://book.example.test',fail=True);build('production','https://book.example.test/unwanted/path',fail=True)
passed('Missing and invalid production origins fail closed')
build('development');local=BeautifulSoup((D/'index.html').read_text(),'html.parser');assert local.select_one('meta[name=robots]')['content']=='noindex, follow';assert not local.select_one('link[rel=canonical]');assert '<loc>' not in (D/'sitemap.xml').read_text()
passed('Unconfigured local build emits no invented canonicals and is not indexable')
build('preview',extra={'VERCEL_PROJECT_PRODUCTION_URL':'book.example.test'})
preview=BeautifulSoup((D/'index.html').read_text(),'html.parser');assert preview.select_one('link[rel=canonical]')['href']=='https://book.example.test/';assert preview.select_one('meta[name=robots]')['content']=='noindex, follow';assert 'Disallow: /' in (D/'robots.txt').read_text();assert '<loc>' not in (D/'sitemap.xml').read_text()
passed('Preview keeps production canonical but noindex directives and an empty sitemap')
ORIGIN='https://book.example.test'
build('production',ORIGIN,{'GOOGLE_SITE_VERIFICATION':'fixture_google_token','BING_SITE_VERIFICATION':'fixture_bing_token','INDEXNOW_KEY':'fixture-indexnow-key-123'})
assert (D/'fixture-indexnow-key-123.txt').read_text()=='fixture-indexnow-key-123'
assert BeautifulSoup((D/'index.html').read_text(),'html.parser').select_one('meta[name=google-site-verification]')['content']=='fixture_google_token'
# Do not leave synthetic verification tokens in the final validation build.
build('production',ORIGIN)
passed('Optional verification and IndexNow key files are generated only from supplied values; no submission made')
html=list(D.rglob('*.html'));fragments=[];docs={};seen_titles={};indexed=[];links=0;structured=0
for p in html:
    file=p.relative_to(D).as_posix();doc=BeautifulSoup(p.read_text(),'html5lib');docs[p.resolve()]=doc
    assert doc.html.get('lang')=='en',file
    assert len(doc.select('head > title'))==1,file
    for name in ['description','author','robots','googlebot','DC.title','DC.creator','DC.rights']:
        assert len(doc.select(f'meta[name="{name}"]'))==1,(file,name)
    assert doc.select_one('meta[name=author]')['content']==META['author']
    assert len(doc.select('link[rel=canonical]'))==1,file
    canonical=doc.select_one('link[rel=canonical]')['href'];assert canonical.startswith(ORIGIN+'/') and '.html' not in urlparse(canonical).path,(file,canonical)
    assert doc.select_one('meta[property="og:url"]')['content']==canonical
    for name in ['og:title','og:description','og:image','og:image:alt','og:image:width','og:image:height']:
        assert len(doc.select(f'meta[property="{name}"]'))==1,(file,name)
    assert doc.select_one('meta[name="twitter:card"]')['content']=='summary_large_image'
    index='noindex' not in doc.select_one('meta[name=robots]')['content']
    if index:
        title=doc.select_one('head > title').get_text();assert title not in seen_titles,(file,seen_titles.get(title));seen_titles[title]=file;indexed.append(canonical)
        scripts=doc.select('script[type="application/ld+json"]');assert len(scripts)==1,file
        graph=json.loads(scripts[0].string)['@graph'];types={r['@type'] for r in graph};assert {'Person','Organization','WebSite','Book'}<=types,file
        assert next(r for r in graph if r['@type']=='Person')['name']==META['author']
        assert not any('aggregateRating' in r or 'reviewedBy' in r or 'sameAs' in r for r in graph)
        structured+=1
    if file.startswith('examples/') or file.startswith('projects/'):
        assert not index
        # Teaching examples intentionally refer to reader-supplied media/modules.
        nodes=doc.head.select('[href],[src]')
    else:nodes=doc.select('[href],[src],[poster]')
    for node in nodes:
        for attr in ['href','src','poster']:
            value=node.get(attr)
            if not value:continue
            u=urlparse(value)
            if u.scheme and not value.startswith(ORIGIN):continue
            if value.startswith('//'):raise AssertionError((file,'Protocol-relative URL',value))
            if value.startswith('#'):
                if value!='#':assert doc.find(id=unquote(value[1:])),(file,value)
                continue
            path=u.path
            if file.startswith('examples/') and path.startswith('/examples/'):continue
            assert path.startswith('/'),(file,'Non-root deployment path',value)
            target=D/unquote(path.lstrip('/'))
            if target.is_dir() and (target/'index.html').is_file():target/='index.html'
            if not target.is_file() and target.suffix!='.html' and (Path(str(target)+'.html')).exists():target=Path(str(target)+'.html')
            assert target.is_file(),(file,value,str(target))
            if u.fragment and target.suffix=='.html':fragments.append((file,target.resolve(),unquote(u.fragment)))
            links+=1
for file,target,fragment in fragments:assert docs[target].find(id=fragment),(file,target,fragment)
for c in BOOK:
    p=D/'chapters'/f'{c["number"]:02}.html';assert docs[p.resolve()].select_one('#chapter-code').get_text()==c['code']
    assert (D/'code'/f'{c["number"]:02}.html.txt').read_bytes()==c['code'].encode('utf-8')
for owner in API['records']:
    slug=re.sub(r'[^a-z0-9]+','-',owner['name'].lower()).strip('-');p=D/'reference/api'/f'{slug}.html'
    assert docs[p.resolve()].select_one('.idl-source code').get_text()=='\n\n'.join(owner['definitions']),owner['name']
xml=ET.parse(D/'sitemap.xml');sitemap=[x.text for x in xml.findall('{*}url/{*}loc')];assert sorted(sitemap)==sorted(indexed)
assert len(sitemap)==len(set(sitemap));assert len(html)==497 and len(indexed)>400
for file in (D/'assets').rglob('*'):
    if file.is_file():assert re.search(r'\.[a-f0-9]{12}\.[a-z0-9]+$',file.name),file.name
manifest=json.loads((D/'site.webmanifest').read_text());assert len(manifest['icons'])==2 and all((D/icon['src'].lstrip('/')).exists() for icon in manifest['icons'])
ET.parse(D/'feed.xml')
robots=(D/'robots.txt').read_text();assert 'Sitemap: '+ORIGIN+'/sitemap.xml' in robots;assert 'User-agent: OAI-SearchBot\nAllow: /' in robots and 'User-agent: GPTBot\nDisallow: /' in robots
assert META['author'] in (D/'llms.txt').read_text() and len(list((D/'markdown').glob('chapter-*.md')))==74
pdf=D/'downloads/ctrotech-html-playbook.pdf';assert pdf.read_bytes()==(R/'deliverables/ctrotech-html-playbook.pdf').read_bytes()
passed('All output HTML metadata, unique indexed titles, real-target links, canonical routes, structured data, sitemaps, hashed assets and text exports',html_documents=len(html),indexed_pages=len(indexed),internal_destinations=links,structured_data_pages=structured,markdown_chapters=74,api_owner_pages=len(API['records']),pdf_sha256=hashlib.sha256(pdf.read_bytes()).hexdigest(),canonical_test_origin=ORIGIN+' (synthetic test fixture only)')

# Validate the actual generated documents over an explicit-root HTTP fixture.
class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self,*args):pass
nu_server=ThreadingHTTPServer(('127.0.0.1',0),functools.partial(QuietHandler,directory=str(D)))
Thread(target=nu_server.serve_forever,daemon=True).start()
try:
    jar=R/'.cache/vnu/vnu.jar';assert jar.exists()
    command=['java','-Dnu.validator.servlet.allow-forbidden-hosts=true','-Xss4m','-jar',str(jar),'--format','json','--skip-non-html']+['http://127.0.0.1:'+str(nu_server.server_port)+'/'+p.relative_to(D).as_posix() for p in sorted(html)]
    result=subprocess.run(command,capture_output=True,text=True,timeout=180);nu=json.loads(result.stderr or result.stdout)
    (R/'tests/seo-nu-result.json').write_text(json.dumps(nu,indent=2)+'\n')
    assert result.returncode==0 and not nu.get('messages'),json.dumps(nu)[:6000]
    passed('Generated Vercel HTML conformance',documents=len(html),nu_messages=0)
finally:nu_server.shutdown();nu_server.server_close()

if '--static-only' in sys.argv:
    report['result']='PASS'
    (R/'tests/seo-static-final.json').write_text(json.dumps(report,indent=2)+'\n')
    print('PASS: final generated metadata, links, fragments, canonicals, exact code, asset hashes and Nu conformance.')
    raise SystemExit(0)

# Bind a short-lived loopback fixture. It is stopped in finally and never deployed.
cert=R/'.cache/test-local-cert.pem';key=R/'.cache/test-local-key.pem'
subprocess.run(['openssl','req','-x509','-newkey','rsa:2048','-nodes','-keyout',str(key),'-out',str(cert),'-days','1','-subj','/CN=localhost','-addext','subjectAltName=DNS:localhost,IP:127.0.0.1'],check=True,capture_output=True)
env=os.environ.copy();env.update(PORT='0',HOST='127.0.0.1',LOCAL_TLS_CERT=str(cert),LOCAL_TLS_KEY=str(key));server=subprocess.Popen([NODE,'deploy/serve.mjs'],cwd=R,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
try:
    ready=select.select([server.stdout],[],[],10)[0];assert ready,'Local route fixture failed to start'
    line=server.stdout.readline();match=re.search(r':(\d+)',line);assert match,line;base='https://127.0.0.1:'+match.group(1)
    browser_results=[];axe_results=[]
    with sync_playwright() as pw:
        for name in ['chromium','firefox','webkit']:
            print('Testing engine:',name,flush=True)
            browser=getattr(pw,name).launch(args=['--no-sandbox'] if name=='chromium' else [])
            context=browser.new_context(ignore_https_errors=True,viewport={'width':1440,'height':1000},permissions=['clipboard-read','clipboard-write'] if name=='chromium' else [])
            page=context.new_page();errors=[];page.on('pageerror',lambda error:errors.append(str(error)))
            response=page.goto(base+'/',wait_until='networkidle');assert response.status==200
            assert response.headers['x-content-type-options']=='nosniff';assert "frame-ancestors 'none'" in response.headers['content-security-policy']
            page.locator('[data-open-search]').click();page.locator('#book-search').fill('HTMLInputElement');expect(page.locator('#search-results a').first).to_have_attribute('href','/reference/api/htmlinputelement')
            page.keyboard.press('Escape');expect(page.locator('#search-dialog')).not_to_be_visible()
            page.goto(base+'/chapters/44',wait_until='networkidle');page.locator('[data-open-lab]').click();page.locator('#lab-code').fill('<!doctype html><title>Isolation probe</title><p id="probe">Waiting</p><script>let result;try{parent.document.body.dataset.probe="wrong";result="parent accessible"}catch{result="parent blocked"}document.getElementById("probe").textContent=result;</script>');page.locator('#lab-run').click();expect(page.frame_locator('#lab-output').locator('#probe')).to_have_text('parent blocked');assert page.locator('body').get_attribute('data-probe') is None;page.locator('[data-close-dialog="lab-dialog"]').click()
            page.goto(base+'/examples/44',wait_until='load');page.locator('#open-help').click();assert page.locator('#help-dialog').evaluate('(d)=>d.open');page.locator('#help-dialog button').click();assert not page.locator('#help-dialog').evaluate('(d)=>d.open')
            page.goto(base+'/reference/api-members',wait_until='networkidle');page.locator('#reference-search').fill('HTMLInputElement');assert page.locator('[data-reference-entry]:visible').count()==1
            page.goto(base+'/projects/registration',wait_until='networkidle');posted=[];page.on('request',lambda r:posted.append(r.url) if r.method=='POST' else None);page.locator('#demo-name').fill('Fictional Reader');page.locator('#demo-email').fill('reader@example.invalid');page.locator('#demo-session').select_option('morning');page.locator('button[type=submit]').click();assert 'No application was sent' in page.locator('#demo-result').inner_text();assert not posted
            response=page.goto(base+'/a-route-that-does-not-exist',wait_until='load');assert response.status==404;assert page.locator('h1').inner_text()=='Page not found'
            response=context.request.get(base+'/chapters/44.html',max_redirects=0);assert response.status==308 and response.headers['location']=='/chapters/44'
            page.set_viewport_size({'width':390,'height':844});overflow=[]
            mobile_paths=['/','/contents','/author','/reference','/reference/api-members','/reference/api/htmlinputelement','/reference/api/window','/reference/keywords','/privacy','/accessibility','/site-map','/chapters/44']
            if name=='chromium':mobile_paths += ['/chapters/'+f'{c["number"]:02}' for c in BOOK if c['number']!=44]+['/reference/api/'+re.sub(r'[^a-z0-9]+','-',r['name'].lower()).strip('-') for r in API['records'] if r['name'] not in ['Window','HTMLInputElement']]
            for route in mobile_paths:
                page.goto(base+route,wait_until='load')
                if page.evaluate('document.documentElement.scrollWidth>innerWidth+1'):overflow.append(route)
            assert not overflow,(name,overflow)
            if name=='chromium':
                page.goto(base+'/chapters/44',wait_until='networkidle');page.screenshot(path=str(R/'.cache/vercel-chapter-mobile.png'),full_page=False)
                audit_paths=['/','/contents','/author','/about','/projects','/chapters/34','/chapters/44','/reference','/reference/api-members','/reference/api/htmlinputelement','/reference/api/window','/reference/keywords','/privacy','/accessibility','/site-map','/projects/registration']
                axe=R/'node_modules/axe-core/axe.min.js';assert axe.exists(),'npm ci must install the audit dependency.'
                for route in audit_paths:
                    page.goto(base+route,wait_until='networkidle');page.add_script_tag(path=str(axe))
                    result=page.evaluate('async()=>await axe.run(document,{runOnly:{type:"tag",values:["wcag2a","wcag2aa","wcag21aa","wcag22aa"]}})')
                    violations=[{'id':v['id'],'impact':v['impact'],'nodes':[n['target'] for n in v['nodes']]} for v in result['violations']]
                    axe_results.append({'path':route,'violations':violations,'incomplete_checks':len(result['incomplete'])})
                bad=[row for row in axe_results if row['violations']];assert not bad,json.dumps(bad)[:6000]
            assert not errors,(name,errors[:8])
            browser_results.append({'engine':name,'version':browser.version,'transport':'local HTTPS fixture; self-signed certificate accepted for testing only','flows':['clean routes and 308 legacy URLs','working search routes','opaque-origin editable sandbox','native dialog open/close','API filtering','non-submitting local form','genuine 404 response'],'mobile_width':390,'overflow_pages_checked':len(mobile_paths),'javascript_errors':0})
            browser.close()
    passed('Cross-engine local route/header and UI smoke tests',browsers=browser_results)
    passed('Automated accessibility sample',engine='Chromium',axe_version=json.loads((R/'node_modules/axe-core/package.json').read_text())['version'],pages=len(axe_results),violations=0,results=axe_results,note='Incomplete axe checks and manual/assistive-technology review remain. Zero automated violations is not WCAG conformance.')
finally:
    server.terminate()
    try:server.wait(timeout=10)
    except subprocess.TimeoutExpired:server.kill();server.wait()
report['result']='PASS'
(R/'tests/seo-verification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
