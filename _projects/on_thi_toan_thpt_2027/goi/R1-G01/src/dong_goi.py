"""Đóng gói HTML độc lập và bản Markdown từ nội dung đã biên tập.
Chạy tại bất kì thư mục nào qua trình khởi chạy Python của repository.
Cần Python, beautifulsoup4; cần pandoc nếu xuất Markdown.
"""
from pathlib import Path
from bs4 import BeautifulSoup
import base64,subprocess,copy,json
from bang_bien_thien import render_table
R=Path(__file__).resolve().parent.parent
def write_text_lf(path,text):
 with path.open('w',encoding='utf-8',newline='\n') as stream:stream.write(text)
s=BeautifulSoup((R/'src/noi_dung.html').read_text(encoding='utf-8'),'html.parser')
# Rebuild registered tables from their one data source.
data={d['id']:d for d in json.loads((R/'src/bang_bien_thien.json').read_text(encoding='utf-8'))}
for table in list(s.select('table[data-bbt]')):
 d=data[table['data-bbt']]
 built=BeautifulSoup(render_table(d['rows'],d['title'],d.get('excluded_columns',[])),'html.parser').find('table')
 built['data-bbt']=d['id'];table.replace_with(built)
# Markdown contains all solutions, with local vector figures.
md=copy.deepcopy(s)
for el in md.select('.answer-link,footer'):el.decompose()
for d in md.find_all('details'):
 d.summary.name='h2';d.unwrap()
for div in list(md.find_all('div')):div.unwrap()
for fig in list(md.find_all('figure')):
 img=fig.find('img');caption=fig.find('figcaption')
 image_p=md.new_tag('p');image_p.append(img.extract());fig.insert_before(image_p)
 if caption:
  caption.name='p';fig.insert_before(caption.extract())
 fig.decompose()
for img in md.find_all('img'):img.attrs={k:v for k,v in img.attrs.items() if k in ['src','alt']}
result=subprocess.run(['pandoc','-f','html','-t','markdown+pipe_tables-simple_tables-multiline_tables-grid_tables','--wrap=none'],input=str(md),text=True,capture_output=True,check=True)
import re
text=result.stdout
text=re.sub(r"^:::.*\n|^:::\s*$", "", text, flags=re.M)
text=text.replace(r"\prime}",r"\prime}")
text=text.replace(r"^{\prime}",r"^\prime")
# Keep mathematical table cells in math delimiters in the editable text.
lines=[]
for line in text.splitlines():
 if line.startswith('|'):
  cells=line.split('|')
  for i,c in enumerate(cells):
   value=c.strip()
   if '$' not in value and (any(ch in value for ch in '∞↗↘′∥−') or value in ['+','\\+','x'] or re.fullmatch(r'[A-Za-z]\(x\)',value)):
    value=value.replace('\\+','+').replace('∥',r'\Vert').replace('−','-').replace('∞',r'\infty').replace('↗',r'\nearrow ').replace('↘',r'\searrow ').replace('′',r'^\prime ')
    cells[i]=' $'+value.strip()+'$ '
  line='|'.join(cells)
 lines.append(line)
write_text_lf(R/'R1-G01_NOI_DUNG_v1.1.md','\n'.join(line.rstrip() for line in lines).strip()+'\n')
# Embed the exact font and vector files; no CDN or network is needed to read HTML.
fonts=''
for name,file in [('ZO Text','STIXTwoText.ttf'),('ZO Math','STIXTwoMath.ttf')]:
 fonts+="@font-face{font-family:'"+name+"';src:url(data:font/ttf;base64,"+base64.b64encode((R/'src/fonts'/file).read_bytes()).decode()+") format('truetype');font-weight:100 900;font-display:swap;}\n"
for img in s.find_all('img'):
 img['src']='data:image/svg+xml;base64,'+base64.b64encode((R/img['src']).read_bytes()).decode()
nav='<nav aria-label="Các phần của học liệu">'+''.join(f'<a href="#{id}">{label}</a>' for id,label in [('bat-dau','Bắt đầu'),('bai-hoc','Học'),('phieu-luyen','Luyện tập'),('tu-kiem-tra','Kiểm tra'),('sua-loi','Sửa lỗi'),('on-lai','Ôn lại'),('loi-giai','Lời giải')])+'</nav>'
controls='<div class="tools"><button type="button" onclick="printEdition(false)">In toàn bộ</button><button type="button" onclick="printEdition(true)">In phần học và bài tập</button></div>'
s.main.h1.insert_after(BeautifulSoup(controls,'html.parser'))
js='''
let savedOpen=[];
function expandForPrint(){savedOpen=[...document.querySelectorAll('details')].map(d=>[d,d.open]);savedOpen.forEach(([d])=>d.open=true);}
function restoreAfterPrint(){savedOpen.forEach(([d,o])=>d.open=o);document.body.classList.remove('print-student');}
function printEdition(student){document.body.classList.toggle('print-student',student);window.print();}
window.addEventListener('beforeprint',expandForPrint);
window.addEventListener('afterprint',restoreAfterPrint);
function revealHash(){let target;try{target=document.getElementById(decodeURIComponent(location.hash.slice(1)));}catch(e){return;}if(!target)return;let el=target;while(el){if(el.tagName==='DETAILS')el.open=true;el=el.parentElement;}target.scrollIntoView({block:'start'});}
window.addEventListener('hashchange',revealHash);window.addEventListener('load',revealHash);
document.addEventListener('click',e=>{const a=e.target.closest('a[href^="#"]');if(!a)return;let target=document.getElementById(decodeURIComponent(a.hash.slice(1)));if(!target)return;let el=target;while(el){if(el.tagName==='DETAILS')el.open=true;el=el.parentElement;}if(location.hash===a.hash)target.scrollIntoView({block:'start'});});
'''
html='<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="Kết nối hàm số, bảng biến thiên và đồ thị. Dấu đạo hàm, tính đơn điệu và cực trị. ZO Math R1-G01 v1.1."><title>R1-G01 · Kết nối hàm số, bảng biến thiên và đồ thị · v1.1</title><style>'+fonts+(R/'src/style.css').read_text(encoding='utf-8')+'</style></head><body>'+nav+str(s.main)+'<script>'+js+'</script></body></html>'
write_text_lf(R/'R1-G01_HOC_LIEU_v1.1.html',html)
print('HTML và Markdown đã được tạo.')
