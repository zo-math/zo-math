"""Meaningful negative cases for the handoff inspector; does not alter the real bundle."""
from pathlib import Path
import importlib.util,json,tempfile,shutil,unittest
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('inspector',HERE/'zo_design.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class IntegrityTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.tmp=tempfile.TemporaryDirectory(prefix='zo_design_test_');cls.root=Path(cls.tmp.name)/'copy with spaces';shutil.copytree(m.ROOT,cls.root,ignore=shutil.ignore_patterns('__pycache__'))
 @classmethod
 def tearDownClass(cls):cls.tmp.cleanup()
 def test_01_clean_copy(self):self.assertTrue(m.check(self.root)['ok'])
 def test_02_missing_logo(self):
  p=self.root/'07_mau_thi_giac/logos/horizontal_color.svg';old=p.read_bytes();p.unlink()
  try:self.assertTrue(any('horizontal_color.svg' in e for e in m.check(self.root)['errors']))
  finally:p.write_bytes(old)
 def test_03_false_status_and_missing_evidence(self):
  p=self.root/'03_du_lieu/quy_tac.json';old=p.read_bytes();d=json.loads(old);d[0]['status']='approved_everywhere';d[0]['evidence']=['NO_SUCH_SOURCE'];p.write_text(json.dumps(d),encoding='utf-8')
  try:
   errors=m.check(self.root)['errors'];self.assertTrue(any('Trạng thái' in e for e in errors));self.assertTrue(any('Căn cứ' in e for e in errors))
  finally:p.write_bytes(old)
 def test_04_changed_original_detected(self):
  p=next((self.root/'06_nguon/tai_lieu_da_cung_cap').glob('01-*.md'));old=p.read_bytes();p.write_bytes(old+b'changed')
  try:self.assertTrue(any('Nguồn gốc đã đổi' in e for e in m.check(self.root)['errors']))
  finally:p.write_bytes(old)
 def test_05_journal_is_mutable(self):
  p=self.root/'09_nhat_ki/lich_su.md';old=p.read_bytes();p.write_bytes(old+b'\nA legitimate new session.\n')
  try:self.assertTrue(m.check(self.root)['ok'])
  finally:p.write_bytes(old)
 def test_06_escape_rejected(self):
  with self.assertRaises(ValueError):m.resolved(self.root,'../outside')
if __name__=='__main__':unittest.main()
