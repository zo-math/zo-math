"""The D0 download must bind its dedicated current PDF, not an R1 receipt."""
import json,tempfile,unittest
from pathlib import Path
from pypdf import PdfWriter
from zo_web_2027_d0 import pdf_download,sha
class D0DownloadTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name);self.pkg=Path('d0');p=self.root/self.pkg;(p/'_quy_trinh').mkdir(parents=True);(p/'index.qmd').write_text('source');w=PdfWriter();w.add_blank_page(100,100);w.write(p/'index.pdf');self.record={'output_sha256':sha(p/'index.pdf'),'inputs_sha256':{'d0/index.qmd':sha(p/'index.qmd')}};self.save()
 def save(self):(self.root/self.pkg/'_quy_trinh/pdf_build.json').write_text(json.dumps(self.record))
 def test_current_pdf_link(self):
  text=pdf_download(self.root,self.pkg,'index.pdf');self.assertIn('href="index.pdf"',text);self.assertIn('1 trang',text);self.assertIn('download=',text)
 def test_changed_source_blocks(self):
  (self.root/self.pkg/'index.qmd').write_text('changed')
  with self.assertRaises(ValueError):pdf_download(self.root,self.pkg,'index.pdf')
 def test_wrong_output_blocks(self):
  self.record['output_sha256']='bad';self.save()
  with self.assertRaises(ValueError):pdf_download(self.root,self.pkg,'index.pdf')
 def test_empty_input_inventory_blocks(self):
  self.record['inputs_sha256']={};self.save()
  with self.assertRaises(ValueError):pdf_download(self.root,self.pkg,'index.pdf')
if __name__=='__main__':unittest.main()
