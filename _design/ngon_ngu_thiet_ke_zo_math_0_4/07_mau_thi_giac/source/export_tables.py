from pathlib import Path
from lxml import html
import json,subprocess,concurrent.futures,fitz,re
from table_engine import variation,texify,samples,R
records=json.loads((R/'design/variation_records.json').read_text());samples()
for rec in records:
 id=rec['id'].lower();raw=variation(rec);(R/'tables'/f'{id}_template.html').write_text(raw)
 # Quarto owns TeX rendering inside native HTML cells through data-qmd.
 qmd=re.sub(r'<span class="math-source" data-tex="([^"]*)"></span>',lambda m:'<span data-qmd="'+m.group(1).replace('"','&quot;')+'"></span>',raw)
 # data-qmd values must include math delimiters.
 qmd=re.sub(r'data-qmd="([^"]*)"',lambda m:'data-qmd="$'+m.group(1)+'$"',qmd)
 (R/'tables'/f'{id}.qmd').write_text('---\ntitle: "'+rec['title']+' · '+rec['id']+'"\nformat:\n  html:\n    css: ../source/system.css\n    html-math-method: mathjax\n---\n\n```{=html}\n'+qmd+'\n```\n')
 rows=rec['rows'];w=len(rows[0]);cols='|'+('|'.join([r'>{\centering\arraybackslash}m{1.7cm}']+[r'>{\centering\arraybackslash}m{1.25cm}' for _ in range(w-1)]))+'|'
 pre=r'''\documentclass[border=.4pt]{standalone}
\usepackage{fontspec,unicode-math,array,xcolor,colortbl}
\setmainfont{STIXTwoText_Regular.ttf}[Path=../assets/]
\setmathfont{STIXTwoMath.ttf}[Path=../assets/]
\definecolor{ink}{HTML}{3E3A35}\definecolor{muted}{HTML}{766F66}\definecolor{grid}{HTML}{DFD7CA}\definecolor{head}{HTML}{F8F5F0}\definecolor{focus}{HTML}{BF4240}
\arrayrulecolor{grid}\setlength\arrayrulewidth{.4pt}\setlength\tabcolsep{6pt}\renewcommand\arraystretch{1.8}
\begin{document}\color{ink}\begin{tabular}{'''+cols+'}\hline\n'
 body=[]
 for ri,row in enumerate(rows):
  cells=[]
  for ci,s in enumerate(row):
   v=texify(s)
   if s=='Không tồn tại':v=r'\scriptsize Không tồn tại'
   elif s:v=('$'+v+'$')
   if ci==0 or ri==0:v=r'\cellcolor{head}'+v
   if '↗' in s or '↘' in s:v=r'\color{focus}\large '+v
   cells.append(v)
  body.append(' & '.join(cells)+r' \\ \hline')
 (R/'tables'/f'{id}.tex').write_text(pre+'\n'.join(body)+r'\end{tabular}\end{document}')
def build(rec):
 id=rec['id'].lower();p=subprocess.run(['xelatex','-interaction=nonstopmode','-halt-on-error',id+'.tex'],cwd=R/'tables',capture_output=True)
 if p.returncode:raise RuntimeError(id+p.stdout.decode()[-1600:])
 d=fitz.open(R/'tables'/f'{id}.pdf');d[0].get_pixmap(matrix=fitz.Matrix(3,3),alpha=True).save(R/'tables'/f'{id}.png');return id
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
 for id in ex.map(build,records):print(id,flush=True)
