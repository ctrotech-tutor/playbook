#!/usr/bin/env python3
"""Build a self-deployable Vercel bundle without credentials or implied content approval."""
from pathlib import Path
import hashlib,json,re,zipfile
import pymupdf
from fingerprint import publication_fingerprint,input_digest
R=Path(__file__).resolve().parents[1];D=R/'deliverables'
S=R/'build/site' if (R/'build/site').is_dir() else R/'site'
def sha(data):return hashlib.sha256(data).hexdigest()
META=json.loads((R/'content/publication.json').read_text());fingerprint=publication_fingerprint(R)
source=json.loads((R/'tests/release-evidence.json').read_text())
seo=json.loads((R/'tests/seo-verification.json').read_text())
final=json.loads((R/'tests/seo-static-final.json').read_text())
for evidence in [source,seo,final]:
    assert evidence['publication_fingerprint']==fingerprint,'Stale verification evidence.'
assert all(x['result']=='PASS' for x in source['results'])
assert seo['result']==final['result']=='PASS'
manifest=json.loads((S/'build-inputs.json').read_text())
for name,digest in manifest['files'].items():assert input_digest(R/name)==digest,name
pdf=D/'ctrotech-html-playbook.pdf'
if not pdf.exists():pdf=S/'downloads/ctrotech-html-playbook.pdf'
assert pdf.read_bytes()==(S/'downloads/ctrotech-html-playbook.pdf').read_bytes()
with pymupdf.open(pdf) as p:
    assert p.metadata['author']==META['author'];pages=len(p);bookmarks=len(p.get_toc())
    assert len(p.embfile_names())==5
api=json.loads((R/'content/api-register.json').read_text())
summary={'title':META['title'],'author':META['author'],'copyright_notice':META['copyright_notice'],'edition':META['edition'],'publication_date':META['publication_date'],'delivery':'Self-deployable Vercel static bundle; no GitHub integration required','content_status':META['technical_release_status'],'independent_content_approved':False,'hosted_vercel_deployment_tested':False,'vercel_project_created_by_agent':False,'vercel_project_created_by_author':True,'search_accounts_verified':False,'indexnow_submitted':False,'chapters':74,'static_reference_projects':7,'source_html_documents':len(list(S.rglob('*.html'))),'generated_html_documents':next(x['html_documents'] for x in seo['checks'] if 'html_documents' in x),'intended_indexable_pages_in_production_fixture':next(x['indexed_pages'] for x in seo['checks'] if 'indexed_pages' in x),'api_register':api['stats'],'pdf_pages':pages,'pdf_bookmarks':bookmarks,'pdf_sha256':sha(pdf.read_bytes()),'publication_fingerprint':fingerprint,'package_rebuild_evidence':'tests/package-rebuild.json','not_certified':source['not_certified']}
D.mkdir(exist_ok=True)
(D/'release-summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
files={}
def include_tree(directory):
    for p in (R/directory).rglob('*'):
        if not p.is_file() or '__pycache__' in p.parts or p.suffix in ['.pyc','.pem','.key']:continue
        if p.name=='github-action-versions.json':continue
        files[p.relative_to(R).as_posix()]=p.read_bytes()
for directory in ['content','assets','fonts','docs','deploy','tools','tests','.github']:include_tree(directory)
for name in ['README.md','PRODUCTION-READINESS.md','SEO-OPERATIONS.md','requirements-build.txt','requirements-verify.txt','package.json','package-lock.json','vercel.json','.vercelignore','.gitignore','.gitattributes','.env.example']:
    p=R/name
    if p.is_file():files[name]=p.read_bytes()
files['release-summary.json']=(D/'release-summary.json').read_bytes()
files['deliverables/ctrotech-html-playbook.pdf']=pdf.read_bytes()
for p in S.rglob('*'):
    if p.is_file() and p.name!='DEPLOY.md':files['site/'+p.relative_to(S).as_posix()]=p.read_bytes()
if (R/'foundation').is_dir():include_tree('foundation')
else:
    for name in ['deliverables/coverage-ledger.xlsx','deliverables/foundation-audit.md','editorial/architecture.json','editorial/chapter-template.md','editorial/findings.json','editorial/requirements.tsv','editorial/publication-standard.md','data/source-manifest.json','data/validation-report.json']:
        p=R.parent/name
        if p.is_file():files['foundation/'+name]=p.read_bytes()
    files['foundation/README.md']=b'# Historical foundation inputs\n\nRetained inventory, architecture and routing material predates the current manuscript. Planned routing is not completed behavioral coverage. This is not a final-release certificate. Raw historical snapshots and the original foundation generator remain separate; current HTML IDL and current publication inputs are retained in content/. See PRODUCTION-READINESS.md and the current receipts.\n'
for name in files:
    assert not name.startswith('/') and '..' not in Path(name).parts,name
    assert not any(x in Path(name).parts for x in ['node_modules','.vercel','.git','.cache','__pycache__']),name
    assert not (Path(name).name.startswith('.env') and name!='.env.example'),name
assert set(manifest['files'])<=set(files)
package_manifest={'edition':META['edition'],'author':META['author'],'publication_fingerprint':fingerprint,'scope':'Every payload file is hashed; this manifest excludes itself. Integrity is not independent technical approval.','files':{name:{'sha256':sha(data),'bytes':len(data)} for name,data in sorted(files.items())}}
path=D/'ctrotech-html-playbook-vercel.zip'
with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for name,data in sorted(files.items()):z.writestr(name,data)
    z.writestr('PACKAGE-MANIFEST.json',json.dumps(package_manifest,ensure_ascii=False,indent=2)+'\n')
with zipfile.ZipFile(path) as z:
    assert z.testzip() is None and len(z.namelist())==len(set(z.namelist()))
    saved=json.loads(z.read('PACKAGE-MANIFEST.json'))
    assert set(z.namelist())==set(saved['files'])|{'PACKAGE-MANIFEST.json'}
    for name,record in saved['files'].items():assert sha(z.read(name))==record['sha256'] and len(z.read(name))==record['bytes']
    assert z.read('site/downloads/ctrotech-html-playbook.pdf')==pdf.read_bytes()
    assert z.read('deliverables/ctrotech-html-playbook.pdf')==pdf.read_bytes()
receipt={'edition':META['edition'],'author':META['author'],'publication_fingerprint':fingerprint,'artifacts':[{'filename':path.name,'bytes':path.stat().st_size,'sha256':sha(path.read_bytes()),'payload_files':len(files),'crc':'PASS','per_file_manifest':'PASS'},{'filename':'ctrotech-html-playbook.pdf','bytes':len(pdf.read_bytes()),'sha256':sha(pdf.read_bytes())}],'status':'Deployment bundle integrity checked. Manuscript and independent review limits remain documented; no hosted deployment performed.'}
(D/'package-checksums.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
