"""Project the current shared HTML support component into print roles.

No account/copy registry lives in the PDF template. HTML markup remains owner.
"""
from pathlib import Path
import hashlib
import re
from string import Template
from bs4 import BeautifulSoup

ROOT=Path(__file__).resolve().parents[1]
KIT=ROOT/'_design/web_2027_mau_dung_chung'
SUPPORT=KIT/'templates/support.html.tpl'
CSS=KIT/'web-shell.css'
DESIGN=ROOT/'_design/ngon_ngu_thiet_ke_zo_math_0_4/07_mau_thi_giac'

def tex(value):
    mapping={'\\':r'\textbackslash{}','{':r'\{','}':r'\}','%':r'\%',
             '&':r'\&','#':r'\#','_':r'\_','$':r'\$','^':r'\textasciicircum{}','~':r'\textasciitilde{}'}
    return ''.join(mapping.get(c,c) for c in value)

def support_model():
    html=Template(SUPPORT.read_text(encoding='utf-8')).substitute(
        support_href='https://zomath.vn/content/support/donate.html',prototype_note='')
    soup=BeautifulSoup(html,'html.parser'); content=soup.select_one('.support-content')
    if content is None: raise ValueError('HTML support content role missing')
    fields=[]
    for n in content.select('.r1-support-details dl>div'):
        if n.dt is None or n.dd is None: raise ValueError('HTML support label/value missing')
        fields.append({'label':n.dt.get_text(' ',strip=True),'value':n.dd.get_text(' ',strip=True)})
    assert len(fields)==4 and len({x['label'] for x in fields})==4, 'HTML support field contract changed'
    title=content.h3.get_text(' ',strip=True)
    assert title and content.select_one('.r1-support-link a'), 'HTML support roles missing'
    # These asset bindings are the same as PreviewBuilder.common_assets, not audit outputs.
    qr=ROOT/'assets/images'/Path(content.select_one('.r1-support-qr')['src']).name
    logo=DESIGN/'logos'/Path(soup.select_one('.support-brand img')['src']).name
    assert qr.is_file() and logo.is_file(), 'Current HTML support assets missing'
    png=logo.with_suffix('.png'); assert png.is_file(), 'Design support logo PNG missing'
    css=CSS.read_text(encoding='utf-8')
    heading=re.search(r'\.support-content\s+h3\{[^}]*color:([^;}]+)',css)
    assert heading, 'HTML support heading token missing'
    return {'title':title,'copy':content.select_one(':scope>p').get_text(' ',strip=True),
            'fields':fields,'cta':content.select_one('.r1-support-link a').get_text(' ',strip=True),
            'url':content.select_one('.r1-support-link a')['href'],'heading_color':heading.group(1),
            'qr_path':qr,'logo_path':png,'html':html,
            'input_hashes':{p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
                            for p in [SUPPORT,CSS,qr,logo,png]}}

def support_tex(model):
    details='\n'.join(r'{\scriptsize\color{zoMuted}'+tex(f['label'])+r'}\par\nopagebreak{\bfseries '+tex(f['value'])+r'}\par\vspace{2mm}'
                      for f in model['fields'])
    values={'zoSupportTitle':model['title'],'zoSupportCopy':model['copy'],'zoSupportCTA':model['cta'],
            'zoSupportURL':model['url']}
    return '\n'.join('\\newcommand{\\'+k+'}{'+tex(v)+'}' for k,v in values.items())+'\n'+r'\newcommand{\zoSupportDetails}{'+details+'}\n'
