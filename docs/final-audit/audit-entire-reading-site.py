"""Every generated reading page, not a selected-page accessibility sample.
Usage: python audit-entire-reading-site.py REPOSITORY START END
Checks are headless automation and are not OS assistive-technology approval.
"""
from pathlib import Path
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from threading import Thread
from functools import partial
from datetime import datetime,timezone
import json,sys,hashlib
from playwright.sync_api import sync_playwright
R=Path(sys.argv[1]).resolve();start=int(sys.argv[2]);end=int(sys.argv[3]);D=Path(__file__).resolve().parent;SITE=R/'site';files=sorted(p for p in SITE.rglob('*.html') if 'examples' not in p.relative_to(SITE).parts)
sys.path.insert(0,str(R/'tools'));from fingerprint import publication_fingerprint
class Handler(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Handler,directory=str(SITE)));Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_port}/'
rows=[]
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch();ctx=browser.new_context(viewport={'width':1280,'height':900});page=ctx.new_page()
  for i,p in list(enumerate(files))[start:end]:
   route=p.relative_to(SITE).as_posix();page.goto(base+route,wait_until='load');page.evaluate('document.fonts.ready');page.add_script_tag(path=str(R/'node_modules/axe-core/axe.min.js'))
   axe=page.evaluate('async()=>await axe.run(document,{runOnly:{type:"tag",values:["wcag2a","wcag2aa","wcag21aa","wcag22aa"]}})')
   issues=[{'id':v['id'],'impact':v['impact'],'targets':[n['target'] for n in v['nodes']]} for v in axe['violations']]
   structure=page.evaluate('({main:document.querySelectorAll("main").length,h1:document.querySelectorAll("h1").length,language:document.documentElement.lang})')
   page.set_viewport_size({'width':320,'height':800});overflow=page.evaluate('({document:document.documentElement.scrollWidth,viewport:innerWidth})');page.set_viewport_size({'width':1280,'height':900})
   rows.append({'index':i,'path':route,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'axe_violations':issues,'axe_incomplete':len(axe['incomplete']),'incomplete_details':[{'id':x['id'],'impact':x.get('impact'),'targets':[n['target'] for n in x['nodes']]} for x in axe['incomplete']],'structure':structure,'reflow_320px':overflow['document']<=overflow['viewport']+1,'overflow_widths':overflow})
   if (i-start)%20==0:print('Checked',i+1,'of',len(files),route,flush=True)
  version=browser.version;browser.close()
finally:server.shutdown();server.server_close()
output={'date':datetime.now(timezone.utc).isoformat(),'publication_fingerprint':publication_fingerprint(R),'tree':'site','engine':'Chromium '+version,'axe_version':json.loads((R/'node_modules/axe-core/package.json').read_text())['version'],'start':start,'end_exclusive':min(end,len(files)),'total_reading_pages':len(files),'checked':len(rows),'result':'PASS_AUTOMATED_SCOPE' if all(not r['axe_violations'] and r['reflow_320px'] and r['structure']['main']==1 and r['structure']['h1']==1 and r['structure']['language']=='en' for r in rows) else 'FINDINGS','scope':'Every reading document in this range, excluding the 74 standalone teaching examples with intentional reader-supplied resources. Automated WCAG-tagged axe and 320 CSS-pixel page reflow, not WCAG conformance, real zoom/forced-colour/device/OS AT or independent approval.','results':rows}
target=D/f'entire-site-a11y-{start:03}-{min(end,len(files)):03}.json.gz'
import gzip
target.write_bytes(gzip.compress(json.dumps(output,separators=(',',':')).encode(),mtime=0))
print(output['result'],len(rows),'pages; axe violations',sum(bool(r['axe_violations']) for r in rows),'overflow',sum(not r['reflow_320px'] for r in rows))
for r in rows:
 if r['axe_violations'] or not r['reflow_320px']:print(json.dumps(r))
