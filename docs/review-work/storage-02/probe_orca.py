"""Native-keyboard Orca follow-up. DOM variants are test fixtures, not published fixes."""
from pathlib import Path
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from functools import partial
from threading import Thread
from datetime import datetime,timezone
import json,subprocess,time,hashlib,traceback
from playwright.sync_api import sync_playwright,expect
R=Path.cwd();OUT=R/'.cache/orca';cases=[]
class H(SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(H,directory=str(R/'site')));Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_port}/'
def key(k):subprocess.run(['xdotool','key','--clearmodifiers',k],check=True);time.sleep(.4)
def clock():return datetime.now().strftime('%H:%M:%S.%f')
def native_goto(page,path,settled=True):
 key('ctrl+l');subprocess.run(['xdotool','type','--clearmodifiers','--delay','5',base+path],check=True)
 if settled:
  with page.expect_navigation(wait_until='load'):key('Return')
  time.sleep(4)
 else:key('Return');page.wait_for_load_state('load');time.sleep(1.4)
def record(id,page,start,**extra):
 time.sleep(2);cases.append({'id':id,'trace_window_start_local':start,'trace_window_end_local':clock(),'keyboard_focus':page.evaluate('({tag:document.activeElement.tagName,id:document.activeElement.id,text:(document.activeElement.innerText||document.activeElement.getAttribute("aria-label")||"").slice(0,200)})'),**extra});print(id,'completed',flush=True)
error=None
try:
 time.sleep(3)
 with sync_playwright() as p:
  b=p.chromium.launch(headless=False,args=['--force-renderer-accessibility','--ozone-platform=x11']);page=b.new_page(viewport={'width':1280,'height':800});page.goto(base);time.sleep(2)
  wins=subprocess.check_output(['xdotool','search','--onlyvisible','--class','chromium'],text=True).splitlines();subprocess.run(['xdotool','windowactivate','--sync',wins[-1]],check=True)
  for trial in range(1,4):
   native_goto(page,f'?settled={trial}');start=clock();key('Tab');expect(page.locator('.skip')).to_be_focused();record(f'settled-first-tab-{trial}',page,start)
   start=clock();key('Tab');key('shift+Tab');expect(page.locator('.skip')).to_be_focused();record(f'reverse-tab-to-skip-{trial}',page,start)
  for variant in ['original','title-focus','brief-description','title-and-description']:
   native_goto(page,'chapters/44.html?variant='+variant)
   if 'description' in variant:
    page.evaluate('''()=>{const p=document.createElement('p');p.id='lab-instructions';p.textContent='Edit the HTML source, then choose Run changes. The preview is isolated. Never paste secrets.';document.querySelector('.dialog-top').after(p);document.querySelector('#lab-dialog').setAttribute('aria-describedby',p.id)}''')
   if variant in ['title-focus','title-and-description']:
    page.evaluate('''()=>{document.querySelector('#lab-title').tabIndex=-1;document.querySelector('[data-open-lab]').addEventListener('click',()=>document.querySelector('#lab-title').focus())}''')
   # Reach the editor using native keys, bypassing sidebar links through the skip link.
   key('Tab');expect(page.locator('.skip')).to_be_focused();key('Return')
   for _ in range(12):
    key('Tab')
    if page.locator('[data-open-lab]').evaluate('(e)=>e===document.activeElement'):break
   expect(page.locator('[data-open-lab]')).to_be_focused()
   start=clock();key('Return');expect(page.locator('#lab-dialog')).to_be_visible()
   ax=page.context.new_cdp_session(page).send('Accessibility.getFullAXTree')['nodes']
   dialogs=[{'role':n.get('role',{}).get('value'),'name':n.get('name',{}).get('value'),'description':n.get('description',{}).get('value')} for n in ax if n.get('role',{}).get('value')=='dialog']
   record('dialog-'+variant,page,start,variant=variant,accessible_dialog_diagnostic=dialogs,fixture_note='Original served page with explicitly recorded runtime-only test modifications; not a published fix.')
   start=clock();key('Escape');expect(page.locator('#lab-dialog')).not_to_be_visible();expect(page.locator('[data-open-lab]')).to_be_focused();record('restore-'+variant,page,start)
  version=b.version;b.close()
except Exception as e:
 error=traceback.format_exc();print(error,flush=True);version=None
finally:server.shutdown();server.server_close()
report={'date':datetime.now(timezone.utc).isoformat(),'error':error,'result':'NATIVE_TASKS_RECORDED' if error is None else 'SETUP_OR_TASK_FAILURE','browser_version':version,'orca_version':subprocess.check_output(['orca','--version'],text=True,stderr=subprocess.DEVNULL).strip(),'baseline_commit':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'baseline_chapter_sha256':hashlib.sha256((R/'site/chapters/44.html').read_bytes()).hexdigest(),'independent':False,'human_listener':False,'scope':'Three settled-load skip-link trials plus original and three runtime-only dialog fixture variants, actual headed Chromium/Orca and native X11 keys. CDP dialog values are diagnostic only, not substituted for Orca output.','cases':cases}
(OUT/'followup.json').write_text(json.dumps(report,indent=2)+'\n');print(report['result'],len(cases),'cases',flush=True)
