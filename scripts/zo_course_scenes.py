"""Canonical context-scene provenance and HTML gate; no generated edits."""
from pathlib import Path
import hashlib,json,re
from urllib.parse import unquote,urlsplit
ROOT=Path(__file__).resolve().parents[1]
# Authored dimension labels are 10 pt; graph labels use a different profile.
WEB_SVG_BP_PER_EM=10.0
def display_size(svg):
 import xml.etree.ElementTree as ET
 return float(ET.parse(svg).getroot().attrib["viewBox"].split()[2])/WEB_SVG_BP_PER_EM
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def declared(source):return (Path(source).parent/'giao_dien/minh_hoa_manifest.json').is_file()
def source_checks(source,repo=ROOT):
 p=Path(source).parent;m=json.loads((p/'giao_dien/minh_hoa_manifest.json').read_text(encoding='utf-8'));s=Path(source).read_text(encoding='utf-8');checks={}
 checks['scene manifest kind']=m.get('kind')=='parametric-scenes-v1'
 checks['canonical scene generator']=m.get('generator')=='_quy_trinh/sinh_hinh.py' and sha(p/m['generator'])==m.get('generator_sha256')
 checks['canonical scene data']=sha(p/'du_lieu/minh_hoa.json')==m.get('data_sha256')
 checks['no draft/audit source dependency']=not re.search(r'ban_thao|_audit', (p/m['generator']).read_text(encoding='utf-8'))
 for key in ['style','font','math_font']:checks[key+' current']=sha(m[key+'_source'])==m[key+'_sha256']
 for name,digest in m['outputs'].items():checks['scene '+name]=Path(name).name==name and sha(p/'hinh'/name)==digest
 data=json.loads((p/'du_lieu/minh_hoa.json').read_text(encoding='utf-8'));body={v['id'] for v in data['scenes'] if not v.get('cover')}
 images={Path(v).stem for v in re.findall(r'!\[[^\n]*\]\(([^)]+\.svg)\)',s)}
 checks['exact body illustration inventory']=images==body
 checks['scenes have no authored BBT']=not re.search(r'zo-native-bbt|\\(?:nearrow|searrow|rightarrow)',s)
 checks['dimension regression retained']=sum(m['dimension_checks'].values())==15 and len(m['dimension_negative_cases'])==5
 checks['kiosk regression retained']=m.get('kiosk_geometry_check')=='passed' and len(m.get('kiosk_negative_cases',[]))==5
 return checks

def html_checks(doc,source,page):
 source=Path(source);m=json.loads((source.parent/'giao_dien/minh_hoa_manifest.json').read_text(encoding='utf-8'));expected={n for n in m['outputs'] if n.endswith('.svg') and n!='huong_bia.svg'}
 images=doc.select('.reader-content .figure-viewport img');checks={'all context figures displayed':{Path(unquote(urlsplit(im['src']).path)).name for im in images}==expected and len(images)==len(expected)}
 for im in images:
  name=Path(unquote(urlsplit(im['src']).path)).name;asset=(Path(page).parent/unquote(urlsplit(im['src']).path)).resolve()
  checks[name+' rendered bytes']=asset.is_file() and sha(asset)==m['outputs'].get(name)
  checks[name+' context role']=im.get('data-zo-figure-role')=='context' and bool(im.get('alt'))
  canonical=source.parent/'hinh'/name
  checks[name+' readable authored label scale']=canonical.is_file() and im.get('style')==f'--figure-em:{display_size(canonical):.5f}em'
  checks[name+' scroll component']='zo-figure-scroll' in im.parent.get('class',[]) and im.parent.get('tabindex')=='0'
  fig=im.find_parent('figure');checks[name+' owned caption']=bool(fig and fig.find('figcaption'))
 return checks


def prepare_print_assets(source):
 """Convert current approved SVG bytes to print vectors, without regenerating scenes."""
 import shutil,subprocess,tempfile,io,xml.etree.ElementTree as ET,importlib.util
 from pypdf import PdfReader,PdfWriter
 from pypdf.generic import NameObject
 source=Path(source).resolve();folder=source.parent
 checks=source_checks(source)
 if not all(checks.values()):raise ValueError('Current canonical scene provenance required')
 binary=shutil.which('inkscape')
 if not binary:raise ValueError('Inkscape required for vector scene conversion')
 m=json.loads((folder/'giao_dien/minh_hoa_manifest.json').read_text(encoding='utf-8'));items={}
 helper=folder/'_quy_trinh/sinh_hinh_in.py';print_layout=None
 if helper.is_file():
  spec=importlib.util.spec_from_file_location('zo_scene_print_layout',helper);print_layout=importlib.util.module_from_spec(spec);spec.loader.exec_module(print_layout)
 for name,digest in m['outputs'].items():
  if not name.endswith('.svg'):continue
  svg=folder/'hinh'/name;target=svg.with_suffix('.pdf');box=[float(x) for x in ET.parse(svg).getroot().attrib['viewBox'].split()]
  with tempfile.TemporaryDirectory(prefix='scene_print_',dir=ROOT/'.quarto') as tmp:
   intermediate=Path(tmp)/target.name
   arranged=bool(print_layout and print_layout.build(name,intermediate))
   if not arranged:subprocess.run([binary,str(svg),'--export-type=pdf','--export-filename='+str(intermediate)],check=True,capture_output=True)
   reader=PdfReader(intermediate);assert len(reader.pages)==1
   writer=PdfWriter();page=reader.pages[0];page.pop(NameObject('/Group'),None);writer.add_page(page);writer.add_metadata({'/Creator':'ZO Math canonical SVG print conversion'})
   stream=io.BytesIO();writer.write(stream);target.write_bytes(stream.getvalue())
  page=PdfReader(target).pages[0]
  if not arranged:assert abs(float(page.mediabox.width)-box[2])<.1 and abs(float(page.mediabox.height)-box[3])<.1
  assert not any(ref.get_object().get('/Subtype')=='/Image' for ref in page['/Resources'].get('/XObject',{}).values()),'Rasterized scene'
  items['hinh/'+name]={'svg_sha256':digest,'pdf':'hinh/'+target.name,'pdf_sha256':sha(target),'width_bp':float(page.mediabox.width),'height_bp':float(page.mediabox.height),'layout':'source-geometry-stacked' if arranged else 'SVG-conversion','label_source_pt':10,'label_print_pt':10}
 receipt={'schema_version':1,'kind':'canonical-svg-print-v1','generator':'scripts/zo_course_scenes.py','generator_sha256':sha(Path(__file__)),'print_layout_sha256':sha(helper) if helper.is_file() else None,'converter':subprocess.check_output([binary,'--version'],text=True).strip(),'items':items,'owner_acceptance':'pending','published':False}
 (folder/'giao_dien/print_assets.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 return receipt


def print_model(source,refs):
 from pypdf import PdfReader
 source=Path(source);folder=source.parent;receipt=json.loads((folder/'giao_dien/print_assets.json').read_text(encoding='utf-8'))
 if receipt.get('kind')!='canonical-svg-print-v1' or receipt.get('generator_sha256')!=sha(Path(__file__)):raise ValueError('Stale scene print converter')
 helper=folder/'_quy_trinh/sinh_hinh_in.py'
 if receipt.get('print_layout_sha256') and (not helper.is_file() or receipt['print_layout_sha256']!=sha(helper)):raise ValueError('Stale source print layout')
 result={}
 for ref in refs:
  item=receipt['items'].get(ref)
  if not item or item['svg_sha256']!=sha(folder/ref) or item['pdf_sha256']!=sha(folder/item['pdf']):raise ValueError('Stale scene print pair: '+ref)
  page=PdfReader(folder/item['pdf']).pages[0];scale=item['label_print_pt']/item['label_source_pt'];width=float(page.mediabox.width)*72.27/72*scale;height=float(page.mediabox.height)*72.27/72*scale
  result[ref]={'pdf':item['pdf'],'width_pt':width,'height_pt':height,'scale':scale,'rotate':width>476,'stream_sha256':__import__('hashlib').sha256(page.get_contents().get_data().strip()).hexdigest()}
 return result
