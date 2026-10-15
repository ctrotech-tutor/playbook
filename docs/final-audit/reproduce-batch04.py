"""Run from an installed candidate checkout after tools/build.py --pdf.
Controlled loopback DOM/security probes. No production secrets, service or OS AT approval.
"""
from pathlib import Path
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from threading import Thread
from urllib.parse import urlsplit
import base64,hashlib,json,secrets,subprocess,sys
from playwright.sync_api import sync_playwright
R=Path.cwd();O=Path(__file__).resolve().parent;F=O/'batch04-fixtures';F.mkdir(exist_ok=True)
sys.path.insert(0,str(R/'tools'))
from fingerprint import publication_fingerprint
SCRIPT=(R/'assets/integrity-demo.js').read_bytes();HASH='sha384-'+base64.b64encode(hashlib.sha384(SCRIPT).digest()).decode();BAD='sha384-'+base64.b64encode(bytes(48)).decode();STRONG_BAD='sha512-'+base64.b64encode(bytes(64)).decode();requests=[]
def fixture(name,body,head=''):
 p=F/(name+'.html');p.write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Fictional '+name+' fixture</title>'+head+'</head><body><h1>Fictional '+name+' fixture</h1>'+body+'</body></html>');return p
fixture('disclosure','<details id="one" name="help" open><summary>First answer</summary><p>One</p></details><details id="two" name="help"><summary>Second answer</summary><p>Two</p></details><details id="changes"><summary>Changes</summary><p>Recorded</p></details>')
fixture('commands','<form id="f"><button id="invoke" type="button" commandfor="command-dialog" command="show-modal">Command open</button><button id="auto" commandfor="command-target" command="--pin">Auto state</button><button id="custom" type="button" commandfor="command-target" command="--pin">Custom event</button></form><div id="command-target"></div><dialog id="command-dialog" aria-label="Command dialog"><button type="button">Inside</button></dialog>')
fixture('state','<label>Outside control <input id="outside"></label><div inert><label>Inert control <input id="inert-control"></label></div><form id="f"><label hidden>Hidden entry <input name="hiddenEntry" value="still-an-entry"></label></form><div id="editable" contenteditable="true"><span id="readonly-part" contenteditable="false">Not editable</span></div><div id="plain" contenteditable="plaintext-only">Plain</div><div id="drag" draggable="false">Drag state</div><p id="reader:name">Punctuated id</p><p id="data" data-count="3"></p>')
fixture('shadow','<notice-panel id="host"><template shadowrootmode="open" shadowrootclonable shadowrootserializable><slot name="heading">Heading fallback</slot><slot>Content fallback</slot><span part="badge">Notice</span></template><h2 slot="heading" id="assigned">Library notice</h2><p>Fictional notice</p></notice-panel><template id="ordinary"><article>Inert template</article></template>')
fixture('defaults','<form id="defaults"><label>Value <input id="field" value="first"></label><fieldset><legend>Contact</legend><label><input type="radio" name="contact" value="email" checked>Email</label><label><input type="radio" name="contact" value="phone">Phone</label></fieldset></form><label>Options <select id="options"><option value="central">Central</option><option value="east">East</option></select></label>')
fixture('popover','<button id="outside" type="button">Outside</button><div id="auto" popover>Auto</div><div id="manual" popover="manual">Manual</div><div id="hint" popover="hint">Hint</div><div id="invalid" popover="unknown">Invalid spelling</div><div id="none">No popover</div><dialog id="request" closedby="none" aria-label="Request-close fixture"><button type="button" autofocus>Inside</button></dialog>')
fixture('integrity', '<p id="integrity-status">Waiting</p>',f'<script src="/good.js" integrity="{HASH}" defer></script><script src="/bad.js" integrity="{BAD}" defer></script><script src="/strong.js" integrity="{HASH} {STRONG_BAD}" defer></script>')
fixture('preload','<p id="integrity-status">Waiting</p>',f'<link rel="preload" href="/preload.js" as="script" integrity="{HASH}"><script src="/preload.js" integrity="{HASH}" defer></script>')
fixture('referrer','<a id="none" href="REFERRER_TARGET/sink" referrerpolicy="no-referrer">No referrer</a><a id="origin" href="REFERRER_TARGET/sink" referrerpolicy="origin">Origin only</a>')
fixture('until-found','<a href="#found">Find fictional section</a><section hidden="until-found"><h2 id="found">Discovered content</h2><p>Fictional text</p></section>')
fixture('invalid-dialog-tabindex','<dialog tabindex="0" aria-label="Invalid focus markup"></dialog>')
fixture('invalid-details-group','<details name="same" open><summary>One</summary><p>One</p></details><details name="same" open><summary>Two</summary><p>Two</p></details>')
class Handler(SimpleHTTPRequestHandler):
 def translate_path(self,path):
  p=urlsplit(path).path
  if p.startswith('/fixtures/'):return str(F/p.removeprefix('/fixtures/'))
  return str(R/'build/site'/p.lstrip('/'))
 def send_data(self,data,kind,headers=()):
  self.send_response(200);self.send_header('Content-Type',kind);self.send_header('Content-Length',str(len(data)))
  for k,v in headers:self.send_header(k,v)
  self.end_headers();self.wfile.write(data)
 def do_GET(self):
  path=urlsplit(self.path).path;requests.append({'path':path,'port':self.server.server_port,'referer':self.headers.get('Referer')})
  if path in ['/good.js','/bad.js','/strong.js','/preload.js','/cors.js','/no-cors.js']:
   headers=[('Cache-Control','public, max-age=3600')]
   if path=='/cors.js':headers.append(('Access-Control-Allow-Origin','*'))
   self.send_data(SCRIPT,'text/javascript; charset=utf-8',headers);return
  if path=='/nonce':
   nonce=base64.b64encode(secrets.token_bytes(16)).decode()
   html=f'<!doctype html><html lang="en"><title>Nonce fixture</title><h1>Nonce fixture</h1><script id="allowed" nonce="{nonce}">window.nonceAllowed=true</script><script>window.nonceDisallowed=true</script></html>'
   self.send_data(html.encode(),'text/html; charset=utf-8',[('Content-Security-Policy',f"default-src 'none'; script-src 'nonce-{nonce}'; base-uri 'none'")]);return
  if path=='/sink':self.send_data(b'<!doctype html><html lang="en"><title>Local receipt</title><h1>Local navigation receipt</h1></html>','text/html');return
  if path=='/cross-integrity':
   html=f'<!doctype html><html lang="en"><title>Cross-origin integrity</title><h1>Cross-origin integrity</h1><script src="{self.server.other}/cors.js" integrity="{HASH}" crossorigin="anonymous"></script><script src="{self.server.other}/no-cors.js" integrity="{HASH}" crossorigin="anonymous"></script>'
   self.send_data(html.encode(),'text/html; charset=utf-8');return
  if path=='/fixtures/referrer.html':
   self.send_data((F/'referrer.html').read_bytes().replace(b'REFERRER_TARGET',self.server.other.encode()),'text/html');return
  try:super().do_GET()
  except (BrokenPipeError,ConnectionResetError):pass
 def log_message(self,*a):pass
servers=[]
for _ in range(2):
 s=ThreadingHTTPServer(('127.0.0.1',0),Handler);Thread(target=s.serve_forever,daemon=True).start();servers.append(s)
base='http://127.0.0.1:'+str(servers[0].server_port);other='http://127.0.0.1:'+str(servers[1].server_port);servers[0].other=other;servers[1].other=base
rows=[]
try:
 with sync_playwright() as pw:
  for engine in ['chromium','firefox','webkit']:
   browser=getattr(pw,engine).launch(args=['--no-sandbox'] if engine=='chromium' else []);page=browser.new_page();loaded=[]
   for n in range(42,54):
    response=page.goto(base+f'/examples/{n:02}.html',wait_until='load');assert response.status==200;loaded.append(n)
    if n==42:
     page.locator('#button-query').fill('fictional query');page.get_by_role('button',name='Restore search defaults').click();assert page.locator('#button-query').input_value()==''
    if n==43:
     page.locator('summary').focus();page.keyboard.press('Enter');assert page.locator('details').evaluate('(x)=>x.open');page.keyboard.press('Space');assert not page.locator('details').evaluate('(x)=>x.open')
    if n==44:
     page.locator('#open-help').focus();page.keyboard.press('Enter');assert page.locator('#help-dialog').evaluate('(x)=>x.open && x.matches(":modal")');assert page.locator('#help-dialog button').evaluate('(x)=>x===document.activeElement')
     page.keyboard.press('Escape');assert not page.locator('#help-dialog').evaluate('(x)=>x.open');assert page.locator('#open-help').evaluate('(x)=>x===document.activeElement')
     page.get_by_role('button',name='Reading tip',exact=True).click();assert page.locator('#reading-tip').evaluate('(x)=>x.matches(":popover-open")');page.get_by_role('button',name='Dismiss reading tip').click();assert not page.locator('#reading-tip').evaluate('(x)=>x.matches(":popover-open")')
    if n==45:
     page.get_by_role('button',name='Move up: Poetry',exact=True).focus();page.keyboard.press('Enter')
     assert page.locator('#reading-list li').first.locator('span').inner_text()=='Poetry';assert page.locator('#reading-list li').first.evaluate('(x)=>x===document.activeElement');assert page.locator('#move-status').inner_text()=='Poetry moved up.'
     page.get_by_role('button',name='Move down: Poetry',exact=True).click();assert page.locator('#reading-list li').nth(1).locator('span').inner_text()=='Poetry'
    if n==46:assert page.locator('#book-results h2').inner_text()=='Local histories'
    if n==47:assert page.locator('#copy-note').inner_text()=='3 copies listed in this fictional record.'
    if n==51:assert page.locator('link[rel=stylesheet]').evaluate('(x)=>x.sheet!==null')
    if n==52:assert page.locator('#integrity-status').inner_text()=='The supplied teaching script ran.'
    if n==53:assert page.locator('#nickname').input_value()=='Ada' and page.locator('#nickname').get_attribute('value')=='Guest'
   page.goto(base+'/fixtures/disclosure.html',wait_until='networkidle');page.locator('#two summary').click();assert page.locator('#two').evaluate('(x)=>x.open') and not page.locator('#one').evaluate('(x)=>x.open')
   page.evaluate('window.changes=[];const x=document.querySelector("#changes");x.addEventListener("toggle",e=>changes.push({oldState:e.oldState,newState:e.newState}));x.open=true;x.open=false;x.open=true')
   page.wait_for_function('()=>window.changes.length>0');coalesced=page.evaluate('window.changes');assert len(coalesced)==1
   page.goto(base+'/fixtures/commands.html');page.evaluate('window.commands=[];window.submits=0;f.addEventListener("submit",e=>{e.preventDefault();submits++});document.querySelector("#command-target").addEventListener("command",e=>commands.push({command:e.command,source:e.source?.id}));')
   page.locator('#custom').click();custom=page.evaluate('window.commands');page.locator('#auto').click();auto=page.evaluate('({events:commands.length,submits})');page.locator('#invoke').click();command_observation=page.evaluate('({interfaceExposed:"CommandEvent" in window,customEvents:commands,autoState:document.querySelector("#auto").type,dialogOpened:document.querySelector("#command-dialog").open,submitCount:submits})')
   if command_observation['dialogOpened']:page.locator('#command-dialog').evaluate('(x)=>x.close()')
   page.goto(base+'/fixtures/state.html');state=page.evaluate('''()=>{const x=document.querySelector('#outside');x.focus();document.querySelector('#inert-control').focus();const d=document.querySelector('#data');d.dataset.nil=null;d.dataset.flag=false;let datasetError;try{d.dataset['loan-days']='4'}catch(e){datasetError=e.name}delete d.dataset.count;return {inertFocusBlocked:document.activeElement===x,hiddenEntry:[...new FormData(document.querySelector('#f'))],editable:document.querySelector('#editable').isContentEditable,readonlyPart:document.querySelector('#readonly-part').isContentEditable,plaintextProperty:document.querySelector('#plain').contentEditable,draggable:document.querySelector('#drag').draggable,idFound:document.getElementById('reader:name')===document.querySelector('#'+CSS.escape('reader:name')),datasetNull:d.dataset.nil,datasetFalse:d.dataset.flag,datasetRemoved:!d.hasAttribute('data-count'),datasetError}}''')
   assert state=={'inertFocusBlocked':True,'hiddenEntry':[['hiddenEntry','still-an-entry']],'editable':True,'readonlyPart':False,'plaintextProperty':'plaintext-only','draggable':False,'idFound':True,'datasetNull':'null','datasetFalse':'false','datasetRemoved':True,'datasetError':'SyntaxError'}
   page.goto(base+'/fixtures/shadow.html');shadow=page.evaluate('''()=>{const h=document.querySelector('#host'),r=h.shadowRoot,t=document.querySelector('#ordinary');const x={shadowCreated:!!r,lightChildRemains:document.querySelector('#assigned').parentNode===h,assigned:r?.querySelector('slot[name=heading]').assignedElements().map(n=>n.id),templateQuery:t.querySelector('article'),fragmentQuery:!!t.content.querySelector('article'),clonedRoot:!!h.cloneNode(true).shadowRoot,serializable:r?.serializable??null};const c=document.createElement('div');document.body.append(c);const closed=c.attachShadow({mode:'closed'});closed.innerHTML='<p>Retained reference</p>';x.closedLookup=c.shadowRoot;x.closedReferenceReadable=closed.querySelector('p').textContent;try{customElements.define('InvalidName',class extends HTMLElement{})}catch(e){x.invalidName=e.name}customElements.define('reading-card',class extends HTMLElement{});try{customElements.define('reading-card',class extends HTMLElement{})}catch(e){x.duplicateName=e.name}return x}''')
   assert shadow['shadowCreated'] and shadow['lightChildRemains'] and shadow['assigned']==['assigned'] and shadow['templateQuery'] is None and shadow['fragmentQuery'];assert shadow['closedLookup'] is None and shadow['closedReferenceReadable']=='Retained reference' and shadow['invalidName']=='SyntaxError' and shadow['duplicateName']=='NotSupportedError'
   page.goto(base+'/fixtures/defaults.html');defaults=page.evaluate('''()=>{const f=document.querySelector('#field'),form=document.querySelector('#defaults');f.setAttribute('value','second');const pristine=f.value;f.value='edited';f.setAttribute('value','third');const dirty={current:f.value,default:f.defaultValue};form.reset();const group=form.elements.namedItem('contact');group.value='phone';return {pristine,dirty,afterReset:f.value,groupClass:group.constructor.name,groupValue:group.value,optionsLength:document.querySelector('#options').options.length,documentAllType:typeof document.all,documentAllFalsy:!document.all}}''');assert defaults=={'pristine':'second','dirty':{'current':'edited','default':'third'},'afterReset':'third','groupClass':'RadioNodeList','groupValue':'phone','optionsLength':2,'documentAllType':'undefined','documentAllFalsy':True}
   page.goto(base+'/fixtures/popover.html');popover=page.evaluate('''()=>{const a=document.querySelector('#auto'),m=document.querySelector('#manual'),n=document.querySelector('#none'),q=document.querySelector('#request');const x={emptyState:a.popover,invalidState:document.querySelector('#invalid').popover,hintState:document.querySelector('#hint').popover,requestCloseSupported:typeof q.requestClose==='function'};try{n.showPopover()}catch(e){x.noAttributeError=e.name}const detached=document.createElement('div');detached.popover='auto';try{detached.showPopover()}catch(e){x.disconnectedError=e.name}a.addEventListener('beforetoggle',e=>e.preventDefault(),{once:true});a.showPopover();x.openingCanceled=!a.matches(':popover-open');m.showPopover();document.querySelector('#outside').focus();x.nonmodalFocusAllowed=document.activeElement.id==='outside';m.hidePopover();q.show();try{q.showModal()}catch(e){x.nonmodalToModalError=e.name}q.close();q.showModal();if(x.requestCloseSupported){const stop=e=>e.preventDefault();q.addEventListener('cancel',stop);q.requestClose();x.cancelKeptOpen=q.open;q.removeEventListener('cancel',stop);q.requestClose('confirmed');x.requestClosed=!q.open;x.returnValue=q.returnValue}else q.close();return x}''')
   assert popover['emptyState']=='auto' and popover['invalidState']=='manual' and popover['noAttributeError']=='NotSupportedError' and popover['disconnectedError']=='InvalidStateError' and popover['openingCanceled'] and popover['nonmodalFocusAllowed'] and popover['nonmodalToModalError']=='InvalidStateError'
   if popover['requestCloseSupported']:assert popover['cancelKeptOpen'] and popover['requestClosed'] and popover['returnValue']=='confirmed'
   page.goto(base+'/fixtures/integrity.html');assert page.evaluate('window.demoIntegrityRuns')==1
   page.goto(base+'/cross-integrity');assert page.evaluate('window.demoIntegrityRuns')==1
   before=sum(r['path']=='/preload.js' and r['port']==servers[0].server_port for r in requests);page.goto(base+'/fixtures/preload.html');assert page.evaluate('window.demoIntegrityRuns')==1;preload_requests=sum(r['path']=='/preload.js' and r['port']==servers[0].server_port for r in requests)-before
   page.goto(base+'/nonce');nonce1=page.locator('#allowed').evaluate('(x)=>x.nonce');nonce_hidden=page.locator('#allowed').get_attribute('nonce');assert nonce_hidden=='' and len(nonce1)==24 and page.evaluate('window.nonceAllowed===true && window.nonceDisallowed===undefined')
   page.reload();nonce2=page.locator('#allowed').evaluate('(x)=>x.nonce');assert nonce1!=nonce2
   refs=[]
   for key,expected in [('none',None),('origin',base+'/')]:
    page.goto(base+'/fixtures/referrer.html');page.locator('#'+key).click();page.wait_for_url(other+'/sink');seen=next(r['referer'] for r in reversed(requests) if r['path']=='/sink' and r['port']==servers[1].server_port);assert seen==expected,(engine,key,seen,expected);refs.append({'policy':key,'observed_referer':seen,'navigation_received':True})
   page.goto(base+'/fixtures/until-found.html');page.evaluate('window.beforeMatch=0;document.querySelector("section").addEventListener("beforematch",()=>beforeMatch++)');page.locator('a').click();page.wait_for_timeout(100);until=page.evaluate('({beforeMatch,attributeRemoved:!document.querySelector("section").hasAttribute("hidden")})')
   page.set_viewport_size({'width':320,'height':800});reflow=[]
   for n in range(42,54):page.goto(base+f'/chapters/{n:02}.html',wait_until='load');assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+1'),(engine,n);reflow.append(n)
   rows.append({'engine':engine,'version':browser.version,'primary_examples_loaded':loaded,'keyboard_pointer_cases':['native details activation','modal initial/return focus and Escape','auto popover open/explicit dismiss','actual reorder by Enter and pointer, moved-item focus and status'],'disclosure_coalesced_events':coalesced,'command_observation':command_observation,'auto_command_observation':auto,'attribute_state':state,'shadow_observation':shadow,'default_state':defaults,'popover_observation':popover,'integrity_checks':{'matching_only_execution_count':1,'weaker_match_did_not_rescue_stronger_mismatch':True,'cors_enabled_only_execution_count':1,'preload_requests_observed':preload_requests,'nonce_attribute_hidden':True,'nonce_property_nonempty':True,'fresh_nonce_between_responses':True,'non_nonce_script_blocked':True},'referrer_navigation':refs,'until_found_observation':until,'chapter_reflow_at_320px':reflow,'limits':'Selected headless native DOM/keyboard/pointer/local-request checks only. No OS AT, actual touch/drag IME, full component/API review, performance guarantee or complete security approval.'});browser.close()
finally:
 for s in servers:s.shutdown();s.server_close()
nu=[]
for p in sorted(F.glob('*.html')):
 result=subprocess.run(['java','-Xss4m','-jar',str(R/'.cache/vnu/vnu.jar'),'--format','json',str(p)],capture_output=True,text=True,timeout=60);out=json.loads(result.stderr or result.stdout);errors=[x for x in out.get('messages',[]) if x.get('type')=='error'];invalid=p.name.startswith('invalid-') or p.name=='popover.html'
 if not invalid:assert not errors,(p.name,out)
 nu.append({'fixture':p.name,'invalid_under_standard':invalid,'checker_errors':len(errors),'checker_gap':invalid and not errors,'messages':out.get('messages',[]),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(O/'batch04-browser-checks.json').write_text(json.dumps({'date':'2026-10-15','candidate_fingerprint':publication_fingerprint(R),'result':'PASS','browsers':rows,'fixture_conformance':nu,'limits':['No independent chapter/answer approval','No OS assistive technology','No actual native drag/touch/IME review','Known-invalid controls remain invalid even if a checker misses them','No complete SRI/CSP/security or exhaustive API coverage','Not a tagged-PDF release']},ensure_ascii=False,indent=2)+'\n')
print('PASS: CH42–53 scoped three-engine interaction, DOM, SRI/CORS/CSP/referrer and reflow probes; checker limitations retained.')
