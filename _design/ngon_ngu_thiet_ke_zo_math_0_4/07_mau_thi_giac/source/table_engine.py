from pathlib import Path
import json,subprocess,html,re
R=Path(__file__).resolve().parents[1];FORMULAS=set();CACHE={}
def texify(s):
 if not s:return ''
 return s.replace('−','-').replace('∞',r'\infty').replace('′',r'^{\prime}').replace('∥',r'\Vert').replace('↗',r'\nearrow').replace('↘',r'\searrow').replace('→',r'\rightarrow')
def M(tex):
 FORMULAS.add(tex);return '<span class="math-source" data-tex="'+html.escape(tex,quote=True)+'"></span>'
def T(s):return html.escape(s)
def cell(s):
 if s.startswith('$'):return M(s[1:])
 return re.sub(r'\$([^$]+)\$',lambda m:M(m.group(1)),T(s))
def variation(rec,idprefix=''):
 rows=rec['rows'];id=idprefix+rec['id'];width=len(rows[0]);s=f'<div class="table-scroll variation-scroll" tabindex="0" role="region" aria-label="{id} — bảng có thể cuộn ngang"><table class="zo-table variation" data-bbt="{rec["id"]}"><caption>{T(rec["title"])} <span class="role-tag inline-tag">{rec["id"]}</span></caption><thead>'
 for ri,row in enumerate(rows):
  if ri==1:s+='</thead><tbody>'
  s+='<tr>'
  for ci,value in enumerate(row):
   tag='th' if ri==0 or ci==0 else 'td';scope=(' scope="col"' if ri==0 and ci>0 else ' scope="row"') if tag=='th' else ''
   cls=[];aria='';val=value
   if not value:
    aria=' aria-label="'+('Khoảng giữa '+row[ci-1]+' và '+row[ci+1] if ri==0 and ci>0 and ci+1<width else 'Không ghi dữ kiện tại ô này')+'"'
   if ci==0:cls.append('row-role')
   if ri>0 and ci>0 and ci%2==0:cls.append('interval-cell')
   if '∥' in value:cls.append('excluded-cell')
   if ri==len(rows)-1 and ('↗' in value or '↘' in value):cls.append('trend-cell')
   body=(T(value) if value=='Không tồn tại' else M(texify(value))) if value else '<span aria-hidden="true">&nbsp;</span>'
   if value=='Không tồn tại':body='<span class="cell-note">Không tồn tại</span>'
   s+=f'<{tag}{scope}{aria} class="{" ".join(cls)}">{body}</{tag}>'
  s+='</tr>'
 s+='</tbody></table></div>';return s
TABLES=[]
def add(id,title,heads,rows,why,kind='text',foot=None,focus=None):
 s=f'<div class="table-scroll" tabindex="0" role="region" aria-label="{title}"><table class="zo-table {kind}" id="{id}"><caption>{title}</caption><thead><tr>'+''.join(f'<th scope="col">{cell(h)}</th>' for h in heads)+'</tr></thead><tbody>'
 for i,row in enumerate(rows):
  s+=f'<tr'+(' class="row-highlight"' if focus==i else '')+'>'
  for j,v in enumerate(row):s+=f'<{"th scope=\"row\"" if j==0 else "td"}>'+cell(v)+f'</{"th" if j==0 else "td"}>'
  s+='</tr>'
 s+='</tbody>'
 if foot:s+='<tfoot><tr>'+''.join(f'<{"th scope=\"row\"" if j==0 else "td"}>'+cell(v)+f'</{"th" if j==0 else "td"}>' for j,v in enumerate(foot))+'</tr></tfoot>'
 s+='</table></div>';TABLES.append({'id':id,'title':title,'html':s,'why':why,'heads':heads,'rows':rows,'foot':foot});return s

def samples():
 add('table_values','01 · Bảng giá trị',['$x','$-2','$-1','$0','$1','$2'],[['$f(x)=x^3','$-8','$-1','$0','$1','$8'],["$f^{\\prime}(x)=3x^2",'$12','$3','$0','$3','$12']],'Bố cục ngang ngắn: một cột giữ một đầu vào. Hàng đạo hàm được nhấn yellow-1 để đọc cùng hàng giá trị, không tô màu theo dấu.','matrix',focus=1)
 add('table_frequency','02 · Bảng dữ liệu và tần số',['Số câu đúng / 10','$n_i','Tần suất'],[['0–2','$12','$24\\%'],['3–5','$18','$36\\%'],['6–8','$14','$28\\%'],['9–10','$6','$12\\%']],'Các số căn phải, đơn vị ở đầu cột, tổng tách bằng nền gray-2. Đường kẻ vẫn cùng độ mảnh; dữ liệu giả lập 50 bài.','numeric',foot=['Tổng','$50','$100\\%'])
 add('table_compare','03 · Bảng đối chiếu khái niệm',['Tại $x=0$','Giá trị hàm','Đạo hàm','Cực trị'],[['$x^3','Có','Bằng 0','Không'],['$|x|','Có','Không tồn tại','Cực tiểu'],['$1/x','Không','Ngoài tập xác định','Không xét']],'Câu chữ căn trái, tiêu chí ổn định theo cột. Hàng đang đọc dùng yellow-1; từ “không” không tự mang nghĩa lỗi.','comparison')
 add('table_matrix','04 · Bảng hai chiều',['Nhóm','$B',r'$\overline B','Tổng'],[['$A','$12','$8','$20'],[r'$\overline A','$6','$14','$20']],'Hai đầu hàng–cột định vị ô; tổng là kiểm toán dữ liệu. yellow-2 chỉ giao điểm đang đối chiếu; nhãn hàng/cột vẫn đủ khi xem sắc xám. Dữ liệu giả lập 40 trường hợp.','matrix contingency',foot=['Tổng','$18','$22','$40'])
 add('table_sign','05 · Bảng dấu',['$x',r'$(-\infty;-1)','$-1','$(-1;1)','$1',r'$(1;+\infty)'],[['$x+1','$-','$0','$+','$+','$+'],['$x-1','$-','$-','$-','$0','$+'],[r'$p^{\prime}(x)=3(x+1)(x-1)','$+','$0','$-','$0','$+']],'Giữ ô riêng cho khoảng và mốc. Hàng kết quả dùng yellow-1; dấu cộng/trừ vẫn viết bằng LaTeX và cùng màu chữ, không suy nghĩa từ màu.','matrix sign',focus=2)
 add('table_rubric','07 · Bảng tiêu chí đánh giá',['Tiêu chí','Cần bổ sung','Đạt yêu cầu','Có chiều sâu'],[['Điều kiện','Chưa nêu khoảng xét','Nêu đủ khoảng và giả thiết','Giải thích vai trò giả thiết'],['Lập luận','Chỉ mô tả hình','Có lập luận hợp lệ','Đối chiếu phản ví dụ'],['Kết luận','Nhầm đối tượng','Gọi đúng đối tượng','Nêu giới hạn của dữ kiện']],'Hàng là tiêu chí, cột là mức mô tả. Cột đang đối chiếu có nền yellow-1 và tên rõ; không biến màu thương hiệu thành thang điểm.','rubric')
 add('table_process','08 · Bảng quy trình và thuật ngữ',['Bước','Việc cần làm','Đầu ra cần giữ'],[['01','Xác định đối tượng và tập xác định',r'$D=\mathbb R\setminus\{0\}'],['02','Xét từng khoảng hợp lệ','Dấu và điều kiện trên mỗi khoảng'],['03','Kết luận đúng dữ kiện','Câu kết luận có điều kiện']],'Số bước hẹp và mờ, mô tả rộng, đầu ra có cột riêng. Biến thể thuật ngữ giữ cột tên ổn định và cột diễn giải rộng; không thêm một kiểu đường kẻ khác.','process')
 return TABLES

def render_sources(texts):
 (R/'design/formula_sources.json').write_text(json.dumps(sorted(FORMULAS),ensure_ascii=False));subprocess.run(['node',str(R/'source/math_render.cjs'),str(R/'design/formula_sources.json'),str(R/'design/mathml_cache.json')],check=True)
 global CACHE;CACHE=json.loads((R/'design/mathml_cache.json').read_text())
 def replace(match):
  t=html.unescape(match.group(1));return '<span class="math-inline" data-latex="'+html.escape(t,quote=True)+'">'+CACHE[t]+'</span>'
 return [re.sub(r'<span class="math-source" data-tex="([^"]*)"></span>',replace,s) for s in texts]
