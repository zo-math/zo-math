"""R2-G01 approved statistical cover. Generates SVG/PNG only; no PDF."""
from pathlib import Path
from collections import Counter
import sys,json,hashlib,xml.etree.ElementTree as ET
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'scripts/zo_python.py').is_file())
sys.path.insert(0,str(ROOT/'scripts'))
from zo_graphics import graphics_root
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
P=Path(__file__).resolve().parent.parent
data=P/'du_lieu/hoc.json';palette=ROOT/'_design/ngon_ngu_thiet_ke_zo_math_0_4/07_mau_thi_giac/design/color_system.json'
font_path=graphics_root(ROOT)/'assets/fonts/STIXTwoText-Regular.otf'
F=TTFont(font_path);G=F.getGlyphSet();CM=F.getBestCmap();UPM=F['head'].unitsPerEm
MF=TTFont(font_path.with_name('STIXTwoMath.otf'));MG=MF.getGlyphSet();MCM=MF.getBestCmap()
C=json.loads(palette.read_text('utf-8'))['palette'];ink=C['gray-8'];red=C['red-6']
rows=[r for r in json.loads(data.read_text('utf-8'))['penguins'] if r['source_row']<=17]
values=[int(r['flipper_length_mm']) for r in rows if r['flipper_length_mm']!='NA']
assert len(rows)==17 and len(values)==16 and sum(values)==3021
mean=sum(values)/len(values);ordered=sorted(values);median=(ordered[7]+ordered[8])/2
bins=[180,185,190,195,200];freq=[sum(a<=v<b for v in values) for a,b in zip(bins,bins[1:])]
assert freq==[4,3,5,4] and median==190
ET.register_namespace('','http://www.w3.org/2000/svg')
NS='{http://www.w3.org/2000/svg}'
svg=ET.Element(NS+'svg',{'viewBox':'0 0 400 400','width':'400','height':'400','role':'img','aria-labelledby':'cover-title cover-desc'})
ET.SubElement(svg,NS+'title',id='cover-title').text='Từ từng quan sát đến số đại diện'
ET.SubElement(svg,NS+'desc',id='cover-desc').text='16 số đo chiều dài chân chèo của Adélie 2007. Trung bình 188,8125 mm; trung vị 190 mm. Bốn khoảng rộng 5 mm có tần số 4, 3, 5, 4.'
def node(tag,**attrs):
 return ET.SubElement(svg,NS+tag,{k.replace('_','-'):str(v) for k,v in attrs.items()})
def text(x,y,label,size=17,anchor='middle',color=ink):
 pen=SVGPathPen(G);advance=0
 for char in label:
  font,glyphs,cmap=(F,G,CM) if ord(char) in CM else (MF,MG,MCM)
  assert ord(char) in cmap,repr(char)
  name=cmap[ord(char)];glyphs[name].draw(TransformPen(pen,(1,0,0,1,advance,0)));advance+=font['hmtx'][name][0]
 scale=size/UPM
 shift={'start':0,'middle':advance*scale/2,'end':advance*scale}[anchor]
 path=node('path',d=pen.getCommands(),transform=f'translate({x-shift:g} {y:g}) scale({scale:g} {-scale:g})',fill=color,aria_label=label)
 ET.SubElement(path,NS+'title').text=label
def line(x1,y1,x2,y2,color=ink,width=1.4,dash=None):
 a=dict(x1=x1,y1=y1,x2=x2,y2=y2,stroke=color,stroke_width=width,fill='none')
 if dash:a['stroke_dasharray']=dash
 node('line',**a)
x=lambda v:40+(v-180)*16
text(40,30,'Từng giá trị',21,'start')
text(40,60,'Trung bình ≈188,81',17,'start',red)
text(360,88,'Trung vị 190',17,'end',red)
# Explicit leaders attach each distinct label to its own marker.
line(80,68,x(mean),96,red,1.3,'4 3');line(x(mean),96,x(mean),184,red,1.5,'4 3')
line(316,96,x(median),117,red,1.3);line(x(median),117,x(median),184,red,1.5)
for value,count in Counter(values).items():
 for k in range(count):node('circle',cx=x(value),cy=174-k*18,r=5.1,fill=ink,data_value=value)
line(34,186,366,186)
for v in bins:line(x(v),186,x(v),192);text(x(v),211,str(v),15)
text(366,231,'mm',14,'end')
text(40,257,'Ghép nhóm',21,'start')
for a,b,f in zip(bins,bins[1:],freq):
 y=348-f*14
 node('rect',x=x(a),y=y,width=x(b)-x(a),height=348-y,fill=C['gray-3'],stroke=ink,stroke_width=1.2,data_interval=f'[{a};{b})',data_frequency=f)
 text((x(a)+x(b))/2,y-10,str(f),18)
line(34,348,366,348)
for v in bins:line(x(v),348,x(v),354);text(x(v),374,str(v),15)
text(366,394,'mm',14,'end')
out=P/'hinh';out.mkdir(exist_ok=True)
dest=out/'bia.svg';dest.write_bytes(ET.tostring(svg,encoding='utf-8',xml_declaration=True))
# PNG is a raster preview of these exact vector bytes, never a second drawing.
import shutil,subprocess
inkscape=shutil.which('inkscape');assert inkscape,'Inkscape required for SVG raster preview'
subprocess.run([inkscape,str(dest),'--export-type=png','--export-width=1000','--export-filename='+str(out/'bia.png')],check=True,capture_output=True)
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
manifest={'schema_version':1,'package':'R2-G01','role':'cover','generator':'_quy_trinh/sinh_bia.py','generator_sha256':sha(Path(__file__)),'data':'du_lieu/hoc.json','data_sha256':sha(data),'selection':{'source_rows':[r['source_row'] for r in rows],'valid_values':values,'n':16,'mean':mean,'median':median,'bins':bins,'frequencies':freq},'style_source':palette.relative_to(ROOT).as_posix(),'style_sha256':sha(palette),'font':'ZO Math Graphics/assets/fonts/STIXTwoText-Regular.otf','font_sha256':sha(font_path),'svg':{'path':'hinh/bia.svg','sha256':sha(dest)},'png':{'path':'hinh/bia.png','sha256':sha(out/'bia.png')},'direction':'owner_approved','rendered_cover':'pending_owner_review','pdf_generated':False}
(P/'giao_dien/bia_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n','utf-8')
cover={'schema_version':1,'package':'r2_g01','image':'hinh/bia.svg','sha256':sha(dest),'selection_reason':'Cùng một mẫu Học: 16 số đo, vị trí trung bình/trung vị và bốn nhóm tần số. Không dùng dữ liệu Luyện, Kiểm tra, Ôn lại hay Sửa lỗi.','approval':'direction_approved','image_acceptance':'pending_owner_review','approval_evidence':'Chủ trì duyệt phương án bìa và HTML rồi giao hoàn thiện, dựng xem ngày 22/10/2026; hồ sơ duyet_qmd_va_huong_html_20261022.json. Hình thành phẩm chờ chủ trì xem.'}
(P/'giao_dien/anh_bia.json').write_text(json.dumps(cover,ensure_ascii=False,indent=2)+'\n','utf-8')
print(json.dumps({'n':len(values),'mean':mean,'median':median,'frequencies':freq,'svg_sha256':sha(dest)},ensure_ascii=False))
