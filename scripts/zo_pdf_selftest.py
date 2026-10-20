"""Regression checks for isolated builds with externally installed graphics tools."""
from pathlib import Path
from types import SimpleNamespace
import tempfile
import unittest
from unittest.mock import patch
import zo_pdf

class IsolationTests(unittest.TestCase):
    def test_external_engine_is_not_copied_back_and_audit_is_excluded(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)/'source';root.mkdir()
            for folder in ('assets','scripts','content/pkg/_audit'):
                (root/folder).mkdir(parents=True,exist_ok=True)
            (root/'content/pkg/index.qmd').write_text('source',encoding='utf-8')
            (root/'content/pkg/_audit/history.txt').write_text('history',encoding='utf-8')
            (root/'shared.txt').write_text('shared',encoding='utf-8')
            directory=Path(temp)/'build';directory.mkdir()
            logical=Path('quy_trinh_xay_dung/cong_cu_bang_bien_thien_zo_math/zo_variation_build.py')
            external=Path(temp)/'external.py';external.write_text('engine',encoding='utf-8')
            def resolve(path,repo):return external if path==root/logical else path.resolve()
            with patch.object(zo_pdf,'ROOT',root),patch.object(zo_pdf,'graph_path',side_effect=resolve),patch.object(zo_pdf,'discover_project_config',return_value=SimpleNamespace(project_root=Path('content/pkg'))),patch.object(zo_pdf,'pipeline_input_paths',return_value=(logical,Path('shared.txt'))):
                mirror=zo_pdf.isolated_project(root/'content/pkg/index.qmd',directory)
            self.assertFalse((mirror/logical).exists())
            self.assertFalse((mirror/'content/pkg/_audit').exists())
            self.assertEqual((mirror/'shared.txt').read_text(),'shared')
            self.assertTrue((mirror/'content/pkg/index.qmd').is_file())

    def test_candidate_build_option_is_explicit(self):
        with patch('sys.argv',['zo_pdf.py','build','index.qmd','--out-dir','.quarto/candidates']),patch.object(zo_pdf,'source_path',return_value=Path('index.qmd')):
            args=zo_pdf.parser().parse_args()
        self.assertEqual(args.out_dir,Path('.quarto/candidates'))

class VariantRegistryTests(unittest.TestCase):
    def definition(self,variants,variant='full'):
        from zo_pdf_contract import pdf_variant
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);source=root/'index.qmd';source.write_text('source',encoding='utf-8')
            with patch('zo_pdf_contract.discover_project_config',return_value=SimpleNamespace(raw={'extensions':{'pdf_variants':variants}})):
                return pdf_variant(root,source,variant)
    def test_full_only_review_is_a_complete_declared_registry(self):
        definition={'output':'index.pdf','metadata':{}}
        self.assertEqual(self.definition({'full':definition}),definition)
    def test_missing_full_still_rejected(self):
        with self.assertRaisesRegex(ValueError,'declare full'):
            self.definition({'student':{'output':'student.pdf'}})
    def test_multiple_variants_keep_output_collision_guard(self):
        with self.assertRaisesRegex(ValueError,'must not share'):
            self.definition({'full':{'output':'index.pdf'},'student':{'output':'index.pdf'}})


class SupportEndingTests(unittest.TestCase):
    def test_missing_support_on_last_page_blocks_replacement(self):
        with tempfile.TemporaryDirectory() as temp:
            pdf=Path(temp)/'candidate.pdf';pdf.write_bytes(b'%PDF-'+b' '*1100+b'%%EOF')
            approved=SimpleNamespace(pages=[SimpleNamespace(extract_text=lambda:'Bảo trợ ZO Math')])
            missing=SimpleNamespace(pages=[SimpleNamespace(extract_text=lambda:'Bảo trợ ZO Math'),SimpleNamespace(extract_text=lambda:'No support')])
            with patch('pypdf.PdfReader',return_value=approved):zo_pdf.validate_rendered_pdf(pdf)
            with patch('pypdf.PdfReader',return_value=missing),self.assertRaisesRegex(ValueError,'Bảo trợ'):
                zo_pdf.validate_rendered_pdf(pdf)

    def test_current_support_copy_and_account_are_required_for_every_variant(self):
        from zo_pdf_course_check import closing_support_checks
        support={'title':'Bảo trợ','copy':'Lời mời tự nguyện','cta':'Tìm hiểu thêm','fields':[{'value':'123456789'}]}
        good='Bảo trợ Lời mời tự nguyện Tìm hiểu thêm 123456789'
        self.assertTrue(all(closing_support_checks([good],support).values()))
        for bad in [good.replace('123456789','000000000'),good.replace('Lời mời tự nguyện',''),good.replace('Bảo trợ','')]:
            self.assertFalse(all(closing_support_checks([bad],support).values()))

if __name__=='__main__':unittest.main()
