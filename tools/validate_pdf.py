"""Validate one exact release PDF with veraPDF; never equate profile pass with certification."""
from pathlib import Path
from datetime import datetime, timezone
import gzip, hashlib, json, os, subprocess, xml.etree.ElementTree as ET
from fingerprint import publication_fingerprint


def validate(root, artifact, output):
    root, artifact, output = Path(root).resolve(), Path(artifact).resolve(), Path(output).resolve()
    output.mkdir(parents=True, exist_ok=True)
    binary = os.environ.get('VERAPDF', str(root/'.cache/verapdf/verapdf'))
    version = subprocess.check_output([binary, '--version'], text=True).splitlines()[0]
    run = subprocess.run([binary, '--flavour', 'ua1', '--format', 'xml', str(artifact)], capture_output=True, timeout=300)
    (output/'pdf-verapdf.xml').write_bytes(run.stdout)
    (output/'pdf-verapdf-diagnostics.log.gz').write_bytes(gzip.compress(run.stderr, mtime=0))
    tree = ET.fromstring(run.stdout)
    report = tree.find('.//validationReport')
    assert run.returncode == 0 and report is not None and report.get('isCompliant') == 'true', 'PDF/UA-1 validation failed; see retained XML and diagnostics.'
    details = report.find('details')
    assert details is not None and details.get('failedChecks') == '0' and details.get('failedRules') == '0'
    proof = {
        'validated_at': datetime.now(timezone.utc).isoformat(),
        'artifact': artifact.name,
        'artifact_sha256': hashlib.sha256(artifact.read_bytes()).hexdigest(),
        'publication_fingerprint': publication_fingerprint(root),
        'engine': version, 'profile': 'PDF/UA-1', 'isCompliant': True,
        'details': dict(details.attrib),
        'scope': 'Exact-artifact machine PDF/UA-1 profile validation. Not independent semantic reading-order, usability, WCAG or actual OS assistive-technology approval.',
        'independent_accessibility_approved': False, 'os_assistive_technology_reviewed': False,
        'diagnostics': 'pdf-verapdf-diagnostics.log.gz; font diagnostics are retained, not hidden by the compliant profile result.'
    }
    (output/'pdf-validation.json').write_text(json.dumps(proof, indent=2)+'\n')
    print(version, 'PDF/UA-1 PASS:', proof['artifact_sha256'])
    return proof


if __name__ == '__main__':
    import sys
    validate(*sys.argv[1:])
