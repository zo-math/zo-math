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

if __name__=='__main__':unittest.main()
