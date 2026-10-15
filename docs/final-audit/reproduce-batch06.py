#!/usr/bin/env python3
"""Same-agent selected project checks. No independent/OS-AT/security approval.
Usage: python reproduce-batch06.py REPOSITORY [build/site|dist] [OUTPUT_JSON]
"""
from pathlib import Path
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from threading import Thread
from functools import partial
from urllib.parse import urlsplit
import json,sys,zipfile,tempfile,hashlib,xml.etree.ElementTree as ET
from playwright.sync_api import sync_playwright,expect
R=Path(sys.argv[1]).resolve();S=R/(sys.argv[2] if len(sys.argv)>2 else 'build/site')
OUT=Path(sys.argv[3]) if len(sys.argv)>3 else R/'.cache/batch06-browser-checks.json'
sys.path.insert(0,str(R/'tools'));from fingerprint import publication_fingerprint
class Handler(SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
 def translate_path(self,path):
  p=urlsplit(path).path
  target=S/p.removeprefix('/review-repo/').lstrip('/')
  if not target.exists() and not target.suffix:target=target.with_suffix('.html')
  return str(target)
server=ThreadingHTTPServer(('127.0.0.1',0),Handler);Thread(target=server.serve_forever,daemon=True).start()
base=f'http://127.0.0.1:{server.server_port}/review-repo/'
rows=[];book=json.loads((R/'content/chapters.json').read_text());project_docs=sorted(S.glob('projects/*/*.html'))
assert len(project_docs)==12
# Compare every exported file to its package bytes, not just ZIP integrity.
for c in book[67:]:
 slug=c['project_slug'];folder=S/'projects'/slug
 with zipfile.ZipFile(S/'downloads'/f'project-{slug}.zip') as z:
  assert z.testzip() is None
  expected={slug+'/'+p.name for p in folder.iterdir() if p.is_file()}
  assert set(z.namelist())==expected,(slug,z.namelist(),expected)
  for p in folder.iterdir():assert z.read(slug+'/'+p.name)==((R/'build/site/projects'/slug/p.name).read_bytes() if S.name=='dist' else p.read_bytes())
  assert c['lesson'] in z.read(slug+'/BRIEF.md').decode()
  assert c['answer'] in z.read(slug+'/SOLUTION.md').decode()
  for name in z.namelist():assert not name.startswith('/') and '..' not in Path(name).parts
# The three real drawings match the declared ratio and alternatives.
for p in (S/'projects/gallery').glob('*.svg'):
 node=ET.fromstring(p.read_text());assert node.attrib['viewBox']=='0 0 640 400';assert node.attrib['width']=='640' and node.attrib['height']=='400'
 assert 'http' not in p.read_text().replace('http://www.w3.org/2000/svg','')
try:
 with sync_playwright() as pw:
  for engine in ['chromium','firefox','webkit']:
   browser=getattr(pw,engine).launch();ctx=browser.new_context(viewport={'width':1280,'height':900})
   page=ctx.new_page();failures=[];errors=[];requests=[];axe=[]
   page.on('pageerror',lambda error:errors.append(str(error)))
   page.on('response',lambda response:failures.append((response.status,response.url)) if response.status>=400 else None)
   page.on('request',lambda request:requests.append((request.method,request.url)))
   def go(path):page.goto(base+path,wait_until='load')
   def rel(p):return p.relative_to(S).as_posix()
   for p in project_docs:
    go(rel(p));assert page.locator('main').count()==1;assert page.locator('h1').count()==1
    page.keyboard.press('Tab');assert page.locator(':focus').get_attribute('class')=='skip';page.keyboard.press('Enter')
    assert page.evaluate('document.activeElement.id')=='main'
    assert page.locator('meta[name=author]').get_attribute('content')=='Odejobi Abiola Samuel'
    if '/portfolio/' in str(p) or '/capstone/' in str(p):
     current=page.locator('nav[aria-label=Primary] [aria-current=page]');assert current.count()==1
     expected='/'+rel(p).removesuffix('index.html').removesuffix('.html').rstrip('/') if S.name=='dist' else p.name
     assert current.get_attribute('href')==expected,(rel(p),current.get_attribute('href'),expected)
    if engine=='chromium':
     page.add_script_tag(path=str(R/'node_modules/axe-core/axe.min.js'))
     result=page.evaluate('async()=>await axe.run(document,{runOnly:{type:"tag",values:["wcag2a","wcag2aa","wcag21aa","wcag22aa"]}})')
     bad=[{'id':v['id'],'nodes':[n['target'] for n in v['nodes']]} for v in result['violations']]
     assert not bad,(rel(p),bad)
     axe.append({'path':rel(p),'violations':0,'incomplete':len(result['incomplete'])})
   go('projects/profile/index.html');page.get_by_role('link',name='Read the contact status').click();assert page.url.endswith('#contact');assert 'No personal contact' in page.locator('#contact').inner_text()
   for filename,label in [('project.html','Read the notice-board note'),('reading-list.html','Read the reading-list note')]:
    go('projects/portfolio/index.html');page.get_by_role('link',name=label).click();assert page.url.endswith('/'+filename) or page.url.endswith('/'+filename.removesuffix('.html'))
    page.get_by_role('link',name='Read the contact status').click();assert page.url.endswith('#contact');assert 'learning portfolio' in page.locator('h1').inner_text()
   go('projects/article/index.html')
   for target in ['borrowing','renewal','returns']:
    page.locator('nav a[href="#'+target+'"]').click();assert page.url.endswith('#'+target)
   assert page.locator('time').get_attribute('datetime')=='2026-10-15'
   assert '15 October 2026' in page.locator('#borrowing').inner_text();assert '29 October' in page.locator('#renewal').inner_text()
   go('projects/dashboard/index.html');counts=[int(t) for t in page.locator('tbody td:nth-child(2)').all_text_contents()]
   assert counts==[42,18,9];assert sum(counts)==69;assert '69 loans' in page.locator('dl').inner_text()
   go('projects/gallery/index.html');assert page.locator('img').count()==3
   for image in page.locator('img').all():
    image.scroll_into_view_if_needed();expect(image).to_be_visible();expect(image).to_have_js_property('complete',True)
    assert image.evaluate('(i)=>i.naturalWidth')==640
   assert 'six panes' in page.locator('img').nth(1).get_attribute('alt')
   # The integration and wrapped chapter share the complete form task, not just DOM IDs.
   for path in ['projects/registration/index.html','projects/capstone/membership.html','examples/70.html']:
    go(path);expect(page.locator('#demo-name')).to_be_enabled();assert not page.locator('#demo-fields').evaluate('(n)=>n.disabled');url=page.url
    requests.clear();page.locator('button[type=submit]').click()
    expect(page.locator('#demo-errors')).to_be_visible();assert page.locator('#demo-error-list a').count()==3
    assert page.evaluate('document.activeElement.id')=='demo-errors'
    if engine=='chromium':
     page.add_script_tag(path=str(R/'node_modules/axe-core/axe.min.js'))
     state=page.evaluate('async()=>await axe.run(document,{runOnly:{type:"tag",values:["wcag2a","wcag2aa","wcag21aa","wcag22aa"]}})')
     assert not state['violations'],(path,'invalid-form state',state['violations'])
     axe.append({'path':path,'state':'invalid','violations':0,'incomplete':len(state['incomplete'])})
    page.locator('#demo-error-list a').first.focus();page.keyboard.press('Enter');assert page.evaluate('document.activeElement.id')=='demo-name'
    page.locator('#demo-name').fill('   ');page.locator('#demo-email').fill('not-an-email')
    page.locator('button[type=submit]').click();assert page.locator('#demo-error-list a').count()==3
    page.locator('#demo-name').fill('Practice Reader');expect(page.locator('#demo-name')).not_to_have_attribute('aria-invalid','true')
    assert page.locator('#demo-error-list a').count()==2
    page.locator('button[type=reset]').click();assert page.locator('#demo-name').input_value()==''
    assert page.locator('#demo-email').input_value()=='';assert page.locator('#demo-session').input_value()==''
    assert not page.locator('#demo-name').evaluate('(n)=>n.validity.customError')
    expect(page.locator('#demo-errors')).to_be_hidden();assert page.locator('[aria-invalid]').count()==0
    page.locator('#demo-name').fill('Practice Reader');page.locator('#demo-email').fill('reader@example.invalid');page.locator('#demo-session').select_option('morning')
    page.locator('#demo-email').press('Enter');expect(page.locator('#demo-result')).to_contain_text('No application was sent')
    assert page.url==url;assert not requests,requests
    assert page.evaluate('localStorage.length')==0;assert page.evaluate('sessionStorage.length')==0
    page.locator('#demo-name').fill('Changed Reader');expect(page.locator('#demo-result')).to_have_text('')
    # Recheck success then reset: no previous success or values survive.
    page.locator('button[type=submit]').click();page.locator('button[type=reset]').click()
    assert 'No application was sent' in page.locator('#demo-result').inner_text()
    assert page.locator('#demo-name').input_value()=='';assert page.locator('#demo-session').input_value()==''
    # A markup-shaped value must not produce an inserted element.
    page.locator('#demo-name').fill('<img src=x onerror=alert(1)>');page.locator('#demo-email').fill('reader@example.invalid');page.locator('#demo-session').select_option('afternoon');page.locator('button[type=submit]').click()
    assert page.locator('img').count()==0;assert page.url==url;assert not requests
   # Deny the actual script, including the hashed production filename.
   blocked=browser.new_context();blocked.route('**/*',lambda route:route.abort() if route.request.resource_type=='script' else route.continue_())
   bp=blocked.new_page()
   for path in ['projects/registration/index.html','projects/capstone/membership.html','examples/70.html']:
    bp.goto(base+path);assert bp.locator('#demo-fields').evaluate('(n)=>n.disabled');assert 'JavaScript must load' in bp.locator('#demo-note').inner_text()
    assert bp.locator('#demo-name').is_disabled()
   blocked.close()
   noimages=browser.new_context(viewport={'width':320,'height':800})
   noimages.route('**/*.svg',lambda route:route.abort())
   ip=noimages.new_page();ip.goto(base+'projects/gallery/index.html')
   assert ip.locator('figcaption').count()==3
   for image in ip.locator('img').all():
    image.scroll_into_view_if_needed();expect(image).to_have_js_property('complete',True)
    assert image.evaluate('(n)=>n.naturalWidth')==0;assert image.get_attribute('alt')
   assert ip.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
   noimages.close()
   noscript=browser.new_context(java_script_enabled=False,viewport={'width':320,'height':800});np=noscript.new_page()
   for p in project_docs:
    np.goto(base+rel(p));assert np.locator('h1').is_visible()
    if '/registration/' in str(p) or p.name=='membership.html':assert np.locator('#demo-name').is_disabled()
    if '/portfolio/' in str(p) or '/capstone/' in str(p):
     for link in np.locator('nav[aria-label=Primary] a').all():
      href=link.get_attribute('href');target=S/href.lstrip('/') if href.startswith('/') else p.parent/href
      assert target.exists() or target.with_suffix('.html').exists(),(rel(p),href)
   noscript.close()
   page.set_viewport_size({'width':320,'height':800})
   for path in [rel(p) for p in project_docs]+[f'chapters/{n}.html' for n in range(68,75)]+[f'examples/{n}.html' for n in range(68,75)]:
    go(path);assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),(engine,path,'overflow')
   for path in ['projects/dashboard/index.html','projects/capstone/catalogue.html']:
    go(path);wrap=page.locator('.tablewrap');wrap.focus();assert wrap.evaluate('(n)=>n===document.activeElement')
    assert wrap.evaluate('(n)=>n.scrollWidth>n.clientWidth');page.keyboard.press('End')
    wrap.evaluate('(n)=>n.scrollLeft=n.scrollWidth');assert wrap.evaluate('(n)=>n.scrollLeft>0')
   # Native file URLs from the actual extracted packages: no HTTP origin required.
   with tempfile.TemporaryDirectory(dir=R/'.cache') as tmp:
    temp=Path(tmp)
    for slug in ['profile','portfolio','registration','article','dashboard','gallery','capstone']:
     with zipfile.ZipFile(S/'downloads'/f'project-{slug}.zip') as z:z.extractall(temp)
     for file in (temp/slug).glob('*.html'):
      page.goto(file.as_uri());assert page.locator('main').is_visible()
      if file.name=='membership.html' or slug=='registration':
       expect(page.locator('#demo-name')).to_be_enabled();assert not page.locator('#demo-fields').evaluate('(n)=>n.disabled');page.locator('button[type=submit]').click();assert page.locator('#demo-error-list a').count()==3
      if slug=='gallery':
       for image in page.locator('img').all():
        image.scroll_into_view_if_needed();expect(image).to_have_js_property('complete',True);assert image.evaluate('(n)=>n.naturalWidth')==640
   assert not errors,(engine,errors);assert not failures,(engine,failures)
   rows.append({'engine':engine,'version':browser.version,'project_documents':12,'form_paths':3,'reflow_paths':26,'width_css_px':320,'no_script_project_documents':12,'blocked_script_form_paths':3,'native_file_zip_documents':12,'errors':errors,'failed_http_responses':failures,'automated_a11y':axe,'flows':['skip-to-main keyboard','distinct portfolio notes and return','article fragment/date consistency','loan arithmetic and units','all SVGs decoded and blocked-image text fallback','empty/whitespace/malformed-email errors','error link keyboard focus','live correction and stale success clearing','reset invalid and success states and implicit Enter submission','local success no request/URL/storage write','markup-shaped practice input inert','failed-script disabled fields','no-script complete project baseline','320px chapter/example/project reflow','named focusable table scroll','byte-exact ZIP members and chapter-derived brief/answers','all extracted document file URLs']})
   ctx.close();browser.close()
finally:server.shutdown();server.server_close()
output={'result':'PASS','scope':'Selected native project behaviour plus automated WCAG-tagged checks. Same-agent and headless, not independent/OS-assistive-technology review, full WCAG conformance, exhaustive security or accessible-PDF approval.','publication_fingerprint':publication_fingerprint(R),'tree':str(S.relative_to(R)),'browsers':rows}
OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(output,indent=2)+'\n');print(json.dumps(output,indent=2))
