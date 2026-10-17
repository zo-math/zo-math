"""Four-package reading presentation regression gate, including rejected defects.

Run against freshly built HTML. This never grants owner acceptance or publishes.
"""
from pathlib import Path
import argparse,copy,json
from bs4 import BeautifulSoup
from zo_web_2027_consistency import presentation_checks
from zo_course_labels import binding_checks,context_html_checks,ROOT

BASE=Path('content/thpt/on_thi_toan_thpt/hoc_lieu')

def run(output):
    checks={}
    for g in range(1,5):
        key=f'r1_g0{g}'
        data=json.loads((ROOT/BASE/key/'giao_dien/he_nhan.json').read_text(encoding='utf-8'))
        doc=BeautifulSoup((output/BASE/key/'index.html').read_text(encoding='utf-8'),'html.parser')
        values=presentation_checks(doc,data)|binding_checks(data)|context_html_checks(doc,data)
        checks.update({key+'/'+k:v for k,v in values.items()})
        prompt=next(u for u in data['units'] if u['function']=='function.guided_thinking')
        bad=copy.deepcopy(data);u=next(u for u in bad['units'] if u['id']==prompt['id']);u['title']=f"Gợi mở {u['number']:02d}"
        checks[key+'/reject bare prompt title']=not all(binding_checks(bad).values())
        bad=copy.deepcopy(doc);bad.find(id=prompt['question']).select_one('.zo-task-title')['class']=[]
        checks[key+'/reject old task typography marker']=not all(presentation_checks(bad,data).values())
        bad=copy.deepcopy(doc);bad.find(id='phieu-luyen').append(bad.find(id=prompt['question']).extract())
        checks[key+'/reject prompt outside lesson']=not all(presentation_checks(bad,data).values())
        bad=copy.deepcopy(doc);note=bad.select_one('.zo-source-note')
        if note.name=='p':
            note.name='span';note.wrap(bad.new_tag('p'))
        note.parent.append(' Lời giảng chen vào chú thích.')
        checks[key+'/reject source note mixed into prose']=not all(presentation_checks(bad,data).values())
        bad=copy.deepcopy(doc);bad.find(id='on-lai').find('table').select('thead th')[-1].decompose()
        checks[key+'/reject incomplete review calendar']=not all(presentation_checks(bad,data).values())
        bad=copy.deepcopy(doc);root=bad.select_one('.reader-content');paper=bad.new_tag('div',attrs={'class':'reading-region'});h=bad.new_tag('h3');h.string='Sửa lỗi';paper.append(h);root.append(paper)
        checks[key+'/reject heading-only paper']=not all(presentation_checks(bad,data).values())
        bad=copy.deepcopy(doc);items=[n for n in bad.select('#on-nen details.r1-foundation-unit') if not n.find_parent('details')]
        items[0].find_parent(class_='reading-region').append(items[1].extract())
        checks[key+'/reject merged independent foundation papers']=not all(presentation_checks(bad,data).values())
        bad=copy.deepcopy(doc);a=bad.new_tag('a',href='https://zomath.vn/content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g01/');a.string='Đọc kiến thức';bad.select_one('.reader-content').append(a)
        checks[key+'/reject absolute cross-package link']=not all(presentation_checks(bad,data).values())
        if g==2:
            from zo_r1_g02_labels_check import predicates
            bad=copy.deepcopy(doc);q=bad.find(id=prompt['question']);q.find_all('p')[-1].extract()
            checks[key+'/reject detached prompt bridge']=not all(predicates(bad,data).values())
    return checks

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output-root',type=Path,required=True);parser.add_argument('--report',type=Path);args=parser.parse_args()
    values=run(args.output_root.resolve());result={'passed':sum(values.values()),'total':len(values),'failures':[k for k,v in values.items() if not v],'checks':values,'owner_acceptance':'pending','published':False}
    if args.report:
        path=args.report.resolve()
        if not path.is_relative_to(ROOT/'_audit'):raise ValueError('Report must stay in audit')
        path.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:result[k] for k in ['passed','total','failures']},ensure_ascii=False));raise SystemExit(int(bool(result['failures'])))
