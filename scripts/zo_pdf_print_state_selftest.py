"""Real provenance fixtures: web-only additions pass; print/PDF drift stays stale."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from pypdf import PdfWriter
import zo_pdf_contract as contract
from zo_pdf_print_state import HTML_ONLY, IMPORTS, inspect_print_states, print_projection

ROOT = Path(__file__).resolve().parents[1]


def video(ident='video-test', youtube='1WBLfF2gTGU'):
    return (HTML_ONLY+'\n```{=html}\n'
            f'<details class="zo-block zo-block-gray zo-learning-video" id="{ident}" data-youtube-id="{youtube}">\n'
            '<summary class="zo-block-title">Xem video: Ví dụ</summary>\n'
            '<div class="zo-block-body"><div class="zo-video-player"></div>\n'
            f'<p><a href="https://www.youtube.com/shorts/{youtube}" target="_blank" rel="noopener noreferrer">YouTube</a></p>\n'
            '</div></details>\n```\n\n:::\n\n')


class PrintStateTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory(prefix='pdf_print_', dir=ROOT/'_audit')
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        package = self.root/'pkg'
        (package/'_quy_trinh/ho_so').mkdir(parents=True)
        self.source = package/'index.qmd'
        self.foundation = package/'foundation.qmd'
        self.config = SimpleNamespace(project_root=Path('pkg'), config_path=Path('pkg/_quy_trinh/config.yml'), raw={'extensions': {
            'pdf_variants': {'full': {'output': 'index.pdf', 'metadata': {}}, 'student': {'output': 'student.pdf', 'metadata': {}}},
            'pdf_provenance_manifest': '_quy_trinh/ho_so/pdf_provenance.json',
            'pdf_source_fingerprint': 'course-qmd-without-download-page-counts-v1',
            'artifact_inputs': ['foundation.qmd', 'figure.svg'],
            'artifact_root_inputs': ['graphics/engine.tex'],
        }})
        self.config_patch = patch.object(contract, 'discover_project_config', return_value=self.config)
        self.config_patch.start(); self.addCleanup(self.config_patch.stop)
        self.external = self.root/'external/engine.tex'
        self.external.parent.mkdir(); self.external.write_bytes(b'original Graphics engine')
        self.graph_patch = patch.object(contract, 'graph_path', side_effect=lambda p, r: self.external if p == r/'graphics/engine.tex' else p)
        self.graph_patch.start(); self.addCleanup(self.graph_patch.stop)
        for relative in contract.pipeline_input_paths(self.root, self.source):
            path = self.root/relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b'original input')
        self.write(self.source, '---\ntitle: Bài học\nresources:\n  - index.pdf\n---\n\nNội dung $x^2$.\n\n')
        self.write(self.foundation, 'Nền $x+1$.\n\n')
        self.write(package/'_quy_trinh/ho_so/index.yml', "package:\n  id: FIXTURE\n  candidate_version: '1'\n")
        for variant in self.config.raw['extensions']['pdf_variants']:
            writer = PdfWriter(); writer.add_blank_page(width=595, height=842)
            writer.write(str(contract.pdf_output_path(self.root, self.source, variant)))
            contract.update_canonical_pdf_provenance(self.root, self.source, contract.pdf_output_path(self.root, self.source, variant), variant=variant)
        self.manifest = contract.canonical_pdf_provenance_path(self.root, self.source)
        self.manifest_bytes = self.manifest.read_bytes()

    def write(self, path, text):
        path.write_bytes(text.encode('utf-8'))

    def add_videos(self):
        text = self.source.read_text('utf-8').replace('resources:\n', 'resources:\n  - giao_dien/video.css\n  - giao_dien/video.js\n')
        text += HTML_ONLY+'\n```{=html}\n' + IMPORTS + '```\n\n:::\n\n' + video()
        self.write(self.source, text)
        self.write(self.foundation, self.foundation.read_text('utf-8') + video('video-foundation'))

    def states(self):
        return inspect_print_states(self.root, self.source)

    def assert_stale(self):
        self.assertTrue(self.states()['full']['errors'])

    def test_unchanged_build_and_all_variants_stay_current(self):
        self.assertTrue(all(s['status'] == 'current' for s in self.states().values()))

    def test_valid_videos_prove_same_print_inputs_without_rewriting_manifest(self):
        self.add_videos()
        self.assertTrue(contract.validate_canonical_pdf_provenance(self.root, self.source))
        states = self.states()
        self.assertTrue(all(s['status'] == 'print-equivalent' and not s['errors'] for s in states.values()))
        self.assertEqual(states['full']['web_only_videos'], ['video-test', 'video-foundation'])
        self.assertEqual(self.manifest.read_bytes(), self.manifest_bytes)

    def test_changed_math_remains_stale(self):
        self.add_videos(); self.write(self.source, self.source.read_text('utf-8').replace('x^2', 'x^3'))
        self.assert_stale()

    def test_changed_foundation_remains_stale(self):
        self.add_videos(); self.write(self.foundation, self.foundation.read_text('utf-8').replace('x+1', 'x-1'))
        self.assert_stale()

    def test_changed_figure_remains_stale(self):
        self.add_videos(); (self.source.parent/'figure.svg').write_bytes(b'changed figure')
        self.assert_stale()

    def test_changed_external_graphics_remains_stale(self):
        self.add_videos(); self.external.write_bytes(b'changed engine')
        self.assert_stale()

    def test_changed_print_metadata_remains_stale(self):
        self.add_videos(); self.write(self.source, self.source.read_text('utf-8').replace('title: Bài học', 'title: Khác'))
        self.assert_stale()

    def test_changed_second_pdf_does_not_inherit_first_pdf_pass(self):
        self.add_videos(); (self.source.parent/'student.pdf').write_bytes((self.source.parent/'student.pdf').read_bytes()+b'changed')
        states = self.states()
        self.assertFalse(states['full']['errors'])
        self.assertIn('PDF hash drift: student', states['student']['errors'])

    def test_forged_second_variant_fingerprint_remains_stale(self):
        self.add_videos(); payload=json.loads(self.manifest.read_text('utf-8')); payload['variants'][1]['input_fingerprint']='0'*64
        self.write(self.manifest,json.dumps(payload))
        self.assertIn('input fingerprint drift: student',self.states()['student']['errors'])

    def test_removed_dependency_or_variant_remains_stale(self):
        self.add_videos(); payload=json.loads(self.manifest.read_text('utf-8'));payload['pipeline_inputs'].pop()
        self.write(self.manifest,json.dumps(payload));self.assert_stale()

    def test_video_like_printed_code_is_not_removed(self):
        self.add_videos(); self.write(self.source,self.source.read_text('utf-8')+'````markdown\n'+video('video-example')+'````\n')
        self.assert_stale()

    def test_unfenced_html_is_not_removed(self):
        self.add_videos(); self.write(self.source,self.source.read_text('utf-8')+video('video-unfenced').replace('```{=html}\n','').replace('```\n',''))
        self.assert_stale()

    def test_latex_and_printed_text_near_video_are_not_removed(self):
        self.add_videos();self.write(self.source,self.source.read_text('utf-8')+'```{=latex}\nChanged print text.\n```\n')
        self.assert_stale()

    def test_invalid_video_markup_is_not_exempt(self):
        for bad in [video().replace('1WBLfF2gTGU', 'invalid'), video().replace('<summary ', '<summary onclick="bad" '), video().replace('</details>', '</div>'), video().replace('https://www.youtube.com/shorts/', 'https://example.com/')]:
            with self.subTest(fragment=bad), self.assertRaises(ValueError): print_projection(bad)

    def test_extra_resource_or_import_is_not_exempt(self):
        self.add_videos(); self.write(self.source,self.source.read_text('utf-8').replace('  - index.pdf', '  - unrelated.js\n  - index.pdf'))
        self.assert_stale()

    def test_duplicate_video_id_is_rejected(self):
        with self.assertRaises(ValueError): print_projection(video()+video())

    def test_raw_html_without_format_guard_is_not_certified(self):
        self.add_videos();self.write(self.source,self.source.read_text('utf-8').replace(HTML_ONLY+'\n', '').replace('\n:::\n','\n'))
        self.assert_stale()

    def test_format_guard_is_explicit_in_the_pandoc_ast(self):
        self.add_videos()
        text = self.source.read_text('utf-8')
        projected, _ = print_projection(text, main=True)
        # The real Quarto filter ordering is covered by the package preflight;
        # Pandoc alone does not implement Quarto's conditional-content feature.
        command = [sys.executable, str(ROOT/'scripts/zo_python.py'), str(ROOT/'scripts/zo_quarto.py'), 'pandoc', '--from=markdown', '--to=json']
        actual = subprocess.run(command, input=text, text=True, encoding='utf-8', capture_output=True, check=True)
        ast = json.loads(actual.stdout)
        guards = [b for b in ast['blocks'] if b['t']=='Div' and b['c'][0][1]==['content-visible']]
        self.assertEqual(len(guards),2)
        self.assertTrue(all(b['c'][0][2]==[['when-format','html']] and len(b['c'][1])==1 and b['c'][1][0]['t']=='RawBlock' and b['c'][1][0]['c'][0]=='html' for b in guards))


if __name__ == '__main__': unittest.main(verbosity=2)
