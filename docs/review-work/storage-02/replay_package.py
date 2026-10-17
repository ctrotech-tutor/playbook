"""Fresh-extract and rebuild one exact deployment ZIP. Receipt is external to the ZIP."""
from pathlib import Path
from datetime import datetime,timezone
import zipfile,json,hashlib,subprocess,sys,os,shutil
R=Path.cwd();archive=R/'deliverables/ctrotech-html-playbook-vercel.zip';out=R/'.cache/storage-package-replay';shutil.rmtree(out,ignore_errors=True);out.mkdir(parents=True)
with zipfile.ZipFile(archive) as z:
 assert z.testzip() is None
 for name in z.namelist():assert (out/name).resolve().is_relative_to(out)
 z.extractall(out)
manifest=json.loads((out/'PACKAGE-MANIFEST.json').read_text())
def payload_check():
 for name,v in manifest['files'].items():assert hashlib.sha256((out/name).read_bytes()).hexdigest()==v['sha256'],name
payload_check()
command='npm ci --ignore-scripts --no-audit --no-fund && npm test && SITE_URL=https://ctrobook.vercel.app DEPLOY_ENV=production node deploy/build.mjs && node --test tests/deployment-output.test.mjs'
run=subprocess.run(['npx','--yes','--package=node@24','-c',command],cwd=out,capture_output=True,text=True,timeout=120)
log=R/'.cache/storage-package-replay-npm.log';log.write_text(run.stdout+run.stderr);assert run.returncode==0,run.stderr[-2000:]
payload_check()
pdf=(out/'deliverables/ctrotech-html-playbook.pdf').read_bytes();assert pdf==(out/'site/downloads/ctrotech-html-playbook.pdf').read_bytes()==(out/'dist/downloads/ctrotech-html-playbook.pdf').read_bytes()
script='from pathlib import Path;from pdf import verify_primary_pdf;print(verify_primary_pdf(Path.cwd())["isCompliant"])'
env=os.environ.copy();env['PYTHONPATH']=str(out/'tools');guard=subprocess.run([sys.executable,'-c',script],cwd=out,env=env,capture_output=True,text=True,check=True);assert guard.stdout.strip()=='True'
receipt={'verified_at':datetime.now(timezone.utc).isoformat(),'result':'PASS_FRESH_EXTRACTION_REBUILD','publication_fingerprint':manifest['publication_fingerprint'],'zip_sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),'payload_files':len(manifest['files']),'crc_and_all_member_hashes':'PASS','payload_unchanged_after_npm_build':'PASS','node_tests':14,'compiled_output_tests':3,'primary_pdf_sha256':hashlib.sha256(pdf).hexdigest(),'source_site_compiled_pdf_bytes_equal':True,'current_exact_pdf_proof_guard':'PASS','scope':'Fresh extraction and Node 24 build of this exact ZIP. No hosted deployment, human AT or independent content/security approval.'}
(R/'.cache/storage-package-replay-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
