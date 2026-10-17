
"""Source and fresh HTML checks for G04; no publication or acceptance."""
from pathlib import Path
import argparse,json,re,os,hashlib
from urllib.parse import urlsplit,unquote,urlunsplit
from bs4 import BeautifulSoup
from zo_web_2027_g04 import PACKAGE,ROLES
from zo_web_2027_preview import REPO,sha
from zo_course_labels import expand,source_checks,html_checks
from zo_math_notation import math_errors
from zo_course_math_assets import strip_variation_math,source_checks as asset_source_checks,html_checks as asset_html_checks
from zo_web_2027_g03_check import formulas

def checks(page,out):
    p=REPO/PACKAGE;s=(p/'index.qmd').read_text(encoding='utf-8');draft=(p/'_quy_trinh/ban_thao/noi_dung.md').read_text(encoding='utf-8')
    doc=BeautifulSoup(page.read_text(encoding='utf-8'),'html.parser');root=doc.select_one('.reader-content');b=json.loads((p/'giao_dien/he_nhan.json').read_text(encoding='utf-8'))
    ids=[n['id'] for n in doc.select('[id]')]
    values={'shell':doc.body.get('data-zo-web-production')=='R1-G04','approved mathematics unchanged':formulas(re.sub(r'::: \{#g04-table-on-lai[^\n]*\n.*?\n:::', '', s.split('---',2)[2], count=1, flags=re.S))==formulas(strip_variation_math(draft)),'fresh HTML math sequence':formulas(expand(p/'index.qmd').split('---',2)[2])==[''.join(n.get_text().split()) for n in root.select('annotation') if not n.find_parent('table',class_='zo-variation-native')],'math notation':not math_errors(s),'unique IDs':len(ids)==len(set(ids)),'draft anchors retained':set(re.findall(r'<a id="([^"]+)"',draft))<=set(ids),'ten functional root areas':all(root.find('section',id=i,recursive=False) for i in ROLES),'headings in papers':all(n.find_parent(class_='reading-region') for n in root.select('h2,h3,h4,h5,h6')),'no nested papers':not root.select('.reading-region .reading-region'),'all disclosures closed':not root.select('details[open]'),'tables classified':all(n.get('data-table-kind') for n in root.select('table')),'no PDF downloads':not root.select('a[download]'),'source notes retained':len(root.select('.zo-source-note'))==5,'shared journal called':'include ../_dung_chung/nhat_ki_hoc_tap.qmd' in s,'shared journal fourteen fields':len(root.select('#r1-table-t13 tbody tr'))==14,'orientation shared':len(root.select('details.r1-lesson-orientation'))==1,'foundation shared':len(root.select('details.r1-foundation-unit'))==4,'lesson count':len(root.select('#bai-hoc h3'))==int(root['data-r1-lesson-count']),'checkpoints own return labels':all(root.find(id=k).get('data-r1-return-label') for k in b['checkpoints'])}
    values['review calendar preserves scheduled intervals']=formulas(re.search(r'::: \{#g04-table-on-lai[^\n]*\n.*?\n:::',s,re.S)[0])==['2','3','7','3','4']
    for n in range(1,6):
        values[f'GM{n} local ownership']=bool(root.find(id=f'GM{n:02}').find_parent(id=f'bh-{n:02}'))
    values.update({'math-assets/source/'+k:v for k,v in asset_source_checks(p/'index.qmd').items()})
    values.update({'math-assets/html/'+k:v for k,v in asset_html_checks(doc,'r1_g04').items()})
    from zo_web_2027_shell import require as require_shell
    values.update({'shell/'+k:v for k,v in require_shell(doc,page).items()})
    values.update({'labels/source/'+k:v for k,v in source_checks(p/'index.qmd').items()})
    values.update({'labels/html/'+k:v for k,v in html_checks(doc,b).items()})
    for u in b['units']:
        if not u.get('answer'):continue
        q=root.find(id=u['question']);a=root.find(id=u['answer'])
        fwd=root.select('#CPK a[href="#lg-kiem-tra"]') if u['function']=='function.test' else q.select('a[href="#'+u['answer']+'"]')
        values['pair/'+u['id']]=bool(fwd and a.select('a[href="#'+u['question']+'"]'))
    broken=[]
    for node in doc.select('a[href],img[src],script[src],link[href]'):
        url=urlsplit(node.get('src',node.get('href')))
        if url.scheme or url.netloc:continue
        target=(page.parent/unquote(url.path)).resolve() if url.path else page
        if not target.is_file() and target.is_relative_to(out):target=REPO/'docs'/target.relative_to(out)
        if not target.is_file():broken.append(node.get('src',node.get('href')));continue
        if url.fragment and target.suffix=='.html':
            other=doc if target==page else BeautifulSoup(target.read_text(encoding='utf-8'),'html.parser')
            if not other.find(id=unquote(url.fragment)):broken.append(node.get('href'))
    values['local files and fragments resolve']=not broken
    for fig in json.loads((p/'giao_dien/hinh_manifest.json').read_text(encoding='utf-8'))['figures']:
        values['figure/'+fig['name']]=all(sha(p/fig[k])==fig[k+'_sha256'] for k in ['input','svg'])
    from zo_course_cover import check_html
    check_html(REPO,'r1_g04',page);values['approved cover']=True
    return values,{'broken_links':broken,'math_count':len(root.select('annotation')),'tables':len(root.select('table')),'reading_regions':len(root.select('.reading-region')),'source_sha256':sha(p/'index.qmd'),'html_sha256':sha(page)}

def deliver(page,out,dest):
    doc=BeautifulSoup(page.read_text(encoding='utf-8'),'html.parser')
    for n in doc.select('[src],a[href],link[href]'):
        key='src' if n.has_attr('src') else 'href';url=urlsplit(n[key])
        if url.scheme or url.netloc or not url.path:continue
        target=(page.parent/unquote(url.path)).resolve()
        if target==page:target=dest
        elif not target.is_file() and target.is_relative_to(out):
            candidate=REPO/'docs'/target.relative_to(out)
            if candidate.is_file():target=candidate
        n[key]=urlunsplit(('','',os.path.relpath(target,dest.parent).replace('\\','/'),url.query,url.fragment))
    from zo_course_html import write
    write(dest,doc)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('html',type=Path);ap.add_argument('--output-root',type=Path,required=True);ap.add_argument('--report',type=Path,required=True);ap.add_argument('--preview',type=Path);a=ap.parse_args()
    values,details=checks(a.html.resolve(),a.output_root.resolve());report={'checks':values,'details':details,'passed':sum(values.values()),'total':len(values),'failures':[k for k,v in values.items() if not v],'owner_acceptance':'pending','published':False,'lesson_pdf_built':False}
    a.report.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    if a.preview:deliver(a.html.resolve(),a.output_root.resolve(),a.preview.resolve())
    print(json.dumps({k:report[k] for k in ['passed','total','failures','details']},ensure_ascii=False))
    return int(bool(report['failures']))
if __name__=='__main__':raise SystemExit(main())
