#!/usr/bin/env python3
"""Check live source URL/fragment targets, not assertion-level interpretation."""
from pathlib import Path
from urllib.parse import urlparse,unquote
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
from datetime import datetime,timezone
from bs4 import BeautifulSoup
import requests,json,hashlib,time
R=Path(__file__).resolve().parents[1]
class Ids(HTMLParser):
    def __init__(self):super().__init__(convert_charrefs=True);self.ids=set()
    def handle_starttag(self,tag,attrs):
        for key,value in attrs:
            if key=='id' or (tag=='a' and key=='name'):self.ids.add(value)
book=json.loads((R/'content/chapters.json').read_text());api=json.loads((R/'content/api-register.json').read_text())
urls={s['url'] for c in book for s in c['sources']}|{r['url'] for r in json.loads((R/'content/value-routes.json').read_text())}
for owner in api['records']:
    urls.add(owner['source_url']);urls.update(m['definition_url'] for m in owner['members'])
urls.update(r['url'] for r in api['keyword_records'])
# Check the publication's current external source links as well as chapter citations.
for p in (R/'build/site').rglob('*.html'):
    if 'examples' in p.relative_to(R/'build/site').parts:continue
    doc=BeautifulSoup(p.read_text(),'html.parser')
    urls.update(a['href'] for a in doc.select('a[href]') if a['href'].startswith('https://'))
urls=sorted(urls);paths=sorted({u.split('#',1)[0] for u in urls});cache=R/'.cache/citations';cache.mkdir(parents=True,exist_ok=True)
def get(url):
    for attempt in range(3):
        try:
            response=requests.get(url,timeout=60,headers={'User-Agent':'CTROTECH-Publication-LinkCheck/0.3'})
            response.raise_for_status();raw=response.content
            parser=Ids();parser.feed(raw.decode(response.encoding if response.encoding and response.encoding.lower()!='iso-8859-1' else 'utf-8',errors='replace'))
            (cache/(hashlib.sha256(url.encode()).hexdigest()[:12]+'.html')).write_bytes(raw)
            return url,{'ids':parser.ids,'sha256':hashlib.sha256(raw).hexdigest(),'http_status':response.status_code,'resolved_url':response.url}
        except requests.RequestException as error:
            if attempt==2:return url,{'ids':set(),'error':str(error),'http_status':getattr(getattr(error,'response',None),'status_code',None)}
            time.sleep(attempt+1)
docs=dict(ThreadPoolExecutor(max_workers=5).map(get,paths));rows=[]
for url in urls:
    record=docs[url.split('#',1)[0]];fragment=unquote(urlparse(url).fragment);found='error' not in record and (not fragment or fragment in record['ids'])
    rows.append({'url':url,'target_found':found,**{k:v for k,v in record.items() if k!='ids'},'source':'Live HTTP retrieval; not an independent interpretation review.'})
output={'checked_at':datetime.now(timezone.utc).isoformat(),'checked':len(rows),'passed':sum(row['target_found'] for row in rows),'documents_retrieved':len(paths),'scope':'Live HTTP/document/fragment availability. This does not prove correctness of the publication’s assertions.','results':rows}
(R/'tests/citation-checks.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
for row in rows:
    if not row['target_found']:print('UNRESOLVED',row['url'],row.get('error','missing fragment'))
print('Citation/source targets:',output['passed'],'/',output['checked'],'in',len(paths),'documents')
if output['passed']!=output['checked']:raise SystemExit(1)
