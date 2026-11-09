"""The final course shell must not restore an obsolete PDF lifecycle warning."""
import unittest
from unittest.mock import patch
from bs4 import BeautifulSoup
import yaml
import zo_course_site as site

class PdfStateTests(unittest.TestCase):
    def document(self):
        source=site.ROOT/site.c.BASE/'hoc_lieu/r1_g03/index.qmd'
        cfg=yaml.safe_load((source.parent/'_quy_trinh/cau_hinh_san_xuat_qmd.yml').read_text('utf-8'))
        cards=''.join('<div class="zo-pdf-card"><a download href="'+v['output']+'">PDF</a><small class="zo-pdf-version-note">Old</small></div>' for v in cfg['extensions']['pdf_variants'].values())
        return BeautifulSoup('<article class="reader-content"><p id="lesson">Giữ nguyên bài học.</p><section id="tai-tai-lieu"><h2>Tải tài liệu</h2><p class="zo-pdf-current-note">Các PDF đang giữ bản cũ, chưa phản ánh bản sửa R01.</p>'+cards+'</section></article>','html.parser')

    def test_current_pdf_replaces_obsolete_revision_warning(self):
        states={name:{'errors':[],'status':'current'} for name in ['full','student','bai_hoc','luyen_tap','kiem_tra','sua_loi','on_lai','loi_giai']}
        with patch('zo_course_pdf_download_state.inspect_print_states',return_value=states):
            doc,notes=site.prepare_reader(self.document(),'r1_g03')
        self.assertIn('bản cũ',notes[0])
        self.assertNotIn('bản cũ',doc.get_text())
        self.assertEqual(doc.select_one('.zo-pdf-current-note').get_text(),'Các bản PDF đã cập nhật từ cùng nguồn học liệu.')
        self.assertEqual(doc.select_one('#lesson').get_text(),'Giữ nguyên bài học.')
        self.assertEqual(len(doc.select('.zo-pdf-card[data-pdf-current="true"]')),8)

    def test_stale_pdf_remains_blocked(self):
        states={name:{'errors':['changed source'],'status':'stale'} for name in ['full','student','bai_hoc','luyen_tap','kiem_tra','sua_loi','on_lai','loi_giai']}
        with patch('zo_course_pdf_download_state.inspect_print_states',return_value=states):
            doc,_=site.prepare_reader(self.document(),'r1_g03')
        self.assertEqual(len(doc.select('.zo-pdf-card[data-pdf-current="false"]')),8)
        self.assertIn('chưa dùng để xuất bản',doc.select_one('.zo-pdf-current-note').get_text())
        self.assertNotIn('PDF đã cập nhật.',doc.get_text())

if __name__=='__main__':unittest.main(verbosity=2)
