"""Audit current course sources, paired figures and all registered PDF variants.

Does not publish or certify owner acceptance. Optional preflight emits TeX only
and stops on the first defect before any expensive book compilation.
"""
from pathlib import Path
import argparse,json,re,subprocess,sys
sys.dont_write_bytecode=True
import yaml
from zo_pdf_contract import course_pdf_source_digest,validate_canonical_pdf_provenance
ROOT=Path(__file__).resolve().parents[1]
PACKAGES=[ROOT/'content/thpt/on_thi_toan_thpt/hoc_lieu'/k for k in ['r1_g01','r1_g02']]

def guards():
    from zo_web_2027_figures import CONFIG,verify_print_source
    config=json.loads(CONFIG.read_text(encoding='utf-8'))
    text=(PACKAGES[0]/'index.qmd').read_text(encoding='utf-8')
    verify_print_source(text,config)
    for old in ['hinh/do_thi_01.svg','hinh/do_thi_01.pdf']:
        wrong=text.replace('giao_dien/assets/figures_0_4/do_thi_01.svg',old)
        try:verify_print_source(wrong,config)
        except ValueError:pass
        else:raise ValueError('Legacy graph fixture escaped preflight')
    from zo_pdf import verify_course_graph_paths
    g02=PACKAGES[1]/'index.qmd'
    current=g02.read_text(encoding='utf-8')
    verify_course_graph_paths(g02,current)
    for old in ['hinh/do_thi_01.svg','hinh/do_thi_01.pdf']:
        try:verify_course_graph_paths(g02,current.replace('giao_dien/assets/figures_0_4/do_thi_01.svg',old))
        except ValueError:pass
        else:raise ValueError('Legacy G02 graph fixture escaped preflight')
    digest=course_pdf_source_digest(text)
    changed=re.sub(r'(\n    pages: )\d+',r'\g<1>999',text)
    assert changed!=text and course_pdf_source_digest(changed)==digest
    for wrong in [text.replace('Đơn điệu và cực trị','Wrong title',1),text+'\nExtra body content',text.replace('figures_0_4/do_thi_01.svg','hinh/do_thi_01.svg')]:
        assert course_pdf_source_digest(wrong)!=digest
    from bs4 import BeautifulSoup
    from unittest.mock import patch
    from zo_course_pdf_download_state import apply
    registry=yaml.safe_load((PACKAGES[0]/'_quy_trinh/cau_hinh_san_xuat_qmd.yml').read_text(encoding='utf-8'))['extensions']['pdf_variants']
    old='Số trang được đọc từ các tệp PDF đang có; các bản PDF này chưa được đồng bộ với HTML mới.'
    fixture='<section id="tai-tai-lieu"><h2>Tải tài liệu</h2><p>'+old+'</p>'+''.join('<div class="zo-pdf-card"><a download href="'+d['output']+'">PDF</a><span class="zo-pdf-version-note"></span></div>' for d in registry.values())+'</section>'
    with patch('zo_course_pdf_download_state.validate_canonical_pdf_provenance',return_value=[]):
        doc=BeautifulSoup(fixture,'html.parser')
        assert all(apply(doc,ROOT,PACKAGES[0].relative_to(ROOT)))
        assert old not in doc.get_text() and 'đang chờ cập nhật' not in doc.get_text()
        for duplicate in [False,True]:
            broken=BeautifulSoup(fixture,'html.parser')
            links=broken.select('a[download]')
            if duplicate:links[-1]['href']=links[0]['href']
            else:links[-1].parent.decompose()
            try:apply(broken,ROOT,PACKAGES[0].relative_to(ROOT))
            except ValueError:pass
            else:raise ValueError('Missing/duplicate PDF card escaped validation')
    with patch('zo_course_pdf_download_state.validate_canonical_pdf_provenance',return_value=['fixture stale']):
        doc=BeautifulSoup(fixture,'html.parser')
        assert not any(apply(doc,ROOT,PACKAGES[0].relative_to(ROOT)))
        assert all(card['data-pdf-current']=='false' for card in doc.select('.zo-pdf-card'))
    return {'legacy_SVG_rejected':True,'legacy_PDF_rejected':True,'HTML_page_count_does_not_invalidate_PDF':True,'title_body_figure_drift_invalidates_PDF':True,'obsolete_download_notice_removed_when_current':True,'missing_PDF_card_rejected':True,'duplicate_PDF_card_rejected':True,'stale_PDF_never_labelled_current':True}

def run(out,preflight=False):
    out.mkdir(parents=True,exist_ok=True)
    report={'guards':guards(),'packages':{},'owner_acceptance':'pending','published':False}
    for pkg in PACKAGES:
        config=yaml.safe_load((pkg/'_quy_trinh/cau_hinh_san_xuat_qmd.yml').read_text(encoding='utf-8'))
        report['packages'][pkg.name]={}
        for variant,definition in config['extensions']['pdf_variants'].items():
            if preflight:
                command=['python','scripts/zo_python.py','-B','scripts/zo_pdf.py','preflight',str((pkg/'index.qmd').relative_to(ROOT)), '--variant',variant]
                log=out/f'{pkg.name}-{variant}-preflight.log'
                with log.open('w',encoding='utf-8') as stream:
                    result=subprocess.run(command,cwd=ROOT,stdout=stream,stderr=subprocess.STDOUT)
                print(pkg.name,variant,'PREFLIGHT',result.returncode,flush=True)
                if result.returncode:raise ValueError('Preflight failed: '+str(log))
                tex=(ROOT/'_audit'/f'{pkg.name}_{variant}_preflight.tex').read_text(encoding='utf-8')
                if re.search(r'Hình\s*\n\s*\n[AB]:',tex):raise ValueError('Caption words became separate paragraphs')
                if re.search(r'\\includegraphics[^\n]*\{hinh/(?:do_thi_|bbt)',tex):raise ValueError('Legacy print picture escaped preflight')
            report['packages'][pkg.name][variant]={'file':definition['output'],'provenance_errors':validate_canonical_pdf_provenance(ROOT,pkg/'index.qmd',variant=variant)}
    (out/'release-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    failures=[f'{p}/{v}' for p,items in report['packages'].items() for v,item in items.items() if item['provenance_errors']]
    print(json.dumps({'PDF_variants':16,'stale':failures,'guards':report['guards']},ensure_ascii=False))
    return int(bool(failures))

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);p.add_argument('--preflight',action='store_true');a=p.parse_args()
    raise SystemExit(run(a.output.resolve(),a.preflight))
