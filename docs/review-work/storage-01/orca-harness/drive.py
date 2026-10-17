from pathlib import Path
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from threading import Thread
from functools import partial
from datetime import datetime,timezone
import subprocess,time,json,traceback,hashlib
from playwright.sync_api import sync_playwright,expect
R=Path.cwd();OUT=R/'.cache/orca';trace=OUT/'orca-debug.log';actions=[];cases=[]
class H(SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(H,directory=str(R/'site')));Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_port}/'
def key(value):subprocess.run(['xdotool','key','--clearmodifiers',value],check=True);time.sleep(.45)
def type_text(value):subprocess.run(['xdotool','type','--clearmodifiers','--delay','15',value],check=True);time.sleep(.6)
def speech():
 return [line for line in trace.read_text(errors='replace').splitlines() if 'SPEECH OUTPUT:' in line] if trace.exists() else []
def focus(page):return page.evaluate('({tag:document.activeElement.tagName,id:document.activeElement.id,text:(document.activeElement.innerText||document.activeElement.getAttribute("aria-label")||"").slice(0,150)})')
def checkpoint(name,page,offset):
 time.sleep(1.1);cases.append({'id':name,'result':'PASS_KEYBOARD_AND_DOM_CHECK','focus':focus(page),'trace_window_start_local':offset,'trace_window_end_local':datetime.now().strftime('%H:%M:%S.%f'),'orca_speech_lines':[]});print(name,'keyboard and DOM check complete',flush=True)
def goto(page,path):
 key('ctrl+l');type_text(base+path);key('Return');page.wait_for_load_state('load');time.sleep(1.4)
def tab_to(page,selector,limit=60):
 for i in range(limit):
  key('Tab')
  if page.locator(selector).evaluate('(e)=>e===document.activeElement'):return i+1
 raise AssertionError('Keyboard did not reach '+selector)
error=None
try:
 time.sleep(3)
 with sync_playwright() as pw:
  b=pw.chromium.launch(headless=False,args=['--force-renderer-accessibility','--ozone-platform=x11'])
  page=b.new_page(viewport={'width':1280,'height':800});page.goto(base,wait_until='load');time.sleep(2)
  wins=subprocess.check_output(['xdotool','search','--onlyvisible','--class','chromium'],text=True).splitlines();assert wins,'No headed Chromium window'
  subprocess.run(['xdotool','windowactivate','--sync',wins[-1]],check=True)
  goto(page,'');offset=datetime.now().strftime("%H:%M:%S.%f");key('Tab');assert page.locator('.skip').evaluate('(e)=>e===document.activeElement');checkpoint('skip-link-reached-by-native-tab',page,offset)
  offset=datetime.now().strftime("%H:%M:%S.%f");key('Return');key('Tab');assert page.evaluate('Boolean(document.activeElement.closest("main"))');checkpoint('skip-link-moves-sequential-focus-into-main',page,offset)
  goto(page,'');offset=datetime.now().strftime("%H:%M:%S.%f");tabs=tab_to(page,'[data-open-search]');key('Return');expect(page.locator('#search-dialog')).to_be_visible();expect(page.locator('#book-search')).to_be_focused();checkpoint('search-dialog-open-label-and-focus',page,offset)
  offset=datetime.now().strftime("%H:%M:%S.%f");type_text('HTMLInputElement');expect(page.locator('#search-results a').first).to_be_visible();time.sleep(1);checkpoint('search-input-and-result-status',page,offset)
  offset=datetime.now().strftime("%H:%M:%S.%f");key('Escape');expect(page.locator('#search-dialog')).not_to_be_visible();expect(page.locator('[data-open-search]')).to_be_focused();checkpoint('search-escape-restores-trigger-focus',page,offset)
  page.set_viewport_size({'width':390,'height':800});goto(page,'chapters/44.html');offset=datetime.now().strftime("%H:%M:%S.%f");tabs=tab_to(page,'[data-chapters-toggle]');key('space');assert page.locator('[data-chapters-toggle]').get_attribute('aria-expanded')=='true';expect(page.locator('#chapter-navigation')).to_be_visible();checkpoint('narrow-viewport-chapter-navigation-expands',page,offset)
  offset=datetime.now().strftime("%H:%M:%S.%f");key('space');assert page.locator('[data-chapters-toggle]').get_attribute('aria-expanded')=='false';checkpoint('chapter-navigation-collapses',page,offset)
  page.set_viewport_size({'width':1280,'height':800});goto(page,'chapters/44.html');offset=datetime.now().strftime("%H:%M:%S.%f");tab_to(page,'[data-open-lab]');key('Return');expect(page.locator('#lab-dialog')).to_be_visible();checkpoint('practice-lab-opens-with-native-keyboard',page,offset)
  offset=datetime.now().strftime("%H:%M:%S.%f");key('Escape');expect(page.locator('#lab-dialog')).not_to_be_visible();expect(page.locator('[data-open-lab]')).to_be_focused();checkpoint('practice-lab-escape-restores-trigger',page,offset)
  versions={'browser':'Chromium','browser_version':b.version,'playwright':subprocess.check_output(['python3','-m','playwright','--version'],text=True).strip(),'orca':subprocess.check_output(['/usr/bin/orca','--version'],text=True,stderr=subprocess.DEVNULL).strip()}
  tree=subprocess.run(['/usr/bin/python3','-c','import pyatspi;d=pyatspi.Registry.getDesktop(0);print([(a.name,a.getRoleName(),a.childCount) for a in d])'],capture_output=True,text=True,timeout=20);(OUT/'at-spi-applications.txt').write_text(tree.stdout+tree.stderr);assert tree.returncode==0
  b.close()
except Exception as e:error=str(e);(OUT/'error.txt').write_text(traceback.format_exc());print(traceback.format_exc(),flush=True);versions={'orca':subprocess.check_output(['/usr/bin/orca','--version'],text=True,stderr=subprocess.DEVNULL).strip()}
finally:server.shutdown();server.server_close()
utterances=speech();report={'date':datetime.now(timezone.utc).isoformat(),'result':'KEYBOARD_TASKS_COMPLETED_PENDING_SPEECH_REVIEW' if error is None else 'FINDINGS_OR_SETUP_FAILURE','error':error,'versions':versions,'served_site_base_commit':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'site_was_not_rebuilt_after_new_manuscript_draft':True,'environment':'Private Xvfb X11, Openbox, private D-Bus/AT-SPI session, actual Orca process and native X11 keyboard events; headed Chromium, speech-dispatcher/eSpeak and a PulseAudio null sink. Not a Playwright accessibility-tree substitute.','trace_assignment':'Speech must be parsed after session teardown using recorded local-clock windows; live trace reads can lag due to debug-file buffering.', 'audio':'Actual PulseAudio monitor captured to speech.raw; null sink is not a claim that a human listened.','independent':False,'human_listener':False,'scope':'Bounded desktop-Linux actual-AT task evidence. Not NVDA/JAWS/VoiceOver, real mobile AT, full book comprehension or independent WCAG certification. Native keyboard assertions and Orca speech traces are recorded separately.','cases':cases,'orca_speech_line_count':len(utterances),'raw_trace_sha256':hashlib.sha256(trace.read_bytes()).hexdigest() if trace.exists() else None}
(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n');(OUT/'speech-output.txt').write_text('\n'.join(utterances)+'\n');print(report['result'],len(cases),'tasks;',len(utterances),'Orca speech-output lines',flush=True)
