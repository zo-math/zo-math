"""Table function regressions: sources and in-memory fragments, no page build."""
import argparse,copy,json,re,sys,subprocess
from pathlib import Path
from unittest.mock import patch
from bs4 import BeautifulSoup
import zo_course_table_roles as roles
import zo_course_tables as tables
from zo_web_2027_production import content_fingerprint
from zo_course_editorial import closure


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--report',type=Path);args=ap.parse_args();c={};data=roles.contract();base=roles.ROOT/'content/thpt/on_thi_toan_thpt/hoc_lieu'
    for key in ['d0','r1_g01','r1_g02','r1_g03','r1_g04']:
        p=base/key/'index.qmd';text=p.read_text(encoding='utf-8');values=roles.source_checks(p);c.update({key+'/'+k:v for k,v in values.items()})
        # A newly inserted unbound table must not escape the source gate.
        bad=text+'\n::: {#unbound-table}\n| A | B |\n|---|---|\n| a | b |\n:::\n'
        c[key+'/reject unbound table']=not all(roles.source_checks(p,text=bad).values())
        if key=='d0':continue
        b=json.loads((p.parent/'giao_dien/he_nhan.json').read_text(encoding='utf-8'));ident=b['learning_goals']['assessment_table'];rows=roles.table_rows(text,ident)
        bad=text.replace('Mục tiêu cần kiểm | Bài làm cần đối chiếu | Biểu hiện cần có','Mục tiêu | Bằng chứng | Nơi hỗ trợ',1)
        c[key+'/reject wrong role headers']=not all(roles.source_checks(p,text=bad).values())
        old=next(l for l in text.splitlines() if l.startswith('| '+rows[1][0]+' |') and rows[1][1] in l)
        for name,replacement in [('missing goal evidence',''),('wrong route',old.replace('](#','](#missing-',1)),('empty criterion','| '+' | '.join(rows[1][:-1])+ ' | |')]:
            c[key+'/reject '+name]=not all(roles.source_checks(p,text=text.replace(old,replacement,1)).values())
        bad=text.replace('Mục tiêu cần kiểm','Kiểm tra 01',1)
        c[key+'/reject old task header']=not all(roles.source_checks(p,text=bad).values())
        for entry in data['pages'][key]:
            if entry.get('function')!='scoring':continue
            score_rows=roles.table_rows(text,entry['selector'][1:].split()[0]);score=score_rows[1][-1]
            line=next(l for l in text.splitlines() if l.startswith('| '+score_rows[1][0]+' |') and score_rows[1][1] in l)
            changed=line.rsplit(score,1)[0]+'Điểm '+score+line.rsplit(score,1)[1]
            c[key+'/'+entry['selector']+'/reject prose in score column']=not all(roles.source_checks(p,text=text.replace(line,changed,1)).values())
    home=roles.ROOT/'content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/index.qmd'
    c['Home needs no invented table']=all(roles.source_checks(home).values()) and not data['pages']['home']
    # Exercise the production binder with every function, using isolated data
    # fixtures rather than files or historical page HTML.
    for name,p in data['function_profiles'].items():
        heads=p.get('headers') or ['Cột '+str(i) for i in range(len(p['widths']))]
        head=''.join('<th>'+h+'</th>' for h in heads)
        body=''.join('<td>'+('1' if i+1 in p.get('right_columns',[]) else '<a href="#kept">Nội dung '+str(i)+'</a>')+'</td>' for i in range(len(heads)))
        doc=BeautifulSoup('<html><body><main class="reader-content"><div id="fixture"><table><thead><tr>'+head+'</tr></thead><tbody><tr>'+body+'</tr></tbody></table></div></main></body></html>','html.parser')
        before=doc.table.get_text(' ',strip=True);links=[a['href'] for a in doc.select('a')]
        local=copy.deepcopy(data);entry={'selector':'#fixture table','kind':p['kind'],'role':name,'function':name};local['pages']['home']=[entry]
        with patch.object(tables,'load_contract',return_value=local):tables.bind(doc,'home')
        c[name+'/production function binding']=all(roles.html_checks(doc,data).values())
        c[name+'/text and URLs unchanged']=doc.table.get_text(' ',strip=True)==before and [a['href'] for a in doc.select('a')]==links
        first=str(doc)
        with patch.object(tables,'load_contract',return_value=local):tables.bind(doc,'home')
        c[name+'/binding idempotent']=str(doc)==first
        bad=copy.deepcopy(doc);bad.table['data-table-responsive']='wrong';c[name+'/reject wrong responsive policy']=not all(roles.html_checks(bad,data).values())
        bad=copy.deepcopy(doc);bad.col['style']='width:99%';c[name+'/reject uneven copied widths']=not all(roles.html_checks(bad,data).values())
        if p['responsive']=='records':
            bad=copy.deepcopy(doc);bad.select_one('.zo-table-field-label')['data-label']='Sai nhãn';c[name+'/reject missing field context']=not all(roles.html_checks(bad,data).values())
        if name=='scoring':
            bad=copy.deepcopy(doc);bad.select_one('tbody .zo-numeric-cell')['class']=[];c['scoring/reject left score']=not all(roles.html_checks(bad,data).values())
        for bad in [dict(entry,widths=p['widths']),dict(entry,function='unknown')]:
            try:roles.function_profile(bad,data);ok=False
            except ValueError:ok=True
            c[name+'/reject '+('override' if 'widths' in bad else 'unknown function')]=ok
    # Bounded G01 reversal uses current QMD fragments, retaining all independent
    # text/math/URL/ID checks instead of accepting a new whole-page fingerprint.
    p=base/'r1_g01/index.qmd';text=p.read_text(encoding='utf-8');plan=json.loads((p.parent/'giao_dien/web_2027_layout.json').read_text(encoding='utf-8'));edits=plan['table_function_transition']['edits'];parts=[]
    for n,e in enumerate(edits):
        if e.get('id'):
            m=re.search(r'(?m)^(:{3,}) \{#'+re.escape(e['id'])+r'[^\n]*\}\n.*?^\1[ \t]*$',text,re.S|re.M);assert m,e['id'];parts.append(m[0])
        else:
            # Match only single source headings/paragraphs by parsed leaf keys.
            for line in text.splitlines():
                if not line.strip() or line.startswith(('|',':')):continue
                from zo_course_editorial import sha,norm
                plain=re.sub(r'^#{1,6} ','',re.sub(r' \{#[^}]+\}$','',line))
                if e['after_signature']['inline']==[['text',sha(norm(plain))]]:parts.append(line);break
            else:raise AssertionError('Missing reviewed paragraph')
    r=subprocess.run([sys.executable,'-B',str(roles.ROOT/'scripts/zo_python.py'),'-B',str(roles.ROOT/'scripts/zo_quarto.py'),'pandoc','-f','markdown','-t','html','--mathml'],input='\n\n'.join(parts),encoding='utf-8',text=True,capture_output=True,check=True,cwd=roles.ROOT)
    fresh=BeautifulSoup(r.stdout,'html.parser');serialized=str(fresh);restored=roles.restore_g01_for_comparison(fresh,plan,p)
    expected=BeautifulSoup('\n'.join(e['before_html'] for e in edits),'html.parser')
    c['G01 exact bounded reversal']=content_fingerprint(restored)==content_fingerprint(expected)
    c['G01 inverse never changes learner DOM']=str(fresh)==serialized
    for e in edits:
        if e.get('id'):c['G01 current node '+e['id']]=roles.same_node_signature(roles.node_signature(roles.source_node(fresh,e['id'],plan)),e['after_signature'])
    for name,mutate in [('word',lambda n:n.table.find('td').append(' Sai.')),('URL',lambda n:n.find('a').__setitem__('href','#wrong')),('math',lambda n:setattr(n.find('annotation'),'string','x+999')),('duplicate',lambda n:n.append(copy.deepcopy(n.find(id=edits[0]['id']))))]:
        bad=copy.deepcopy(fresh);mutate(bad)
        try:roles.restore_g01_for_comparison(bad,plan,p);ok=False
        except ValueError:ok=True
        c['G01 reject changed '+name]=ok
    outside=BeautifulSoup('<p id="outside">Ngoài phạm vi.</p>','html.parser').p;fresh.append(outside);before=content_fingerprint(roles.restore_g01_for_comparison(fresh,plan,p));outside.append(' Đã đổi.');c['G01 outside changes remain visible']=content_fingerprint(roles.restore_g01_for_comparison(fresh,plan,p))!=before
    css=(roles.ROOT/'_design/web_2027_mau_dung_chung/course-tables.css').read_text(encoding='utf-8')
    for before,after in [('text-align:right;','text-align:left;'),('clip-path:inset(50%)','display:none'),('min-width:0!important','min-width:80em!important')]:c['reject CSS '+after]=not all(roles.style_checks(css.replace(before,after)).values())
    report={'passed':sum(c.values()),'total':len(c),'failures':[k for k,v in c.items() if not v],'checks':c,'rendered_pages':False,'visual_review':False}
    if args.report:
        dest=args.report.resolve();assert dest.is_relative_to(roles.ROOT/'_audit');dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k!='checks'},ensure_ascii=False));return int(bool(report['failures']))
if __name__=='__main__':raise SystemExit(main())
