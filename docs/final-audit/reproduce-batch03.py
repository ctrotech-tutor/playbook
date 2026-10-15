"""Run from an installed candidate checkout after tools/build.py --pdf.
Uses controlled loopback receivers and fictional entries. No live backend or OS AT approval.
Requires repository verification dependencies, installed Playwright engines and Java 21.
"""
from pathlib import Path
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from threading import Thread
from urllib.parse import urlsplit, parse_qs
import hashlib, json, subprocess, sys
from playwright.sync_api import sync_playwright
R=Path.cwd();O=Path(__file__).resolve().parent;F=O/'batch03-fixtures';F.mkdir(exist_ok=True)
sys.path.insert(0,str(R/'tools'))
from fingerprint import publication_fingerprint
requests=[]
def fixture(name,body,head=''):
 p=F/(name+'.html');p.write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Audit '+name+'</title>'+head+'</head><body><h1>Fictional '+name+' fixture</h1>'+body+'</body></html>');return p
fixture('entries','''<form id="f"><label>Reader <input name="reader" value="Demo Reader"></label><label>Disabled <input name="disabled" value="omit" disabled></label><label>Read only <input name="readonly" value="keep" readonly></label><label><input type="checkbox" name="unchecked" value="no">Unchecked</label><label><input type="checkbox" name="topic" value="history" checked>History</label><label><input type="checkbox" name="topic" value="fiction" checked>Fiction</label><label><input type="checkbox" name="defaultCheck" checked>Default checkbox</label><fieldset disabled><legend><label>Legend entry <input name="legendEntry" value="keep"></label></legend><label>Group entry <input name="groupEntry" value="omit"></label></fieldset><label>Writing name <input name="display" dirname="display.dir" dir="auto" value="مريم"></label><input type="hidden" name="_charset_" value="not-authoritative"><label>Empty file <input type="file" name="emptyFile"></label><label>Result <output id="result" name="result">2</output></label><button id="send" type="submit" name="action" value="apply">Apply</button><button id="ordinary" type="button">Ordinary</button></form><fieldset form="f"><legend>External group</legend><label>Unassociated <input id="outside" name="outside" value="omit"></label><label>Associated <input id="external" name="external" form="f" value="keep"></label></fieldset><form id="other"><button id="foreign" type="submit">Other submit</button></form>''')
fixture('states','''<label>Quantity <input id="number" type="number" step="1"></label><label>Date <input id="date" type="date" value="2026-10-15"></label><label>Local time <input id="local" type="datetime-local" value="2026-10-15T09:30"></label><label>Plain text <input id="text" type="text"></label><label>File <input id="file" type="file" accept=".pdf"></label><label>Slider <input id="range" type="range"></label><label>Colour <input id="colour" type="color"></label><label>Pattern <input id="pattern" pattern="[0-9]{6}" required></label><label>Length <input id="length" minlength="4"></label><label>Longer text <textarea id="long">initial</textarea></label><label>Branch <select id="select" required><option value="">Choose</option><option value="central">Central</option></select></label><label>Progress <progress id="progress"></progress></label><label>Seats <meter id="meter" min="0" max="20" low="5" high="15" optimum="8" value="12">12 seats</meter></label>''')
fixture('wire','''<iframe title="Local receipt" name="receipt"></iframe><form id="f" action="/sink" method="get" target="receipt"><label>Query <input name="q" value="red room"></label><button id="get" type="submit" name="action" value="search">Get</button><button id="post" type="submit" name="action" value="save" formaction="/sink/alternate" formmethod="post">Post</button></form><form id="upload" action="/sink/upload" method="post" enctype="multipart/form-data" target="receipt"><label>Proof <input id="proof" type="file" name="proof"></label><button id="upload-send" type="submit">Upload fiction</button></form><form id="validation" action="/sink/bypass" target="receipt"><label>Required <input id="required" name="required" required></label><button id="validate-send" type="submit">Validate</button></form><dialog id="dialog"><form method="dialog"><button id="done" value="confirmed">Close</button></form></dialog>''')
fixture('custom-select','''<label for="choice">Shelf</label><select id="choice" name="shelf"><button><selectedcontent></selectedcontent></button><option value="fiction" label="Fiction label">Fiction content</option><option value="history" label="History label">History content</option></select>''')
fixture('foreign','''<canvas id="canvas"><p>The fictional chart has one solid green rectangle.</p></canvas><math xmlns="http://www.w3.org/1998/Math/MathML"><msup><mi>x</mi><mn>2</mn></msup></math>''')
fixture('invalid-number-pattern','<label>Quantity <input type="number" pattern="[0-9]+"></label>')
fixture('invalid-track-defaults','<video><track src="one.vtt" kind="captions" srclang="en" default><track src="two.vtt" kind="captions" srclang="fr" default></video>')
fixture('invalid-selectedcontent','<p><selectedcontent></selectedcontent></p>')
fixture('invalid-select-placeholder','<label>Required branch <select required><option value="central">Central</option><option value="east">East</option></select></label>')
class Handler(SimpleHTTPRequestHandler):
 def translate_path(self,path):
  p=urlsplit(path).path
  if p.startswith('/fixtures/'):return str(F/p.removeprefix('/fixtures/'))
  if p in ['/foreign.png','/cors.png']:return str(R/'build/site/assets/media/floor-plan-400.png')
  return str(R/'build/site'/p.lstrip('/'))
 def receipt(self,body):
  requests.append({'method':self.command,'path':self.path,'content_type':self.headers.get('Content-Type',''),'body':body.decode('utf-8','replace')})
  data=b'<!doctype html><html lang="en"><title>Local receipt</title><h1>Fictional request received locally</h1></html>'
  self.send_response(200);self.send_header('Content-Type','text/html; charset=utf-8');self.send_header('Content-Length',str(len(data)));self.end_headers();self.wfile.write(data)
 def do_GET(self):
  if urlsplit(self.path).path.startswith('/sink'):self.receipt(b'')
  else:
   try:super().do_GET()
   except (BrokenPipeError,ConnectionResetError):pass  # Client can cancel a media read.
 def end_headers(self):
  if urlsplit(self.path).path=='/cors.png':self.send_header('Access-Control-Allow-Origin','*')
  super().end_headers()
 def do_POST(self):self.receipt(self.rfile.read(int(self.headers.get('Content-Length','0'))))
 def log_message(self,*args):pass
servers=[]
for _ in range(2):
 s=ThreadingHTTPServer(('127.0.0.1',0),Handler);Thread(target=s.serve_forever,daemon=True).start();servers.append(s)
base='http://127.0.0.1:'+str(servers[0].server_port);foreign='http://127.0.0.1:'+str(servers[1].server_port)
rows=[]
try:
 with sync_playwright() as pw:
  for engine in ['chromium','firefox','webkit']:
   browser=getattr(pw,engine).launch(args=['--no-sandbox'] if engine=='chromium' else [])
   context=browser.new_context();page=context.new_page();loaded=[]
   for n in range(28,42):
    response=page.goto(base+f'/examples/{n:02}.html',wait_until='load');assert response.status==200
    assert page.locator('body').count()==1
    if n!=32:assert page.locator('body').inner_text().strip()
    loaded.append(n)
    if n==28:
     page.wait_for_function('()=>document.querySelector("img").complete')
     assert page.locator('img').evaluate('(x)=>x.naturalWidth===640 && x.naturalHeight===360')
    if n==31:
     img=page.locator('img');page.wait_for_function('()=>document.querySelector("img").complete');img.click(position={'x':158,'y':281});assert page.url.endswith('#reading-room')
     page.goto(base+'/examples/31.html');page.locator('area').focus();page.keyboard.press('Enter');assert page.url.endswith('#reading-room')
    if n==32:
     frame=page.frame_locator('iframe');assert frame.locator('h1').inner_text()=='Quiet study';assert frame.locator('p').inner_text()=='Keep calls outside the reading room.'
   broken_image=page.evaluate('''async()=>{const x=new Image();x.src='/deliberately-missing-image.png';let error=null;try{await x.decode()}catch(e){error=e.name}return {complete:x.complete,naturalWidth:x.naturalWidth,decodeError:error}}''')
   assert broken_image=={'complete':True,'naturalWidth':0,'decodeError':'EncodingError'}
   # Selection observations use fresh contexts, not exact filename promises.
   responsive=[]
   for width,dpr in [(360,1),(1000,1),(360,2)]:
    c=browser.new_context(viewport={'width':width,'height':700},device_scale_factor=dpr);p=c.new_page();p.goto(base+'/examples/29.html')
    p.wait_for_function('()=>document.querySelector("img").complete && document.querySelector("img").naturalWidth>0')
    v=p.locator('img').evaluate('(x)=>({currentSrc:x.currentSrc,naturalWidth:x.naturalWidth,renderedWidth:x.getBoundingClientRect().width})')
    assert abs(v['renderedWidth']-(width if width<=640 else width/2))<1
    assert any(v['currentSrc'].endswith(f'floor-plan-{w}.png') for w in [400,800,1200])
    responsive.append({'viewport':width,'device_scale_factor':dpr,**v});c.close()
   page.goto(base+'/examples/30.html');page.wait_for_function('()=>document.querySelector("video").readyState>=1',timeout=20000)
   media=page.locator('video').evaluate('(v)=>({width:v.videoWidth,height:v.videoHeight,duration:v.duration,currentSrc:v.currentSrc})')
   assert media['width']==640 and media['height']==360 and abs(media['duration']-4)<.25
   page.evaluate('''()=>{const v=document.querySelector('video');v.textTracks[0].mode='hidden';const b=document.createElement('button');b.id='audit-play';b.textContent='Play local fixture';b.onclick=()=>{v.play().then(()=>window.__played=true).catch(e=>window.__playError=e.name)};document.body.append(b)}''')
   page.locator('#audit-play').click();page.wait_for_function('()=>window.__played || window.__playError',timeout=20000);assert page.evaluate('window.__played') is True
   page.wait_for_function('()=>document.querySelector("track").readyState===2',timeout=20000)
   cue=page.locator('track').evaluate('(t)=>({readyState:t.readyState,cues:[...t.track.cues].map(c=>({text:c.text,start:c.startTime,end:c.endTime}))})')
   assert cue['cues']==[{'text':'[Short tone]','start':0,'end':.6}]
   page.locator('video').evaluate('(v)=>{v.pause();v.currentTime=.25}')
   page.wait_for_function('()=>document.querySelector("video").textTracks[0].activeCues?.length===1')
   # Form entry-list construction, not a live service.
   page.goto(base+'/fixtures/entries.html')
   entry=page.evaluate('''()=>{const f=document.querySelector('#f');let events=0;f.addEventListener('formdata',e=>{events++;e.formData.append('added','local')});const simplify=d=>[...d].map(([k,v])=>[k,v instanceof File?{name:v.name,size:v.size,type:v.type}:v]);const plain=simplify(new FormData(f));const submitter=simplify(new FormData(f,document.querySelector('#send')));const o=document.querySelector('#result');o.value='4';const outputBefore={value:o.value,defaultValue:o.defaultValue,willValidate:o.willValidate};f.reset();return {plain,submitter,events,outputBefore,outputAfter:o.value,externalOwner:document.querySelector('#external').form?.id,outsideOwner:document.querySelector('#outside').form?.id??null,legendDisabled:document.querySelector('[name=legendEntry]').matches(':disabled'),groupDisabled:document.querySelector('[name=groupEntry]').matches(':disabled')}}''')
   plain=entry['plain'];keys=[v[0] for v in plain]
   assert not {'disabled','unchecked','groupEntry','result','outside','action'}.intersection(keys)
   assert [v[1] for v in plain if v[0]=='topic']==['history','fiction']
   assert ['defaultCheck','on'] in plain and ['_charset_','UTF-8'] in plain and ['display.dir','rtl'] in plain
   assert next(v[1] for v in plain if v[0]=='emptyFile')=={'name':'','size':0,'type':'application/octet-stream'}
   assert ['action','apply'] in entry['submitter'] and entry['events']==2
   assert entry['outputBefore']=={'value':'4','defaultValue':'2','willValidate':False} and entry['outputAfter']=='2'
   assert entry['externalOwner']=='f' and entry['outsideOwner'] is None and entry['legendDisabled'] is False and entry['groupDisabled'] is True
   exceptions=page.evaluate('''()=>{const f=document.querySelector('#f');const r={};for(const [key,id] of [['nonSubmit','ordinary'],['foreignOwner','foreign']])try{f.requestSubmit(document.getElementById(id));r[key]='no exception'}catch(e){r[key]=e.name}return r}''')
   assert exceptions=={'nonSubmit':'TypeError','foreignOwner':'NotFoundError'}
   reentrant=page.evaluate('''()=>{let result=null;const f=document.querySelector('#f');f.addEventListener('formdata',()=>{try{new FormData(f);result='no exception'}catch(e){result=e.name}},{once:true});new FormData(f);return result}''');assert reentrant=='InvalidStateError'
   # State-specific conversion, invalidity and real edits.
   page.goto(base+'/fixtures/states.html')
   states=page.evaluate('''()=>{const n=document.querySelector('#number'),d=document.querySelector('#date'),l=document.querySelector('#local'),f=document.querySelector('#file'),t=document.querySelector('#text');const r={emptyNumberNaN:Number.isNaN(n.valueAsNumber),dateUTC:d.valueAsDate.toISOString(),localDate:l.valueAsDate,rangeDefault:document.querySelector('#range').value,colourDefault:document.querySelector('#colour').value};for(const [key,fn] of [['infinite',()=>n.valueAsNumber=Infinity],['unsupportedNumber',()=>t.valueAsNumber=1],['unsupportedDate',()=>l.valueAsDate=new Date()],['filePath',()=>f.value='private.pdf'],['anyStep',()=>{n.step='any';n.stepUp()}]])try{fn();r[key]='no exception'}catch(e){r[key]=e.name}n.step='1';n.value='2.5';r.stepMismatch=n.validity.stepMismatch;const p=document.querySelector('#pattern');p.value='123456';r.validPattern=p.validity.valid;p.value='x123456x';r.wholeValueMismatch=p.validity.patternMismatch;p.value='';r.emptyRequired=p.validity.valueMissing;const s=document.querySelector('#select');r.placeholderMissing=s.validity.valueMissing;s.value='central';r.selectValid=s.validity.valid;const v=document.querySelector('#progress');r.indeterminatePosition=v.position;v.value=0;r.determinatePosition=v.position;r.progressMax=v.max;const a=document.querySelector('#long');a.value='changed';r.textareaDefault=a.defaultValue;r.textareaCurrent=a.value;r.colourExtensions={alpha:'alpha' in HTMLInputElement.prototype,colorSpace:'colorSpace' in HTMLInputElement.prototype};return r}''')
   for k,v in {'emptyNumberNaN':True,'dateUTC':'2026-10-15T00:00:00.000Z','localDate':None,'rangeDefault':'50','colourDefault':'#000000','infinite':'TypeError','unsupportedNumber':'InvalidStateError','unsupportedDate':'InvalidStateError','filePath':'InvalidStateError','anyStep':'InvalidStateError','stepMismatch':True,'validPattern':True,'wholeValueMismatch':True,'emptyRequired':True,'placeholderMissing':True,'selectValid':True,'indeterminatePosition':-1,'determinatePosition':0,'progressMax':1,'textareaDefault':'initial','textareaCurrent':'changed'}.items():assert states[k]==v,(engine,k,states[k])
   page.locator('#length').focus();page.keyboard.type('abc');assert page.locator('#length').evaluate('(x)=>x.validity.tooShort')
   page.keyboard.type('d');assert page.locator('#length').evaluate('(x)=>x.validity.valid')
   page.locator('#pattern').evaluate('(x)=>x.setCustomValidity("Fix the fictional condition")');assert page.locator('#pattern').evaluate('(x)=>x.validity.customError')
   page.locator('#pattern').fill('123456');page.locator('#pattern').evaluate('(x)=>x.setCustomValidity("")');assert page.locator('#pattern').evaluate('(x)=>x.validity.valid')
   # Real local native requests, including an override and multipart body.
   page.goto(base+'/fixtures/wire.html')
   with page.expect_response(lambda r:urlsplit(r.url).path=='/sink'):page.locator('#get').click()
   get=requests[-1];assert get['method']=='GET' and parse_qs(urlsplit(get['path']).query)=={'q':['red room'],'action':['search']}
   with page.expect_response(lambda r:urlsplit(r.url).path=='/sink/alternate'):page.locator('#post').click()
   post=requests[-1];assert post['method']=='POST' and parse_qs(post['body'])=={'q':['red room'],'action':['save']}
   page.locator('#proof').set_input_files({'name':'fictional.pdf','mimeType':'application/pdf','buffer':b'fictional bytes, not a valid PDF'})
   with page.expect_response(lambda r:urlsplit(r.url).path=='/sink/upload'):page.locator('#upload-send').click()
   upload=requests[-1];assert upload['method']=='POST' and 'multipart/form-data; boundary=' in upload['content_type'] and 'fictional bytes, not a valid PDF' in upload['body'] and 'filename="fictional.pdf"' in upload['body']
   page.evaluate('''()=>{window.__submit=0;window.__invalid=0;const f=document.querySelector('#validation');f.addEventListener('submit',()=>window.__submit++);f.addEventListener('invalid',()=>window.__invalid++,true);f.requestSubmit()}''')
   assert page.evaluate('[window.__submit,window.__invalid]')==[0,1]
   page.evaluate('window.__invalid=0')
   with page.expect_response(lambda r:urlsplit(r.url).path=='/sink/bypass'):page.evaluate('document.querySelector("#validation").submit()')
   assert page.evaluate('[window.__submit,window.__invalid]')==[0,0]
   page.evaluate('document.querySelector("#dialog").showModal()');before=len(requests);page.locator('#done').click()
   assert page.locator('#dialog').evaluate('(d)=>!d.open && d.returnValue==="confirmed"') and len(requests)==before
   # Namespace, bitmap reset and controlled cross-origin tainting.
   page.goto(base+'/fixtures/foreign.html')
   canvas=page.evaluate('''()=>{const c=document.querySelector('canvas'),x=c.getContext('2d');const r={defaultSize:[c.width,c.height],differentContext:c.getContext('bitmaprenderer')===null,mathNamespace:document.querySelector('math').namespaceURI};x.fillStyle='#00ff00';x.fillRect(0,0,1,1);r.before=[...x.getImageData(0,0,1,1).data];c.width=c.width;r.after=[...x.getImageData(0,0,1,1).data];r.resetFill=x.fillStyle;return r}''')
   assert canvas=={'defaultSize':[300,150],'differentContext':True,'mathNamespace':'http://www.w3.org/1998/Math/MathML','before':[0,255,0,255],'after':[0,0,0,0],'resetFill':'#000000'}
   taint=page.evaluate('''async(url)=>{const i=new Image();i.src=url;await i.decode();const c=document.createElement('canvas');c.getContext('2d').drawImage(i,0,0);const r={};for(const [key,fn] of [['toDataURL',()=>c.toDataURL()],['toBlob',()=>c.toBlob(()=>{})]])try{fn();r[key]='no exception'}catch(e){r[key]=e.name}return r}''',foreign+'/foreign.png');assert taint=={'toDataURL':'SecurityError','toBlob':'SecurityError'}
   cors=page.evaluate('''async(url)=>{const i=new Image();i.crossOrigin='anonymous';i.src=url;await i.decode();const c=document.createElement('canvas');c.getContext('2d').drawImage(i,0,0);return c.toDataURL().startsWith('data:image/png')}''',foreign+'/cors.png');assert cors is True
   page.goto(base+'/fixtures/custom-select.html')
   page.add_style_tag(content='select,::picker(select){appearance:base-select}')
   custom=page.evaluate('''()=>({interfaceExposed:'HTMLSelectedContentElement' in window,elementRetained:!!document.querySelector('selectedcontent'),initial:document.querySelector('selectedcontent')?.textContent??null,cssOptInSupported:CSS.supports('appearance','base-select')})''')
   page.locator('#choice').select_option('history');custom['afterSelection']=page.locator('selectedcontent').text_content() if page.locator('selectedcontent').count() else None
   reflow=[];page.set_viewport_size({'width':320,'height':800})
   for n in range(28,42):
    page.goto(base+f'/chapters/{n:02}.html',wait_until='load');assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+1'),(engine,n);reflow.append(n)
   rows.append({'engine':engine,'version':browser.version,'primary_examples_loaded':loaded,'chapters_without_page_level_overflow_at_320px':reflow,'responsive_observations':responsive,'broken_image_observation':broken_image,'media_decoding':media,'text_track':cue,'form_entries':entry,'submitter_exceptions':exceptions,'formdata_reentrant_exception':reentrant,'state_API_results':states,'native_requests':[get,post,upload],'submission_checks':{'requestSubmit_invalid_events':1,'requestSubmit_submit_events_while_invalid':0,'direct_submit_invalid_events':0,'direct_submit_submit_events':0,'dialog_closed_without_application_request':True},'canvas':canvas,'cross_origin_export_exceptions':taint,'cors_enabled_export_succeeded':cors,'selectedcontent_observation':custom,'limits':'DOM/native-request/headless-decoding observations, not OS AT or caption usability approval. File bytes are deliberately fictional and illustrate why metadata is not validation. New-feature observations are not universal stable-browser claims.'})
   browser.close()
finally:
 for s in servers:s.shutdown();s.server_close()
jar=R/'.cache/vnu/vnu.jar';nu=[]
for p in sorted(F.glob('*.html')):
 proc=subprocess.run(['java','-Xss4m','-jar',str(jar),'--format','json',str(p)],capture_output=True,text=True,timeout=60);result=json.loads(proc.stderr or proc.stdout)
 errors=[m for m in result.get('messages',[]) if m.get('type')=='error'];expected=p.name.startswith('invalid-')
 checker_gap=p.name=='invalid-selectedcontent.html'
 if checker_gap:assert not errors,(p.name,result)  # Preserve observed checker gap, not authoring approval.
 else:assert bool(errors)==expected,(p.name,result)
 nu.append({'fixture':p.name,'expected_invalid_under_standard':expected,'checker_detected_error':bool(errors),'known_checker_gap':checker_gap,'exit_code':proc.returncode,'messages':result.get('messages',[]),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
assets={}
for p in sorted((R/'assets/media').glob('*')):assets[p.relative_to(R).as_posix()]={'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
report={'date':'2026-10-15','candidate_fingerprint':publication_fingerprint(R),'result':'PASS','browsers':rows,'fixture_conformance':nu,'supplied_media_assets':assets,'limits':['No independent exercise-key approval','No OS assistive-technology run','No human listening/caption usability review','No production application endpoint','No exhaustive input/API/Canvas coverage','No complete security or tagged-PDF approval']}
(O/'batch03-browser-checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('PASS: CH28–41 scoped checks in three engines. Nu accepts five positive HTML fixtures and rejects three invalid controls; one known selectedcontent placement gap is recorded, not approved.')
