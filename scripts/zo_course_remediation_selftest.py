"""Source and in-memory component regressions; no page HTML/PDF build."""
import argparse,copy,json,re,subprocess,sys,tempfile
from pathlib import Path
from bs4 import BeautifulSoup
from zo_course_remediation import ROOT,HEADERS,source_checks,html_checks,restore_g01_for_comparison,source_node
from zo_web_2027_production import content_fingerprint
from zo_course_editorial import inline_signature

def fragment(s):
    result=subprocess.run([sys.executable,'-B',str(ROOT/'scripts/zo_python.py'),'-B',str(ROOT/'scripts/zo_quarto.py'),'pandoc','-f','markdown','-t','html','--mathml'],input=s,text=True,encoding='utf-8',capture_output=True,check=True,cwd=ROOT)
    return BeautifulSoup(result.stdout,'html.parser')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--report',type=Path);args=ap.parse_args();checks={};base=ROOT/'content/thpt/on_thi_toan_thpt/hoc_lieu'
    for g in ['r1_g01','r1_g02','r1_g03','r1_g04']:
        p=base/g/'index.qmd';t=p.read_text(encoding='utf-8');b=json.loads((p.parent/'giao_dien/he_nhan.json').read_text(encoding='utf-8'))['remediation'];ident=b['table']
        checks.update({g+'/'+k:v for k,v in source_checks(p).items()})
        block=re.search(r'(?m)^(:{3,}) \{#'+ident+r'[^\n]*\}\n.*?^\1[ \t]*$',t,re.S|re.M)[0]
        for name,bad in [('missing row',t.replace(next(x for x in block.splitlines() if x.startswith('| '+b['rows'][0]['title']+' |'))+'\n','',1)),('old columns',t.replace('Nút thắt nhận thức | Biểu hiện dễ nhầm','Dấu hiệu cần sửa | Sau Luyện tập',1)),('missing question',t.replace(block,block.replace('?','.'),1)),('wrong target',t.replace('](#'+b['rows'][0]['knowledge_anchors'][0]+')','](#missing-bottleneck-target)')),('duplicate',t+'\n'+block)]:
            checks[g+'/reject '+name]=not all(source_checks(p,text=bad).values())
        doc=fragment(block);table=doc.table;table['data-table-kind']='process';table['data-table-variant']='routing'
        checks[g+'/parsed source table component']=all(html_checks(doc).values())
        bad=copy.deepcopy(doc);bad.table.find('th').string='Cột cũ';checks[g+'/reject stale rendered column']=not all(html_checks(bad).values())
        bad=copy.deepcopy(doc);bad.find(id=ident).wrap(bad.new_tag('details'));checks[g+'/reject hidden table']=not all(html_checks(bad).values())
        if g=='r1_g01':
            plan=json.loads((p.parent/'giao_dien/web_2027_layout.json').read_text(encoding='utf-8'))
            fresh=fragment(block);text_before=str(fresh)
            expected=BeautifulSoup(plan['remediation_transition']['edits'][0]['before_html'],'html.parser')
            restored=restore_g01_for_comparison(fresh,plan,p)
            checks['G01 exact previous table restored for comparison']=content_fingerprint(restored)==content_fingerprint(expected)
            checks['G01 inverse does not change source DOM']=str(fresh)==text_before
            checks['G01 output uses current QMD table']=inline_signature(source_node(fresh,ident,plan))==inline_signature(fresh.find(id=ident))
            checks['G01 accepted fingerprint retained']=plan['accepted_sha256']=='5c97396dd9656971e442cb60a07aa799935d3233bf2ae15a53ebc57f76c77e3c'
            for name,bad in [('changed content',copy.deepcopy(fresh)),('duplicate table',copy.deepcopy(fresh))]:
                if name=='changed content':bad.table.find('td').append(' Nội dung khác.')
                else:bad.append(copy.deepcopy(bad.find(id=ident)))
                try:source_node(bad,ident,plan);checks['G01 rejects '+name]=False
                except ValueError:checks['G01 rejects '+name]=True
            sample=copy.deepcopy(fresh);sample.append(BeautifulSoup('<p id="outside">Ngoài bảng.</p>','html.parser'))
            a=content_fingerprint(restore_g01_for_comparison(sample,plan,p));sample.find(id='outside').append(' Thay đổi khác.')
            checks['G01 changes outside table remain detectable']=a!=content_fingerprint(restore_g01_for_comparison(sample,plan,p))
    with tempfile.TemporaryDirectory() as tmp:
        p=Path(tmp)/'content/thpt/on_thi_toan_thpt/hoc_lieu/r2_g07/index.qmd';p.parent.mkdir(parents=True);p.write_text('## Sửa lỗi {#sua-loi}\n',encoding='utf-8')
        checks['future package cannot omit declaration']=not all(source_checks(p,Path(tmp)).values())
        checks['D0 is not forced into R1']=source_checks(base/'d0/index.qmd')=={}
    report={'passed':sum(checks.values()),'total':len(checks),'failures':[k for k,v in checks.items() if not v],'checks':checks,'rendered_pages':False}
    if args.report:
        dest=args.report.resolve();assert dest.is_relative_to(ROOT/'_audit');dest.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k!='checks'},ensure_ascii=False));return int(bool(report['failures']))
if __name__=='__main__':raise SystemExit(main())
