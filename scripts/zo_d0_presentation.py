"""D0 presentation gates; shares action vocabulary without applying R1 architecture."""
from pathlib import Path
import copy,json,re,hashlib
from urllib.parse import urlsplit,parse_qs
from bs4 import BeautifulSoup
from zo_course_labels import answer_action_labels

ROOT=Path(__file__).resolve().parents[1]
PACKAGE=Path('content/thpt/on_thi_toan_thpt/hoc_lieu/d0')
NUMERIC={'d0-r2-02':3,'d0-r2-03':6,'d0-r4-03':4,'d0-r8-03':6,'doi-chieu-r8-03':15}
PAIRS={f'd0-r{r}-{i:02}':f'doi-chieu-r{r}-{i:02}' for r in range(1,9) for i in range(1,4)}


def restore_bai00_logic_source(text, root=ROOT):
    """Reverse only the approved Bài 00 revision for historical comparison."""
    path=Path(root)/PACKAGE/'_quy_trinh/d0_bai00_logic_delta.json'
    delta=json.loads(path.read_text(encoding='utf-8'))
    assert delta['authority']=='Owner-approved D0 Bài 00 logic correction, 2026-10-21'
    assert hashlib.sha256(text.encode()).hexdigest()==delta['source_after_sha256'], 'Unexpected D0 Bài 00 source'
    for change in reversed(delta['replacements']):
        assert change['after'] and text.count(change['after'])==1, 'Missing/repeated Bài 00 revision'
        text=text.replace(change['after'],change['before'],1)
    assert hashlib.sha256(text.encode()).hexdigest()==delta['source_before_sha256'], 'Bài 00 inverse mismatch'
    return text


def numbered_tasks(text):
    """Read titles from QMD; the page order owns numbers, IDs stay stable."""
    records=[]
    for match in re.finditer(r'\{#(cau-minh-hoa|d0-r[1-8]-0[1-3]) [^\n]+\}\n.*?^#### ([^\n]+)',text,re.M|re.S):
        owner,heading=match.groups()
        heading=re.sub(r' \{#[^}]+\}$','',heading)
        records.append((owner,heading))
    return records


def numbering_source_checks(text):
    records=numbered_tasks(text);expected=['cau-minh-hoa',*PAIRS];checks={}
    checks['25 question headings in stable page order']=[r[0] for r in records]==expected
    checks['no task badges or context labels']=not re.search(r'\.d0-task-(?:number|code)|data-reading-label|\{[^\n}]*\.role\b',text)
    checks['no R1 branch labels']=not re.search(r'MẠCH HỌC|HỖ TRỢ',text)
    for number,(owner,heading) in enumerate(records):
        checks[owner+' page-wide Bai number']=bool(re.fullmatch(f'Bài {number:02} — .+',heading))
        answer='doi-chieu-minh-hoa' if owner=='cau-minh-hoa' else PAIRS[owner]
        match=re.search(r'\{#'+answer+r' [^\n]+\}\n::: zo-learning-summary\n([^\n]+)\n:::',text)
        checks[owner+' matching comparison title']=bool(match and match[1]==heading)
    return checks


def restore_numbering_source(text,root=ROOT):
    """Undo the exact authorized source delta for immutable approval checks only."""
    tables=json.loads((Path(root)/PACKAGE/'_quy_trinh/d0_editorial_comparison_delta.json').read_text(encoding='utf-8')).get('table_function_revision')
    if tables:
        assert tables['rule']=='TABLE-FUNCTIONS-20261019' and text.count(tables['after'])==1
        text=text.replace(tables['after'],tables['before'],1)
    delta=json.loads((Path(root)/PACKAGE/'_quy_trinh/d0_numbering_delta.json').read_text(encoding='utf-8'))
    assert delta['authority']=='owner_requested_D0_global_Bai_numbers_no_labels_2026_10_18'
    for change in reversed(delta['replacements']):
        assert text.count(change['after'])==1,'Missing/repeated D0 display delta'
        text=text.replace(change['after'],change['before'],1)
    return text


def restore_presentation_source(text, root=ROOT):
    """Undo the hash-bound 18/10 display delta for historical comparison."""
    data=json.loads((Path(root)/PACKAGE/'_quy_trinh/d0_presentation_comparison_delta.json').read_text(encoding='utf-8'))
    assert data['authority']=='d0_trinh_bay_20261018.json; owner-authorized source presentation delta'
    assert hashlib.sha256(text.encode()).hexdigest()==data['source_after_sha256'],'Unexpected D0 presentation source'
    for change in reversed(data['replacements']):
        after=change['after'];before=change['before']
        assert after and text.count(after)>=1,'Missing D0 presentation delta fragment'
        text=text.replace(after,before,1)
    assert hashlib.sha256(text.encode()).hexdigest()==data['source_before_sha256'],'D0 presentation inverse mismatch'
    return text


def restore_editorial_source(text, root=ROOT):
    """Undo the bounded editorial delta before immutable approval checks."""
    data=json.loads((Path(root)/PACKAGE/'_quy_trinh/d0_editorial_comparison_delta.json').read_text(encoding='utf-8'))
    assert data['authority']=='EDITORIAL-20261018 owner-approved matrix; bounded inverse for unchanged historical approval only'
    changes=data['source_changes']
    removed=[change for change in changes if change['after']=='']
    assert len(removed)==24 and len({change['before'] for change in removed})==1
    repeated=removed[0]['before']
    assert repeated not in text,'Repeated D0 guidance unexpectedly present before inversion'
    for change in reversed([change for change in changes if change['after']]):
        assert text.count(change['after'])==1,'Missing/repeated D0 editorial source delta'
        text=text.replace(change['after'],change['before'],1)
    targets=re.findall(r'\[Xem đề bài\]\(#(d0-r[1-8]-0[1-3])\)',text)
    assert len(targets)==24 and len(set(targets))==24,'Missing/repeated D0 return links'
    for target in targets:
        marker='\n\n\n\n[Xem đề bài](#'+target+')'
        assert text.count(marker)==1,'Unexpected spacing at D0 removed guidance: '+target
        text=text.replace(marker,'\n\n'+repeated+'\n\n[Xem đề bài](#'+target+')',1)
    return text


def restore_numbering_html(clone):
    """Reverse numbering/removed badges in memory, without weakening prose checks."""
    strands={}
    for r in range(1,9):
        strands[r]=clone.select_one(f'#mach-r{r} > h3').get_text(' ',strip=True).removeprefix(f'R{r} — ')
    for number,owner in enumerate(['cau-minh-hoa',*PAIRS]):
        task=clone.select_one('#'+owner);heading=task.select_one('h4')
        prefix=f'Bài {number:02} — ';title=heading.get_text(' ',strip=True)
        assert title.startswith(prefix),'Wrong D0 question number'
        answer=clone.select_one('#'+('doi-chieu-minh-hoa' if number==0 else PAIRS[owner])+' summary')
        assert answer.get_text(' ',strip=True)==title,'D0 comparison title mismatch'
        heading.string=title.removeprefix(prefix)
        r=(number-1)//3+1;local=(number-1)%3+1
        p=clone.new_tag('p')
        badge=clone.new_tag('span',attrs={'class':'d0-task-number'});badge.string=f'Bài {local:02}' if number else 'Bài 00';p.append(badge);p.append(' ')
        code=clone.new_tag('span',attrs={'class':'d0-task-code'});code.string=f'R{r}' if number else 'Hàm số, đạo hàm, đồ thị';p.append(code)
        task.insert(0,p)
        answer.string=f'{strands[r]} — Bài {local:02}' if number else 'Đối chiếu Bài 00 sau khi tự làm'
    return clone


def restore_editorial_html(clone,root=ROOT):
    """Compare the already-authorized editorial revision with its old receipt.

    Every changed fragment must match its recorded text and TeX before inversion;
    all other words/formulas still pass through the original whole-page check.
    """
    import sys
    sys.path.insert(0,str(Path(root)/PACKAGE/'cong_cu'))
    from tich_hop_html_da_duyet import signature
    data=json.loads((Path(root)/PACKAGE/'_quy_trinh/d0_editorial_comparison_delta.json').read_text(encoding='utf-8'))
    for change in data['html_replacements']:
        nodes=clone.select(change['selector']);assert len(nodes)==1,'Missing/repeated editorial fragment'
        assert signature(nodes[0])==change['after_signature'],'Changed editorial text or mathematics'
        nodes[0].replace_with(BeautifulSoup(change['before_markup'],'html.parser').find())
    for change in data['removed_repeated_guidance']:
        answer=clone.select_one('#'+change['answer']);back=answer.select_one('a[href^="#d0-r"]')
        assert back and not any(n.get_text().startswith('Em có thể đọc lại cách giải') for n in answer.select('p'))
        back.find_parent('p').insert_before(BeautifulSoup(change['before_markup'],'html.parser').p)
    return clone


def source_checks(path,root=ROOT,text=None):
    root=Path(root);text=Path(path).read_text(encoding='utf-8') if text is None else text
    labels=answer_action_labels(root);checks={}
    checks.update(numbering_source_checks(text))
    links=re.findall(r'\[([^\]\n]+)\]\(#([^\s)]+)\)',text)
    for kind,targets in [('forward',set(PAIRS.values())),('return',set(PAIRS))]:
        actions=[(label,target) for label,target in links if target in targets]
        checks[kind+' complete unique action targets']=len(actions)==24 and {target for _,target in actions}==targets
        for label,target in actions: checks[target+' exact '+kind]=label==labels[kind]
    table_lines=[line.strip() for line in text.splitlines() if line.lstrip().startswith('|')]
    cells=[v.strip() for line in table_lines for v in line.strip('|').split('|')]
    checks['no bare numeric table cells']=not any(re.fullmatch(r'[+-]?\d+(?:[.,]\d+)?',c) for c in cells)
    checks['34 numeric cells use LaTeX']=sum(bool(re.fullmatch(r'\$\d+\$',c)) for c in cells)==sum(NUMERIC.values())
    records=json.loads((root/PACKAGE/'du_lieu/bang_bien_thien.json').read_text(encoding='utf-8'))
    checks['sign caption has no plain mathematical identifier']=records[0]['title']=='Bảng dấu đạo hàm'
    from zo_course_cover import load_cover
    try:load_cover(root,'d0',allow_direction_approved=True);checks['owned cover declaration and current asset']=True
    except (ValueError,OSError,KeyError):checks['owned cover declaration and current asset']=False
    return checks


def html_checks(doc,root=ROOT):
    labels=answer_action_labels(root);reader=doc.select_one('.reader-content');checks={}
    from zo_course_tables import media_html_checks
    checks.update(media_html_checks(doc))
    checks['exactly one owned hero cover']=len(doc.select('.hero-art img'))==1
    checks['all seven tables classified']=len(reader.select('table'))==7 and all(t.get('data-table-kind') for t in reader.select('table'))
    tasks=reader.select('.d0-primary-task')
    checks['24 question numbers continuous']=[n.select_one('h4').get_text(' ',strip=True).split(' — ',1)[0] for n in tasks]==[f'Bài {n:02}' for n in range(1,25)]
    checks['no D0 badges or R1 context labels']=not reader.select('.d0-task-number,.d0-task-code,.role,[data-reading-label]')
    example=reader.select_one('#cau-minh-hoa')
    checks['Bai 00 remains in preparation']=bool(example and example.find_parent(id='khai-bao-pham-vi') and example.select_one('h4').get_text(' ',strip=True).startswith('Bài 00 — '))
    for q,a in [('cau-minh-hoa','doi-chieu-minh-hoa'),*PAIRS.items()]:
        heading=reader.select_one('#'+q+' h4');summary=reader.select_one('#'+a+' summary')
        checks[q+' question and comparison titles match']=bool(heading and summary and heading.get_text(' ',strip=True)==summary.get_text(' ',strip=True))
    for q,a in PAIRS.items():
        forward=reader.select('a[href="#'+a+'"]');back=reader.select('#'+a+' a[href="#'+q+'"]')
        checks[q+' exact pair']=len(forward)==1 and forward[0].get_text(' ',strip=True)==labels['forward'] and len(back)==1 and back[0].get_text(' ',strip=True)==labels['return']
    for owner,count in NUMERIC.items():
        table=reader.select_one('#'+owner+' table');valid=[]
        if table:
            for cell in table.select('th,td'):
                math=cell.select('math');annotations=cell.select('annotation[encoding="application/x-tex"]')
                plain=cell.get_text(' ',strip=True)
                if not math and re.fullmatch(r'[+-]?\d+(?:[.,]\d+)?',plain):valid.append(False)
                elif len(math)==1 and len(annotations)==1 and re.fullmatch(r'\d+',annotations[0].get_text()):valid.append(True)
        checks[owner+' all numeric cells are math']=len(valid)==count and all(valid)
    for owner in ['d0-r2-02','d0-r2-03']:
        table=reader.select_one('#'+owner+' table')
        checks[owner+' transposed columns centred']=bool(table) and all('zo-center-cell' in c.get('class',[]) for row in table.select('tbody tr') for c in row.select('td'))
    figure=reader.select_one('figure.zo-variation-asset')
    checks['sign caption below grid']=bool(figure and figure.select_one(':scope > figcaption')) and figure.find_all(recursive=False)[-1].name=='figcaption' and figure.select_one(':scope > figcaption').get_text(' ',strip=True)=='Bảng dấu đạo hàm'
    return checks


def approved_projection(root):
    """Reverse only owner-requested action wording and integer typesetting in memory.

    The immutable approval still checks every original word/value/formula. A changed
    integer becomes changed plain text and therefore fails its original text hash.
    """
    clone=copy.deepcopy(root)
    # A detached Tag has no new_tag factory; retain a soup for bounded inverses.
    clone=BeautifulSoup(str(clone),'html.parser')
    clone=restore_numbering_html(clone)
    clone=restore_editorial_html(clone)
    for q,a in PAIRS.items():
        for link in clone.select('a[href="#'+a+'"]'):link.string='Đối chiếu bài này sau khi tự làm'
        for link in clone.select('#'+a+' a[href="#'+q+'"]'):link.string='Quay lại đề bài'
    for owner,count in NUMERIC.items():
        tables=clone.select('#'+owner+' table');assert len(tables)==1,owner
        converted=0
        for math in list(tables[0].select('math')):
            annotation=math.select_one('annotation[encoding="application/x-tex"]')
            if annotation and re.fullmatch(r'\d+',annotation.get_text()):
                math.replace_with(annotation.get_text());converted+=1
        assert converted==count,(owner,converted)
    return clone.select_one('.d0-package') or clone


def asset_version_checks(doc,root=ROOT):
    paths={'web_2027.css':Path(root)/PACKAGE/'giao_dien/web_2027.css','course-tables.css':Path(root)/'_design/web_2027_mau_dung_chung/course-tables.css'}
    checks={}
    for name,path in paths.items():
        links=[n for n in doc.select('link[rel="stylesheet"][href]') if Path(urlsplit(n['href']).path).name==name]
        expected=hashlib.sha256(path.read_bytes()).hexdigest()[:16]
        checks[name+' version matches canonical bytes']=len(links)==1 and parse_qs(urlsplit(links[0]['href']).query).get('v')==[expected]
    return checks
