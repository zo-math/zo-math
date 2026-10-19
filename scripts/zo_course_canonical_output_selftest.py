"""Canonical-output regressions using isolated files; no course render."""
import json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import zo_web_2027_bundle as b

class OutputTests(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name).resolve()
  (self.root/'_quarto.yml').write_text('project: {output-dir: docs}\n')
  self.produced=self.root/'.quarto/stage/docs';self.produced.mkdir(parents=True)
  self.out=self.root/'docs';self.out.mkdir()
 def tearDown(self):self.temp.cleanup()
 def write(self,path,value):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(value);return path
 def test_configured_docs_only(self):
  self.assertEqual(b.canonical_output(self.root),self.out)
  (self.root/'_quarto.yml').write_text('project: {output-dir: _audit/current}\n')
  with self.assertRaisesRegex(ValueError,'configured docs'):b.canonical_output(self.root)
 def test_overwrites_current_and_keeps_unrelated(self):
  self.write(self.produced/'lesson/index.html','fresh');self.write(self.out/'lesson/index.html','old');self.write(self.out/'unrelated.html','keep')
  files=b.install_current(self.produced,self.out,['lesson/index.html'],root=self.root)
  self.assertEqual((self.out/'lesson/index.html').read_text(),'fresh');self.assertEqual((self.out/'unrelated.html').read_text(),'keep');self.assertEqual(files['lesson/index.html'],b.sha(self.out/'lesson/index.html'))
 def test_audit_cannot_be_install_input(self):
  self.write(self.root/'_audit/old.html','historical')
  with self.assertRaisesRegex(ValueError,'freshly generated'):b.install_current(self.root/'_audit',self.out,['old.html'],root=self.root)
 def test_audit_cannot_be_product_destination(self):
  self.write(self.produced/'lesson.html','fresh')
  with self.assertRaisesRegex(ValueError,'canonical docs'):b.install_current(self.produced,self.root/'_audit/current',['lesson.html'],root=self.root)
 def test_traversal_rejected_before_output_change(self):
  self.write(self.produced/'lesson.html','fresh');self.write(self.out/'lesson.html','old')
  with self.assertRaisesRegex(ValueError,'Unsafe'):b.install_current(self.produced,self.out,['../escape.html'],root=self.root)
  self.assertEqual((self.out/'lesson.html').read_text(),'old')
 def test_copy_failure_restores_prior_outputs(self):
  for name in ['one.html','two.html']:self.write(self.produced/name,'fresh');self.write(self.out/name,'old')
  real=b.shutil.copyfile
  def copy(source,target):
   if Path(source)==self.produced/'two.html':raise OSError('copy fixture failure')
   return real(source,target)
  with patch.object(b.shutil,'copyfile',side_effect=copy):
   with self.assertRaisesRegex(OSError,'fixture'):b.install_current(self.produced,self.out,['one.html','two.html'],root=self.root)
  self.assertEqual((self.out/'one.html').read_text(),'old');self.assertEqual((self.out/'two.html').read_text(),'old')
 def test_missing_dependency_rejected_before_output_change(self):
  self.write(self.produced/'lesson.html','fresh');self.write(self.out/'lesson.html','old')
  with self.assertRaisesRegex(ValueError,'missing'):b.install_current(self.produced,self.out,['lesson.html','missing.css'],root=self.root)
  self.assertEqual((self.out/'lesson.html').read_text(),'old')

if __name__=='__main__':unittest.main(verbosity=2)
