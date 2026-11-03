"""Regression checks for the explicit integrated-course publication path."""
import hashlib,tempfile,unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
import zo_publish as p
import zo_publish_current_course as current
import zo_publish_course as course

class CurrentReleaseTests(unittest.TestCase):
 def test_reviewed_file_tampering_is_rejected(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);f=root/'page.html';f.write_text('reviewed','utf-8');seal={'page.html':hashlib.sha256(f.read_bytes()).hexdigest()}
   current.verify_files(root,seal);f.write_text('changed','utf-8')
   with self.assertRaises(p.ConfigError):current.verify_files(root,seal)
 def test_missing_reviewed_file_is_rejected(self):
  with tempfile.TemporaryDirectory() as d:
   with self.assertRaises(p.ConfigError):current.verify_files(Path(d),{'missing.pdf':'0'*64})
 def test_review_seal_cannot_escape_checkout(self):
  with tempfile.TemporaryDirectory() as d:
   with self.assertRaises(p.ConfigError):current.verify_files(Path(d),{'../outside.pdf':'0'*64})
 def test_current_and_historical_modes_are_exclusive(self):
  self.assertNotEqual(p.main(['prepare','--current-course','--approved-course']),0)
  self.assertNotEqual(p.main(['prepare','--current-course','--page','index.html']),0)
 def test_current_mode_does_not_apply_to_publish_action(self):
  self.assertNotEqual(p.main(['publish','--current-course']),0)
 def test_current_receipt_reverifies_current_seal(self):
  payload={'approved_course':{'verification_mode':'current-course','approval_seal':{'old':True}}}
  with patch.object(current,'verify_current',return_value={'new':True}) as verifier:
   with self.assertRaises(p.ConfigError):course.validate_receipt(Path('.'),Path('.'),{},payload)
   verifier.assert_called_once()
 def test_historical_receipts_keep_original_acceptance_gate(self):
  payload={'approved_course':{'approval_seal':{'old':True}}}
  with patch.object(course,'verify_approved',return_value={'new':True}) as verifier:
   with self.assertRaises(p.ConfigError):course.validate_receipt(Path('.'),Path('.'),{},payload)
   verifier.assert_called_once()

if __name__=='__main__':unittest.main()
