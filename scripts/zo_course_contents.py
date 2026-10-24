"""Opt-in course contents projection and bounded HTML refresh from canonical sources."""
from pathlib import Path
import argparse, hashlib, html, json, re, subprocess, sys
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]
KIT=ROOT/'_design/web_2027_mau_dung_chung'

def apply_contents(root, settings):
    if not settings.get('contents'): return
    def resolve(node):
        target=root.find(id=node['target'])
        if target is None: raise ValueError('Missing contents target: '+node['target'])
        heading=target.find(re.compile('^h[2-6]$'))
        label=node.get('label') or (heading.get_text(' ',strip=True) if heading else '')
        if not label: raise ValueError('Missing contents title: '+node['target'])
        result={'target':node['target'],'label':label}
        if node.get('children'):result['children']=[resolve(n) for n in node['children']]
        return result
    tree=[{'view':g['view'],'items':[resolve(n) for n in g['items']]} for g in settings['contents']]
    root['data-zo-contents']=json.dumps(tree,ensure_ascii=False,separators=(',',':'))

def refresh(page, report):
    source=ROOT/page.relative_to(ROOT/'docs').with_suffix('.qmd')
    settings=json.loads((source.parent/'giao_dien/html.json').read_text('utf-8'))
    before=page.read_text('utf-8');doc=BeautifulSoup(before,'html.parser');root=doc.select_one('.reader-content')
    old_tag=str(root).split('>',1)[0]+'>'
    apply_contents(root,settings)
    root['data-r1-review-rounds']=json.dumps(settings['review_rounds'],ensure_ascii=False)
    new_tag=str(root).split('>',1)[0]+'>'
    assert before.count(old_tag)==1
    after=before.replace(old_tag,new_tag,1)
    # Only the practice map changed in learner prose. Render it from QMD.
    text=source.read_text('utf-8')
    fragment=re.search(r'(?ms)^::: \{#r2g01-table-12[^\n]*\}\n(.*?)^:::',text).group(1)
    cmd=[sys.executable,'-B','scripts/zo_python.py','-B','scripts/zo_quarto.py','pandoc','--from=markdown','--to=html5','--wrap=none']
    result=subprocess.run(cmd,input=fragment,text=True,encoding='utf-8',cwd=ROOT,capture_output=True,check=True)
    rendered=BeautifulSoup(result.stdout,'html.parser').find('tbody')
    table=doc.find(id='r2g01-table-12');old_body=str(table.find('tbody'))
    # Preserve table accessibility/role attributes supplied by the normal adapter.
    body=table.find('tbody')
    for oldrow,newrow in zip(body.find_all('tr'),rendered.find_all('tr'),strict=True):
        oldrow.find('td').clear()
        for child in list(newrow.find('td').contents):oldrow.find('td').append(child.extract())
    from zo_course_table_roles import apply_function, contract
    apply_function(table.find('table'),contract()['function_profiles']['practice'],'practice',doc)
    new_body=str(body);assert after.count(old_body)==1
    after=after.replace(old_body,new_body,1)
    # Byte-for-byte outside the generated root attributes and three source cells.
    assert before.replace(old_tag,'ROOT',1).replace(old_body,'TABLE',1)==after.replace(new_tag,'ROOT',1).replace(new_body,'TABLE',1)
    page.write_text(after,encoding='utf-8',newline='\n')
    runtime=ROOT/'docs/assets/zo_web_2027'/settings['runtime']
    assets=['r1-controller.js','site-ui.js','web-shell.css']
    for name in assets:(runtime/name).write_bytes((KIT/name).read_bytes())
    result={'outside_fragments_unchanged':True,'rendered_from':str(source.relative_to(ROOT)), 'assets':assets,'html_sha256':hashlib.sha256(page.read_bytes()).hexdigest(),'PDF_built':False}
    report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False))

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--html',type=Path,required=True);ap.add_argument('--report',type=Path,required=True);args=ap.parse_args();refresh(args.html.resolve(),args.report.resolve())
