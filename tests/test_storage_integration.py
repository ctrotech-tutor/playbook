"""Check the maintained Storage unit against actual HTML, PDF and text exports.
Run after the verified production build: python3 tests/test_storage_integration.py
"""
from pathlib import Path
from html import escape
import unittest,json,re,sys,subprocess
from bs4 import BeautifulSoup
import pymupdf
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from behavior_reference import units,render_unit,anchor
from fingerprint import input_paths,input_manifest
SITE=R/'build/site' if (R/'build/site').is_dir() else R/'site'
class StorageIntegration(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.unit=units(R)[0];cls.html=BeautifulSoup((SITE/'reference/api/storage.html').read_text(),'html.parser')
  with pymupdf.open(R/'deliverables/ctrotech-html-playbook.pdf') as doc:cls.pdf=''.join(page.get_text(sort=True,clip=pymupdf.Rect(0,48,page.rect.width,page.rect.height-50)) for page in doc)
 @staticmethod
 def normalized(text):return re.sub(r'\s+','',text.replace('`',''))
 def test_source_snapshot_is_current(self):
  self.assertEqual(json.loads((SITE/'build-inputs.json').read_text()),input_manifest(R))
 def test_exercise_is_exact_executed_source(self):
  old=json.loads((R/'docs/review-work/storage-01/contract-source.json').read_text())['units'][0]
  self.assertEqual(self.unit['exercise'],old['exercise'])
 def test_six_direct_members(self):
  self.assertEqual([m['name'] for m in self.unit['members']],['length','key','getItem','setItem','removeItem','clear'])
  register=json.loads((R/'content/api-register.json').read_text())
  owner=next(r for r in register['records'] if r['name']=='Storage')
  self.assertEqual([m['name'] for m in owner['members']],[m['name'] for m in self.unit['members']])
  for m in self.unit['members']:self.assertIsNotNone(self.html.find(id=anchor(self.unit,m)))
 def test_complete_teaching_text_in_html_and_pdf(self):
  values=[self.unit['introduction'],self.unit['compatibility'],self.unit['exercise']['question'],self.unit['exercise']['answer'],self.unit['exercise']['implementation_notes']]
  values+=self.unit['objectives']+self.unit['prerequisites']+list(self.unit['terms'].values())+self.unit['still_open']
  values += [s['text'] for s in self.unit['shared_sections']]
  for m in self.unit['members']:
   values+=[m[k] for k in ['meaning','inputs_and_conversions','returns_and_defaults','errors_and_restrictions','effects_and_ordering','explanation']]+m['algorithm']
  for value in values:
   for label,text in [('HTML',self.html.get_text()),('PDF',self.pdf)]:self.assertIn(self.normalized(value),self.normalized(text),(label,value[:70]))
 def test_exact_example_code_and_exercise_present(self):
  codes=[m['code'] for m in self.unit['members']]+[self.unit['exercise'][k] for k in ['html','code','usage_code']]
  rendered=[n.get_text() for n in self.html.select('.behavior-unit pre code')]
  self.assertEqual(rendered,codes)
  for code in codes:self.assertIn(self.normalized(code),self.normalized(self.pdf))
 def test_source_and_renderer_are_fingerprinted(self):
  protected={p.relative_to(R).as_posix() for p in input_paths(R)}
  self.assertIn('content/api-behavior.json',protected);self.assertIn('tools/behavior_reference.py',protected)
 def test_export_is_same_source(self):
  data=json.loads((SITE/'data/api-behavior.json').read_text());self.assertEqual(data['units'][0],self.unit)
  md=(SITE/'markdown/behavior-storage.md').read_text();self.assertIn(self.unit['exercise']['code'],md)
 def test_unique_ids_and_real_search_target(self):
  ids=[n['id'] for n in self.html.select('[id]')];self.assertEqual(len(ids),len(set(ids)))
  entries=json.loads((SITE/'assets/search.js').read_text().removeprefix('window.BOOK_SEARCH = ').strip().removesuffix(';'))
  self.assertTrue(any(e['path']=='reference/api/storage.html#behavior-storage' and e['kind']=='BEHAVIOUR' for e in entries))
 def test_source_url_attributes_are_escaped(self):
  u=json.loads(json.dumps(self.unit));u['members'][0]['sources']=['https://example.invalid/?x=" onmouseover="bad']
  text=render_unit(u,escape,lambda code,lang:'<pre>'+escape(code)+'</pre>')
  soup=BeautifulSoup(text,'html.parser');self.assertFalse(soup.select('[onmouseover]'))
 def test_no_em_dashes_in_authored_unit(self):self.assertNotIn('\u2014',json.dumps(self.unit,ensure_ascii=False))
if __name__=='__main__':unittest.main()
