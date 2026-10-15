"""Check an actual course PDF: links, print destinations, fonts and shell.

Technical evidence only. Page-by-page visual review and owner acceptance stay
separate. Run with the repository Python launcher.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import yaml
from pypdf import PdfReader
from zo_pdf_support import support_model


def footer_checks(reader):
    results=[]
    for page in reader.pages:
        width,height=float(page.mediabox.width),float(page.mediabox.height)
        matches=[]
        for ref in page.get('/Annots',[]):
            ann=ref.get_object(); action=ann.get('/A',{})
            if action.get('/URI')=='https://zomath.vn':
                rect=[float(x) for x in ann['/Rect']]
                if rect[3]<height*.10: matches.append(rect)
        results.append(len(matches)==1 and abs((matches[0][0]+matches[0][2])/2-width/2)<3)
    return results


def orphan_task_pages(reader):
    """Reject a task heading as the last body line, before the running footer."""
    failures=[]
    for number,page in enumerate(reader.pages[1:-1],2):
        lines=[line.strip() for line in page.extract_text().splitlines() if line.strip()]
        lines=[line for line in lines if line!='Ôn thi Toán THPT 2027' and line!='zomath.vn' and not line.isdigit()]
        # Depending on text extraction, all three footer items share one line.
        lines=[line for line in lines if not line.startswith('Ôn thi Toán THPT 2027')]
        if lines and '(trang' not in lines[-1] and re.match(r'^Nhiệm vụ\s+\d+\b',lines[-1]):failures.append(number)
    return failures


def clipped_text_pages(reader):
    failures=[]
    for number,page in enumerate(reader.pages,1):
        height=float(page.mediabox.height)
        form_depth=0
        def before(operator,operands,cm,tm):
            nonlocal form_depth
            if operator==b'Do':form_depth+=1
        def after(operator,operands,cm,tm):
            nonlocal form_depth
            if operator==b'Do':form_depth-=1
        def visitor(text,cm,tm,font,size):
            # pypdf emits a second, consolidated Form XObject string using
            # the outer text matrix. It is not a physical glyph position.
            # Vector artwork is validated separately by paired-asset checks
            # and raster review; inspect native page text here.
            if form_depth or not text.strip():return
            baseline=tm[4]*cm[1]+tm[5]*cm[3]+cm[5]
            # Interior glyphs must also stay below the physical top margin;
            # a box may overrun into that margin without leaving the paper.
            top=height-35 if 1<number<len(reader.pages) else height+1
            if baseline < -1 or baseline > top:
                failures.append({'page':number,'baseline':round(baseline,2),'text':text.strip()[:90]})
        page.extract_text(visitor_text=visitor,visitor_operand_before=before,visitor_operand_after=after)
    return failures


def check(path):
    reader=PdfReader(path); texts=[p.extract_text() for p in reader.pages]
    all_text='\n'.join(texts); support=support_model()
    config=yaml.safe_load((path.parent/'_quy_trinh/cau_hinh_san_xuat_qmd.yml').read_text(encoding='utf-8'))
    profile=yaml.safe_load((path.parent/'_quy_trinh/ho_so/index.yml').read_text(encoding='utf-8'))
    definition=next(v for v in config['extensions']['pdf_variants'].values() if v['output']==path.name)
    shell=config['extensions']['course_pdf_shell']
    norm=lambda t:re.sub(r'\s+',' ',t).strip()
    compact=lambda t:re.sub(r'\s+','',t)
    checks={
        'A4 every page':all(abs(float(p.mediabox.width)-595.276)<1 and abs(float(p.mediabox.height)-841.89)<1 for p in reader.pages),
        'centered HTTPS website footer every page':all(footer_checks(reader)),
        'resolved print page references':'??' not in all_text and (path.name not in ['index.pdf','index_hoc_sinh.pdf'] or '(trang' in all_text),
        'cover title and version':norm(' '.join(shell['cover_lines'])) in norm(texts[0]) and 'Phiên bản nội dung '+str(profile['package']['candidate_version']) in texts[0],
        'cover creation date and rights':'Ngày tạo PDF:' in texts[0] and 'Bản quyền nội dung thuộc ZO Math' in texts[0],
        'closing learning invitation':'Chọn điều em' in texts[-1] and 'Mở học liệu' in texts[-1],
        'current support title and account':(support['title'] in texts[-1] and all(compact(f['value']) in compact(texts[-1]) for f in support['fields'])) if definition.get('include_support',True) else support['title'] not in texts[-1],
        'no former support wording':'ủng hộ' not in all_text.lower(),
        'learning projection':all(s in all_text for s in ['Bắt đầu','Bài học','Luyện tập','Kiểm tra','Ôn lại','Ôn nền','Sửa lỗi','Nhật kí','Lời giải','Nguồn']) if path.name=='index.pdf' else len(texts)>2,
        'no nearly empty interior pages':all(len(t.strip())>160 for t in texts[1:-1]),
        'no task heading stranded at page end':not orphan_task_pages(reader),
        'no text clipped beyond physical page':not clipped_text_pages(reader),
    }
    fonts=set();missing=[]
    def resources(res):
        for font_ref in res.get('/Font',{}).values():
            font=font_ref.get_object(); fonts.add(str(font.get('/BaseFont','')))
            face=font.get('/DescendantFonts',[font])[0].get_object()
            descriptor=face.get('/FontDescriptor')
            if descriptor is None or not any(k in descriptor.get_object() for k in ['/FontFile','/FontFile2','/FontFile3']):
                missing.append(str(font.get('/BaseFont')))
        for ref in res.get('/XObject',{}).values():
            obj=ref.get_object()
            if obj.get('/Resources'):resources(obj['/Resources'])
    for p in reader.pages:resources(p['/Resources'])
    checks['all fonts embedded']=not missing
    checks['Be Vietnam Pro and STIX Math']=any('BeVietnamPro' in f for f in fonts) and any('STIXTwoMath' in f for f in fonts)
    # Negative guard case uses an in-memory reader; never changes the PDF.
    negative=PdfReader(path)
    for ref in negative.pages[0].get('/Annots',[]):
        ann=ref.get_object()
        if ann.get('/A',{}).get('/URI')=='https://zomath.vn':
            from pypdf.generic import NameObject,TextStringObject
            ann['/A'][NameObject('/URI')]=TextStringObject('https://example.invalid')
    checks['negative wrong footer rejected']=not all(footer_checks(negative))
    from types import SimpleNamespace
    bad=SimpleNamespace(extract_text=lambda:'Previous question text\nNhiệm vụ 13 – Xen kẽ cực trị và giá trị lớn nhất\nÔn thi Toán THPT 2027 zomath.vn 8')
    good=SimpleNamespace(extract_text=lambda:'Lượt quay lại\nNhiệm vụ 03 (trang 38)\nÔn thi Toán THPT 2027 zomath.vn 35')
    checks['negative stranded task heading rejected']=orphan_task_pages(SimpleNamespace(pages=[None,bad,None]))==[2] and not orphan_task_pages(SimpleNamespace(pages=[None,good,None]))
    bad_page=SimpleNamespace(mediabox=SimpleNamespace(height=841.89),extract_text=lambda visitor_text,**kwargs:visitor_text('Clipped task',[1,0,0,1,0,0],[1,0,0,1,20,900],None,10))
    checks['negative clipped text rejected']=bool(clipped_text_pages(SimpleNamespace(pages=[bad_page])))
    return {'checks':checks,'pages':len(reader.pages),'fonts':sorted(fonts),
            'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'passed':sum(checks.values()),'total':len(checks),
            'failures':[k for k,v in checks.items() if not v],
            'owner_acceptance':'pending','publication':'pending'}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pdf',type=Path);parser.add_argument('--report',type=Path)
    args=parser.parse_args();report=check(args.pdf)
    if args.report:
        args.report.parent.mkdir(parents=True,exist_ok=True)
        args.report.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))
    return int(bool(report['failures']))


if __name__=='__main__':raise SystemExit(main())
