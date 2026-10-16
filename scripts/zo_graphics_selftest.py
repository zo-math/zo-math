"""Regression checks for tool discovery and isolated-repository integration."""
from pathlib import Path
import os
import tempfile
import unittest
from unittest.mock import patch
from types import SimpleNamespace
from zo_graphics import graphics_root, graph_path, load_graph, _graph_api, load_variation, load_variation_html

class DiscoveryTests(unittest.TestCase):
    def test_relative_sibling_and_override_in_source_mirror(self):
        with tempfile.TemporaryDirectory() as temp:
            base=Path(temp)
            tool=base/'zo_math_graphics';tool.mkdir()
            (tool/'zo_geometry.py').write_text('# entry',encoding='utf-8')
            with patch.dict(os.environ,{},clear=True):
                self.assertEqual(graphics_root(base/'zo_math'),tool.resolve())
            with patch.dict(os.environ,{'ZO_MATH_GRAPHICS_ROOT':str(tool)},clear=True):
                self.assertEqual(graphics_root(base/'isolated/source'),tool.resolve())

    def test_missing_tool_and_audit_source_are_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            with patch.dict(os.environ,{},clear=True):
                with self.assertRaises(FileNotFoundError):graphics_root(Path(temp)/'zo_math')
            with patch.dict(os.environ,{'ZO_MATH_GRAPHICS_ROOT':str(Path(temp)/'_audit/tool')},clear=True):
                with self.assertRaises(ValueError):graphics_root()

    def test_graph_manifest_paths_resolve_without_old_files(self):
        repo=Path(__file__).resolve().parents[1]
        logical=repo/'quy_trinh_xay_dung/cong_cu_do_thi_ham_so_zo_math/tex/zo_graph_v02.tex'
        self.assertEqual(graph_path(logical),graphics_root()/'graph/tex/zo_graph_v02.tex')
        self.assertTrue(graph_path(logical).is_file())
        self.assertEqual(graph_path(repo/'index.qmd'),repo/'index.qmd')

    def test_graph_source_and_sidecar_scope_guards(self):
        with tempfile.TemporaryDirectory() as temp:
            project=Path(temp)/'project';project.mkdir()
            source=project/'valid.tex';source.write_text('source',encoding='utf-8')
            engine=load_graph('graph_scope_test',project)
            engine.validate_source(source,project)
            outside=Path(temp)/'outside.tex';outside.write_text('outside',encoding='utf-8')
            with self.assertRaises(engine.BuildError):engine.validate_source(outside,project)
            audit=project/'_audit/source.tex';audit.parent.mkdir();audit.write_text('audit',encoding='utf-8')
            with self.assertRaises(engine.BuildError):engine.validate_source(audit,project)
            args=engine.parse_args([str(source),'--style','0.4','--label-layout',str(audit)])
            with self.assertRaises(engine.BuildError):engine.build(args)

    def test_variation_resolution_html_import_and_source_boundary(self):
        repo=Path(__file__).resolve().parents[1]
        logical=repo/'quy_trinh_xay_dung/cong_cu_bang_bien_thien_zo_math/zo_variation_build.py'
        self.assertEqual(graph_path(logical),graphics_root()/'variation/zo_variation_build.py')
        engine=load_variation(logical)
        self.assertEqual(engine.ROOT,graphics_root())
        renderer=load_variation_html()
        source=repo/'content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g01/du_lieu/bang_bien_thien.json'
        self.assertEqual(engine.load_data(source),renderer.load_data(source))
        with self.assertRaises(ValueError):engine.load_data(repo/'_audit/table.json')

    def test_variation_binding_preserves_environment_and_prepends_style(self):
        calls=[]
        module=SimpleNamespace(run=lambda command,cwd,env:calls.append(env))
        _graph_api().bind_variation(module)
        original={'TEXINPUTS':'existing;','OTHER':'kept'}
        module.run(['dummy'],Path.cwd(),original)
        self.assertEqual(original,{'TEXINPUTS':'existing;','OTHER':'kept'})
        self.assertEqual(calls[0]['OTHER'],'kept')
        self.assertTrue(calls[0]['TEXINPUTS'].startswith(str(graphics_root()/'graph/tex')))
        self.assertTrue(calls[0]['TEXINPUTS'].endswith('existing;'))

if __name__=='__main__':unittest.main()
