"""Whole captured-register reconciliation, not semantic completion.
Run from the repository. Reads the current maintained source, fetches official indices
and Webref declarations to a cache, and records every owning/member/keyword/route gap.
"""
from pathlib import Path
from collections import Counter
from datetime import datetime,timezone
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlsplit
import json,hashlib,gzip,csv,io,re,sys,requests
from bs4 import BeautifulSoup
R=Path.cwd();D=Path(__file__).resolve().parent;cache=R/'.cache/gates-reconciliation';cache.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(R/'tools'));from fingerprint import publication_fingerprint
api=json.loads((R/'content/api-register.json').read_text());inv=json.loads((R/'content/reference-snapshot.json').read_text())['inventories'];audit=json.loads((D/'audit-register.json').read_text())
urls=['https://html.spec.whatwg.org/multipage/indices.html','https://html.spec.whatwg.org/multipage/obsolete.html',api['idl_source_url'],api['definitions_source_url']]
def get(url):
 response=requests.get(url,timeout=45);response.raise_for_status();data=response.content;name=hashlib.sha256(url.encode()).hexdigest()[:14];(cache/name).write_bytes(data)
 return url,{'url':url,'resolved_url':response.url,'status':response.status_code,'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data),'cache_name':name,'retrieved_at':datetime.now(timezone.utc).isoformat()}
retrievals=dict(ThreadPoolExecutor(max_workers=5).map(get,urls));current_idl=(cache/retrievals[api['idl_source_url']]['cache_name']).read_bytes();current_dfns=json.loads((cache/retrievals[api['definitions_source_url']]['cache_name']).read_bytes())
index=BeautifulSoup((cache/retrievals[urls[0]]['cache_name']).read_bytes(),'html5lib')
# The actual table whose non-normative discovery ID is elements-3.
anchor=index.find(id='elements-3');table=anchor if anchor and anchor.name=='table' else anchor.find_next('table') if anchor else None
assert table is not None
live_names=set()
for row in table.select('tbody tr'):
 cell=row.find(['th','td'])
 if cell:
  live_names.update(c.get_text(strip=True) for c in cell.select('code') if re.fullmatch('[a-z][a-z0-9]*',c.get_text(strip=True)))
assert len(live_names)>90,len(live_names)
snapshot_names={x['name'] for x in inv['elements']};idl_same=hashlib.sha256(current_idl).hexdigest()==api['idl_sha256'];dfns_same=retrievals[api['definitions_source_url']]['sha256']==api['definitions_sha256']
rows=[]
def add(kind,id,owner,name,route,shape,reason):
 rows.append({'row_type':kind,'id':id,'owner':owner,'name':name,'source_route':route,'captured_shape':shape,'route_evidence':reason,'behaviour':'open','values_defaults':'open','restrictions_applicability':'open','conversion_overload':'open','exceptions':'open','algorithms_events_lifecycle':'open','cross_specification_inheritance':'open','native_compatibility_evidence':'open','independent_review':'pending'})
known={r['name'] for r in api['records']};external=[]
for owner in api['records']:
 add('api-owner',owner['name'],owner['name'],owner['name'],owner['source_url'],owner['type'],'captured declaration, not complete behaviour')
 if owner.get('inheritance'):
  parent=owner['inheritance'];external.append((owner['name'],parent,parent in known))
  add('inheritance',owner['name']+'->'+parent,owner['name'],parent,owner['source_url'],'inheritance edge','in captured register' if parent in known else 'external owner must be reconciled; not excluded')
 for name in owner['includes']:add('mixin-inclusion',owner['name']+' includes '+name,owner['name'],name,owner['source_url'],'includes edge','in captured register' if name in known else 'external mixin route remains open')
 for n,member in enumerate(owner['members'],1):add('direct-member',owner['name']+'#member-'+str(n),owner['name'],member['name'],member['definition_url'],member['signature'],member['definition_match'])
for n,record in enumerate(api['keyword_records'],1):add('keyword-state-event',record['id']+'-'+str(n),'|'.join(record['contexts']),'|'.join(record['names']),record['url'],record['type'],'captured definition route, not complete default or applicability contract')
for group,records in inv.items():
 for record in records:
  route=record.get('definition_url') or next(iter(record.get('definition_urls',[])),None) or record.get('source_url','')
  add('inventory-'+group,record.get('id',record['name']),'|'.join(record.get('owner_chapters',[])),record['name'],route,record.get('specification_status',record.get('assignment_status','captured route')),'captured route; review states preserved, not silently completed')
for req in audit['requirements']:add('requirement',req['id'],'|'.join(req['owner_chapters']),req['requirement'],'','required; no exclusions',req['completion'])
buf=io.StringIO();writer=csv.DictWriter(buf,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows);payload=gzip.compress(buf.getvalue().encode(),mtime=0);(D/'full-coverage-gap-ledger.csv.gz').write_bytes(payload)
# Overloads are distinct member rows; no signature deduplication loses a contract.
member_rows=[r for r in rows if r['row_type']=='direct-member'];fallback=[r for r in member_rows if r['route_evidence']!='member']
(D/'unresolved-member-routes.json').write_text(json.dumps({'scope':'All captured non-exact member routes. Not dropped from scope and not labelled documented.','count':len(fallback),'records':fallback},separators=(',',':'))+'\n')
checks=[];book=json.loads((R/'content/chapters.json').read_text());ids={c['id'] for c in book}
for c in book:
 errors=[]
 if not c['objectives']:errors.append('no objectives')
 if not c.get('prerequisites') and c['number']!=1:errors.append('no prerequisite record')
 if any(x not in ids for x in c.get('prerequisites',[])):errors.append('prerequisite ID missing')
 if any(int(x[3:])>=c['number'] for x in c.get('prerequisites',[])):errors.append('non-earlier prerequisite')
 for key in ['lesson','code','explanation','mistake','question','answer','sources']:
  if not c.get(key):errors.append('missing '+key)
 if '\u2014' in json.dumps(c,ensure_ascii=False):errors.append('authored em dash')
 # A field or chapter pass is not substantive independent correctness approval.
 checks.append({'chapter':c['id'],'structural_errors':errors,'terminology_review':'explicit heading present' if re.search(r'(?im)^#+ (working terms|key terms|terms|vocabulary)',c['lesson']) else 'no explicitly labelled terminology section; claim-level check remains open','independent_answer_correctness':'pending'})
report={'date':'2026-10-16','publication_fingerprint':publication_fingerprint(R),'scope':'Full captured-row gap accounting and live discovery/declaration comparison. Not completed teaching or full normative/algorithm reconciliation.','retrievals':list(retrievals.values()),'live_element_index':{'captured_conforming_elements':len(snapshot_names),'live_discovery_names':len(live_names),'only_in_live_index':sorted(live_names-snapshot_names),'only_in_snapshot':sorted(snapshot_names-live_names),'boundary':'Discovery table row names, not independent per-element content-model approval.'},'webref_idl_bytes_equal_snapshot':idl_same,'webref_public_definitions_bytes_equal_snapshot':dfns_same,'ledger_rows':len(rows),'ledger_rows_by_type':dict(Counter(r['row_type'] for r in rows)),'direct_members':len(member_rows),'non_exact_member_routes':len(fallback),'external_parent_edges':[{'owner':a,'parent':b} for a,b,inside in external if not inside],'all_required_requirements_accounted':len(audit['requirements'])==81,'requirements_closed':0,'exclusions':0,'chapter_record_checks':checks,'ledger_sha256':hashlib.sha256(payload).hexdigest(),'critical_interpretation':'No open flag is a claim that a feature is absent from every chapter. Selected teaching exists, but exhaustive dimensions have not received evidence sufficient for closure.'}
(D/'full-coverage-reconciliation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='chapter_record_checks'},indent=2))
