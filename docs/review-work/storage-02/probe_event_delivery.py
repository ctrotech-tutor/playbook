"""Controlled follow-up: obtaining a Storage object versus reading its map.
Run from repository root: python3 docs/review-work/storage-02/probe_event_delivery.py REPORT.json
No production data; one fresh context per observation; bounded event windows.
"""
from pathlib import Path
from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
from threading import Thread
from datetime import datetime,timezone
import json,sys
from playwright.sync_api import sync_playwright
class H(BaseHTTPRequestHandler):
 def do_GET(self):
  body=b'<!doctype html><html lang="en"><meta charset="utf-8"><title>Disposable event initialization probe</title><h1>Storage probe</h1>'
  self.send_response(200);self.send_header('Content-Type','text/html; charset=utf-8');self.end_headers();self.wfile.write(body)
 def log_message(self,*a):pass
server=ThreadingHTTPServer(('127.0.0.1',0),H);Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_port}'
modes={'listener-only':'void 0','object-getter':'window.area=localStorage','length-read':'window.area=localStorage;void area.length','missing-entry-read':'window.area=localStorage;area.getItem("never-present")','peer-write':'window.area=localStorage;area.setItem("peer-initialization","ready")'}
rows=[]
try:
 with sync_playwright() as pw:
  for engine in ['chromium','firefox','webkit']:
   b=getattr(pw,engine).launch()
   for name,init in modes.items():
    for repetition in range(1,4):
     ctx=b.new_context();mut=ctx.new_page();mut.goto(base+'/mutator');peer=ctx.new_page();peer.goto(base+'/unrelated-peer')
     peer.evaluate('window.received=[];addEventListener("storage",e=>received.push({key:e.key,oldValue:e.oldValue,newValue:e.newValue,url:e.url,receivingArea:e.storageArea===localStorage}))')
     peer.evaluate(init)
     state=peer.evaluate('({visibility:document.visibilityState,focused:document.hasFocus(),opener:!!window.opener,origin:location.origin,isolated:crossOriginIsolated})')
     mut.evaluate('localStorage.setItem("follow-up-key","new-value")');peer.wait_for_timeout(800)
     observed=peer.evaluate('({events:received.slice(),sharedValue:localStorage.getItem("follow-up-key")})')
     assert observed['sharedValue']=='new-value'
     assert all(e=={'key':'follow-up-key','oldValue':None,'newValue':'new-value','url':base+'/mutator','receivingArea':True} for e in observed['events'])
     rows.append({'engine':engine,'version':b.version,'initialization':name,'repetition':repetition,'window_ms':800,'state_before_mutation':state,'actual':observed,'delivery':'OBSERVED' if observed['events'] else 'NOT_OBSERVED_WITHIN_WINDOW'})
     ctx.close()
    print(engine,name,[len(r['actual']['events']) for r in rows if r['engine']==engine and r['initialization']==name],flush=True)
   b.close()
finally:server.shutdown();server.server_close()
report={'date':datetime.now(timezone.utc).isoformat(),'scope':'Fresh unrelated Playwright pages in one browser context; same origin; listener registration precedes initialization and mutation. Shared getter value measured after event window. Not a Safari/device matrix, full WPT run, or proof of an engine-internal cause.','independent':False,'result':'CONTROLLED_OBSERVATIONS_RECORDED','observations':rows}
p=Path(sys.argv[1]);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(report,indent=2)+'\n')
