"""Execute the exact authored exercise controller and wiring on disposable origins.
Run: python3 tests/test_storage_exercise.py REPOSITORY REPORT.json
The denial/quota branches below are fault injections, not measured browser policies.
"""
from pathlib import Path
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from threading import Thread
from datetime import datetime, timezone
import json, sys
from playwright.sync_api import sync_playwright
ROOT=Path(sys.argv[1]).resolve(); OUT=Path(sys.argv[2]).resolve()
e=json.loads((ROOT/'docs/review-work/storage-01/contract-source.json').read_text())['units'][0]['exercise']
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        body=('<!doctype html><html lang="en"><meta charset="utf-8"><title>Theme exercise fixture</title><body>'+e['html']+'</body></html>').encode()
        self.send_response(200);self.send_header('Content-Type','text/html; charset=utf-8');self.end_headers();self.wfile.write(body)
    def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),Handler);Thread(target=server.serve_forever,daemon=True).start()
rows=[]
try:
    with sync_playwright() as pw:
        for engine in ['chromium','firefox','webkit']:
            browser=getattr(pw,engine).launch();ctx=browser.new_context();page=ctx.new_page();cases=[]
            for name,stored in [('absent',None),('paper','paper'),('night','night'),('empty',''),('unexpected-truthy','sepia'),('untrusted-markup','<img src=x onerror="window.injected=true">')]:
                page.goto(f'http://127.0.0.1:{server.server_port}/practice');page.evaluate('localStorage.clear()')
                if stored is not None:page.evaluate('(v)=>localStorage.setItem("ctro:theme",v)',stored)
                page.add_script_tag(content=e['code']+'\n'+e['usage_code'])
                actual=page.evaluate('({theme:preference.value,rendered:document.documentElement.dataset.theme,selected:document.querySelector("select").value,status:document.querySelector("#theme-status").textContent,images:document.querySelectorAll("img").length,injected:window.injected===true})')
                expected=stored if stored in ['paper','night'] else 'paper'
                assert actual=={'theme':expected,'rendered':expected,'selected':expected,'status':'Preference read; saving is not yet verified.','images':0,'injected':False},actual
                page.select_option('select','night');assert page.evaluate('localStorage.getItem("ctro:theme")')=='night'
                assert page.locator('#theme-status').inner_text()=='Preference saved.'
                cases.append({'id':name,'result':'PASS','initial':actual,'successful_save_verified':True})
            for name in ['getter-denied','write-quota-failure','invalid-next-value','read-failure-preserves-memory']:
                page.goto(f'http://127.0.0.1:{server.server_port}/practice');page.evaluate('localStorage.clear();localStorage.setItem("ctro:theme","paper")')
                if name=='getter-denied':page.evaluate('Object.defineProperty(window,"localStorage",{get(){throw new DOMException("Fixture denial","SecurityError")}})')
                if name=='write-quota-failure':page.evaluate('Object.defineProperty(Storage.prototype,"setItem",{value(){throw new DOMException("Fixture quota failure","QuotaExceededError")}})')
                page.add_script_tag(content=e['code']+'\n'+e['usage_code'])
                if name=='invalid-next-value':
                    result=page.evaluate('()=>{let error;try{preference.set("sepia")}catch(e){error=e.name}return {error,value:preference.value,stored:localStorage.getItem("ctro:theme")}}')
                    assert result=={'error':'TypeError','value':'paper','stored':'paper'},result
                else:
                    page.select_option('select','night')
                    assert page.evaluate('preference.value')=='night'
                    assert page.evaluate('document.documentElement.dataset.theme')=='night'
                    if name=='read-failure-preserves-memory':
                        page.evaluate('Object.defineProperty(window,"localStorage",{get(){throw new DOMException("Fixture denial","SecurityError")}})')
                        assert page.evaluate('preference.read()')=='night'
                        assert page.locator('#theme-status').inner_text()=='Preference storage is unavailable.'
                    else:
                        assert page.locator('#theme-status').inner_text()=='Theme changed for this page only.'
                        if name=='write-quota-failure':assert page.evaluate('localStorage.getItem("ctro:theme")')=='paper'
                    result={'in_memory_theme':'night','status':page.locator('#theme-status').inner_text()}
                cases.append({'id':name,'result':'PASS','actual':result,'fault_injection':name not in ['invalid-next-value']})
            rows.append({'engine':engine,'version':browser.version,'scenarios':cases});browser.close()
finally:
    server.shutdown();server.server_close()
report={'date':datetime.now(timezone.utc).isoformat(),'result':'PASS_TESTED_EXERCISE_SCOPE','scope':'Exact authored exercise code and DOM wiring; allowlist, untrusted values, normal saves, invalid requests and injected access/quota failures. Not real policy/quota measurements, independent security review or AT testing.','browsers':rows}
OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(report,indent=2)+'\n')
print(report['result'],sum(len(r['scenarios']) for r in rows),'executed scenarios across',len(rows),'engines')
