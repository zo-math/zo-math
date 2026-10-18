"""Source and in-memory regressions; never render or write HTML/PDF."""
from pathlib import Path
import argparse,copy,json,re,tempfile
from bs4 import BeautifulSoup
from zo_course_instructions import source_checks,html_checks,restore_g01_for_comparison,RULE
from zo_web_2027_production import content_fingerprint

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'content/thpt/on_thi_toan_thpt/hoc_lieu'

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--report',type=Path);args=ap.parse_args();checks={}
    for name in ['r1_g01','r1_g02','r1_g03','r1_g04']:
        path=BASE/name/'index.qmd';s=path.read_text(encoding='utf-8');binding=json.loads((path.parent/'giao_dien/he_nhan.json').read_text(encoding='utf-8'));b=binding['instructions']
        checks.update({name+'/'+k:v for k,v in source_checks(path).items()})
        first=b['required'][0]
        marker=re.search(r'(^:{3,} \{#'+re.escape(first)+r'[^\n]+\}\n\s*)(\w)',s,re.M)
        broken=s[:marker.start(2)]+marker[2].lower()+s[marker.end(2):]
        checks[name+' reject lowercase source']=not all(source_checks(path,text=broken).values())
        broken=s+'\n<details><summary>Cách thực hiện</summary>Đọc rồi tự làm.</details>\n'
        checks[name+' reject undeclared repetitive box']=not all(source_checks(path,text=broken).values())
        parts=['<main class="reader-content">']
        parts += ['<div id="'+ident+'" data-zo-instructions="required"><p>Tự làm và giữ bài gốc.</p></div>' for ident in b['required']]
        parts += ['<span id="'+ident+'"></span>' for ident in b['retired_aliases']]
        parts += ['</main>'];doc=BeautifulSoup(''.join(parts),'html.parser')
        checks[name+' valid visible DOM']=all(html_checks(doc,binding).values())
        bad=copy.deepcopy(doc);node=bad.find(id=first);wrapper=bad.new_tag('details');node.wrap(wrapper)
        checks[name+' reject hidden mandatory instruction']=not all(html_checks(bad,binding).values())
        bad=copy.deepcopy(doc);bad.find(id=first).p.string='tự làm và giữ bài gốc.'
        checks[name+' reject lowercase DOM']=not all(html_checks(bad,binding).values())
        bad=copy.deepcopy(doc);bad.find(id=first).decompose()
        checks[name+' reject missing instruction']=not all(html_checks(bad,binding).values())
        optional=copy.deepcopy(binding);optional['instructions']['optional']=['optional-help']
        good=copy.deepcopy(doc);help=BeautifulSoup('<details id="optional-help" data-zo-instructions="optional"><summary>Cách thực hiện</summary><p>Nếu cần hỗ trợ thao tác, xem các bước.</p></details>','html.parser').details;good.main.append(help)
        checks[name+' allow justified optional closed help']=all(html_checks(good,optional).values())
        help['open']='';checks[name+' reject open optional box']=not all(html_checks(good,optional).values())
    p=BASE/'r1_g01/index.qmd';plan=json.loads((p.parent/'giao_dien/web_2027_layout.json').read_text(encoding='utf-8'));edits=plan['instructions_transition']['edits']
    before=BeautifulSoup('<div id="root"></div>','html.parser').div
    for edit in edits:
        node=BeautifulSoup('<details></details>','html.parser').details;node['id']=edit['id'];node.string=edit['before_text'];before.append(node)
    extra=BeautifulSoup('<p id="outside">Nội dung cần giữ <math><semantics><annotation encoding="application/x-tex">x</annotation></semantics></math></p>','html.parser').p;before.append(extra)
    expected=content_fingerprint(before);after=copy.deepcopy(before)
    for edit in edits:
        node=after.find(id=edit['id']);node.name='div' if edit['mode']=='visible' else 'span';node.clear()
        if edit['mode']=='visible':node['data-zo-instructions']='required';node.string=edit['after_text']
    restored=restore_g01_for_comparison(after,plan,p)
    checks['G01 complete bounded inverse']=content_fingerprint(restored)==expected
    serialized=str(after);restore_g01_for_comparison(after,plan,p)
    checks['G01 inverse never mutates output']=str(after)==serialized
    for name,modify in [
        ('outside words',lambda d:d.find(id='outside').append(' Thay đổi ngoài phạm vi.')),
        ('outside math',lambda d:setattr(d.find('annotation'),'string','y')),
        ('outside ID',lambda d:d.find(id='outside').__setitem__('id','new-outside')),
        ('outside disclosure',lambda d:d.append(BeautifulSoup('<details id="new-details"></details>','html.parser').details))]:
        bad=copy.deepcopy(after);modify(bad)
        checks['G01 unrelated '+name+' remain protected']=content_fingerprint(restore_g01_for_comparison(bad,plan,p))!=expected
    edit=next(e for e in edits if e['mode']=='visible');bad=copy.deepcopy(after);bad.find(id=edit['id']).append(' Sai nội dung.')
    try:restore_g01_for_comparison(bad,plan,p);checks['G01 rejects altered bound prose']=False
    except ValueError:checks['G01 rejects altered bound prose']=True
    stale=copy.deepcopy(plan);stale['instructions_transition']['source_qmd_sha256']='0'*64
    try:restore_g01_for_comparison(after,stale,p);checks['G01 rejects stale source binding']=False
    except ValueError:checks['G01 rejects stale source binding']=True
    checks['D0 outside learning package contract']=source_checks(BASE/'d0/index.qmd')=={}
    report={'checks':checks,'passed':sum(checks.values()),'total':len(checks),'failures':[k for k,v in checks.items() if not v],'rendered':False}
    if args.report:
        dest=args.report.resolve()
        if not dest.is_relative_to(ROOT/'_audit') or dest.suffix!='.json':raise ValueError('Audit JSON path required')
        dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:report[k] for k in ['passed','total','failures']},ensure_ascii=False));return int(bool(report['failures']))
if __name__=='__main__':raise SystemExit(main())
