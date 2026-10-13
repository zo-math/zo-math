from pathlib import Path
from lxml import html,etree
from collections import Counter
import json,hashlib,copy,re,subprocess,fitz
R=Path(__file__).resolve().parents[1];old=R.parent/'specimen_0_2';src=R/'reference/r1_g01_original.html';s=html.fromstring(src.read_text());n=html.fromstring((R/'r1_g01.html').read_text());checks=[]
def check(name,result,detail=None):checks.append(dict(name=name,pass_=bool(result),detail=detail))
baseline=json.loads((R/'design/r1_preservation.json').read_text());ids=Counter(n.xpath('//*[@id]/@id'))
check('Toàn bộ id nội dung nguồn còn nguyên',set(baseline['original_ids'])<=set(ids));check('Không trùng id',not [k for k,v in ids.items() if v>1],[k for k,v in ids.items() if v>1])
original=Counter(baseline['original_formulas']);current=Counter(n.xpath('//math//annotation/text()'))
for p in baseline['punctuation_changes']:original[p['before']]-=1;original[p['after']]+=1
check('Bảo toàn toàn bộ nguồn LaTeX, trừ dấu chấm được ghi nhận',not list((original-current).elements()),list((original-current).elements())[:3])
def content(doc):
 root=copy.deepcopy(doc.xpath('//div[contains(@class,"zo-on-thi-package")]')[0])
 for e in root.xpath('.//figure[@data-bbt]|.//div[contains(@class,"variation-scroll")]|.//*[@data-added-role]|.//*[@data-added-note]'):e.drop_tree()
 for e in root.xpath('.//math'):
  a=e.xpath('.//annotation');t=(a[0].text or '') if a else ''.join(e.itertext())
  for p in baseline['punctuation_changes']:t=t.replace(p['before'],p['after'])
  x=html.Element('span');x.text='$'+t.strip()+'$';x.tail=e.tail;e.getparent().replace(e,x)
 return re.sub(r'\s+',' ',root.text_content()).strip()
a=content(s);b=content(n);check('Bảo toàn văn bản và thứ tự nội dung ngoài BBT',a==b,{'source_chars':len(a),'new_chars':len(b)})
if a!=b:
 import difflib
 (R/'qa/text_diff.txt').write_text('\n'.join(difflib.unified_diff(a.split(),b.split())))
check('Mã màu 0.2 giữ nguyên', set(json.loads((R/'design/color_system.json').read_text())['palette'].values())==set(v.upper() for v in json.loads((old/'design/color_system.json').read_text())['palette'].values()))
for p in (R/'social/retained_0_2').glob('*.png'):check('Giữ nguyên bìa '+p.name,p.read_bytes()==(old/'social'/p.name).read_bytes())
for p in (R/'reference/r1_pdf').glob('*.pdf'):
 d=fitz.open(p);check('PDF nguồn đọc được '+p.name,len(d)>0)
for rec in json.loads((R/'design/variation_records.json').read_text()):
 t=n.xpath('//table[@data-bbt="'+rec['id']+'"]')[0];rows=t.xpath('./thead/tr|./tbody/tr');actual=[]
 for tr in rows:
  actual.append([c.xpath('.//annotation/text()')[0] if c.xpath('.//annotation') else c.text_content().strip() for c in tr])
 from table_engine import texify
 expected=[[texify(v) for v in row] for row in rec['rows']]
 check('Dữ liệu bảng '+rec['id'],actual==expected)
 for ext in ['html','qmd','tex','pdf','png']:check(rec['id']+' có nguồn '+ext,(R/'tables'/(rec['id'].lower()+'.'+ext)).exists())
 p=R/'tables'/(rec['id'].lower()+'.pdf');check(rec['id']+' PDF 1 trang',len(fitz.open(p))==1)
 check(rec['id']+' LaTeX không mất glyph','Missing character' not in p.with_suffix('.log').read_text())
source_dir=R.parent/'evidence/r1_g01/content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g01'
for p in (source_dir/'hinh').glob('do_thi_*.svg'):
 originalsvg=p.read_text();expected=re.sub(r'rgb\(100%,97\.645569%,91\.372681%\)','#FBFAF8',originalsvg)
 check('Đồ thị giữ đường và tọa độ '+p.name,expected==(R/'graphics'/('r1_'+p.name)).read_text())
for orient in ['doc','ngang']:
 p=R/'media'/('video_'+orient+'.mp4');out=subprocess.run(['ffprobe','-v','error','-show_entries','stream=codec_type,width,height','-of','json',str(p)],capture_output=True,check=True);streams=json.loads(out.stdout)['streams'];v=next(x for x in streams if x['codec_type']=='video')
 check('Video '+orient+' kích thước', [v['width'],v['height']]==([1080,1920] if orient=='doc' else [1920,1080]));check('Video '+orient+' có âm thanh',any(x['codec_type']=='audio' for x in streams));p2=subprocess.run(['ffmpeg','-v','error','-i',str(p),'-f','null','-'],capture_output=True);check('Video '+orient+' giải mã đủ',p2.returncode==0 and not p2.stderr,p2.stderr.decode())
report={'scope':'Source/content/media audit; not a visual browser test','checks':[{'name':c['name'],'pass':c['pass_'],'detail':c['detail']} for c in checks],'total':len(checks),'passed':sum(c['pass_'] for c in checks)}
(R/'qa/source_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps({'total':report['total'],'failed':[c for c in checks if not c['pass_']]},ensure_ascii=False,indent=2))
