"""Validate the frozen review checkpoint and its production non-change boundary."""
from pathlib import Path
import unittest,json,csv,hashlib,subprocess,sys
ROOT=Path(__file__).resolve().parents[3];P=ROOT/'docs/review-work';S=P/'storage-01'
class ReviewCheckpoint(unittest.TestCase):
    def test_exact_evidence_files(self):
        manifest=json.loads((S/'evidence-manifest.json').read_text())
        for name,sha in manifest['sha256'].items():
            path=(ROOT/name).resolve();self.assertTrue(path.is_relative_to(ROOT))
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),sha,name)
    def test_generated_manuscript(self):
        before=(S/'storage-behavior-review.md').read_bytes()
        subprocess.run([sys.executable,str(S/'render_review.py')],check=True,capture_output=True)
        self.assertEqual((S/'storage-behavior-review.md').read_bytes(),before)
    def test_six_draft_contracts_not_published(self):
        d=json.loads((S/'coverage-delta.json').read_text())
        self.assertEqual(d['draft_contracts_added'],6);self.assertEqual(len(d['members']),6)
        self.assertEqual(d['production_contracts_added'],0);self.assertEqual(d['formal_requirements_closed'],[])
        for m in d['members']:self.assertFalse(m['production_integrated']);self.assertFalse(m['independent_approval'])
    def test_browser_scope_and_open_finding(self):
        r=json.loads((S/'storage-browser-results.json').read_text())
        self.assertEqual(len(r['browsers']),3);self.assertEqual(sum(len(b['cases']) for b in r['browsers']),267)
        self.assertEqual(len(r['open_findings']),1);self.assertEqual(r['result'],'PASS_TESTED_STORAGE_SCOPE_WITH_FINDINGS')
    def test_exact_exercise_results(self):
        r=json.loads((S/'exercise-browser-results.json').read_text())
        self.assertEqual(len(r['browsers']),3);self.assertEqual(sum(len(b['scenarios']) for b in r['browsers']),30)
        self.assertTrue(all(c['result']=='PASS' for b in r['browsers'] for c in b['scenarios']))
    def test_actual_at_limits_preserved(self):
        r=json.loads((S/'orca-evidence/assessment.json').read_text())
        self.assertEqual(len(r['cases']),9);self.assertEqual(r['orca_speech_utterance_count'],308)
        self.assertEqual(sum(c['trace_result']=='EXPECTED_FRAGMENTS_OBSERVED' for c in r['cases']),8)
        self.assertEqual(len(r['open_observations']),2);self.assertFalse(r['human_listener']);self.assertFalse(r['independent'])
    def test_independent_queue_is_not_approval(self):
        with (P/'chapter-review-queue.csv').open() as f:rows=list(csv.DictReader(f))
        self.assertEqual(len(rows),74)
        self.assertTrue(all(r['state']=='AWAITING_INDEPENDENT_REVIEW' and not r['reviewer'] for r in rows))
    def test_production_inputs_unchanged(self):
        sys.path.insert(0,str(ROOT/'tools'));from fingerprint import publication_fingerprint
        self.assertEqual(publication_fingerprint(ROOT),'f9aa1fabe4430ce52c944abb127d2a8236be43fc7e943b0dc5aafc399fe7d408')
    def test_production_pdf_unchanged(self):
        self.assertEqual(hashlib.sha256((ROOT/'deliverables/ctrotech-html-playbook.pdf').read_bytes()).hexdigest(),'5685f8eb1dd9f073835e89a538e678e4151e809b8d4d26a801dbf1d99101590d')
if __name__=='__main__':unittest.main()
