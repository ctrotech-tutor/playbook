"""Run axe and narrow reflow checks on the actual compiled updated reading pages."""
from pathlib import Path
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from functools import partial
from threading import Thread
from datetime import datetime,timezone
import hashlib,json,sys
from playwright.sync_api import sync_playwright
R=Path.cwd();D=R/'dist';rows=[]
class H(SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(H,directory=str(D)));Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_port}/'
try:
 with sync_playwright() as pw:
  for name in ['chromium','firefox','webkit']:
   b=getattr(pw,name).launch();ctx=b.new_context();page=ctx.new_page()
   for path in ['reference/api/storage.html','accessibility.html']:
    for width in [1280,390]:
     page.set_viewport_size({'width':width,'height':900});page.goto(base+path,wait_until='networkidle');page.evaluate('document.fonts.ready')
     page.add_script_tag(path=str(R/'node_modules/axe-core/axe.min.js'))
     result=page.evaluate('async()=>await axe.run(document,{runOnly:{type:"tag",values:["wcag2a","wcag2aa","wcag21aa","wcag22aa"]}})')
     overflow=page.evaluate('({width:innerWidth,scroll:document.documentElement.scrollWidth})')
     rows.append({'engine':name,'version':b.version,'path':path,'sha256':hashlib.sha256((D/path).read_bytes()).hexdigest(),'viewport_width':width,'axe_version':result['testEngine']['version'],'violations':result['violations'],'incomplete':result['incomplete'],'reflow':overflow,'passed':not result['violations'] and overflow['scroll']<=overflow['width']+1})
     print(name,path,width,'PASS' if rows[-1]['passed'] else 'FINDING',flush=True)
   b.close()
finally:server.shutdown();server.server_close()
p=R/'docs/review-work/storage-02/updated-page-browser-results.json';p.write_text(json.dumps({'date':datetime.now(timezone.utc).isoformat(),'result':'PASS_SCOPED_AUTOMATED_CHECKS' if all(r['passed'] for r in rows) else 'OPEN_AUTOMATED_FINDINGS','scope':'Two actual compiled pages in three engines at desktop and 390px; axe WCAG rule subsets and page-level horizontal overflow. Incomplete/manual targets retained. Not independent WCAG approval, actual AT or whole-site recertification.','observations':rows},indent=2)+'\n')
if not all(r['passed'] for r in rows):raise SystemExit(1)
