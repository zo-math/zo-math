"""Tạo PDF đủ lời giải từ cùng nguồn Markdown. Cần pandoc và XeLaTeX."""
from pathlib import Path
import subprocess,json,tempfile
R=Path(__file__).resolve().parent.parent
text=(R/'R1-G01_NOI_DUNG_v1.1.md').read_text().replace('.svg)', '.png)')
text=text.replace('Lời giải nằm ở cuối tài liệu, trong các mục có thể mở khi cần. Nút **In toàn bộ** in cả lời giải; nút **In phần học và bài tập** ẩn lời giải. Khi học trên màn hình, nhấn vào tên câu hoặc bài để đi đến lời giải tương ứng.', 'Bản PDF này chứa đầy đủ bài học, bài tập, lời giải và hướng dẫn chấm. Khi tự làm bài, hãy dừng trước phần Lời giải. Các nút mở lời giải và lựa chọn bản in có trong tệp HTML đi kèm.')
# Let tables break by row while reducing dense overview tables slightly.
ast=json.loads(subprocess.run(['pandoc','-f','markdown-implicit_figures','-t','json'],input=text,text=True,capture_output=True,check=True).stdout)
for b in ast['blocks']:
 if b['t']=='Table' and b['c'][1][1]:
  cols=b['c'][2];n=len(cols)
  b['c'][2]=[[{'t':'AlignCenter'},{'t':'ColWidth','c':1/n}] for _ in cols]
cmd=['pandoc','-f','json','-t','latex','-s','--wrap=none','--top-level-division=section','-V','documentclass=article','-V','fontsize=11pt','-V','geometry=a4paper,margin=20mm','-V','linestretch=1.12','-H','src/pdf_header.tex']
r=subprocess.run(cmd,input=json.dumps(ast),text=True,capture_output=True,cwd=R,check=True)
tex=r.stdout.replace('\\begin{longtable}', '\\small\n\\begin{longtable}').replace('\\end{longtable}', '\\end{longtable}\n\\normalsize')
with tempfile.TemporaryDirectory(prefix='r1-g01-pdf-') as temp_name:
 temp=Path(temp_name)
 tex_path=temp/'ban_in.tex'
 tex_path.write_text(tex,encoding='utf-8')
 for _ in range(2):
  proc=subprocess.run(['xelatex','-interaction=nonstopmode','-halt-on-error',f'-output-directory={temp}',str(tex_path)],cwd=R,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
  (R/'kiem_chung/pdf_build.log').write_text(proc.stdout,encoding='utf-8')
  if proc.returncode:raise RuntimeError(proc.stdout[-4000:])
 (R/'R1-G01_HOC_LIEU_v1.1.pdf').write_bytes((temp/'ban_in.pdf').read_bytes())
print('PDF đã được tạo.')
