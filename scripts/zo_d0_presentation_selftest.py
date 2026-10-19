"""D0 regression: source and HTML presentation, with immutable learner approval."""
import argparse,copy,json,re
from pathlib import Path
from bs4 import BeautifulSoup
from zo_d0_presentation import ROOT,PACKAGE,source_checks,html_checks,asset_version_checks,restore_editorial_source,restore_numbering_source,restore_presentation_source


def run(page=None):
    source=ROOT/PACKAGE/'index.qmd';text=source.read_text(encoding='utf-8');checks={}
    checks['current source passes']=all(source_checks(source).values())
    import hashlib
    delta=json.loads((ROOT/PACKAGE/'_quy_trinh/d0_numbering_delta.json').read_text(encoding='utf-8'))
    checks['only authorized source delta']=hashlib.sha256(restore_numbering_source(text).encode()).hexdigest()==delta['source_before_sha256']
    for name,bad in {
        'old forward':text.replace('[Xem lời giải]','[Đối chiếu bài này sau khi tự làm]',1),
        'old return':text.replace('[Xem đề bài]','[Quay lại đề bài]',1),
        'missing target':text.replace('](#doi-chieu-r1-01)','](#missing-answer)',1),
        'bare numeric cell':re.sub(r'(\|\s*)\$(\d+)\$(\s*\|)',r'\1\2\3',text,count=1),
        'number reset':text.replace('#### Bài 04 —','#### Bài 01 —',1),
        'example counted as task':text.replace('#### Bài 00 —','#### Bài 01 —',1),
        'old badge':text.replace('#### Bài 01 —','[Bài 01]{.d0-task-number}\n\n#### Bài 01 —',1),
        'wrong answer number':text.replace('::: zo-learning-summary\nBài 04 —','::: zo-learning-summary\nBài 01 —',1),
    }.items():
        checks['source rejects '+name]=bad!=text and not all(source_checks(source,text=bad).values())
    if page:
        from zo_web_2027_d0_check import verify_approved_content
        from zo_web_2027_d0 import strip_papers
        doc=BeautifulSoup(Path(page).read_text(encoding='utf-8'),'html.parser')
        checks['current HTML passes']=all(html_checks(doc).values())
        bad=copy.deepcopy(doc)
        for node in bad.select('link[rel=stylesheet][href]'):node['href']=node['href'].split('?')[0]
        checks['HTML rejects unversioned changed CSS']=not all(asset_version_checks(bad).values())
        bad=copy.deepcopy(doc);bad.select_one('.hero-art').decompose()
        checks['HTML rejects missing D0 cover']=not all(html_checks(bad).values())
        try:verify_approved_content(strip_papers(doc.select_one('.d0-package')));checks['immutable approval matches after display delta']=True
        except AssertionError:checks['immutable approval matches after display delta']=False
        for name in ['old forward','old return','bare number','misaligned columns','missing table','caption above','number reset','wrong answer title','context label','matrix header left','numeric header left','first numeric header left']:
            bad=copy.deepcopy(doc)
            if name=='old forward':bad.select_one('a[href="#doi-chieu-r1-01"]').string='Đối chiếu bài này sau khi tự làm'
            elif name=='old return':bad.select_one('#doi-chieu-r1-01 a[href="#d0-r1-01"]').string='Quay lại đề bài'
            elif name=='bare number':bad.select_one('#d0-r2-02 tbody td').clear();bad.select_one('#d0-r2-02 tbody td').string='2'
            elif name=='misaligned columns':bad.select_one('#d0-r2-02 tbody td').attrs.pop('class',None)
            elif name=='missing table':bad.select_one('#d0-r8-03 table').decompose()
            elif name=='number reset':bad.select_one('#d0-r2-01 h4').string='Bài 01 — Thước đo phù hợp'
            elif name=='wrong answer title':bad.select_one('#doi-chieu-r2-01 summary').string='Bài 04 — Tên khác'
            elif name=='context label':
                label=bad.new_tag('p',attrs={'class':'role'});label.string='MẠCH HỌC';bad.select_one('#khao-sat').insert(0,label)
            elif name=='matrix header left':bad.select_one('#d0-r4-03 thead th:nth-child(2)').attrs.pop('class',None)
            elif name=='numeric header left':bad.select_one('#d0-r8-03 thead th:nth-child(2)').attrs.pop('class',None)
            elif name=='first numeric header left':bad.select_one('#doi-chieu-r8-03 thead th:first-child').attrs.pop('class',None)
            else:
                fig=bad.select_one('figure.zo-variation-asset');fig.insert(0,fig.select_one('figcaption').extract())
            checks['HTML rejects '+name]=not all(html_checks(bad).values())
        bad=copy.deepcopy(doc);cell=bad.select_one('#d0-r2-02 tbody td annotation');cell.string='999'
        try:verify_approved_content(strip_papers(bad.select_one('.d0-package')));rejected=False
        except AssertionError:rejected=True
        checks['original receipt rejects changed numeric value']=rejected
        bad=copy.deepcopy(doc);bad.select_one('#d0-r8-01 annotation').string='999'
        try:verify_approved_content(strip_papers(bad.select_one('.d0-package')));rejected=False
        except AssertionError:rejected=True
        checks['bounded editorial inverse rejects changed math']=rejected
        bad=copy.deepcopy(doc);bad.select_one('#bat-dau p').string='Nội dung khác'
        try:verify_approved_content(strip_papers(bad.select_one('.d0-package')));rejected=False
        except AssertionError:rejected=True
        checks['original receipt rejects changed learner prose']=rejected
    return checks


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--html',type=Path);parser.add_argument('--report',type=Path);args=parser.parse_args()
    checks=run(args.html);result={'passed':sum(checks.values()),'total':len(checks),'failures':[k for k,v in checks.items() if not v],'checks':checks,'rendered':False}
    if args.report:
        path=args.report.resolve()
        if not path.is_relative_to(ROOT/'_audit'):raise ValueError('Report belongs in audit')
        path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k!='checks'},ensure_ascii=False));raise SystemExit(bool(result['failures']))
