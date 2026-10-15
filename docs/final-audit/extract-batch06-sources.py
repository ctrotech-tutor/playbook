"""Extract bounded review excerpts from the actual successful citation retrieval cache.
Run from the checkout after tools/check_sources.py; writes beside this script.
"""
from pathlib import Path
from bs4 import BeautifulSoup
import hashlib,json,gzip
R=Path.cwd();D=Path(__file__).resolve().parent
book=json.loads((R/'content/chapters.json').read_text());check=json.loads((R/'tests/citation-checks.json').read_text());byurl={r['url']:r for r in check['results']};rows=[];excerpts=[]
for url in sorted({s['url'] for c in book[67:] for s in c['sources']}):
 row=byurl[url];assert row['target_found'];raw=(R/'.cache/citations'/(hashlib.sha256(url.split('#')[0].encode()).hexdigest()[:12]+'.html')).read_bytes();assert hashlib.sha256(raw).hexdigest()==row['sha256'];soup=BeautifulSoup(raw,'html.parser')
 # Omit the compatibility sidebars from the bounded quotation, not the source hash.
 for node in soup.select('.mdn-anno'):node.decompose()
 fragment=url.split('#',1)[1] if '#' in url else '';node=soup.find(id=fragment) if fragment else soup.find('main') or soup.body
 assert node is not None,url
 parts=[node.get_text(' ',strip=True)]
 if fragment:
  for x in node.next_siblings:
   if sum(map(len,parts))>5500:break
   if hasattr(x,'get_text'):parts.append(x.get_text(' ',strip=True))
 text=' '.join(parts)[:7500];excerpts.append({'url':url,'text':text});rows.append(row)
 print(url+'\n'+text[:1200]+'\n')
(D/'batch06-source-retrievals.json').write_text(json.dumps({'checked_at':check['checked_at'],'scope':'Dated HTTP/fragment retrieval and bounded excerpts, with compatibility sidebars omitted from excerpts only. Selected same-agent claim review, not exhaustive normative approval.','results':rows},indent=2)+'\n')
(D/'batch06-source-excerpts.json.gz').write_bytes(gzip.compress(json.dumps(excerpts,ensure_ascii=False).encode(),mtime=0))
