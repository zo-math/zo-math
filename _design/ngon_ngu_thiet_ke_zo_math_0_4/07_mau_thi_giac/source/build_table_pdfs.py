from pathlib import Path
import json,subprocess,fitz,html as H,re,sys
sys.path.insert(0,str(Path(__file__).parent))
from table_engine import TABLES,samples
R=Path(__file__).resolve().parents[1];samples();P=R/'pdf'
# Produce editable native LaTeX examples for the seven non-variation table families.
def esc(s):
 if s.startswith('$'):return '$'+s[1:]+'$'
 return re.sub(r'([%&_#])',r'\\\1',s)
def preamble():return r'''\documentclass[11pt,a4paper]{article}
\usepackage{fontspec,unicode-math,graphicx,xcolor,colortbl,array,tabularx,longtable,geometry,fancyhdr,enumitem,hyperref}
\geometry{left=20mm,right=20mm,top=19mm,bottom=20mm}
\setmainfont{BeVietnamPro_Regular.ttf}[Path=../assets/,BoldFont=BeVietnamPro_SemiBold.ttf]
\setmathfont{STIXTwoMath.ttf}[Path=../assets/]
\definecolor{ink}{HTML}{3E3A35}\definecolor{muted}{HTML}{766F66}\definecolor{grid}{HTML}{DFD7CA}\definecolor{paper}{HTML}{FBFAF8}\definecolor{head}{HTML}{F8F5F0}\definecolor{red}{HTML}{BF4240}\definecolor{brandred}{HTML}{EF5350}\definecolor{yellow}{HTML}{FFCA28}\definecolor{focus}{HTML}{FFF9E9}
\pagecolor{paper}\color{ink}\arrayrulecolor{grid}\setlength\arrayrulewidth{.4pt}\setlength\tabcolsep{7pt}\renewcommand\arraystretch{1.5}\setlength\parindent{0pt}\setlength\parskip{8pt}\linespread{1.12}
\pagestyle{fancy}\fancyhf{}\fancyhead[L]{\scriptsize\color{muted}ZO MATH / HỆ THIẾT KẾ 0.4}\fancyhead[R]{\scriptsize\color{muted}06.10.2026}\fancyfoot[L]{\scriptsize\color{muted}Nhận ra ZO. Tập trung vào Toán.}\fancyfoot[R]{\scriptsize\thepage}\renewcommand{\headrulewidth}{.3pt}\renewcommand{\footrulewidth}{0pt}
\hypersetup{colorlinks=true,urlcolor=red,linkcolor=red}\setlist{nosep,leftmargin=1.5em}
\newcommand{\tagline}[1]{{\small\color{muted}\MakeUppercase{#1}}\par}
\newcommand{\titlepagehead}[2]{\tagline{#1}{\fontsize{27}{32}\selectfont\bfseries #2}\par\vspace{6mm}}
\newcommand{\why}[1]{\par{\small\color{muted}\textbf{Vì sao.} #1}\par}
\newcommand{\pic}[2]{\begin{center}\includegraphics[width=#2\linewidth]{#1}\end{center}}
\begin{document}
'''
def table(t):
 n=len(t['heads']);align=r'>{\raggedright\arraybackslash}X';center=r'>{\centering\arraybackslash}X';right=r'>{\raggedleft\arraybackslash}X';spec=[align]*n
 if t['id'] in ['table_values','table_sign']:spec=[r'>{\raggedright\arraybackslash}p{.28\linewidth}']+[center]*(n-1)
 if t['id']=='table_matrix':spec=[center]*n
 if t['id']=='table_frequency':spec=[align,right,right]
 if t['id']=='table_process':spec=[r'>{\centering\arraybackslash}p{.08\linewidth}',align,align]
 cols='|'+'|'.join(spec)+'|';s=r'\begin{tabularx}{\linewidth}{'+cols+'}\\hline\n\\rowcolor{head}'+' & '.join(esc(x) for x in t['heads'])+r'\\\hline'+'\n'
 for i,row in enumerate(t['rows']):
  highlight=(t['id']=='table_values' and i==1) or (t['id']=='table_sign' and i==2)
  s+=(r'\rowcolor{focus}' if highlight else '')+' & '.join(esc(x) for x in row)+r'\\\hline'+'\n'
 if t['foot']:s+=r'\rowcolor{head}'+' & '.join(esc(x) for x in t['foot'])+r'\\\hline'
 return s+r'\end{tabularx}'
for t in TABLES:
 code=preamble()+r'\tagline{Bảng mẫu / 0.4}\section*{'+t['title']+'}\n'+table(t)+r'\why{'+t['why']+'}'+r'\end{document}'
 (P/(t['id']+'.tex')).write_text(code)

for t in TABLES:
 p=subprocess.run(['xelatex','-interaction=nonstopmode','-halt-on-error',t['id']+'.tex'],cwd=P,capture_output=True)
 if p.returncode:raise RuntimeError(p.stdout.decode()[-1500:])
 print(t['id'],flush=True)
