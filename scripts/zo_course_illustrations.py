"""Explicit contextual illustrations; bounded projection from canonical QMD."""
from pathlib import Path
import argparse, hashlib, json, os, re
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]

def materialize(root, package, builder):
    for img in root.select('img[src]'):
        figure=img.find_parent('figure',attrs={'data-zo-role':'context-illustration'})
        if figure is None or not img.get('alt') or not img.get('width') or not img.get('height'):
            raise ValueError('Body image needs explicit contextual role, alt and dimensions')
        src=(package/img['src']).resolve()
        if not src.is_relative_to((package/'hinh').resolve()) or not src.is_file():
            raise ValueError('Illustration escapes canonical image directory')
        img['src']=builder.materialize(src,'illustrations/'+src.name)
        figure.attrs.pop('data-insert-before',None)

def refresh(page,report,selected):
    from zo_web_2027_package import Builder
    source=ROOT/page.relative_to(ROOT/'docs').with_suffix('.qmd')
    settings=json.loads((source.parent/'giao_dien/html.json').read_text('utf-8'))
    before=page.read_text('utf-8'); after=before
    figures=re.findall(r'<figure[^>]*data-zo-role="context-illustration".*?</figure>',source.read_text('utf-8'),re.S)
    if not selected or len(selected)!=len(set(selected)): raise ValueError('Provide unique approved illustration IDs')
    figures=[f for f in figures if BeautifulSoup(f,'html.parser').figure['id'] in selected]
    if len(figures)!=len(selected): raise ValueError('Approved illustration missing from source')
    builder=Builder(ROOT/'docs',settings['runtime'])
    inserts=[]
    for fragment in figures:
        parsed=BeautifulSoup(fragment,'html.parser'); figure=parsed.figure
        anchor=figure['data-insert-before']; ident=figure['id']
        doc=BeautifulSoup(after,'html.parser')
        if doc.find(id=ident): raise ValueError('Illustration already exists: '+ident)
        targets=[p for p in doc.find_all('p') if p.get_text().startswith(anchor)]
        if len(targets)!=1: raise ValueError('Ambiguous insertion anchor')
        target=str(targets[0]); assert after.count(target)==1
        materialize(parsed,source.parent,builder)
        img=figure.img
        img['src']=os.path.relpath(builder.output/img['src'],page.parent).replace('\\','/')
        addition=str(figure)+'\n'; after=after.replace(target,addition+target,1); inserts.append(addition)
    restored=after
    for addition in inserts: restored=restored.replace(addition,'',1)
    assert restored==before
    page.write_text(after,encoding='utf-8',newline='\n')
    result={'outside_insertions_unchanged':True,'figures':len(figures),'html_sha256':hashlib.sha256(page.read_bytes()).hexdigest(),'math_unchanged':True}
    report.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps(result))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--html',type=Path,required=True);p.add_argument('--report',type=Path,required=True);p.add_argument('--ids',nargs='+',required=True);a=p.parse_args();refresh(a.html.resolve(),a.report.resolve(),a.ids)
