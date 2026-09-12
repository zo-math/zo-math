from pathlib import Path
import subprocess,shutil,concurrent.futures
root=Path(__file__).resolve().parents[1]
build=root.parents[1]/'tmp/pdf_build';build.mkdir(parents=True,exist_ok=True)
names=['hoc_sinh','loi_giai','huong_dan_phan_tich','thu_lai']
def render(name):
 stem=f'2027_D0_{name}_v1.0'; work=build/stem;work.mkdir(exist_ok=True)
 tex=work/(stem+'.tex')
 subprocess.run(['pandoc',str(root/(stem+'.md')),'-s','--from=markdown+tex_math_dollars','--pdf-engine=xelatex','-H',str(root/'src/style.tex'),'-V','mainfont=DejaVu Serif','-V','sansfont=DejaVu Sans','-V','monofont=DejaVu Sans Mono','-V','mathfont=Latin Modern Math','-V','fontsize=11pt','-V','geometry=a4paper,margin=18mm,top=21mm,bottom=20mm','-V','linestretch=1.10','-V','colorlinks=true','-V','urlcolor=zored','-o',str(tex)]+(['--lua-filter',str(root/'src/bang_huong_dan.lua')] if name=='huong_dan_phan_tich' else []),check=True,cwd=root)
 for _ in range(2):
  p=subprocess.run(['xelatex','-interaction=nonstopmode','-halt-on-error','-output-directory',str(work),str(tex)],cwd=root,capture_output=True,text=True)
  (work/'compile_output.txt').write_text(p.stdout+p.stderr)
  if p.returncode:raise RuntimeError(p.stdout[-5000:])
 shutil.copy2(work/(stem+'.pdf'),root/(stem+'.pdf'))
 return stem
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
 for result in ex.map(render,names):print(result)
