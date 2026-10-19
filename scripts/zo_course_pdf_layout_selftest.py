"""Regression tests for the shared print contract; no production files changed."""
import copy,json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import zo_course_pdf_layout as layout

ROOT=Path(__file__).resolve().parents[1]
class PrintContractTests(unittest.TestCase):
 def fixture(self,widths=(28,72),extra=''):
  tmp=tempfile.TemporaryDirectory();self.addCleanup(tmp.cleanup);root=Path(tmp.name)
  (root/layout.PROFILE).parent.mkdir(parents=True)
  (root/layout.PROFILE).write_bytes((ROOT/layout.PROFILE).read_bytes())
  src=root/'r1_g04/index.qmd';src.parent.mkdir();(src.parent/'du_lieu').mkdir()
  (src.parent/'du_lieu/bang_bien_thien.json').write_text('[]','utf-8')
  src.write_text('---\ntitle: Test\n---\n::: {#goals}\n| A | B |\n|---|---|\n| one | two |\n:::\n'+extra,'utf-8')
  data={'pages':{'r1_g04':[{'selector':'#goals table','kind':'rubric','function':'goals'}]},'function_profiles':{'goals':{'kind':'rubric','widths':list(widths)}}}
  return root,src,data
 def model(self,root,src,data):
  with patch.object(layout,'contract',return_value=data),patch.object(layout,'lesson_layout',return_value={'id':'lesson-g03'}):return layout.model(root,src)
 def test_shared_widths_override_stale_qmd_metadata(self):
  root,src,data=self.fixture();self.assertEqual(self.model(root,src,data)['tables']['goals']['widths'],[28,72])
 def test_wrong_column_count_rejected(self):
  root,src,data=self.fixture((20,30,50))
  with self.assertRaisesRegex(ValueError,'column mismatch'):self.model(root,src,data)
 def test_missing_native_variation_rejected(self):
  root,src,data=self.fixture(extra='::: {#bbt .zo-native-bbt data-bbt="bbt"}\n:::\n')
  with self.assertRaisesRegex(ValueError,'variation data'):self.model(root,src,data)
 def test_wrong_graph_preset_rejected(self):
  root,src,data=self.fixture()
  with patch.object(layout,'lesson_layout',return_value={'id':'other'}),self.assertRaisesRegex(ValueError,'G03'):layout.model(root,src)
 def test_missing_print_table_detected(self):
  data={'tables':{'goals':{'widths':[28,72]}},'variation_ids':['bbt']}
  checks=layout.validate_tex(r'\section{B}\subsection{C}\n% zo-variation bbt',data)
  self.assertFalse(checks['all bound table profiles projected'])
 def test_missing_print_variation_detected(self):
  data={'tables':{},'variation_ids':['bbt']}
  self.assertFalse(layout.validate_tex(r'\section{B}\subsection{C}',data)['all native variation tables projected'])
 def test_flattened_hierarchy_detected(self):
  self.assertFalse(layout.validate_tex(r'\subsubsection{B}',{'tables':{},'variation_ids':[]})['header hierarchy is promoted'])
 def test_other_packages_not_opted_in(self):
  from types import SimpleNamespace
  self.assertFalse(layout.enabled(SimpleNamespace(raw={'extensions':{'course_pdf_shell':{'reference':'D0_owner_approved_2026_10_14'}}})))

 def test_variation_cell_change_rejected(self):
  data={'tables':{},'variation_ids':['bbt'],'variations':{'bbt':{'rows':[['x','0'],["f′(x)",'+']]}}}
  tex='% zo-variation bbt\n'+r'\begin{tabular}{|c|c|}\hline'+'\n'+r'$x$ & $0$ \\ \hline'+'\n'+r"$f'(x)$ & $-$ \\ \hline"+'\n'+r'\end{tabular}\section{B}\subsection{C}'
  self.assertFalse(layout.validate_tex(tex,data)['variation cells preserved/bbt'])
 def test_variation_cells_intact(self):
  data={'tables':{},'variation_ids':['bbt'],'variations':{'bbt':{'rows':[['x','0'],["f′(x)",'+']]}}}
  tex='% zo-variation bbt\n'+r'\begin{tabular}{|c|c|}\hline'+'\n'+r'$x$ & $0$ \\ \hline'+'\n'+r"$f'(x)$ & $+$ \\ \hline"+'\n'+r'\end{tabular}\section{B}\subsection{C}'
  self.assertTrue(layout.validate_tex(tex,data)['variation cells preserved/bbt'])
 def reference_fixture(self,printed,task_only=False):
  from pypdf import PdfWriter,PdfReader
  from pypdf.generic import DictionaryObject,NameObject,DecodedStreamObject,ArrayObject,FloatObject,TextStringObject
  tmp=tempfile.TemporaryDirectory();self.addCleanup(tmp.cleanup);path=Path(tmp.name)/'reference.pdf';w=PdfWriter()
  for text in [f'BT /F1 11 Tf 100 750 Td (Xem loi giai \\(trang {printed}\\)) Tj ET', 'BT /F1 11 Tf 520 35 Td (2) Tj ET']:
   if task_only and len(w.pages)==0:text='BT /F1 11 Tf 520 750 Td (08) Tj ET'
   page=w.add_blank_page(width=595.276,height=841.89)
   font=DictionaryObject({NameObject('/Type'):NameObject('/Font'),NameObject('/Subtype'):NameObject('/Type1'),NameObject('/BaseFont'):NameObject('/Helvetica')})
   page[NameObject('/Resources')]=DictionaryObject({NameObject('/Font'):DictionaryObject({NameObject('/F1'):w._add_object(font)})})
   stream=DecodedStreamObject();stream.set_data(text.encode());page[NameObject('/Contents')]=w._add_object(stream)
  w.add_named_destination('answer',1);w.add_named_destination('bat-dau',0)
  ann=DictionaryObject({NameObject('/Type'):NameObject('/Annot'),NameObject('/Subtype'):NameObject('/Link'),NameObject('/Rect'):ArrayObject([FloatObject(v) for v in ([515,745,570,765] if task_only else [95,745,300,765])]),NameObject('/A'):DictionaryObject({NameObject('/S'):NameObject('/GoTo'),NameObject('/D'):TextStringObject('answer')})})
  w.pages[0][NameObject('/Annots')]=ArrayObject([w._add_object(ann)]);w.write(path)
  return path,PdfReader(path)
 def test_stale_printed_page_rejected(self):
  p,r=self.reference_fixture(3);report=layout.print_reference_checks(p,r);self.assertEqual(len(report['errors']),1)
 def test_current_printed_page_passes(self):
  p,r=self.reference_fixture(2);report=layout.print_reference_checks(p,r);self.assertEqual(len(report['samples']),1);self.assertEqual(report['errors'],[])

 def test_task_number_at_right_is_not_a_contents_page_number(self):
  p,r=self.reference_fixture(2,True);report=layout.print_reference_checks(p,r);self.assertEqual(report['errors'],[]);self.assertEqual(report['samples'],[])
 def test_vietnamese_row_label_in_math_rejected(self):
  data={'tables':{},'variation_ids':['bbt'],'variations':{'bbt':{'rows':[['Biến thiên','0']]}}}
  tex='% zo-variation bbt\n'+r'\begin{tabular}{|c|c|}\hline'+'\n'+r'$Biến thiên$ & $0$ \\ \hline'+'\n'+r'\end{tabular}\section{B}\subsection{C}'
  self.assertFalse(layout.validate_tex(tex,data)['variation text labels use text/bbt'])

 def heading_fixture(self,has_body):
  from types import SimpleNamespace
  def extract(**kw):
   v=kw['visitor_text'];cm=[1,0,0,1,0,0]
   v('Next lesson',[1,0,0,1,0,0],[1,0,0,1,60,120],{'/BaseFont':'/ABCDEF+BeVietnamPro-SemiBold'},13)
   if has_body:v('First paragraph',cm,[1,0,0,1,60,90],{'/BaseFont':'/ABCDEF+STIXTwoText-Regular'},11)
   return ''
  page=SimpleNamespace(mediabox=SimpleNamespace(height=841.89),extract_text=extract)
  return SimpleNamespace(pages=[None,page,None])
 def test_orphan_parent_heading_rejected(self):
  self.assertEqual(layout.orphan_print_headers(self.heading_fixture(False)),[{'page':2,'text':'Next lesson'}])
 def test_heading_with_body_passes(self):
  self.assertEqual(layout.orphan_print_headers(self.heading_fixture(True)),[])
 def test_projection_excludes_removed_solution_targets(self):
  root,src,data=self.fixture()
  src.write_text('---\ntitle: Test\nr1-section-download-files:\n  - variant: bai_hoc\n    start: bai-hoc\n---\n## Bắt đầu {#bat-dau}\nStart\n## Bài học {#bai-hoc}\n### Nhiệm vụ 01 {#Q1}\n[Xem lời giải](#A1)\n## Lời giải {#loi-giai}\n### Nhiệm vụ 01 {#A1}\n[Xem đề bài](#Q1)\n## Nguồn {#nguon}\nEnd\n','utf-8')
  with patch.object(layout,'contract',return_value=data),patch.object(layout,'lesson_layout',return_value={'id':'lesson-g03'}):
   full=layout.model(root,src);student=layout.model(root,src,'student');part=layout.model(root,src,'bai_hoc')
  self.assertEqual(full['solution_targets'],['A1']);self.assertEqual(student['solution_targets'],[]);self.assertEqual(part['task_numbers'],{'Q1':1});self.assertEqual(part['problem_targets'],[])
 def test_unicode_target_encoding_is_stable_and_ascii(self):
  value=layout.pdf_id('dừng-lại-1-d01')
  self.assertTrue(value.isascii());self.assertNotEqual(value,'dừng-lại-1-d01');self.assertEqual(layout.pdf_id('KD01'),'KD01')
 def test_rotated_graph_uses_all_four_transformed_corners(self):
  from pypdf import PdfWriter,PdfReader
  from pypdf.generic import DictionaryObject,NameObject,DecodedStreamObject,ArrayObject,FloatObject
  import hashlib
  tmp=tempfile.TemporaryDirectory();self.addCleanup(tmp.cleanup);p=Path(tmp.name)/'rotate.pdf';writer=PdfWriter();page=writer.add_blank_page(595,842)
  form=DecodedStreamObject();form.set_data(b'q Q');form.update({NameObject('/Type'):NameObject('/XObject'),NameObject('/Subtype'):NameObject('/Form'),NameObject('/BBox'):ArrayObject([FloatObject(v) for v in [0,0,100,200]]),NameObject('/Resources'):DictionaryObject()})
  page[NameObject('/Resources')]=DictionaryObject({NameObject('/XObject'):DictionaryObject({NameObject('/Fm1'):writer._add_object(form)})})
  stream=DecodedStreamObject();stream.set_data(b'q 0 1 -1 0 580 50 cm /Fm1 Do Q');page[NameObject('/Contents')]=writer._add_object(stream)
  with p.open('wb') as f:writer.write(f)
  rows=layout.embedded_graphs(PdfReader(p),{'graphs':{'wide.svg':{'stream_sha256':hashlib.sha256(b'q Q').hexdigest(),'scale':1}}})
  self.assertEqual(len(rows),1);self.assertTrue(rows[0]['inside_page'])

 def test_duplicate_automatic_figure_caption_rejected(self):
  data={'tables':{},'variation_ids':[],'explicit_figure_captions':1}
  tex='% zo-explicit-figure-caption\n'+r'\begin{figure}\caption{Alt text}\end{figure}\section{B}\subsection{C}'
  self.assertFalse(layout.validate_tex(tex,data)['explicit figure captions emitted once'])
 def test_explicit_caption_without_alt_caption_passes(self):
  data={'tables':{},'variation_ids':[],'explicit_figure_captions':1}
  tex='% zo-explicit-figure-caption\n'+r'\begin{figure}\includegraphics{a.pdf}\captionsetup{labelformat=empty}\caption{Hình 01 — Caption}\end{figure}\section{B}\subsection{C}'
  self.assertTrue(layout.validate_tex(tex,data)['explicit figure captions emitted once'])

 def test_floating_graph_rejected(self):
  data={'tables':{},'variation_ids':[]}
  self.assertFalse(layout.validate_tex(r'\begin{figure}\end{figure}\section{B}\subsection{C}',data)['figures remain in source order'])
 def test_anchored_graph_passes(self):
  data={'tables':{},'variation_ids':[]}
  self.assertTrue(layout.validate_tex(r'\begin{figure}[H]\end{figure}\section{B}\subsection{C}',data)['figures remain in source order'])

 def test_implicit_figure_uses_verified_common_H_default(self):
  data={'tables':{},'variation_ids':[],'figure_placement':'H'}
  self.assertTrue(layout.validate_tex(r'\input{zo-course-print-layout.tex}\begin{figure}\end{figure}\section{B}\subsection{C}',data)['figures remain in source order'])

class SourceOwnershipTests(unittest.TestCase):
 def test_left_aligned_graph_is_rejected(self):
  self.assertFalse(layout.centered_graphs([{'center_offset_pt':40}]))
  self.assertTrue(layout.centered_graphs([{'center_offset_pt':.2}]))
 def test_g04_refuses_overwriting_changed_tex(self):
  import importlib.util
  source=ROOT/'content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g04/_quy_trinh/sinh_hinh.py'
  spec=importlib.util.spec_from_file_location('g04_source_guard_test',source);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
  item=json.loads((module.PACKAGE/'du_lieu/hinh_do_thi.json').read_text('utf-8'))[0]
  with tempfile.TemporaryDirectory() as tmp:
   target=Path(tmp)/(item['id']+'.tex');target.write_text('manual label correction','utf-8')
   with patch.object(module,'ROOT',Path(tmp)),self.assertRaisesRegex(ValueError,'TEX differs'):
    module.make_source(item)
   self.assertEqual(target.read_text('utf-8'),'manual label correction')
 def test_g04_regeneration_matches_all_current_tex_without_writing(self):
  import importlib.util
  source=ROOT/'content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g04/_quy_trinh/sinh_hinh.py'
  spec=importlib.util.spec_from_file_location('g04_source_roundtrip_test',source);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
  captured={}
  with patch.object(Path,'write_text',lambda path,text,**kw:captured.__setitem__(path,text)):
   for item in json.loads((module.PACKAGE/'du_lieu/hinh_do_thi.json').read_text('utf-8')):module.make_source(item)
  self.assertEqual(len(captured),35)
  for path,text in captured.items():self.assertEqual(path.read_text('utf-8'),text,str(path))

if __name__=='__main__':unittest.main(verbosity=2)
