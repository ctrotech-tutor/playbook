"""Normative Storage contract probes in fresh browser contexts on a disposable origin.
No reader storage, production server, real credentials or fixed quota is used.
Run: python3 tests/test_storage_behavior.py REPOSITORY REPORT.json
"""
from pathlib import Path
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from threading import Thread
from datetime import datetime, timezone
import json, sys
from playwright.sync_api import sync_playwright

ROOT = Path(sys.argv[1]).resolve()
OUTPUT = Path(sys.argv[2]).resolve()


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = b'<!doctype html><html lang="en"><meta charset="utf-8"><title>Disposable Storage contract fixture</title><body><h1>Fictional storage test only</h1></body></html>'
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
Thread(target=server.serve_forever, daemon=True).start()
base = f'http://127.0.0.1:{server.server_port}'
script = r'''() => {
 const rows=[];
 const equal=(id,actual,expected)=>{
   if(JSON.stringify(actual)!==JSON.stringify(expected))throw Error(id+': '+JSON.stringify({actual,expected}));
   rows.push({id,result:'PASS',actual});
 };
 const error=(fn)=>{try{fn();return 'NO_ERROR'}catch(e){return e.name}};
 equal('window-exposure',typeof Storage,'function');
 equal('not-public-constructor',error(()=>new Storage()),'TypeError');
 for(const areaName of ['localStorage','sessionStorage']){
   const s=window[areaName];s.clear();
   equal(areaName+':empty-count',s.length,0);
   equal(areaName+':missing',s.getItem('missing'),null);
   equal(areaName+':absent-property',typeof s.ctroUniqueAbsentKey,'undefined');
   equal(areaName+':set-return',s.setItem('empty',''),undefined);
   equal(areaName+':empty-vs-absent',[s.getItem('empty'),s.getItem('missing'),s.length],['',null,1]);
   s.setItem('empty','changed');equal(areaName+':replace-count',s.length,1);
   equal(areaName+':index-conversions',[s.key(0),s.key(undefined),s.key(null),s.key(NaN),s.key(Infinity),s.key(-Infinity),s.key(2**32),s.key(-(2**32)),s.key(-0.9)],Array(9).fill('empty'));
   equal(areaName+':outside-index',[s.key(-1),s.key(1.9),s.key(1)],[null,null,null]);
   for(const method of ['key','getItem','removeItem'])equal(areaName+':missing-'+method,error(()=>s[method]()),'TypeError');
   equal(areaName+':missing-set-value',error(()=>s.setItem('new')),'TypeError');
   equal(areaName+':no-write-on-missing-value',s.getItem('new'),null);
   equal(areaName+':key-bigint',error(()=>s.key(0n)),'TypeError');
   equal(areaName+':key-symbol',error(()=>s.key(Symbol())),'TypeError');
   for(const method of ['getItem','removeItem'])equal(areaName+':symbol-'+method,error(()=>s[method](Symbol())),'TypeError');
   equal(areaName+':symbol-set-key',error(()=>s.setItem(Symbol(),'v')),'TypeError');
   equal(areaName+':symbol-set-value',error(()=>s.setItem('x',Symbol())),'TypeError');
   s.setItem(null,null);s.setItem(undefined,undefined);s.setItem(7,false);
   equal(areaName+':DOMString-conversions',[s.getItem(null),s.getItem(undefined),s.getItem(7)],['null','undefined','false']);
   const trace=[];s.setItem({toString(){trace.push('key');return 'ordered'}},{toString(){trace.push('value');return 'converted'}});
   equal(areaName+':conversion-order',trace,['key','value']);
   s.setItem('preserved','old');const marker=new RangeError('Fictional conversion failure');let observed;
   try{s.setItem('preserved',{toString(){throw marker}})}catch(e){observed=e===marker}
   equal(areaName+':conversion-error-propagates-and-preserves',[observed,s.getItem('preserved')],[true,'old']);
   for(const method of ['key','getItem','setItem','removeItem','clear'])equal(areaName+':brand-'+method,error(()=>Storage.prototype[method].call({},0,'v')),'TypeError');
   equal(areaName+':brand-length',error(()=>Object.getOwnPropertyDescriptor(Storage.prototype,'length').get.call({})),'TypeError');
   const count=s.length;equal(areaName+':strict-readonly-length',error(()=>{(function(){'use strict';s.length=999})()}),'TypeError');equal(areaName+':readonly-count-preserved',s.length,count);
   s.ctroNamed='named';equal(areaName+':named-set-and-read',[s.ctroNamed,s.getItem('ctroNamed')],['named','named']);delete s.ctroNamed;equal(areaName+':named-delete',s.getItem('ctroNamed'),null);
   s.setItem('length','stored length');s.setItem('getItem','stored method name');equal(areaName+':prototype-name-collision',[s.getItem('length'),s.getItem('getItem'),typeof s.getItem],['stored length','stored method name','function']);
   const keys=()=>Array.from({length:s.length},(_,i)=>s.key(i));const before=keys();s.setItem('empty','another');equal(areaName+':replace-does-not-reorder',keys(),before);
   equal(areaName+':remove-return',s.removeItem('empty'),undefined);equal(areaName+':missing-remove-return',s.removeItem('empty'),undefined);
   s.clear('ctro:');equal(areaName+':clear-extra-argument-is-not-prefix-filter',s.length,0);
   let converted=false;s.setItem('x','v');s.clear({toString(){converted=true;throw Error('Must not convert extra argument')}});equal(areaName+':clear-ignores-object-extra',[converted,s.length],[false,0]);
   s.setItem('quota-anchor','old');let quota='NOT_TRIGGERED_WITHIN_BOUND';
   try{s.setItem('quota-anchor','x'.repeat(16*1024*1024))}catch(e){if(e.name!=='QuotaExceededError')throw e;quota='QuotaExceededError';equal(areaName+':quota-failed-replacement-preserves-value',s.getItem('quota-anchor'),'old')}
   rows.push({id:areaName+':bounded-quota-observation',result:quota==='QuotaExceededError'?'PASS_OBSERVED':'NOT_TRIGGERED_WITHIN_BOUND',actual:quota,max_attempt_value_code_units:16*1024*1024,scope:'One bounded allocation. Not a universal quota size or free-space measurement.'});s.clear();
 }
 return rows;
}'''
rows = []
try:
    with sync_playwright() as pw:
        for engine in ['chromium', 'firefox', 'webkit']:
            print('Testing',engine,flush=True)
            browser = getattr(pw, engine).launch()
            context = browser.new_context()
            page = context.new_page()
            page.goto(base+'/mutator')
            cases = page.evaluate(script)
            unrelated = context.new_page()
            unrelated.goto(base+'/unrelated')
            unrelated.evaluate('window.probeEvents=[];window.probeArea=localStorage;addEventListener("storage",e=>probeEvents.push(e.key))')
            page.evaluate('localStorage.setItem("ctro:unrelated-probe","observed")')
            unrelated.wait_for_timeout(1200)
            delivery=unrelated.evaluate('({sharedValue:localStorage.getItem("ctro:unrelated-probe"),events:probeEvents})')
            assert delivery['sharedValue']=='observed'
            cases.append({'id':'unrelated-automated-page-event-delivery','result':'OBSERVED_DELIVERY' if delivery['events'] else 'NEEDS_TRIAGE','actual':delivery,'observation_window_ms':1200,'scope':'Separate Playwright context pages. Bounded absence is not proof of permanent non-delivery or universal engine nonconformance; opener-connected delivery is tested separately.'})
            page.evaluate('localStorage.removeItem("ctro:unrelated-probe")')
            with context.expect_page() as opened_peer:
                page.evaluate('window.open("/peer", "_blank")')
            peer = opened_peer.value
            peer.wait_for_load_state()
            peer.evaluate('window.peerArea=localStorage;window.events=[];addEventListener("storage",e=>events.push({key:e.key,oldValue:e.oldValue,newValue:e.newValue,url:e.url,area:e.storageArea===localStorage}))')
            page.evaluate('window.ownEvents=[];addEventListener("storage",e=>ownEvents.push(e.key));localStorage.setItem("ctro:event","one")')
            peer.wait_for_function('events.length>=1',polling=50)
            assert peer.evaluate('events.length')==1,peer.evaluate('events')
            page.evaluate('localStorage.setItem("ctro:event","one");localStorage.removeItem("absent");localStorage.setItem("ctro:event","two");localStorage.removeItem("ctro:event");localStorage.setItem("ctro:clear","x");localStorage.clear();localStorage.clear()')
            peer.wait_for_function('events.length===5',polling=50)
            peer.wait_for_timeout(300)
            events = peer.evaluate('events')
            assert [[e['key'], e['oldValue'], e['newValue']] for e in events] == [['ctro:event',None,'one'],['ctro:event','one','two'],['ctro:event','two',None],['ctro:clear',None,'x'],[None,None,None]], events
            assert all(e['url']==base+'/mutator' and e['area'] for e in events)
            assert page.evaluate('ownEvents') == []
            cases.append({'id':'local-events-and-noop-observation','result':'PASS','events':events,'settling_observation_ms':300,'scope':'Positive delivery and bounded no-op/same-mutator silence, not a proof about all future time.'})
            frame = page.locator('body').evaluate_handle('(body)=>{const f=document.createElement("iframe");f.src="/same-tab";body.append(f);return f}')
            same_tab = page.frame(url=base+'/same-tab')
            if same_tab is None:
                page.wait_for_function('(url)=>document.querySelector("iframe").contentWindow.location.href===url && document.querySelector("iframe").contentDocument?.readyState==="complete"',arg=base+'/same-tab')
                same_tab = page.frame(url=base+'/same-tab')
            assert same_tab is not None
            same_tab.evaluate('window.sessionEvents=[];addEventListener("storage",e=>sessionEvents.push({key:e.key,value:e.newValue,area:e.storageArea===sessionStorage}))')
            peer.evaluate('window.sessionEvents=[];addEventListener("storage",e=>sessionEvents.push(e.key))')
            page.evaluate('sessionStorage.setItem("ctro:session","one")')
            same_tab.wait_for_function('sessionEvents.length===1',polling=50)
            assert same_tab.evaluate('sessionEvents') == [{'key':'ctro:session','value':'one','area':True}]
            peer.wait_for_timeout(300)
            assert peer.evaluate('sessionStorage.getItem("ctro:session")') is None
            assert peer.evaluate('sessionEvents') == []
            cases.append({'id':'session-same-tab-frame-versus-separate-tab','result':'PASS','separate_tab_observation_ms':300})
            with context.expect_page() as opened:
                page.evaluate('window.open("/auxiliary", "_blank")')
            auxiliary = opened.value
            auxiliary.wait_for_load_state()
            assert auxiliary.evaluate('sessionStorage.getItem("ctro:session")') == 'one'
            page.evaluate('sessionStorage.setItem("ctro:session","parent-change")')
            assert auxiliary.evaluate('sessionStorage.getItem("ctro:session")') == 'one'
            auxiliary.evaluate('sessionStorage.setItem("ctro:session","copy-change")')
            assert page.evaluate('sessionStorage.getItem("ctro:session")') == 'parent-change'
            cases.append({'id':'auxiliary-session-initial-copy-not-live-sharing','result':'PASS'})
            other = context.new_page()
            other.goto(base.replace('127.0.0.1','localhost')+'/other-origin')
            page.evaluate('localStorage.setItem("ctro:origin","origin-one")')
            assert other.evaluate('localStorage.getItem("ctro:origin")') is None
            cases.append({'id':'different-host-origin-isolation','result':'PASS'})
            opaque = page.evaluate('''async()=>{const f=document.createElement('iframe');f.sandbox='allow-scripts';const done=new Promise(resolve=>{addEventListener('message',function handler(e){if(e.source===f.contentWindow&&e.data?.storageProbe){removeEventListener('message',handler);resolve(e.data.storageProbe)}})});f.srcdoc='<script>const r={};for(const n of ["localStorage","sessionStorage"]){try{window[n];r[n]="allowed"}catch(e){r[n]=e.name}}parent.postMessage({storageProbe:r},"*")<\\/script>';document.body.append(f);return await done}''')
            assert opaque == {'localStorage':'SecurityError','sessionStorage':'SecurityError'}, opaque
            cases.append({'id':'opaque-origin-getters','result':'PASS','actual':opaque})
            worker = page.evaluate('''async()=>{const url=URL.createObjectURL(new Blob(['postMessage({storage:typeof Storage,local:typeof localStorage,session:typeof sessionStorage})'],{type:'text/javascript'}));const w=new Worker(url);const v=await new Promise(resolve=>w.onmessage=e=>resolve(e.data));w.terminate();URL.revokeObjectURL(url);return v}''')
            assert worker == {'storage':'undefined','local':'undefined','session':'undefined'}
            cases.append({'id':'worker-exposure-boundary','result':'PASS','actual':worker})
            rows.append({'engine':engine,'version':browser.version,'cases':cases})
            browser.close()
finally:
    server.shutdown()
    server.server_close()
report = {'date':datetime.now(timezone.utc).isoformat(),'result':'PASS_TESTED_STORAGE_SCOPE_WITH_FINDINGS' if any(c['result']=='NEEDS_TRIAGE' for r in rows for c in r['cases']) else 'PASS_TESTED_STORAGE_SCOPE','open_findings':[{'engine':r['engine'],'case':c} for r in rows for c in r['cases'] if c['result']=='NEEDS_TRIAGE'],'scope':'Six Storage members in both local and session areas; binding/conversion/mutation and bounded quota probes; local peer events; session frame/tab/opener-copy boundaries; opaque origins; distinct origins and worker exposure. Not exhaustive policy, all-device, full Web IDL/WPT conformance, real AT or independent review.','fixture':'Fresh browser context and disposable loopback HTTP origins. No production or reader data touched.','browsers':rows}
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_text(json.dumps(report, indent=2)+'\n')
print(report['result']+':', sum(len(r['cases']) for r in rows), 'executed observations across', len(rows), 'engines;', len(report['open_findings']), 'open finding(s)')
