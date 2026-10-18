"""Current-source and negative regressions for package-visible numbering."""
from pathlib import Path
from collections import Counter
import copy,json,hashlib
from bs4 import BeautifulSoup
from zo_course_labels import ROOT,binding,expand,binding_checks,context_unit_label
from zo_course_numbering import source_checks,group,restore_g01_for_comparison,reference_checks

def main():
    checks={}
    for n in range(1,5):
        p=ROOT/f'content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g{n:02d}/index.qmd'
        data=binding(p);text=expand(p)
        checks[f'G{n:02d} current source and references']=all(source_checks(text,data).values()) and all(binding_checks(data).values())
        units=[u for u in data['units'] if group(u)=='Nhiệm vụ']
        for function in sorted({u['function'] for u in units}):
            bad=copy.deepcopy(data);u=next(u for u in bad['units'] if u['function']==function)
            if u['number']==1:continue
            u['number']=1
            checks[f'G{n:02d} reset at {function} rejected']=not all(source_checks(text,bad).values())
        bad=copy.deepcopy(data);bad['units'][0]['title']='Nhiệm vụ 99 — Sai số'
        checks[f'G{n:02d} wrong title rejected']=not all(source_checks(text,bad).values())
        bad=copy.deepcopy(data);u=next(u for u in bad['units'] if u.get('answer'));u['answer_title']='Nhiệm vụ 99 — Sai lời giải'
        checks[f'G{n:02d} mismatched answer rejected']=not all(source_checks(text,bad).values())
        bad=copy.deepcopy(data);bad['checkpoint_numbers'][next(iter(bad['checkpoints']))]=99
        checks[f'G{n:02d} wrong checkpoint rejected']=not all(source_checks(text,bad).values())
        lesson=[u for u in data['units'] if u['function'] in ('function.warmup','function.self_check','function.guided_thinking')]
        checks[f'G{n:02d} lesson context exactly two levels']=all(context_unit_label(u,'question',data)=='MẠCH HỌC · BÀI HỌC' for u in lesson)
        checks[f'G{n:02d} answers belong to actual support area']=all(context_unit_label(u,'answer',data).startswith('HỖ TRỢ · ') for u in data['units'] if u.get('answer'))
    from zo_course_numbering import retired_self_check_absent
    from zo_course_remediation import HEADERS, CONTRACT
    fixture=BeautifulSoup('<main class="reader-content"><div id="routing" data-zo-remediation="'+CONTRACT+'"><table><thead><tr>'+''.join('<th>'+h+'</th>' for h in HEADERS)+'</tr></thead><tbody><tr><td>Nội dung</td></tr></tbody></table></div></main>','html.parser').main
    data={'remediation':{'contract':CONTRACT,'table':'routing'}}
    before=str(fixture)
    checks['routing column allowed in its exact owned component']=retired_self_check_absent(fixture,data)
    checks['numbering inspection never changes rendered content']=str(fixture)==before
    for name,tag in [('heading','h3'),('paragraph','p'),('link','a')]:
        bad=copy.deepcopy(fixture);bad.append(BeautifulSoup('<'+tag+'>Tự kiểm tra 01</'+tag+'>','html.parser'))
        checks['retired activity outside routing '+name+' rejected']=not retired_self_check_absent(bad,data)
    bad=copy.deepcopy(fixture);bad.div.attrs.pop('data-zo-remediation')
    checks['unmarked routing column rejected']=not retired_self_check_absent(bad,data)
    bad=copy.deepcopy(fixture);bad.div['id']='other'
    checks['unowned routing column rejected']=not retired_self_check_absent(bad,data)
    bad=copy.deepcopy(fixture);bad.select('th')[-1].string='Tự kiểm tra 01'
    checks['numbered old activity inside routing column rejected']=not retired_self_check_absent(bad,data)
    bad=copy.deepcopy(fixture);bad.append(copy.deepcopy(bad.div))
    checks['duplicate routing exception rejected']=not retired_self_check_absent(bad,data)
    from zo_course_editorial import inline_signature
    from zo_web_2027_production import content_fingerprint
    qmd=ROOT/'content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g01/index.qmd'
    checks['old reference number in metadata rejected']=not all(reference_checks('nhiệm vụ 07 của Luyện tập',binding(qmd)).values())
    checks['current reference number in metadata accepted']=all(reference_checks('nhiệm vụ 18 của Luyện tập',binding(qmd)).values())
    new=BeautifulSoup('<main><h4 id="task">Nhiệm vụ 05</h4><p id="outside">Nội dung giữ nguyên.</p></main>','html.parser').main
    plan={'numbering_transition':{'id':'NUMBERING-20261018','historical_comparison_only':True,'source_qmd_sha256':hashlib.sha256(qmd.read_bytes()).hexdigest(),'sources':{},'edits':[{'tag':'h4','source':'fixture','line_before':1,'before_html':'<h4 id="task">Tự kiểm tra 01</h4>','after_signature':inline_signature(new.h4)}]}}
    old=copy.deepcopy(new);old.h4.string='Tự kiểm tra 01'
    saved=str(new)
    checks['G01 bounded inverse preserves the complete comparison']=content_fingerprint(restore_g01_for_comparison(new,plan,qmd))==content_fingerprint(old)
    checks['G01 historical inverse never mutates learner output']=str(new)==saved
    bad=copy.deepcopy(new);bad.p.append(' Thay ngoài phạm vi.')
    checks['G01 changes outside numbering remain detectable']=content_fingerprint(restore_g01_for_comparison(bad,plan,qmd))!=content_fingerprint(old)
    bad=copy.deepcopy(new);bad.h4.append(' Sai số.')
    try:restore_g01_for_comparison(bad,plan,qmd);checks['G01 altered numbered title rejected']=False
    except ValueError:checks['G01 altered numbered title rejected']=True
    print(json.dumps({'passed':sum(checks.values()),'total':len(checks),'failures':[k for k,v in checks.items() if not v]},ensure_ascii=False))
    return int(not all(checks.values()))

if __name__=='__main__':raise SystemExit(main())
