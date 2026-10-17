"""Single-source production PDF build and exact-artifact publication guard.

Rendering, structural checks and machine PDF/UA-1 validation must all pass before
an artifact is promoted. An older good PDF/proof is retained on renderer failure.
The PDF is not represented as independently accessibility-certified.
"""
from pathlib import Path
import hashlib, json, shutil, subprocess, sys
from fingerprint import publication_fingerprint


def verify_primary_pdf(root):
    root = Path(root)
    target = root/'deliverables/ctrotech-html-playbook.pdf'
    proof = json.loads((root/'docs/releases/2026.1/pdf-validation.json').read_text())
    assert proof.get('isCompliant') is True and proof.get('profile') == 'PDF/UA-1', 'Primary PDF has no passing machine validation evidence.'
    assert proof['artifact_sha256'] == hashlib.sha256(target.read_bytes()).hexdigest(), 'Primary PDF does not match its exact validation report.'
    assert proof['publication_fingerprint'] == publication_fingerprint(root), 'Primary PDF was not generated and validated for the current publication inputs.'
    return proof


def build_pdf(root, site, book, inv):
    root, site = Path(root).resolve(), Path(site).resolve()
    staging = root/'.cache/production-pdf'
    staging.mkdir(parents=True, exist_ok=True)
    subprocess.run([sys.executable, str(root/'tools/tagged_pdf.py'), str(root), str(staging)], check=True)
    from validate_pdf import validate
    validate(root, staging/'ctrotech-html-playbook.pdf', staging)
    # Do not promote a newly rendered file unless the exact bytes validated.
    artifact = staging/'ctrotech-html-playbook.pdf'
    proof = json.loads((staging/'pdf-validation.json').read_text())
    assert proof['artifact_sha256'] == hashlib.sha256(artifact.read_bytes()).hexdigest()
    records = root/'docs/releases/2026.1'
    records.mkdir(parents=True, exist_ok=True)
    for name in ['pdf-structure-checks.json', 'pdf-validation.json', 'pdf-verapdf.xml', 'pdf-verapdf-diagnostics.log.gz']:
        shutil.copy2(staging/name, records/name)
    target = root/'deliverables'/artifact.name
    shutil.copy2(artifact, target)
    verify_primary_pdf(root)
    (site/'downloads').mkdir(parents=True, exist_ok=True)
    shutil.copy2(target, site/'downloads'/target.name)
    print('Validated, tagged production PDF:', target)
