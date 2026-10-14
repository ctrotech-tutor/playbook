from pathlib import Path
import hashlib

def input_paths(root):
    paths=[p for directory in ['content','assets','fonts','deploy'] for p in (root/directory).rglob('*') if p.is_file()]
    paths += [root/'tools'/name for name in ['build.py','pdf.py','pdf_syntax.py','projects.py','fingerprint.py','verify.py','check_build.py','check_syntax.py','check_sources.py','install_nu.py','api_reference.py','identity.py','verify_seo.py','update_api_register.mjs']]
    paths += [root/name for name in ['requirements-build.txt','requirements-verify.txt','package.json','package-lock.json','vercel.json','tests/nu-download-provenance.json']]
    return sorted(paths)

def input_manifest(root):
    return {'scope':'Exact maintained input bytes; generated HTML, PDF and evidence are not circular inputs.','files':{p.relative_to(root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in input_paths(root)}}

def publication_fingerprint(root):
    h=hashlib.sha256()
    for p in input_paths(root):
        h.update(p.relative_to(root).as_posix().encode()+b'\0');h.update(p.read_bytes());h.update(b'\0')
    return h.hexdigest()
