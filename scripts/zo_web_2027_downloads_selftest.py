"""Regression coverage for metadata-owned PDF utilities."""
import unittest
from bs4 import BeautifulSoup
from zo_web_2027_downloads import metadata_section, project_source_section, download_region_coverage
class DownloadSectionTests(unittest.TestCase):
 def test_explicit_opt_in_required(self):
  d=BeautifulSoup('<div class="zo-on-thi-package reader-content"><p>Existing lesson</p></div>','html.parser')
  with self.assertRaises(ValueError):metadata_section(d)
  self.assertIsNone(d.select_one('#tai-tai-lieu'))
 def test_metadata_region_does_not_replace_lesson(self):
  d=BeautifulSoup('<div class="zo-on-thi-package reader-content"><p>Existing lesson</p></div>','html.parser')
  region=metadata_section(d,create_missing=True)
  self.assertEqual(d.p.string,'Existing lesson');self.assertEqual(region.h2.string,'Tải tài liệu')
  self.assertIs(metadata_section(d,create_missing=True),region)
  self.assertEqual(len(d.select('#tai-tai-lieu')),1)
 def test_requires_source_reader(self):
  d=BeautifulSoup('<main>Unrelated page</main>','html.parser')
  with self.assertRaises(ValueError):metadata_section(d,create_missing=True)
 def test_broken_existing_region_is_not_hidden(self):
  d=BeautifulSoup('<div class="zo-on-thi-package reader-content"><section id="tai-tai-lieu"></section></div>','html.parser')
  with self.assertRaises(ValueError):metadata_section(d,create_missing=True)
class SourceProjectionTests(unittest.TestCase):
 def test_fresh_content_keeps_layout_without_mutating_source(self):
  d=BeautifulSoup('<section id="tai-tai-lieu" class="level2"><p>Current 79 pages</p><div class="zo-pdf-card"></div></section>','html.parser')
  section=project_source_section(d.section,{'class':['level2','reading-region']})
  self.assertEqual(section.get_text(),'Current 79 pages')
  self.assertEqual(section['class'],['level2','reading-region'])
  self.assertEqual(d.section['class'],['level2'])
  self.assertTrue(download_region_coverage(section))
 def test_lost_reading_region_rejected(self):
  d=BeautifulSoup('<section><div class="zo-pdf-card"></div></section>','html.parser')
  self.assertFalse(download_region_coverage(d.section))
 def test_child_region_supported(self):
  d=BeautifulSoup('<section><div class="reading-region"><div class="zo-pdf-card"></div></div></section>','html.parser')
  self.assertTrue(download_region_coverage(d.section))
if __name__=='__main__':unittest.main()
