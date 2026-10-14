#!/usr/bin/env python3
"""Install only the recorded Nu jar bytes. Refuse a changed mutable release asset."""
from pathlib import Path
import hashlib,json,requests
R=Path(__file__).resolve().parents[1]
record=json.loads((R/'tests/nu-download-provenance.json').read_text())
response=requests.get(record['download_url'],timeout=120);response.raise_for_status()
actual=hashlib.sha256(response.content).hexdigest()
if actual!=record['sha256']:
    raise SystemExit('The upstream checker asset changed. Do not bypass this check. Obtain the recorded archived jar or review/update checker provenance and rerun all verification. Expected '+record['sha256']+'; received '+actual)
p=R/'.cache/vnu/vnu.jar';p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(response.content)
print('Saved verified Nu jar:',p)
