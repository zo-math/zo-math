"""Source-only regression for question/solution action wording; no page render."""
from pathlib import Path
import argparse,json
from bs4 import BeautifulSoup
from zo_course_labels import (ROOT,expand,binding,answer_action_labels,
    answer_action_source_checks,answer_action_html_checks)

BASE=Path('content/thpt/on_thi_toan_thpt/hoc_lieu')


def run():
    results={};counts={};labels=answer_action_labels()
    for key in ['d0',*[f'r1_g0{g}' for g in range(1,5)]]:
        source=ROOT/BASE/key/'index.qmd';text=expand(source)
        checks=answer_action_source_checks(source);counts[key]=len(checks)
        results[key+' canonical source actions']=bool(checks) and all(checks.values())
        for old in ['Xem lời giải sau khi tự làm','Đối chiếu sau khi tự làm','Xem đáp án câu xác nhận']:
            bad=text.replace('['+labels['forward']+']','['+old+']',1)
            results[key+'/reject forward '+old]=bad!=text and not all(answer_action_source_checks(source,text=bad).values())
        for old in ['Trở lại đề','Trở về đề — Tên nhiệm vụ','Xem câu xác nhận','Câu hỏi gốc']:
            bad=text.replace('['+labels['return']+']','['+old+']',1)
            results[key+'/reject return '+old]=bad!=text and not all(answer_action_source_checks(source,text=bad).values())
        # A DOM fixture validates the same post-render gate without writing HTML.
        unit=next(u for u in binding(source)['units'] if u.get('answer'))
        q,a=unit['question'],unit['answer'];data={'units':[unit]}
        doc=BeautifulSoup('<div class="reader-content"><section id="'+q+'"><a href="#'+a+'">'+labels['forward']+'</a></section><section id="'+a+'"><a href="#'+q+'">'+labels['return']+'</a></section></div>','html.parser')
        results[key+' canonical DOM actions']=all(answer_action_html_checks(doc,data).values())
        doc.select_one('a').string='Đối chiếu sau khi tự làm'
        results[key+' DOM rejects old forward']=not all(answer_action_html_checks(doc,data).values())
        doc.select_one('a').string=labels['forward'];doc.select('a')[-1].string='Câu hỏi gốc'
        results[key+' DOM rejects arbitrary return']=not all(answer_action_html_checks(doc,data).values())
    source=ROOT/BASE/'r1_g02/index.qmd';text=expand(source)
    results['G02 separate formula disclosure retained']='[Xem công thức để kiểm tra](#loi-giai-l06-cong-thuc)' in text and all(answer_action_source_checks(source).values())
    results['unrelated d0 directory unaffected']=answer_action_source_checks(ROOT/'content/another_project/d0/index.qmd')=={}
    results['other projects unaffected']=answer_action_source_checks(ROOT/'content/about.qmd')=={}
    return results,counts


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--report',type=Path);args=parser.parse_args()
    checks,counts=run();result={'passed':sum(checks.values()),'total':len(checks),'failures':[k for k,v in checks.items() if not v],'checks':checks,'source_actions':counts,'html_rebuilt':False,'owner_acceptance':'pending'}
    if args.report:
        path=args.report.resolve()
        if not path.is_relative_to(ROOT/'_audit'):raise ValueError('Report must stay in audit')
        path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:result[k] for k in ['passed','total','failures','source_actions']},ensure_ascii=False));raise SystemExit(int(bool(result['failures'])))
