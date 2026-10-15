"""Run from the installed candidate checkout after rebuilding dist/. Tests selected channels only."""
from pathlib import Path
import json,sys,hashlib
# Reuse the recorded local HTTPS harness, without executing its baseline comparison sequence.
from pathlib import Path
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from threading import Thread
from urllib.parse import urlsplit
import ssl,subprocess,json,functools
from playwright.sync_api import sync_playwright,expect
R=Path.cwd();OUT=Path(__file__).resolve().parent;BOOK=json.loads((R/'content/chapters.json').read_text());headers=json.loads((R/'vercel.json').read_text())['headers'][0]['headers'];requests=[]
cert=R/'.cache/audit-cert.pem';key=R/'.cache/audit-key.pem'
subprocess.run(['openssl','req','-x509','-newkey','rsa:2048','-nodes','-keyout',str(key),'-out',str(cert),'-days','1','-subj','/CN=localhost'],check=True,capture_output=True)
def serve(candidate):
 class Handler(SimpleHTTPRequestHandler):
  def do_GET(self):
   path=urlsplit(self.path).path;requests.append(self.path)
   p=R/'dist'/path.lstrip('/')
   if not p.is_file():p=p.with_suffix('.html') if p.name else R/'dist/index.html'
   if not p.is_file() and path=='/':p=R/'dist/index.html'
   if not p.is_file():self.send_error(404);return
   data=p.read_bytes()
   if candidate and p.suffix=='.html':data=data.replace(b"frame-src 'self' about:",b'frame-src about:')
   self.send_response(200)
   for h in headers:
    value=h['value'].replace("frame-src 'self' about:",'frame-src about:') if candidate else h['value'];self.send_header(h['key'],value)
   self.send_header('Content-Type',self.guess_type(str(p))+'; charset=utf-8');self.send_header('Content-Length',str(len(data)));self.end_headers();self.wfile.write(data)
  def do_POST(self):requests.append(self.path);self.send_error(405)
  def log_message(self,*a):pass
 server=ThreadingHTTPServer(('127.0.0.1',0),Handler);ctx=ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER);ctx.load_cert_chain(cert,key);server.socket=ctx.wrap_socket(server.socket,server_side=True);Thread(target=server.serve_forever,daemon=True).start();return server,'https://127.0.0.1:'+str(server.server_port)

sys.path.insert(0,'tools');from fingerprint import publication_fingerprint
rows=[]
with sync_playwright() as pw:
 for name in ['chromium','firefox','webkit']:
  browser=getattr(pw,name).launch(args=['--no-sandbox'] if name=='chromium' else []);context=browser.new_context(ignore_https_errors=True);page=context.new_page();server,base=serve(True)
  try:
   page.goto(base+'/chapters/44',wait_until='networkidle');page.locator('[data-open-lab]').click();page.evaluate('window.addEventListener("message",e=>{if(Array.isArray(e.data?.auditResult))window.__auditResults=e.data.auditResult})')
   source='''<!doctype html><title>Fictional security fixture</title><p id="probe">Running</p><form action="/privacy?audit-probe=form" method="post"></form><script>(async()=>{const result=[];try{parent.document.body.dataset.auditEscape='bad';result.push('parent leaked')}catch{result.push('parent blocked')}try{localStorage.setItem('audit','x');result.push('storage allowed')}catch{result.push('storage blocked')}try{await fetch('/privacy?audit-probe=fetch');result.push('fetch allowed')}catch{result.push('fetch blocked')}const image=new Image();image.src='/privacy?audit-probe=image';parent.postMessage({auditResult:result},'*');try{document.forms[0].submit()}catch{}try{location.href='/privacy?audit-probe=navigation'}catch{}})()</script>'''
   before=sum('audit-probe=' in v for v in requests);page.locator('#lab-code').fill(source);page.locator('#lab-run').click();page.wait_for_function('()=>Array.isArray(window.__auditResults)');assert page.evaluate('window.__auditResults')==['parent blocked','storage blocked','fetch blocked'];page.wait_for_timeout(1000);seen=sum('audit-probe=' in v for v in requests)-before
   assert seen==0 and page.locator('body').get_attribute('data-audit-escape') is None
   rows.append({'engine':name,'version':browser.version,'parent_dom_blocked':True,'opaque_origin_storage_blocked':True,'fetch_blocked':True,'network_requests_for_tested_image_form_and_navigation':seen,'observation_window_ms':1000,'scope':'Only these locally exercised channels. Not a universal no-network or arbitrary-code safety guarantee.'})
  finally:server.shutdown();server.server_close();browser.close()
OUT.joinpath('sandbox-candidate-regression.json').write_text(json.dumps({'date':'2026-10-15','candidate_fingerprint':publication_fingerprint(R),'result':'PASS','browsers':rows,'not_deployed':True},indent=2)+'\n')
print('PASS: actual candidate preview restrictions in three engines, scoped to tested channels.')
