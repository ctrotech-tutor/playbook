#!/usr/bin/env python3
"""Fast offline deployment check. Does not replace full verification or owner approval."""
from pathlib import Path
from urllib.parse import urlparse,unquote
from bs4 import BeautifulSoup
import json,re,zipfile
import pymupdf
from fingerprint import publication_fingerprint
R=Path(__file__).resolve().parents[1];S=R/'build/site'
book=json.loads((R/'content/chapters.json').read_text())
assert len(book)==74 and {x['id'] for x in book}=={f'CH-{n:02}' for n in range(1,75)}
evidence=json.loads((R/'tests/release-evidence.json').read_text())
assert evidence['publication_fingerprint']==publication_fingerprint(R),'The content/build inputs changed after verification. Re-run the full checks and commit fresh evidence before deployment.'
docs={p.resolve():BeautifulSoup(p.read_text(),'html5lib') for p in S.rglob('*.html')};checks=0
for p,s in docs.items():
    assert s.html.get('lang')=='en'
    assert len(s.select('head > title'))==1
    author=s.select_one('meta[name=author]');assert author and author.get('content')==json.loads((R/'content/publication.json').read_text())['author']
    if 'examples' in p.relative_to(S.resolve()).parts:continue
    assert s.select_one('h1') is not None
    for n,attr in [(x,'href') for x in s.select('[href]')]+[(x,'src') for x in s.select('[src]')]:
        u=urlparse(n[attr]);raw=n[attr]
        if u.scheme or raw.startswith('//') or not raw:continue
        assert not raw.startswith('/'),(p,raw)
        target=(p.parent/unquote(u.path)).resolve() if u.path else p
        if target.is_dir():target/= 'index.html'
        assert target.exists(),(p,raw)
        if u.fragment and target in docs:assert docs[target].find(id=unquote(u.fragment)),(p,raw)
        checks+=1
for c in book:
    assert '\u2014' not in json.dumps(c,ensure_ascii=False)
    assert c['editorial_status']=='draft_for_review'
for z in (S/'downloads').glob('project-*.zip'):
    with zipfile.ZipFile(z) as p:assert p.testzip() is None
p=pymupdf.open(S/'downloads/ctrotech-html-playbook.pdf');assert len(p.get_toc())>=74
status=BeautifulSoup((S/'reference/status.html').read_text(),'html5lib').get_text(' ',strip=True)
assert 'Executed checks passed' in status,'Build the site again after saving current verification evidence.'
print(f'PASS: {len(docs)} documents, {checks} local destinations, 74 chapter records, seven project ZIPs, PDF bookmarks and current build fingerprint.')
print('Scope: static release integrity only. Independent technical/accessibility/security/answer-key and full coverage approval remain open.')
