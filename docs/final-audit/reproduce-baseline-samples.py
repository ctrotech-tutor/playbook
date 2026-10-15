"""Run from an installed baseline checkout of commit 41550987440d2b9cb59f1eac11d46c7463ba42e7. Requires its dist/ output. Candidate mode changes only the served parent policy, not source files."""
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
  def log_message(self,*a):pass
 server=ThreadingHTTPServer(('127.0.0.1',0),Handler);ctx=ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER);ctx.load_cert_chain(cert,key);server.socket=ctx.wrap_socket(server.socket,server_side=True);Thread(target=server.serve_forever,daemon=True).start();return server,'https://127.0.0.1:'+str(server.server_port)
claims=[];keyboard=[];security=[]
with sync_playwright() as pw:
 for name in ['chromium','firefox','webkit']:
  browser=getattr(pw,name).launch(args=['--no-sandbox'] if name=='chromium' else []);context=browser.new_context(ignore_https_errors=True);page=context.new_page()
  # Isolated fixtures: chapter code is unchanged and the assertions are exact, not screenshot claims.
  checks=[]
  for n in range(1,14):
   page.set_content(BOOK[n-1]['code'])
   if n==1:assert page.locator('main h1').inner_text()=='Neighbourhood Library';assert page.locator('a').get_attribute('href')=='catalogue.html'
   if n==2:assert page.evaluate('document.compatMode')=='CSS1Compat';assert page.title()=='Library notes'
   if n==3:expect(page.locator('#opening')).to_have_text('Open Tuesday to Saturday.')
   if n==4:assert page.locator('a').get_attribute('class')=='catalogue-link';assert page.locator('a').inner_text()=='Browse available books'
   if n==5:assert page.evaluate("document.querySelector('em').parentElement.tagName==='P' && document.querySelector('h1').parentElement===document.querySelector('p').parentElement")
   if n==6:assert page.title()=='Neighbourhood Library';assert page.locator('h1').inner_text()=='A good place to start reading'
   if n==7:assert page.title()=='Opening hours | Neighbourhood Library';assert page.locator('html').get_attribute('lang')=='en'
   if n==8:assert page.locator('body header').count()==1;assert page.locator('head header').count()==0
   if n==9:assert page.locator('code').inner_text()=='<button>';assert page.locator('button').count()==0;assert page.locator('p').nth(2).get_attribute('title')=='She said "welcome"'
   if n==10:assert page.locator('img').count()==1;assert page.locator('img strong').count()==0
   if n==11:assert page.locator('button').is_disabled();assert page.locator('input').evaluate('(n)=>n.required && n.labels[0].textContent==="Email"')
   if n==12:assert page.locator('a button').count()==0;assert page.locator('button').get_attribute('type')=='button'
   if n==13:assert page.locator('input').evaluate('(n)=>n.labels[0].htmlFor===n.id');assert page.locator('form').get_attribute('method')=='post'
   checks.append('CH-'+f'{n:02}')
  page.set_content('<button disabled="false">Save</button>');assert page.locator('button').is_disabled();page.locator('button').evaluate('(n)=>n.removeAttribute("disabled")');assert page.locator('button').is_enabled()
  page.set_content('<p><div>Notice</div></p>');assert page.locator('p div').count()==0;assert page.locator('div').inner_text()=='Notice'
  page.set_content('<code>&lt;p&gt;Hello&lt;/p&gt;</code>');assert page.locator('code').inner_text()=='<p>Hello</p>';assert page.locator('code p').count()==0
  page.set_content('<ul><li>One<li>Two</ul>');assert page.locator('ul > li').all_text_contents()==['One','Two']
  claims.append({'engine':name,'version':browser.version,'chapter_example_assertions_passed':checks,'additional_answer_and_optional_tag_fixtures':4,'scope':'Selected observable claims from opening chapters, not every algorithm or independent approval.'})
  for candidate in [False,True]:
   server,base=serve(candidate)
   try:
    page.goto(base+'/chapters/44',wait_until='networkidle');page.locator('[data-open-lab]').click();page.locator('#lab-code').fill('<!doctype html><title>Navigation probe</title><p>Fictional local audit only.</p><script>location.href="/privacy?audit-probe=fictional"</script>')
    before=sum('audit-probe=' in p for p in requests);page.locator('#lab-run').click()
    # A fixed bounded negative-observation window, not a network-isolation proof.
    page.wait_for_timeout(1000)
    observed=sum('audit-probe=' in p for p in requests)-before
    assert observed==(0 if candidate else 1),(name,candidate,observed)
    security.append({'engine':name,'policy':'candidate frame-src about:' if candidate else 'published frame-src self + about','same_origin_probe_requests_observed':observed,'window_ms':1000,'parent_data_used':'none; fictional local query only','status':'candidate blocks tested navigation' if candidate else 'confirmed gap in blanket network-blocking claim'})
    if not candidate:
     page.goto(base+'/chapters/44',wait_until='networkidle');trigger=page.locator('[data-open-search]');trigger.focus();page.keyboard.press('Enter');expect(page.locator('#book-search')).to_be_focused();page.keyboard.type('HTMLInputElement');expect(page.locator('#search-results a').first).to_have_attribute('href','/reference/api/htmlinputelement');page.keyboard.press('Escape');expect(page.locator('#search-dialog')).not_to_be_visible();expect(trigger).to_be_focused()
     summary=page.locator('.exercise summary');summary.focus();page.keyboard.press('Enter');assert summary.evaluate('(n)=>n.parentElement.open');page.keyboard.press('Space');assert not summary.evaluate('(n)=>n.parentElement.open')
     page.goto(base+'/examples/44',wait_until='load');page.keyboard.press('Tab');expect(page.locator('#open-help')).to_be_focused();page.keyboard.press('Enter');assert page.locator('#help-dialog').evaluate('(n)=>n.open');page.keyboard.press('Escape');assert not page.locator('#help-dialog').evaluate('(n)=>n.open');expect(page.locator('#open-help')).to_be_focused()
     page.goto(base+'/chapters/44',wait_until='networkidle');page.keyboard.press('Tab');expect(page.locator('.skip')).to_be_focused();page.keyboard.press('Enter');assert page.url.endswith('#main');page.keyboard.press('Tab');skip_next=page.evaluate('({tag:document.activeElement.tagName,id:document.activeElement.id,text:document.activeElement.textContent.slice(0,90),inMain:!!document.activeElement.closest("main")})');print('Skip-link next focus',name,skip_next,flush=True)
     page.set_viewport_size({'width':320,'height':800});paths=['/','/start','/chapters/44','/reference/api-members','/projects/registration']
     for path in paths:
      page.goto(base+path,wait_until='load');assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+1'),(name,path)
     keyboard.append({'engine':name,'version':browser.version,'search_keyboard_open_initial_focus_escape_restore':'PASS','exercise_enter_space_toggle':'PASS','native_dialog_tab_enter_escape_restore':'PASS','skip_link_next_focus_in_main':skip_next,'320px_reflow_sample':paths,'scope':'Agent-operated keyboard assertions and viewport sample. Not a human usability or OS screen-reader assessment.'})
     page.set_viewport_size({'width':1280,'height':900})
   finally:server.shutdown();server.server_close()
  browser.close()
for filename,body in [('opening-chapter-browser-checks.json',claims),('keyboard-and-reflow-checks.json',keyboard),('sandbox-navigation-checks.json',security)]:
 (OUT/filename).write_text(json.dumps({'date':'2026-10-15','baseline_commit':'41550987440d2b9cb59f1eac11d46c7463ba42e7','results':body},indent=2)+'\n')
print('PASS: opening-chapter claims and keyboard samples, three engines. Confirmed navigation gap and tested candidate policy separately.')
