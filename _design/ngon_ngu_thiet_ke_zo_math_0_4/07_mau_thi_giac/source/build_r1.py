from pathlib import Path
from lxml import html,etree
import base64,mimetypes,json,re,copy,hashlib
from table_engine import R,variation,render_sources,M
from web04 import upgrade,support
SRC=R.parent/'evidence/r1_g01/content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g01';source=html.fromstring((SRC/'index.html').read_text());root=copy.deepcopy(source.xpath('//main/div[contains(@class,"zo-on-thi-package")]')[0]);original=copy.deepcopy(root)
def uri(p):return 'data:'+(mimetypes.guess_type(p.name)[0] or 'application/octet-stream')+';base64,'+base64.b64encode(p.read_bytes()).decode()
def make(tag,text=None,**attrs):
 e=html.Element(tag,**attrs);e.text=text;return e
records={r['id']:r for r in json.loads((R/'design/variation_records.json').read_text())}
for fig in root.xpath('.//figure[@data-bbt]'):
 id=fig.get('data-bbt');rep=html.fragment_fromstring(variation(records[id]));rep.tail=fig.tail;fig.getparent().replace(fig,rep)
for image in root.xpath('.//img'):
 src=image.get('src','')
 if src.startswith('hinh/do_thi_'):p=R/'graphics'/('r1_'+Path(src).name)
 elif src.endswith('dau_nhan_zo.svg'):p=R/'logos/motif.svg'
 else:p=(SRC/src).resolve()
 if p.exists():image.set('src',uri(p));image.set('loading','lazy')
 else:raise FileNotFoundError(src)
for a in root.xpath('.//a'):
 href=a.get('href','')
 if href.endswith('.pdf'):
  p=R/'pdf/r1_editions'/href;a.set('href',uri(p));a.set('download','ZO_Math_R1_G01_'+p.stem+'_0_4.pdf');a.set('data-source-pdf',p.name)
# Preserve all original text and mathematics; add semantic labels above the content they qualify.
for block in root.xpath('.//*[contains(concat(" ",normalize-space(@class)," ")," zo-block ")]'):
 title=block.xpath('./*[contains(@class,"zo-block-title")]');cl=block.get('class','')
 if not title:continue
 t=title[0];text=t.text_content().strip();role='Hỗ trợ'
 if 'zo-block-red' in cl:role='Định nghĩa' if 'Định nghĩa' in text else 'Định lí'
 elif 'zo-block-yellow' in cl:role='Khám phá'
 elif 'solution' in cl:role='Lời giải'
 elif 'guidance' in cl:role='Hướng dẫn'
 label=make('span',role,**{'class':'role-tag block-tag','data-added-role':'true'})
 if t.tag=='summary':t.insert(0,label);label.tail=t.text;t.text=None
 else:block.insert(0,label)
for sec in root.xpath('.//section[contains(@class,"zo-learning-task--item")]'):
 sec.insert(0,make('span','Nhiệm vụ',**{'class':'role-tag','data-added-role':'true'}))
for table in root.xpath('.//table[not(@data-bbt)]'):
 table.set('class',table.get('class','')+' zo-table')
 for th in table.xpath('./thead/tr/th'):th.set('scope','col')
 for tr in table.xpath('./tbody/tr'):
  if len(tr) and tr[0].tag=='td':tr[0].tag='th';tr[0].set('scope','row')
# Explain downloaded PDFs as untouched source editions; no false claim of a PDF redesign.
pdf_sec=root.xpath('.//section[@id="tai-tai-lieu"]')[0];pdf_sec.insert(1,make('p','Các PDF dưới đây có bìa và trang kết thiết kế mới 0.4. Phần ruột giữ nguyên bản nội dung v1.3 bạn cung cấp ngày 06/10/2026; số trang ruột giữ hệ đánh số của bản nguồn.',**{'class':'reader-note','data-added-note':'true'}))
# One missing period in the source piecewise expression is a punctuation-only adjustment.
punct=[]
for ann in root.xpath('.//math//annotation'):
 tex=ann.text or ''
 if '\\begin{cases}' in tex and re.search(r'x\\geq1\s*\\end\{cases\}',tex):
  new=re.sub(r'x\\geq1(\s*\\end\{cases\})',r'x\\geq1.\1',tex);math=ann.getparent().getparent();rep=html.fragment_fromstring(M(new));rep.tail=math.tail;math.getparent().replace(math,rep);punct.append({'before':tex,'after':new})
# Organize every source chapter as readable white cards without changing text order.
for top in root.xpath('./section'):
 children=list(top)
 if any(c.tag=='section' for c in children):
  batch=[]
  def flush():
   if not batch:return
   wrap=make('div',**{'class':'reading-card section-intro'});top.insert(list(top).index(batch[0]),wrap)
   for c in batch:wrap.append(c)
   batch.clear()
  for c in children:
   if c.tag=='section':flush();c.set('class',c.get('class','')+' reading-card')
   else:batch.append(c)
  flush()
 else:top.set('class',top.get('class','')+' reading-card')
# Support appears at the end of the start/lesson/review stages and in the source download area.
for sid in ['bat-dau','bai-hoc','on-lai']:
 target=root.xpath('.//section[@id="'+sid+'"]')[0];target.append(html.fragment_fromstring(support(compact=True)))
orig_support=root.xpath('.//div[contains(@class,"r1-download-support")]')[0]
orig_support.set('class',orig_support.get('class')+' support-panel')
intro=make('p','ZO Math hiện chưa có tài trợ và cần kinh phí để tiếp tục biên soạn, xây dựng và duy trì học liệu. Sự ủng hộ của bạn giúp công việc này tiếp tục.',**{'class':'support-copy','data-added-note':'true'});orig_support.insert(2,intro)
# Keep bank details and the original QR unchanged; add a local copy action.
button=make('button','Sao chép số tài khoản',**{'type':'button','class':'button','data-copy-account':'0601000137768','data-added-note':'true'});orig_support.append(button);orig_support.append(make('p','',**{'class':'support-copy-status','role':'status','data-added-note':'true'}))
content=html.tostring(root,encoding='unicode');content=render_sources([content])[0]
css=(R/'source/system.css').read_text()
for f in (R/'assets').glob('*.ttf'):css=css.replace("url('../assets/"+f.name+"')",'url('+uri(f)+')')
controller=(R.parent/'evidence/r1_script_5.js').read_text().replace("lessonPanel.querySelector(':scope > .lesson-toc')","lessonPanel.querySelector('.lesson-toc')");(R/'source/r1_controller.js').write_text(controller)
common=(R/'source/common.js').read_text()
header=f'''<a class="skip" href="#readerMain">Đến nội dung</a><header class="topbar"><a href="#readerMain" aria-label="ZO Math — đến nội dung"><img src="{uri(R/'logos/horizontal_color.svg')}" alt="ZO Math"></a><div class="top-meta">Ôn thi Toán THPT 2027<br>R1-G01 · Bản dùng thử 0.4</div></header><div class="reader-shell"><section class="reader-hero"><div><span class="eyebrow">Học liệu nền tảng · R1-G01</span><h1>Đơn điệu<br>và cực trị</h1><p class="lead">Đọc đúng biểu diễn.<br>Giữ đủ điều kiện.</p><p class="reader-note">Dấu đạo hàm, tính đơn điệu và cực trị</p><img class="motif" src="{uri(R/'logos/motif.svg')}" alt="Dấu nhấn ZO"></div><div class="hero-picture"><img src="{uri(R/'graphics/r1_do_thi_02.svg')}" alt="Đồ thị hàm bậc ba dùng trong bài học"><p class="smallprint">Một công thức, một bảng và một hình cùng cần khớp nhau.</p></div></section><div class="toolbar screen-only"><label><input id="grayMode" type="checkbox"> Xem sắc xám</label><label>Cỡ chữ <select id="textSize"><option value="1">100%</option><option value="1.25">125%</option><option value="1.5">150%</option></select></label></div><main id="readerMain" tabindex="-1" style="margin-top:36px">'''
page='<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>ZO Math · R1-G01 · Đơn điệu và cực trị · 0.4</title><style>'+css+'</style></head><body class="r1-g01-page">'+header+content+'</main></div><footer class="footer">ZO Math · R1-G01 · Giữ điều kiện. Kiểm kết luận.</footer><script>'+controller+'</script><script>'+common+'</script></body></html>'
page=upgrade(page,'r1')
(R/'r1_g01.html').write_text(page);(R.parent/'ZO_Math_R1_G01_0_4.html').write_text(page)
# Preservation baseline excludes new BBT representation but compares every original text node and formula.
def semantic(el):
 el=copy.deepcopy(el)
 for node in el.xpath('.//figure[@data-bbt]|.//div[contains(@class,"variation-scroll")]|.//*[@data-added-role]|.//*[@data-added-note]'):node.drop_tree()
 for m in el.xpath('.//math'):
  a=m.xpath('.//annotation');t='$'+(a[0].text or '').strip()+'$' if a else ''.join(m.itertext());p=make('span',t);p.tail=m.tail;m.getparent().replace(m,p)
 return re.sub(r'\s+',' ',el.text_content()).strip()
# Full hashes and id/LaTeX inventories allow audit without trusting a visual summary.
audit={'source_sha256':hashlib.sha256((SRC/'index.html').read_bytes()).hexdigest(),'original_ids':[e.get('id') for e in original.xpath('.//*[@id]')],'original_formulas':[a.text or '' for a in original.xpath('.//math//annotation')],'original_sections':[(s.get('id'),len(s.xpath('.//h3'))) for s in original.xpath('./section')],'punctuation_changes':punct,'bbt_replaced':list(records),'original_math_count':len(original.xpath('.//math')),'original_text_normalized':semantic(original)}
(R/'design/r1_preservation.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2));print('R1 bytes',len(page.encode()),'math source',audit['original_math_count'],'BBT',len(records))
