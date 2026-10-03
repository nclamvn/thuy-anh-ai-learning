"""Adversarial checks for the references-only publication profile."""
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools'))
from check_public import verify_distribution

class PublicDistribution(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.project=Path(self.temp.name)/'repo'
        shutil.copytree(ROOT,self.project,ignore=shutil.ignore_patterns('.git','__pycache__','.venv','node_modules','exports','observed','runtime'))
    def test_available_source_integrity_passes_but_capture_is_unavailable(self):
        result=verify_distribution(self.project)
        self.assertEqual(result['status'],'PASS',result)
        self.assertEqual(result['fullCaptureProvenance']['status'],'UNAVAILABLE')
        self.assertGreater(result['fullCaptureProvenance']['omittedRawCaptures'],0)
    def test_modified_generated_lesson_detected(self):
        path=self.project/'app/resources/lessons.json';path.write_bytes(path.read_bytes()+b' ')
        result=verify_distribution(self.project);self.assertEqual(result['status'],'FAIL');self.assertIn('fingerprint',result['errors'][0])
    def test_missing_available_authored_document_detected(self):
        (self.project/'materials/en/curriculum/lesson-02.md').unlink()
        self.assertEqual(verify_distribution(self.project)['status'],'FAIL')
    def test_raw_third_party_capture_is_rejected(self):
        path=self.project/'research/fulltexts/SRC-08.pdf';path.write_bytes(b'Synthetic forbidden raw distribution fixture')
        self.assertEqual(verify_distribution(self.project)['status'],'FAIL')
    def test_symlink_alias_is_rejected_even_when_bytes_match(self):
        path=self.project/'materials/en/curriculum/lesson-02.md'
        clone=Path(self.temp.name)/'outside.md';clone.write_bytes(path.read_bytes());path.unlink();path.symlink_to(clone)
        self.assertEqual(verify_distribution(self.project)['status'],'FAIL')

if __name__=='__main__':unittest.main()
