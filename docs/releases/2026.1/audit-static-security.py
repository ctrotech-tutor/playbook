"""Whole reading-site static boundary checks, not independent penetration testing.
Run from the repository after site generation. Standalone examples are separately
inventoried because intentional teaching cases/resources are not production controls.
"""
from pathlib import Path
from urllib.parse import urlsplit
from bs4 import BeautifulSoup
import json,hashlib,re,sys
R=Path.cwd();D=Path(__file__).resolve().parent;S=R/'site'
sys.path.insert(0,str(R/'tools'));from fingerprint import publication_fingerprint
issues=[];rows=[];handlers=[];schemes=[];external_resources=[];frames=[];forms=[];passive_resources=[]
hosting=json.loads((R/'vercel.json').read_text());global_rule=next(x for x in hosting['headers'] if x['source']=='/(.*)');global_csp=next(x['value'] for x in global_rule['headers'] if x['key'].lower()=='content-security-policy')
assert all(x in global_csp for x in ["connect-src 'none'","form-action 'none'","object-src 'none'","frame-src about:"])
for p in sorted(S.rglob('*.html')):
 rel=p.relative_to(S).as_posix();teaching=rel.startswith('examples/');soup=BeautifulSoup(p.read_bytes(),'html5lib')
 if teaching:continue
 for n in soup.find_all(True):
  for key,value in n.attrs.items():
   if key.lower().startswith('on'):handlers.append({'path':rel,'element':n.name,'attribute':key})
  for attr in ['href','src','action']:
   v=n.get(attr,'')
   if isinstance(v,str) and urlsplit(v).scheme.lower() in ['javascript','vbscript']:schemes.append({'path':rel,'element':n.name,'attribute':attr})
 for n in soup.select('script[src],link[rel=stylesheet][href],img[src],iframe[src],video[src],audio[src],source[src]'):
  v=n.get('src') or n.get('href');u=urlsplit(v)
  if u.scheme in ['http','https'] or v.startswith('//'):external_resources.append({'path':rel,'element':n.name,'url':v})
 for n in soup.select('a[target="_blank"]'):
  if not {'noopener','noreferrer'}<=set(n.get('rel',[])):issues.append({'path':rel,'rule':'new-window link lacks explicit noopener+noreferrer','href':n.get('href')})
 for frame in soup.select('iframe'):
  rec={'path':rel,'id':frame.get('id'),'sandbox':frame.get('sandbox',[])};frames.append(rec)
  if frame.get('id')=='lab-output' and frame.get('sandbox')!=['allow-scripts']:issues.append({'path':rel,'rule':'lab sandbox does not retain script-only opaque-origin boundary'})
 for form in soup.select('form'):
  if form.get('id')=='demo-form':
   f=form.find('fieldset',id='demo-fields');named=form.select('input[name],select[name],textarea[name]');rec={'path':rel,'disabled_fieldset_baseline':f is not None and f.has_attr('disabled'),'named_application_controls':len(named),'explicit_application_endpoint':form.get('action')};forms.append(rec)
   if not rec['disabled_fieldset_baseline'] or named or form.get('action'):issues.append({'path':rel,'rule':'practice form collection boundary changed'})
 if rel=='assets/media/schematic-transcript.html':
  assert not soup.select('script,iframe,form,object,embed'),rel
  passive_resources.append({'path':rel,'active_content':False,'host_csp_scope':'/(.*) global response policy; no shell-specific meta required for this passive local resource'})
 if not rel.startswith('projects/') and rel!='assets/media/schematic-transcript.html':
  csp=soup.select_one('meta[http-equiv="Content-Security-Policy"]');value=csp.get('content','') if csp else ''
  for required in ["connect-src 'none'","form-action 'none'","object-src 'none'","frame-src about:"]:
   if required not in value:issues.append({'path':rel,'rule':'expected book CSP directive missing','directive':required})
 rows.append({'path':rel,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
assert len(rows)==422
sinks=[]
for p in sorted((R/'assets').glob('*.js')):
 for n,line in enumerate(p.read_text().splitlines(),1):
  if re.search(r'innerHTML|insertAdjacentHTML|\beval\s*\(|new\s+Function|\bsrcdoc\b|postMessage|document\.write|fetch\s*\(',line):
   sinks.append({'path':p.relative_to(R).as_posix(),'line':n,'kind':'isolated editor source assignment' if 'srcdoc' in line else 'worker message' if 'postMessage' in line else 'needs explicit review','sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
assert not handlers,handlers;assert not schemes,schemes;assert not external_resources,external_resources;assert not issues,issues
assert all(x['kind']!='needs explicit review' for x in sinks),sinks
result={'date':'2026-10-17','publication_fingerprint':publication_fingerprint(R),'result':'PASS_STATIC_SCOPE','reading_documents':len(rows),'standalone_teaching_examples_excluded':74,'inline_event_handlers':handlers,'script_url_schemes':schemes,'external_runtime_resources':external_resources,'issues':issues,'passive_local_resources':passive_resources,'global_host_csp_checked':True,'editor_frames':len(frames),'practice_forms':forms,'maintained_asset_sensitive_sites':sinks,'reading_document_hashes':rows,'scope':'Every generated reading document plus maintained top-level asset JavaScript sensitive-site inventory. Same-agent static review and targeted runtime regression, not every possible browser channel, dependency supply-chain audit, server/backend assessment or independent penetration test. There is no lending/membership backend here.','manual_reasoning':['The editor parses source into a document and prepends its restrictive CSP before assigning srcdoc to the script-only sandbox; no same-origin permission is granted. Actual tested channels are separately re-exercised.','The worker checks finite numeric payloads and bounded input before posting a typed result; the chapter handles completion/error/timeout and validates the result.','The practice form installs local prevention/error/reset handlers before enabling fields, builds messages with text nodes and claims no application acceptance.','No online payment, login, session or database application is supplied; static checks must not be sold as a backend security audit.']}
import gzip
(D/'entire-site-security.json.gz').write_bytes(gzip.compress(json.dumps(result,separators=(',',':')).encode(),mtime=0));print('PASS: 422 reading documents; no inline handlers/script-scheme links/external runtime resources; static sandbox/form boundaries and maintained JS sensitive sites checked.')
