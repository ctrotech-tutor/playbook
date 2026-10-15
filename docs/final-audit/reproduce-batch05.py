"""Run inside the maintained checkout after building. Loopback fixtures only.
Tests selected parser/lifecycle/API/interaction behavior, not full API, OS AT or security approval.
"""
from pathlib import Path
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from threading import Thread,Event
from urllib.parse import urlsplit
import json,subprocess,hashlib,sys
from playwright.sync_api import sync_playwright
R=Path.cwd();O=Path(__file__).resolve().parent;F=O/'batch05-fixtures';F.mkdir(exist_ok=True);sys.path.insert(0,str(R/'tools'))
from fingerprint import publication_fingerprint
COMPILED="--compiled" in sys.argv
SITE=R/("dist" if COMPILED else "build/site")
requests=[];async_gate=Event()
def fixture(name,body,head=''):
 p=F/(name+'.html');p.write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Controlled '+name+'</title>'+head+'</head><body><h1>Controlled '+name+'</h1>'+body+'</body></html>');return p
fixture('invalid-recovery','<p id="p">Alpha<div id="d">Beta</div>Gamma</p><table id="t">Foster<tr><td>Fiction</td></tr></table><b>One<i>Two</b>Three</i>')
mode='<?xml version="1.0" encoding="utf-8"?><html xmlns="http://www.w3.org/1999/xhtml" lang="en"><head><title>Served mode</title></head><body><h1>Served mode</h1><div id="case" Data-Label="kept"/><span id="sibling">Sibling</span></body></html>'
(F/'invalid-html-mode.html').write_text(mode)
fixture('state','<p id="slot">Safe fixture destination</p><input aria-label="Focusable state control">')
fixture('lifecycle','<p id="after-blocking">Parser reached body</p><img src="/pixel.png" alt="Controlled transparent pixel" width="1" height="1">','''<script>window.life=[];document.addEventListener('readystatechange',()=>life.push(document.readyState));document.addEventListener('DOMContentLoaded',()=>life.push('dcl'));window.addEventListener('load',()=>life.push('load'));</script><script src="/blocking.js"></script><script defer src="/defer1.js"></script><script defer src="/defer2.js"></script><script async src="/async-gated.js"></script><script async src="/async-ready.js"></script><script type="module" src="/main.mjs"></script><script nomodule>window.nomoduleRan=true</script>''')
fixture('import-map','<p>Controlled mapping, not a fetched-package guarantee</p>','<script type="importmap">{"imports":{"demo-math":"/mapped.mjs","never-used":"/never-imported.mjs"}}</script><script type="module">import { answer } from "demo-math"; window.mapAnswer=answer;</script>')
fixture('bad-module','<p>Controlled wrong-MIME negative execution case</p>','<script type="module" src="/wrong-mime"></script>')
fixture('messages','<iframe id="peer" src="/peer" title="Expected same-origin sender"></iframe><iframe id="other" src="/peer" title="Other same-origin sender"></iframe><iframe id="foreign" src="OTHER_ORIGIN/peer" title="Cross-origin sender"></iframe>')
fixture('peer','<p>Controlled messaging peer; no private data.</p>')
fixture('order','<div style="display:flex;flex-direction:row-reverse"><button type="button" id="first">First in DOM</button><button type="button" id="second">Second in DOM</button></div>')
fixture('trust','<p id="safe"></p><div id="unsafe"></div>')
class Handler(SimpleHTTPRequestHandler):
 def translate_path(self,path):
  p=urlsplit(path).path
  return str(F/p.removeprefix('/fixtures/')) if p.startswith('/fixtures/') else str(SITE/p.lstrip('/'))
 def send_data(self,data,kind,headers=()):
  self.send_response(200);self.send_header('Content-Type',kind);self.send_header('Content-Length',str(len(data)));self.send_header('X-Content-Type-Options','nosniff')
  for k,v in headers:self.send_header(k,v)
  self.end_headers();self.wfile.write(data)
 def do_GET(self):
  path=urlsplit(self.path).path;requests.append({'path':path,'port':self.server.server_port})
  scripts={'/blocking.js':"life.push('blocking');window.bodyAbsentAtBlocking=!document.getElementById('after-blocking');",'/defer1.js':"life.push('defer1');",'/defer2.js':"life.push('defer2');",'/async-gated.js':"life.push('async-gated');",'/async-ready.js':"life.push('async-ready');",'/dependency.mjs':"window.life.push('dependency');export const value=7;",'/main.mjs':"import {value} from './dependency.mjs';const modulePrivate=value;window.moduleThisUndefined=this===undefined;window.moduleValue=value;window.life.push('module');",'/mapped.mjs':'export const answer=42;', '/wrong-mime':'window.badModuleRan=true;'}
  if path in scripts:
   if path=='/async-gated.js':async_gate.wait(12)
   self.send_data(scripts[path].encode(),'text/plain' if path=='/wrong-mime' else 'text/javascript');return
  if path in ['/html-mode','/xml-mode']:self.send_data(mode.encode(),'text/html; charset=utf-8' if path=='/html-mode' else 'application/xhtml+xml; charset=utf-8');return
  if path=='/peer':self.send_data((F/'peer.html').read_bytes(),'text/html');return
  if path=='/fixtures/messages.html':self.send_data((F/'messages.html').read_bytes().replace(b'OTHER_ORIGIN',self.server.other.encode()),'text/html');return
  if path=='/pixel.png':
   import base64
   self.send_data(base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+jRZkAAAAASUVORK5CYII='),'image/png');return
  try:super().do_GET()
  except (BrokenPipeError,ConnectionResetError):pass
 def log_message(self,*args):pass
servers=[]
for _ in range(2):
 s=ThreadingHTTPServer(('127.0.0.1',0),Handler);Thread(target=s.serve_forever,daemon=True).start();servers.append(s)
base='http://127.0.0.1:'+str(servers[0].server_port);other='http://127.0.0.1:'+str(servers[1].server_port);servers[0].other=other;servers[1].other=base
rows=[]
try:
 with sync_playwright() as pw:
  for engine in ['chromium','firefox','webkit']:
   browser=getattr(pw,engine).launch(args=['--no-sandbox'] if engine=='chromium' else []);context=browser.new_context();page=context.new_page();loaded=[]
   for n in range(54,68):
    response=page.goto(base+f'/examples/{n:02}.html');assert response.status==200;loaded.append(n)
    if n==54:assert page.locator('#message').inner_text()=='<strong>Recommended</strong>' and page.locator('#message strong').count()==0
    if n==56:assert page.locator('#status-message').inner_text()=='Catalogue view ready.'
    if n in [57,61,66]:
     page.locator('#catalogue-query').fill('POETRY');page.get_by_role('button',name='Filter titles',exact=True).focus();page.keyboard.press('Enter');assert page.locator('#catalogue-list li:visible').all_text_contents()==['Poetry'];assert page.locator('#catalogue-result').inner_text()=='1 supplied title matches.'
     page.locator('#catalogue-query').fill('<img onerror="not-a-script">');page.get_by_role('button',name='Filter titles',exact=True).click();assert page.locator('#catalogue-list li:visible').count()==0 and page.locator('#catalogue-result').inner_text()=='No supplied titles matched.';page.get_by_role('button',name='Show all titles').click();assert page.locator('#catalogue-list li:visible').count()==3 and page.locator('#catalogue-query').input_value()==''
    if n==58:assert page.evaluate('document.contentType')=='text/html'
    if n==59:page.locator('a').click();assert page.url.endswith('#example-hours')
    if n==60:
     page.locator('#example-view').select_option('compact');page.get_by_role('button',name='Store example preference').click();assert page.locator('#preference-result').inner_text()=='Example preference stored in this browser.';page.reload();assert page.locator('#example-view').input_value()=='compact';page.get_by_role('button',name='Remove stored preference').click();assert page.evaluate('localStorage.getItem("ctrotech.teaching.view")') is None
     page.get_by_role('button',name='Run background sum').click();page.wait_for_function('()=>document.querySelector("#worker-result").textContent==="Background sum: 10"')
    if n==62:
     page.keyboard.press('Tab');assert page.locator('.skip-link').evaluate('(x)=>x===document.activeElement');assert page.locator('.skip-link').bounding_box()['y']>=0;page.keyboard.press('Enter');assert page.locator('#keyboard-main').evaluate('(x)=>x===document.activeElement')
     page.get_by_role('button',name='Remove Poetry',exact=True).focus();page.keyboard.press('Enter');assert page.get_by_role('button',name='Remove Fiction',exact=True).evaluate('(x)=>x===document.activeElement');page.keyboard.press('Enter');assert page.get_by_role('button',name='Remove Local histories',exact=True).evaluate('(x)=>x===document.activeElement');page.keyboard.press('Enter');assert page.locator('#list-heading').evaluate('(x)=>x===document.activeElement');page.get_by_role('button',name='Restore initial titles').click();assert page.locator('#removable-list li').count()==3 and page.locator('#list-heading').evaluate('(x)=>x===document.activeElement')
    if n==63:assert page.locator('#reader-comment script').count()==0 and '<script>example</script>' in page.locator('#reader-comment').inner_text()
    if n==64:assert page.locator('img').evaluate('(x)=>x.complete && x.naturalWidth===800 && x.naturalHeight===450')
    if n==65:page.locator('a').click();assert page.url.endswith('#sample-document-list')
   # Separate no-script and failed-resource baselines, not just noscript text.
   noscript=context.browser.new_context(java_script_enabled=False);np=noscript.new_page()
   for n in [57,61,66]:np.goto(base+f'/examples/{n:02}.html');assert np.locator('#catalogue-list li:visible').count()==3 and np.locator('#catalogue-query').is_disabled() and np.locator('noscript').is_visible()
   noscript.close();blocked=context.new_page();blocked.route('**/assets/catalogue-demo*.js',lambda route:route.abort())
   for n in [57,61,66]:blocked.goto(base+f'/examples/{n:02}.html');assert blocked.locator('#catalogue-query').is_disabled() and blocked.locator('#catalogue-list li:visible').count()==3 and not blocked.locator('noscript').is_visible()
   blocked.close()
   denied=context.new_page();denied.add_init_script("Object.defineProperty(window,'localStorage',{get(){throw new DOMException('Controlled denial','SecurityError')}})");denied.goto(base+'/examples/60.html');assert 'Storage unavailable' in denied.locator('#preference-result').inner_text();denied.get_by_role('button',name='Store example preference').click();assert 'Not stored' in denied.locator('#preference-result').inner_text();denied.close()
   broken=context.new_page();broken.add_init_script("window.Worker=class{constructor(){throw new DOMException('Controlled worker denial','SecurityError')}}");broken.goto(base+'/examples/60.html');broken.get_by_role('button',name='Run background sum').click();assert broken.locator('#worker-result').inner_text()=='Background calculation unavailable.' and broken.get_by_role('button',name='Run background sum').is_enabled();broken.close()
   stalled=context.new_page();stalled.route('**/assets/worker-demo*.js',lambda route:route.fulfill(status=200,content_type='text/javascript',body='self.onmessage=()=>{};'));stalled.goto(base+'/examples/60.html');stalled.get_by_role('button',name='Run background sum').click();stalled.wait_for_function('()=>document.querySelector("#worker-result").textContent==="Calculation timed out; try again."',timeout=10000);assert stalled.get_by_role('button',name='Run background sum').is_enabled();stalled.close()
   page.goto(base+'/fixtures/invalid-recovery.html');recovery=page.evaluate('''()=>({sectionOutsideParagraph:document.querySelector('#d').parentNode===document.body,implicitRowGroup:document.querySelector('#t tbody tr td').textContent,tableText:document.querySelector('#t').textContent,formattingTexts:[...document.querySelectorAll('i')].map(x=>x.textContent)})''');assert recovery['sectionOutsideParagraph'] and recovery['implicitRowGroup']=='Fiction' and 'Foster' not in recovery['tableText'] and recovery['formattingTexts']==['Two','Three']
   page.goto(base+'/fixtures/state.html');parser=page.evaluate('''()=>{const d=document.createElement('div'),t=document.createElement('tbody');d.innerHTML='<tr><td>Fiction</td></tr>';t.innerHTML='<tr><td>Fiction</td></tr>';const xml=new DOMParser().parseFromString('<root><x></root>','application/xml');let invalidMime;try{new DOMParser().parseFromString('<p>x</p>','not/a-parser-type')}catch(e){invalidMime=e.name}return {divHasRow:!!d.querySelector('tr'),bodyHasRow:!!t.querySelector('tr'),xmlParserError:xml.getElementsByTagName('parsererror').length>0,invalidMime}}''');assert parser=={'divHasRow':False,'bodyHasRow':True,'xmlParserError':True,'invalidMime':'TypeError'}
   modes=[]
   for modeName in ['html','xml']:
    page.goto(base+'/'+modeName+'-mode');modes.append(page.evaluate('({type:document.contentType,attributeNames:document.getElementById("case").getAttributeNames(),siblingParent:document.getElementById("sibling").parentNode.localName})'))
   assert modes[0]['siblingParent']=='div' and modes[1]['siblingParent']=='body' and 'data-label' in modes[0]['attributeNames'] and 'Data-Label' in modes[1]['attributeNames']
   async_gate.clear();page.goto(base+'/fixtures/lifecycle.html',wait_until='domcontentloaded');page.wait_for_function('()=>life.includes("async-ready")');before=page.evaluate('({life,ready:document.readyState,bodyAbsentAtBlocking,moduleThisUndefined,moduleValue,privateGlobalAbsent:window.modulePrivate===undefined,nomoduleAbsent:window.nomoduleRan===undefined})');assert before['bodyAbsentAtBlocking'] and before['moduleThisUndefined'] and before['privateGlobalAbsent'] and before['nomoduleAbsent'] and before['moduleValue']==7
   seq=before['life'];assert seq.index('blocking')<seq.index('defer1')<seq.index('defer2')<seq.index('dcl') and seq.index('dependency')<seq.index('module')<seq.index('dcl') and 'async-gated' not in seq
   async_gate.set();page.wait_for_function('()=>life.includes("load")');after=page.evaluate('({life,ready:document.readyState})');assert after['ready']=='complete' and after['life'].index('async-gated')<after['life'].index('load')
   page.goto(base+'/fixtures/import-map.html');page.wait_for_function('()=>window.mapAnswer===42');assert not any(r['path']=='/never-imported.mjs' for r in requests);page.goto(base+'/fixtures/bad-module.html');assert page.evaluate('window.badModuleRan===undefined')
   page.goto(base+'/fixtures/state.html');schedule=page.evaluate('''()=>new Promise(resolve=>{const order=['sync'];setTimeout(()=>{order.push('timer');resolve(order)},0);queueMicrotask(()=>order.push('microtask'));Promise.resolve().then(()=>order.push('promise'));order.push('end')})''');assert schedule==['sync','end','microtask','promise','timer']
   page.evaluate('window.storageEvents=[];addEventListener("storage",e=>storageEvents.push({key:e.key,old:e.oldValue,value:e.newValue}))');peer=context.new_page();peer.goto(base+'/fixtures/state.html');peer.evaluate('window.storageEvents=[];addEventListener("storage",e=>storageEvents.push(e.key));localStorage.setItem("ctrotech.audit.storage","one")');page.wait_for_function('()=>storageEvents.length===1');storage=page.evaluate('storageEvents');assert storage==[{'key':'ctrotech.audit.storage','old':None,'value':'one'}] and peer.evaluate('storageEvents.length')==0;peer.evaluate('localStorage.removeItem("ctrotech.audit.storage")');peer.close()
   history=page.evaluate('''(other)=>{window.pops=[];addEventListener('popstate',e=>pops.push(e.state));history.replaceState({view:'before'},'');history.pushState({view:'compact'},'','?view=compact');let crossOrigin,errorClone;try{history.pushState({},'',other)}catch(e){crossOrigin=e.name}try{history.pushState({f(){ }},'')}catch(e){errorClone=e.name}return {crossOrigin,errorClone,popCount:pops.length,state:history.state}}''',other);assert history=={'crossOrigin':'SecurityError','errorClone':'DataCloneError','popCount':0,'state':{'view':'compact'}};page.evaluate('history.back()');page.wait_for_function('()=>pops.length===1');assert page.evaluate('history.state.view')=='before'
   page.goto(base+'/fixtures/messages.html');page.evaluate('''window.messages=[];addEventListener('message',e=>{const expected=document.querySelector('#peer').contentWindow;messages.push({originMatches:e.origin===location.origin,sourceMatches:e.source===expected,accepted:e.origin===location.origin && e.source===expected && e.data?.kind==='book' && typeof e.data.title==='string'})})''');payload={'kind':'book','title':'Fiction'}
   for id,data in [('peer',payload),('other',payload),('foreign',payload),('peer',{'kind':'book','title':5})]:page.locator('#'+id).content_frame.locator('body').evaluate('(x,args)=>parent.postMessage(args.data,args.origin)',{'data':data,'origin':base})
   page.wait_for_function('()=>messages.length===4');messages=page.evaluate('messages');assert sum(x['accepted'] for x in messages)==1
   transfer=page.evaluate('''()=>new Promise(resolve=>{const c=new MessageChannel(),buffer=new ArrayBuffer(8);c.port1.addEventListener('message',e=>{const result={receivedBytes:e.data.byteLength,senderBytes:buffer.byteLength};c.port1.close();c.port2.close();resolve(result)});c.port1.start();c.port2.postMessage(buffer,[buffer])})''');assert transfer=={'receivedBytes':8,'senderBytes':0}
   page.goto(base+'/fixtures/order.html');page.keyboard.press('Tab');assert page.locator('#first').evaluate('(x)=>x===document.activeElement');assert page.locator('#first').bounding_box()['x']>page.locator('#second').bounding_box()['x']
   page.goto(base+'/fixtures/trust.html');page.evaluate('''document.querySelector('#safe').textContent='<img src=x onerror="window.textInjected=true">';document.querySelector('#unsafe').innerHTML='<script>window.fragmentScriptRan=true<'+ '/script><img src="/missing-pixel" alt="Controlled error image" onerror="window.fragmentEventRan=true">';''');page.wait_for_function('()=>window.fragmentEventRan===true');assert page.evaluate('window.textInjected===undefined && window.fragmentScriptRan===undefined')
   page.set_viewport_size({'width':320,'height':800})
   for n in range(54,68):
    for kind in ['chapters','examples']:
     page.goto(base+f'/{kind}/{n:02}.html');assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+1'),(engine,kind,n)
   rows.append({'engine':engine,'version':browser.version,'primary_examples_loaded':loaded,'filter_cases':'PASS: Enter/match/no-match/reset; no-script and failed-resource baseline separately','focus_cases':'PASS: skip destination; remove next/previous/final, restore','storage_and_worker':'PASS: store/reload/remove; denied storage; actual supplied worker=10; controlled Worker constructor denial; native nonresponding-worker timeout','recovery':recovery,'fragment_and_xml_parser':parser,'served_modes':modes,'lifecycle_before_async_release':before,'lifecycle_after_async_release':after,'module_cases':'PASS: dependency order, strict/module scope, import map, unused mapping not fetched, wrong-MIME module blocked, nomodule skipped','microtask_order':schedule,'storage_event':storage,'history':history,'native_messages':messages,'transferred_buffer':transfer,'rendering_order':'PASS: reversed visual order did not reverse native Tab order','trust_boundary':'PASS: text insertion inert; innerHTML script not executed but handler executed in controlled unsafe destination','chapter_and_standalone_example_reflow_320px':list(range(54,68)),'limits':'Selected headless native/local-request probes, not OS AT, full parser/API algorithms, bfcache/device/field performance or complete security review.'});context.close();browser.close()
finally:
 async_gate.set()
 for s in servers:s.shutdown();s.server_close()
nu=[]
for p in sorted(F.glob('*.html')):
 result=subprocess.run(['java','-Xss4m','-jar',str(R/'.cache/vnu/vnu.jar'),'--format','json',str(p)],capture_output=True,text=True,timeout=60);out=json.loads(result.stderr or result.stdout);errors=[x for x in out.get('messages',[]) if x.get('type')=='error'];invalid=p.name.startswith('invalid-');assert bool(errors)==invalid,(p.name,out)
 nu.append({'fixture':p.name,'intentionally_invalid_html':invalid,'checker_errors':len(errors),'messages':out.get('messages',[]),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(O/('batch05-compiled-browser-checks.json' if COMPILED else 'batch05-browser-checks.json')).write_text(json.dumps({'date':'2026-10-15','candidate_fingerprint':publication_fingerprint(R),'tested_tree':'dist' if COMPILED else 'build/site','result':'PASS','browsers':rows,'fixture_conformance':nu,'limits':['No independent chapter/answer approval','No OS AT or real touch/IME review','No full parser/API/algorithm coverage','No field or comparative performance claim','No actual bfcache/device matrix','No complete security or tagged-PDF approval']},ensure_ascii=False,separators=(',',':'))+'\n')
print('PASS: CH54–67 selected native parser, lifecycle, API, local enhancement/focus/security and reflow checks in three engines.')
