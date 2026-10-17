"""Unit tests for publication guards, not synthetic PDF/UA validation claims."""
from pathlib import Path
import hashlib, json, subprocess, sys, tempfile, unittest
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'tools'))
import pdf


class ReleaseGuard(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root/'deliverables').mkdir()
        (self.root/'docs/releases/2026.1').mkdir(parents=True)
        self.target = self.root/'deliverables/ctrotech-html-playbook.pdf'
        self.target.write_bytes(b'unit-test artifact; not a real validated PDF')
        self.proof_path = self.root/'docs/releases/2026.1/pdf-validation.json'
        self.proof = {'isCompliant': True, 'profile': 'PDF/UA-1', 'artifact_sha256': hashlib.sha256(self.target.read_bytes()).hexdigest(), 'publication_fingerprint': 'test-fingerprint'}
        self.write()
        self.fp = patch.object(pdf, 'publication_fingerprint', return_value='test-fingerprint')
        self.fp.start()

    def tearDown(self):
        self.fp.stop()
        self.temp.cleanup()

    def write(self):
        self.proof_path.write_text(json.dumps(self.proof))

    def test_matching_guard(self):
        self.assertTrue(pdf.verify_primary_pdf(self.root)['isCompliant'])

    def test_reject_modified_artifact(self):
        self.target.write_bytes(b'altered artifact')
        with self.assertRaisesRegex(AssertionError, 'does not match'):
            pdf.verify_primary_pdf(self.root)

    def test_reject_stale_source(self):
        self.proof['publication_fingerprint'] = 'old'
        self.write()
        with self.assertRaisesRegex(AssertionError, 'current publication inputs'):
            pdf.verify_primary_pdf(self.root)

    def test_reject_failed_or_wrong_profile(self):
        for field, value in [('isCompliant', False), ('profile', 'PDF/A-1B')]:
            with self.subTest(field=field):
                good = self.proof.copy()
                self.proof[field] = value
                self.write()
                with self.assertRaises(AssertionError):
                    pdf.verify_primary_pdf(self.root)
                self.proof = good

    def test_reject_missing_proof(self):
        self.proof_path.unlink()
        with self.assertRaises(FileNotFoundError):
            pdf.verify_primary_pdf(self.root)

    def test_selects_current_records_without_overwriting_history(self):
        (self.root/'content').mkdir()
        (self.root/'content/publication.json').write_text(json.dumps({'pdf_validation_directory':'docs/releases/update-test'}))
        records=self.root/'docs/releases/update-test'
        records.mkdir()
        (records/'pdf-validation.json').write_text(json.dumps(self.proof))
        self.proof_path.write_text('historical record deliberately not the active proof')
        self.assertTrue(pdf.verify_primary_pdf(self.root)['isCompliant'])

    def test_rejects_out_of_release_records(self):
        (self.root/'content').mkdir()
        (self.root/'content/publication.json').write_text(json.dumps({'pdf_validation_directory':'../outside'}))
        with self.assertRaisesRegex(AssertionError,'inside docs/releases'):
            pdf.verify_primary_pdf(self.root)

    def test_renderer_failure_preserves_old_artifact_and_proof(self):
        original = self.target.read_bytes(), self.proof_path.read_bytes()
        with patch.object(pdf.subprocess, 'run', side_effect=subprocess.CalledProcessError(1, 'renderer')):
            with self.assertRaises(subprocess.CalledProcessError):
                pdf.build_pdf(self.root, self.root/'site', [], {})
        self.assertEqual(original, (self.target.read_bytes(), self.proof_path.read_bytes()))


if __name__ == '__main__':
    unittest.main()
