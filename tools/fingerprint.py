from pathlib import Path
import hashlib
import json
import re

MANIFEST_VERSION = 2
HASH_POLICY = 'sha256-json-whitespace-v1'
JSON_TOKENS = re.compile(r'"(?:\\.|[^"\\])*"|[ \t\r\n]+')


def input_bytes(path):
    data = path.read_bytes()
    if path.suffix.lower() != '.json':
        return data
    text = data.decode('utf-8')
    json.loads(text)
    # Preserve quoted source, escapes, token spelling and key order exactly.
    # Only whitespace outside strings is insignificant to this manifest.
    return JSON_TOKENS.sub(lambda m: m[0] if m[0].startswith('"') else '', text).encode('utf-8')


def input_digest(path):
    return hashlib.sha256(input_bytes(path)).hexdigest()


def input_paths(root):
    paths = [p for directory in ['content', 'assets', 'fonts', 'deploy'] for p in (root/directory).rglob('*') if p.is_file()]
    paths += [root/'tools'/name for name in ['build.py', 'pdf.py', 'pdf_syntax.py', 'projects.py', 'fingerprint.py', 'verify.py', 'check_build.py', 'check_syntax.py', 'check_sources.py', 'install_nu.py', 'api_reference.py', 'identity.py', 'verify_seo.py', 'update_api_register.mjs']]
    paths += [root/name for name in ['requirements-build.txt', 'requirements-verify.txt', 'package.json', 'package-lock.json', 'vercel.json', 'tests/nu-download-provenance.json']]
    return sorted(paths)


def input_manifest(root):
    return {'format_version': MANIFEST_VERSION, 'hash_policy': HASH_POLICY, 'scope': 'Maintained inputs; only insignificant JSON whitespace outside strings is normalized. Non-JSON bytes and all JSON string/token content remain protected. Runtime hosting configuration vercel.json is validated separately, not pinned to the Python book cache; full verification fingerprints still include it for QA provenance. Generated output/evidence are not circular inputs.', 'files': {p.relative_to(root).as_posix(): input_digest(p) for p in input_paths(root) if p != root/'vercel.json'}}


def publication_fingerprint(root):
    h = hashlib.sha256()
    h.update((HASH_POLICY+'\0').encode())
    for p in input_paths(root):
        h.update(p.relative_to(root).as_posix().encode()+b'\0')
        h.update(input_bytes(p))
        h.update(b'\0')
    return h.hexdigest()
