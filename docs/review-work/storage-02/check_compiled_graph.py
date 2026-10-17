"""Verify the final real-origin compiled artifact graph, without claiming hosted delivery."""
from pathlib import Path
from urllib.parse import urljoin,urlsplit,unquote
from bs4 import BeautifulSoup
import json,hashlib,sys
R=Path.cwd();D=R/'dist';sys.path.insert(0,str(R/'tools'));from fingerprint import publication_fingerprint
origin='https://ctrobook.vercel.app';docs={p:BeautifulSoup(p.read_text(),'html5lib') for p in D.rglob('*.html')};count=0
for path,soup in docs.items():
 rel=path.relative_to(D).as_posix()
 if rel.startswith('examples/'):continue
 for node,attr in [(n,'href') for n in soup.select('[href]')]+[(n,'src') for n in soup.select('[src]')]:
  value=node[attr]
  if not value:continue
  u=urlsplit(urljoin(origin+'/'+rel,value))
  if u.scheme not in ['http','https'] or u.netloc!=urlsplit(origin).netloc:continue
  p=D/unquote(u.path).lstrip('/')
  if not p.is_file():
   if Path(str(p)+'.html').is_file():p=Path(str(p)+'.html')
   elif (p/'index.html').is_file():p=p/'index.html'
  assert p.is_file(),(rel,value,p)
  if u.fragment and p.suffix=='.html':assert docs[p].find(id=unquote(u.fragment)),(rel,value)
  count+=1
llm=(D/'llms-full.txt').read_text();assert 'function createThemePreference' in llm and 'Storage: the six-member behaviour contract' in llm
access=docs[D/'accessibility.html'].get_text(' ',strip=True);assert 'but is not a tagged accessible PDF' not in access;assert 'PDF/UA-1' in access
report={'publication_fingerprint':publication_fingerprint(R),'result':'PASS','scope':'Final locally compiled production-origin artifact graph and discovery text; not a hosted Vercel test or independent approval. Example resource placeholders excluded from existence assertions.','origin':origin,'html_documents':len(docs),'local_destinations_checked':count,'new_behavior_in_full_text':True,'stale_untagged_pdf_copy_removed':True,'html_sha256':{p.relative_to(D).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(docs)}}
(R/'tests/seo-static-final.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS:',len(docs),'compiled HTML documents;',count,'local targets; Storage full text and corrected PDF notice.')
