"""G02 reading adapter, shared by isolated previews and opt-in QMD renders."""
from __future__ import annotations
import copy
import html
import json
from pathlib import Path
import re
import socket
import subprocess
import tempfile
import time
from urllib.parse import unquote, urlsplit
import sys
import xml.etree.ElementTree as ET
sys.dont_write_bytecode = True
from bs4 import BeautifulSoup, Tag
from zo_web_2027_preview import REPO, KIT, BRAND_THOUGHT, PreviewBuilder, audit_path, dump, inventory, projection, relative_href, sha, template

PROFILE = KIT / 'profiles/r1-g02.json'
AUTHORIZED_RECORDS = [
    'content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/_quy_trinh/README.md',
    'content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/_quy_trinh/03_dieu_hanh_chuong_trinh.md',
    'content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/_quy_trinh/goi/R1_G02.md',
]


def inv(root):
    item = inventory(root)
    item['ids'] = [n['id'] for n in root.select('[id]') if not n.has_attr('data-design-added-id')]
    return item


def canonical_math_matches(canonical, rendered):
    # Alt text is not a visible MathML formula; it is checked as image semantics.
    def expand(path):
        text = path.read_text(encoding='utf-8')
        return re.sub(r'\{\{<\s*include\s+([^>]+?)\s*>\}\}',
            lambda m: expand((path.parent/m.group(1).strip()).resolve()), text)
    body = expand(canonical).split('---', 2)[2]
    body = re.sub(r'^!\[.*$', '', body, flags=re.M)
    formulas = [''.join(x.split()) for pair in re.findall(r'\$\$(.*?)\$\$|\$(.*?)\$', body, re.S) for x in pair if x]
    annotations = [''.join(n.get_text().split()) for n in rendered.select('annotation')]
    return formulas == annotations


def build(output, fresh_source=None, *, builder=None):
    production = builder is not None
    output = output.resolve() if production else audit_path(output)
    b = builder or PreviewBuilder(output)
    p = json.loads(PROFILE.read_text(encoding='utf-8'))
    if fresh_source:
        p['figure_label_pt'].update({'nen_do_thi_01.svg': 16.5, 'nen_do_thi_02.svg': 16.5})
        p['absent_source_features']=[]
        p['home']='docs/content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/index.html'
    source = Path(fresh_source).resolve() if fresh_source else REPO / p['source']
    if fresh_source:
        if not production and not source.is_relative_to(REPO/'_audit'):
            raise ValueError('Fresh prototype input must be an isolated audit render')
        p['source'] = source.relative_to(REPO).as_posix()
    original = BeautifulSoup(source.read_text(encoding='utf-8'), 'html.parser')
    root = copy.deepcopy(original.select_one('.zo-on-thi-package'))
    baseline = inv(root)
    if not canonical_math_matches(REPO / p['canonical'], root):
        raise ValueError('Current canonical QMD/include formula sequence differs from the supplied fresh G02 render.')
    protected = output / 'protected-before.json'
    if not production and not protected.exists():
        paths = [REPO / '_quarto.yml']
        for directory in ['assets', 'content/thpt/on_thi_toan_thpt', 'docs/content/thpt/on_thi_toan_thpt',
                          '_audit/zo_web_2027_tuy_chinh_2026-10-08',
                          '_audit/zo_design_web_2027_discovery_2026-10-07',
                          '_design/ngon_ngu_thiet_ke_zo_math_0_4/06_nguon',
                          '_design/ngon_ngu_thiet_ke_zo_math_0_4/07_mau_thi_giac']:
            paths += [n for n in (REPO / directory).rglob('*') if n.is_file() and '__pycache__' not in n.parts]
        paths += [KIT / n for n in ['reading-regions.css','web-shell.css','r1-controller.js','site-ui.js','appearance-inline.css','templates/page.html.tpl']]
        dump(protected, {n.relative_to(REPO).as_posix(): sha(n) for n in paths})
    b.ui_baseline = REPO / p['home']
    b.common_assets()
    b.materialize(KIT / 'r1-g02-adapter.css', 'r1-g02-adapter.css')
    b.materialize(KIT / 'site-footer.css', 'site-footer.css')
    external_routes=[]
    if fresh_source and not production:
        raw_root=source.parents[5]
        for link in root.select('a[href]'):
            value=link['href'];split=urlsplit(value)
            if split.scheme or split.netloc or not split.path or split.path.startswith('/'):
                continue
            resolved=(source.parent/unquote(split.path)).resolve()
            if not resolved.is_file() and resolved.is_relative_to(raw_root):
                destination=REPO/'docs'/resolved.relative_to(raw_root)
                if not destination.is_file(): raise ValueError('Missing existing site route: '+value)
                external_routes.append((link,value))
                link['href']='/'+destination.relative_to(REPO/'docs').as_posix()+('?' + split.query if split.query else '')+('#'+split.fragment if split.fragment else '')
    b.normalize_links(root, source)
    for link,value in external_routes:
        link['data-canonical-href']=value
    root['class'] += ['reader-content']
    doc = BeautifulSoup('', 'html.parser')
    beats = []

    def region(parent, nodes, label, reason):
        nodes = [n for n in nodes if isinstance(n, Tag)]
        if not nodes:
            return
        paper = doc.new_tag('div', attrs={'class': 'reading-region', 'data-reading-beat': str(len(beats)+1), 'data-reading-reason': reason})
        nodes[0].insert_before(paper)
        paper.append(b.label(doc, label))
        ids = [n.get('id') for n in nodes if n.get('id')]
        for n in nodes:
            paper.append(n.extract())
        beats.append({'label': label, 'source_ids': ids, 'reason': reason, 'text_start': projection(paper)[:100]})
        return paper

    lesson = root.find(id='bai-hoc')
    semantic_plan = None
    if fresh_source:
        semantic_plan = json.loads((REPO/p['canonical']).parent.joinpath('giao_dien/web_2027_layout.json').read_text(encoding='utf-8'))
        p['semantic_layout'] = semantic_plan
        # A supplemental confirmation belongs to its explicit foundation owner,
        # not to a peer paper. Keep source order and every atomic target intact.
        for extra_id,owner_id in semantic_plan.get('foundation_owners',{}).items():
            extra=root.find(id=extra_id);owner=root.find(id=owner_id)
            if extra is None:raise ValueError('Missing supplemental foundation confirmation '+extra_id)
            if owner is None or 'r1-foundation-unit' not in owner.get('class',[]):
                raise ValueError('Unknown foundation owner: '+owner_id)
            extra['data-zo-owner']=owner_id
            owner.append(extra.extract())

    def semantic_wrap(section, fallback):
        ident = section.get('id','')
        spec = semantic_plan['sections'].get(ident, {})
        label = spec.get('label', fallback)
        reason = spec.get('reason', 'Một nhiệm vụ trọn vẹn giữ dữ kiện, tiêu đề, hình và đích; ngắt theo chức năng, không đếm heading.')
        if spec.get('unit'):
            region(section, list(section.find_all(recursive=False)), label, reason)
            return
        # Opening guidance is one reading result, not one paper per h4.
        # Explicit groups keep the same three Cách học beats as current G01.
        if spec.get('opening_groups'):
            groups = spec['opening_groups']
            opening = []
            grouped_ids = {anchor for group in groups for anchor in group}
            for node in list(section.find_all(recursive=False)):
                if node.name != 'section' or node.get('id') in grouped_ids:
                    opening.append(node)
                else:
                    break
            expected = [anchor for group in groups for anchor in group]
            if [n.get('id') for n in opening if n.name == 'section'] != expected:
                raise ValueError('G02 opening beat binding drift: '+ident)
            region(section, opening, label, reason)
            for child in list(section.find_all('section',recursive=False)):
                semantic_wrap(child,label)
            return
        current = []
        def flush():
            nonlocal current
            if current:
                region(section,current,label,reason)
                current=[]
        for node in list(section.find_all(recursive=False)):
            if node.name == 'section':
                flush()
                child_id=node.get('id','')
                child_label = ('Điểm dừng' if child_id.startswith('cp-') else
                    'Nhiệm vụ' if 'zo-learning-task--item' in node.get('class',[]) else
                    'Chặng học' if child_id.startswith('g02-c') else
                    'Bài học' if section is root.find(id='bai-hoc') else label)
                semantic_wrap(node,child_label)
            elif node.name=='div' and node.get('id') in semantic_plan['sections']:
                flush()
                semantic_wrap(node,label)
            elif node.name=='details' and ('zo-learning-guidance' in node.get('class',[]) or 'r1-guidance' in node.get('class',[])):
                # Orientation/usage belongs with its section opening, like G01.
                current.append(node)
            elif node.name=='details':
                # Foundation unit + inner explanation/confirmation is one resource.
                if current and not any(n.name in ['p','table','ol','ul','div'] for n in current):
                    current.append(node);flush()
                else:
                    flush()
                    region(section,[node], 'Ôn nền' if any(c in node.get('class',[]) for c in ['r1-foundation-unit','r1-foundation-confirmation']) else 'Lời giải',
                        'Một tài nguyên nền hoặc lời giải đầy đủ, có đường quay về đúng hoạt động.')
            elif node.name=='div' and 'zo-learning-task' in node.get('class',[]):
                flush()
                role='Tự kiểm tra' if 'zo-learning-task--pause' in node.get('class',[]) else 'Nhiệm vụ'
                region(section,[node],role,'Tự làm trước khi đối chiếu; đề, dữ kiện và link cùng một vùng.')
            else:
                current.append(node)
        flush()

    if fresh_source:
        # Every lesson and utility now uses the canonical semantic map, not
        # the historical prototype heading-number grouping.
        semantic_wrap(root.find(id='bai-hoc'),'Mạch học chính')
    else:
        # Existing unsectioned lead remains unsectioned: no invented start view/ID.
        lead = []
        for n in root.find_all(recursive=False):
            if n.name == 'section':
                break
            lead.append(n)
        lead_region = region(root, lead, 'Bắt đầu', 'Giới thiệu hiện có thuộc điểm vào Cách học; Toàn văn vẫn đọc đủ, không đổi ID/thứ tự nguồn.')
        if lead_region:
            lead_region['class'].append('g02-start-region')
        lesson = root.find(id='bai-hoc')
        region(lesson, [n for n in lesson.find_all(recursive=False) if n.name != 'section'], 'Bài học', 'Tiêu đề và mục lục cùng thuộc định hướng bài học.')
        for ident, spec in p['lesson_beats'].items():
            section = root.find(id=ident)
            children = section.find_all(recursive=False)
            leading = [n for n in children if n.name != 'section']
            # For kickoff, orientation + objectives complete the opening beat.
            groups = copy.deepcopy(spec['groups'])
            if ident == 'bắt-đầu-từ-đâu':
                leading += [section.find(id=n, recursive=False) for n in groups.pop(0)]
            opening_role = {'doi-tuong':'Khái niệm', 'dinh-nghia':'Định nghĩa',
                            'tren-doan':'Định lí', 'tap-khac':'Giới hạn suy luận',
                            'loi-van':'Mô hình và ràng buộc', 'khép-lại-bài-học':'Tổng kết'}
            region(section, leading, opening_role.get(ident, spec['label']), spec['reason'])
            covered = []
            for group in groups:
                nodes = [section.find(id=n, recursive=False) for n in group]
                if any(n is None for n in nodes):
                    raise ValueError('G02 map drift: ' + repr(group))
                # A chapter title is not a reusable functional role. Preserve its
                # source heading, but label the reading beat by its actual work.
                group_roles = {
                    'bắt-đầu-từ-đâu': ['Nhiệm vụ', 'Tự đối chiếu'],
                    'doi-tuong': ['Ví dụ'],
                    'dinh-nghia': ['Ví dụ · Cận và sự đạt được', 'Đối chứng'],
                    'tren-doan': ['Phương pháp và ví dụ'],
                    'tap-khac': ['Đối chứng · Tập đang xét', 'Tổng hợp cách xét'],
                }
                region(section, nodes, group_roles[ident][groups.index(group)] if ident in group_roles else spec['label'], spec['reason'])
                covered += group
            if section.select(':scope > section'):
                raise ValueError('Unmapped G02 lesson section: ' + ident)

    support = root.select_one('.r1-download-support')
    foot = root.select_one('#tai-tai-lieu > .r1-footer')
    support.extract(); foot.extract()
    support['class'] = ['support-region', 'reading-region']
    support['id'] = 'ung-ho'; support['data-design-added-id'] = ''
    old_accent = support.select_one('.r1-brand-mark')
    old_accent.extract()
    mark = doc.new_tag('div', attrs={'class':'support-brand'})
    mark.append(doc.new_tag('img', attrs={'src':'assets/logos/stack_color.svg','alt':'ZO Math'}))
    body = doc.new_tag('div', attrs={'class':'support-content'})
    for child in list(support.contents):
        body.append(child.extract())
    body.append(foot)
    support.append(mark); support.append(body)
    # Empty decorative accent has no text/math/ID; keep old asset immutable, not in UI.
    root.append(support)

    roles = {'bat-dau':'Bắt đầu', 'cách-học-với-tài-liệu-này':'Cách học', 'phieu-luyen':'Luyện tập', 'tu-kiem-tra':'Kiểm tra',
               'on-nen':'Ôn nền', 'sua-loi':'Sửa lỗi', 'on-lai':'Ôn lại', 'nhat-ky':'Nhật kí', 'loi-giai':'Lời giải', 'nguon':'Nguồn đối chiếu', 'tai-tai-lieu':'Tải tài liệu'}
    def wrap_section(section, label):
        children = section.find_all(recursive=False)
        chunks, current = [], []
        for n in children:
            if n.name in ['section','details'] or (n.name=='div' and 'zo-learning-task' in n.get('class', [])):
                if current:
                    chunks.append(current); current = []
                chunks.append([n])
            else:
                current.append(n)
        if current:
            chunks.append(current)
        for chunk in chunks:
            node = chunk[0]
            if len(chunk)==1 and node.name=='section':
                ident=node.get('id','')
                if ident.startswith('cp-'): role='Điểm dừng'
                elif ident.startswith('g02-c'): role='Chặng học'
                elif ident.startswith('o0'): role='Ôn lại · Nhiệm vụ'
                elif ident=='nhat-ky': role='Nhật kí học tập'
                elif ident=='cách-học-với-tài-liệu-này': role='Cách học'
                else: role=label
                wrap_section(node,role)
            elif len(chunk)==1 and node.name=='details':
                region(section,chunk,'Ôn nền' if 'r1-foundation-unit' in node.get('class',[]) else label,
                    'Một thẻ nền hoặc đối chiếu hoàn chỉnh, cùng ví dụ, tự kiểm tra và điểm quay về.')
            else:
                role='Nhiệm vụ' if 'zo-learning-task' in node.get('class',[]) else label
                region(section,chunk,role,'Một kết quả đọc hoặc thao tác trọn vẹn; nhãn, tiêu đề, dữ kiện và hành động cùng một vùng.')

    foundation=root.find(id='on-nen')
    if foundation and not fresh_source: wrap_section(foundation,'Ôn nền')
    for section in root.select(':scope > section.level2'):
        if section is lesson:
            continue
        label = roles[section['id']]
        if fresh_source:
            semantic_wrap(section,label)
            continue
        children = section.find_all(recursive=False)
        chunks, current = [], []
        for n in children:
            if n.name == 'section' or 'zo-learning-task' in n.get('class', []):
                if current:
                    chunks.append(current); current = []
                chunks.append([n])
            else:
                current.append(n)
        if current:
            chunks.append(current)
        for chunk in chunks:
            node = chunk[0]
            if len(chunk) == 1 and node.name == 'section' and node.select(':scope > details.r1-solution'):
                details = node.select(':scope > details.r1-solution')
                intro = [c for c in node.find_all(recursive=False) if c is not details[0] and c not in details]
                region(node, intro + [details[0]], 'Lời giải', 'Nhóm đối chiếu mở đầu cùng lời giải đầu; mỗi lời giải sau là một nhịp đối chiếu riêng.')
                for d in details[1:]:
                    region(node, [d], 'Lời giải', 'Một lời giải cùng liên kết trở về đề, không tách câu trả lời khỏi nguồn đối chiếu.')
            else:
                region(section, chunk, label if node.name != 'div' or 'zo-learning-task' not in node.get('class',[]) else 'Nhiệm vụ',
                       'Một công việc hoàn chỉnh với dữ kiện, hình/bảng, chỉ dẫn và liên kết liên quan; giữ đúng thứ tự nguồn.')

    # A heading-only paper is not a reading beat. Attach it to the next task
    # without moving any source ID, heading, formula or disclosure out of order.
    for paper in list(root.select('.reading-region')):
        if paper is support:
            continue
        payload = [n for n in paper.find_all(recursive=False) if not n.has_attr('data-reading-label')]
        meaningful = paper.select('li,table,figure,details,.zo-learning-task') or any(
            p.get_text(' ',strip=True) for p in paper.select('p'))
        if payload and not meaningful:
            following = paper.find_next(class_='reading-region')
            owner=next((p for p in paper.parents if p.name=='section' and p.parent is root),None)
            if following and owner and following in owner.descendants:
                label_node = following.select_one(':scope > [data-reading-label]')
                for n in reversed(payload):
                    if label_node:label_node.insert_after(n.extract())
                    else:following.insert(0,n.extract())
                paper.decompose()
    # Keep source words, but expose the same semantic title/pause markers as G01.
    for n in root.select('.r1-unboxed-label'):
        n['class'] = n.get('class', []) + ['r1-task-label']
    for n in root.select('.zo-learning-task--pause'):
        if not n.find_parent(class_='reading-region') and not n.select_one(':scope > [data-reading-label]'):
            n.insert(0, b.label(doc, 'Tự kiểm tra'))
    beats = [{'label': n.select_one('[data-reading-label]').get_text(' ', strip=True),
              'source_ids': [x['id'] for x in n.select('[id]')],
              'reason': n.get('data-reading-reason', 'Header rỗng ghép với nhiệm vụ kế tiếp; không đổi thứ tự nguồn.'),
              'text_start': projection(n)[:100]} for n in root.select('.reading-region') if n is not support]

    figures = []
    for img in root.select('figure img'):
        filename = Path(img['src']).name.split('_', 1)[-1]
        if filename not in p['figure_label_pt']:
            raise ValueError('No G02 figure scale contract: ' + filename)
        vector = ET.parse(output / img['src']).getroot()
        width = float(vector.attrib['viewBox'].split()[2])
        label_pt = p['figure_label_pt'][filename]
        em = width / label_pt
        img['class'] = img.get('class', []) + ['math-illustration']
        img['style'] = f'--figure-em:{em:.5f}em'
        img['data-label-pt'] = str(label_pt)
        img['data-vector-width'] = str(width)
        wrap = doc.new_tag('div', attrs={'class':'figure-viewport','tabindex':'0','role':'region','aria-label':img.get('alt','Hình toán học') + ' — có thể cuộn ngang'})
        img.wrap(wrap)
        figures.append({'asset':filename,'viewbox_width':width,'label_pt':label_pt,'width_em':em})
    after = inv(root)
    if after != baseline:
        dump(output / 'preservation-failure.json', {'before':baseline,'after':after})
        raise ValueError('G02 exact inventory changed')
    home = b.href(b.output_root / 'content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/index.html') if production else relative_href(REPO / p['home'], output)
    title = root['data-r1-title']
    subtitle = original.select_one('.subtitle').get_text(' ', strip=True)
    hero = f'<section class="hero" aria-label="Bìa học liệu"><div class="hero-copy"><span class="eyebrow">Ôn thi Toán THPT 2027 · Hàm số</span><h1>{html.escape(title)}</h1><p>{html.escape(subtitle)}</p><a class="hero-action" href="?r1-view=bai-hoc#bai-hoc">Vào Bài học <span aria-hidden="true">↗</span></a></div><figure class="hero-art"><img src="assets/cover-graph.svg" alt="Minh họa hàm số; không phải dữ kiện bài tập"><figcaption>Minh họa nhận diện · Không phải dữ kiện của nhiệm vụ</figcaption></figure></section>'
    footer, footer_info = b.site_footer()
    page = template('page.html', title=html.escape(title), body_class='g02-preview', home_href=home,
                    appearance=b.appearance(), brand_thought=html.escape(BRAND_THOUGHT), navigation='<div id="nav-mount"></div>',
                    breadcrumb=html.escape(title), hero=hero,
                    content=str(root), support='', site_footer=footer, drawer_title='Các phần của học liệu',
                    styles='\n'.join(f'<link rel="stylesheet" href="{n}">' for n in ['reading-regions.css','web-shell.css','site-footer.css','appearance-inline.css','r1-g02-adapter.css']),
                    scripts='<script src="r1-controller.js"></script><script src="site-ui.js"></script>')
    normalized = BeautifulSoup(page, 'html.parser')
    from zo_web_2027_consistency import apply as apply_consistency
    apply_consistency(normalized, output/'g02-reading.html', output)
    if production:
        return normalized
    (output / 'g02-reading.html').write_text(str(normalized), encoding='utf-8')
    report = {'profile':p, 'source_sha256':sha(source), 'canonical_sha256':sha(REPO / p['canonical']),
              'source_inventory':baseline, 'preview_inventory':after, 'reading_beats':beats,'figures':figures,
              'resources':b.resources,'links':b.links,'footer':footer_info,
              'output_sha256':sha(output / 'g02-reading.html'), 'adapter_sha256':sha(Path(__file__)),
              'kit_hashes':{n.relative_to(REPO).as_posix():sha(n) for n in KIT.rglob('*') if n.is_file()},
              'preserved_inventory':True}
    dump(output / 'g02-manifest.json', report)
    return {'html':str(output / 'g02-reading.html'),'regions':len(beats)+1,'preserved':True}


def check_preview(output):
    from zo_web_2027_check import Browser, Checks, GEOMETRY, edge_executable
    import requests
    output = audit_path(output)
    (output / 'images').mkdir(exist_ok=True)
    manifest = json.loads((output / 'g02-manifest.json').read_text(encoding='utf-8'))
    previous = output / 'qa-results.json'
    if previous.exists() and not (output / 'qa-first-run.json').exists():
        dump(output / 'qa-first-run.json', json.loads(previous.read_text(encoding='utf-8')))
    c = Checks(output)
    # G01 checks prose separately from its accepted two-column Support component.
    # G02 retains Support in source projection/ID order; apply the same scope.
    prose_geometry = GEOMETRY.replace('visible=n=>', "visible=n=>!n.closest('.support-region')&&")
    page = BeautifulSoup((output / 'g02-reading.html').read_text(encoding='utf-8'),'html.parser')
    source = BeautifulSoup((REPO / manifest['profile']['source']).read_text(encoding='utf-8'),'html.parser')
    c.check('Current G02 rendered source unchanged',sha(REPO / manifest['profile']['source']),manifest['source_sha256'])
    c.check('Current G02 canonical source unchanged',sha(REPO / manifest['profile']['canonical']),manifest['canonical_sha256'])
    c.check('Exact G02 content math ID heading disclosure order',inv(page.select_one('.reader-content')),inv(source.select_one('.zo-on-thi-package')))
    c.check('Current QMD all visible TeX formulas equal rendered sequence',canonical_math_matches(REPO / manifest['profile']['canonical'],page.select_one('.reader-content')))
    c.check('All source image alt/caption semantics preserved',[(n.get('alt'),n.find_parent('figure').select_one('figcaption').get_text(' ',strip=True)) for n in page.select('.reader-content figure img')],[(n.get('alt'),n.find_parent('figure').select_one('figcaption').get_text(' ',strip=True)) for n in source.select('.zo-on-thi-package figure img')])
    c.check('Current preview matches manifest',sha(output / 'g02-reading.html'),manifest['output_sha256'])
    c.check('Current adapter matches manifest',sha(Path(__file__)),manifest['adapter_sha256'])
    c.check('Current kit matches manifest',[n for n,h in manifest['kit_hashes'].items() if sha(REPO / n)!=h],[])
    c.check('All copied resources match', [n for n,r in manifest['resources'].items() if sha(output/n)!=r['sha256']],[])
    ids = [n['id'] for n in page.select('[id]')]
    c.check('No duplicate IDs',len(ids),len(set(ids)))
    c.check('No nested paper',len(page.select('.reading-region .reading-region')),0)
    c.check('Brand accepted full sentence',page.select_one('.brand-thought').get_text(' ',strip=True),BRAND_THOUGHT)
    c.check('Six radio circles and grayscale retained',len(page.select('.appearance input[type=radio]'))==6 and bool(page.select_one('#grayscale[aria-pressed]')))
    missing=[]
    for n in page.select('[src],a[href],link[href]'):
        value=n.get('src',n.get('href','')); split=urlsplit(value)
        if split.scheme or split.netloc: continue
        path=(output/unquote(split.path)).resolve() if split.path else output/'g02-reading.html'
        if not path.is_file(): missing.append(value); continue
        if split.fragment and path.suffix=='.html':
            target=page if path==output/'g02-reading.html' else BeautifulSoup(path.read_text(encoding='utf-8'),'html.parser')
            if not target.find(id=unquote(split.fragment)): missing.append(value)
    c.check('All local links assets fragments resolve',missing,[])
    before_links=[(n.get('href'),n.get('download')) for n in source.select('.zo-on-thi-package a')]
    after_links=[(n.get('data-canonical-href',n.get('href')),n.get('download')) for n in page.select('.reader-content a')]
    c.check('Every learner route and download attribute unchanged',after_links,before_links)
    # Negative fixtures must be rejected, not merely count checks on a good build.
    damaged=copy.deepcopy(page.select_one('.reader-content')); damaged.select_one('math').decompose()
    c.check('Negative guard rejects removed math',inv(damaged)!=manifest['source_inventory'])
    damaged=copy.deepcopy(page.select_one('.reader-content')); damaged.select_one('[id]').attrs['id']='regression-bad-id'
    c.check('Negative guard rejects changed ID',inv(damaged)!=manifest['source_inventory'])
    with socket.socket() as s: s.bind(('127.0.0.1',0)); port=s.getsockname()[1]
    base=f'http://127.0.0.1:{port}'
    url=(output/'g02-reading.html').as_uri()
    traces=[]
    with tempfile.TemporaryDirectory(prefix='_tmp_browser_',dir=output) as profile:
        process=subprocess.Popen([edge_executable(),'--headless=new','--disable-gpu','--no-first-run','--no-default-browser-check',
                                  '--remote-debugging-address=127.0.0.1',f'--remote-debugging-port={port}',
                                  '--remote-allow-origins=http://localhost','--user-data-dir='+profile,'about:blank'],
                                 stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
        browser=None
        try:
            for _ in range(100):
                try:
                    if requests.get(base+'/json/version',timeout=.3).ok: break
                except requests.RequestException: time.sleep(.1)
            target=requests.put(base+'/json/new?about:blank',timeout=10).json()
            browser=Browser(target['webSocketDebuggerUrl']); browser.call('Page.enable'); browser.call('Runtime.enable')
            browser.call('Page.addScriptToEvaluateOnNewDocument',{'source':"window.zoQaErrors=[];addEventListener('error',e=>zoQaErrors.push(e.message));console.error=(...a)=>zoQaErrors.push(a.map(String).join(' '));"})
            for width in [1440,390,768,1000,1920,320,360,375]:
                print('G02 viewport',width,flush=True)
                browser.viewport(width,960 if width>500 else 844); browser.navigate(url)
                tabs=browser.evaluate('[...document.querySelectorAll(".r1-tab")].map(n=>n.id)')
                c.check(f'{width} controller initialized',bool(tabs))
                c.check(f'{width} main order',browser.evaluate('[...document.querySelectorAll(".r1-tab-group--main button")].map(n=>n.id)'),['r1-tab-cach-hoc','r1-tab-bai-hoc','r1-tab-luyen-tap','r1-tab-kiem-tra','r1-tab-on-lai'])
                c.check(f'{width} no invented support tabs',not any(n in tabs for n in ['r1-tab-on-nen','r1-tab-nhat-ky']))
                for tab in tabs:
                    browser.click('#'+tab)
                    state=browser.evaluate(prose_geometry)
                    for k in ['orphan','overflow','axes']: c.check(f'{width}/{tab} {k}',state[k],[])
                    for k in ['fits','white','widths','gaps','loaded']: c.check(f'{width}/{tab} {k}',state[k])
                    c.check(f'{width}/{tab} single paper level',state['nested'],0)
                    c.check(f'{width}/{tab} bounded column',state['readerWidth']<=816)
                    c.check(f'{width}/{tab} active tab',browser.evaluate('document.querySelector(".r1-tab[aria-selected=true]").id'),tab)
                    if width in [1440,390]:
                        browser.screenshot(output/'images'/f'{tab}-{width}.png')
                browser.navigate(url); browser.click('[name=background][value=yellow-1]'); browser.evaluate('scrollTo(0,0)')
                if width in [1440,390]: browser.screenshot(output/'images'/f'g02-cover-{width}.png')
                for theme in ['gray-3','gray-2','yellow-1','yellow-2','red-1','red-2']:
                    browser.click(f'[name=background][value={theme}]')
                    c.check(f'{width}/{theme} selected and white paper',browser.evaluate(f'document.querySelector("[name=background][value={theme}]").checked') and browser.evaluate(GEOMETRY)['white'])
                browser.click('#grayscale'); c.check(f'{width} grayscale',browser.evaluate('document.documentElement.classList.contains("grayscale")&&document.getElementById("grayscale").getAttribute("aria-pressed")==="true"'))
                browser.call('Page.reload'); browser.ready(); c.check(f'{width} saved settings',browser.evaluate('document.querySelector("[value=red-2]").checked&&document.documentElement.classList.contains("grayscale")'))
                browser.click('#grayscale'); browser.click('[value=yellow-1]')
                c.check(f'{width} controls one row',browser.evaluate('new Set([...document.querySelectorAll(".swatches label,.gray-toggle")].map(n=>n.getBoundingClientRect().top)).size===1'))
                c.check(f'{width} toolbar controls fit',browser.evaluate('[...document.querySelectorAll(".swatches label,.gray-toggle")].every(n=>{const r=n.getBoundingClientRect();return r.x>=0&&r.right<=innerWidth&&r.height>=44})'))
                c.check(f'{width} Support own accepted text axis',browser.evaluate('(()=>{const s=document.querySelector(".support-region"),body=s.querySelector(".support-content"),title=body.querySelector("h3");return Math.abs(title.getBoundingClientRect().left-body.getBoundingClientRect().left)<1&&getComputedStyle(s).backgroundColor==="rgb(255, 255, 255)"&&Math.abs(s.getBoundingClientRect().width-document.querySelector(".reader-content").getBoundingClientRect().width)<2})()'))
                if width in [1440,390]:
                    for ident in ['doi-tuong','dinh-nghia','tren-doan','l06','kt03','loi-giai-l06','ung-ho']:
                        browser.navigate(url+'#'+ident); c.check(f'{width} deep target {ident}',browser.evaluate(f'document.getElementById({json.dumps(ident)}).getClientRects().length>0&&document.getElementById({json.dumps(ident)}).getBoundingClientRect().top>=63'))
                        if ident in ['l06','kt03','loi-giai-l06']:
                            c.check(f'{width} deep target role visible {ident}',browser.evaluate(f'document.getElementById({json.dumps(ident)}).closest(".reading-region").querySelector(".role").getBoundingClientRect().top>=64'))
                        browser.screenshot(output/'images'/f'g02-{ident}-{width}.png')
                    browser.navigate(url+'?r1-view=toan-van#bai-hoc')
                    browser.evaluate('document.querySelectorAll(".reader-content details").forEach(n=>n.open=true)')
                    state=browser.evaluate(prose_geometry)
                    for k in ['orphan','overflow','axes']: c.check(f'{width}/all-disclosures-open {k}',state[k],[])
                    c.check(f'{width}/all-disclosures-open page fits',state['fits'])
                    browser.evaluate('document.querySelector(".reader-content .role").style.transform="translateX(8px)"')
                    c.check(f'{width} negative guard rejects inset label',bool(browser.evaluate(prose_geometry)['axes']))
                    browser.evaluate('document.querySelector(".reader-content .role").style.transform=""')
                    sizes=browser.evaluate('[...document.querySelectorAll("img.math-illustration")].map(n=>({width:n.getBoundingClientRect().width,font:parseFloat(getComputedStyle(n).fontSize),em:parseFloat(n.style.getPropertyValue("--figure-em")),view:Number(n.dataset.vectorWidth),pt:Number(n.dataset.labelPt),scroll:n.closest(".figure-viewport").scrollWidth>=n.closest(".figure-viewport").clientWidth}))')
                    for i,n in enumerate(sizes):
                        c.check(f'{width}/figure{i} normal label scale',abs(n['width']/n['view']*n['pt']-n['font'])<.1)
                        c.check(f'{width}/figure{i} local scroll',n['scroll'])
                    positions=[]
                    for y in [250,450,850,1250,850,450]:
                        browser.evaluate(f'scrollTo(0,{y})'); time.sleep(.08)
                        positions.append(browser.evaluate('({y:scrollY,top:document.querySelector(".site-top").getBoundingClientRect().top,nav:document.querySelector(innerWidth>=1000?".rail":".mobile-trigger").getBoundingClientRect().top})'))
                    c.check(f'{width} no scroll jumps',[n['y'] for n in positions],[250,450,850,1250,850,450])
                    c.check(f'{width} stable toolbar',len({n['top'] for n in positions}),1)
                    c.check(f'{width} stable navigation',len({n['nav'] for n in positions}),1)
                    browser.navigate(url+'#l01'); browser.click('#l01 .answer-link a'); c.check(f'{width} answer route',browser.evaluate('decodeURIComponent(location.hash)'), '#loi-giai-l01')
                    browser.click('#loi-giai-l01 .answer-link a'); c.check(f'{width} back to task',browser.evaluate('decodeURIComponent(location.hash)'), '#l01')
                    browser.evaluate('history.back()'); time.sleep(.2); c.check(f'{width} history restores solution',browser.evaluate('decodeURIComponent(location.hash)'), '#loi-giai-l01')
                    browser.navigate(url); browser.evaluate('document.querySelector("[value=gray-3]").focus()'); browser.key('ArrowRight',39)
                    c.check(f'{width} native circle keyboard selection',browser.evaluate('document.querySelector("[value=gray-2]").checked'))
                    browser.evaluate('document.getElementById("grayscale").focus()'); browser.key('Enter',13,'\r')
                    c.check(f'{width} grayscale keyboard state',browser.evaluate('document.getElementById("grayscale").getAttribute("aria-pressed")==="true"'))
                    browser.click('#grayscale'); browser.click('[value=yellow-1]')
                if width<1000:
                    browser.click('.mobile-trigger'); c.check(f'{width} drawer opens',browser.evaluate('document.getElementById("mobile-nav").open'))
                    if width==390: browser.screenshot(output/'images'/'g02-drawer-390.png')
                    browser.key('Escape',27); c.check(f'{width} drawer Escape focus',browser.evaluate('!document.getElementById("mobile-nav").open&&document.activeElement.matches(".mobile-trigger")'))
                    browser.click('.mobile-trigger'); browser.click('#r1-tab-on-lai'); c.check(f'{width} drawer navigation closes',browser.evaluate('!document.getElementById("mobile-nav").open&&document.getElementById("r1-tab-on-lai").getAttribute("aria-selected")==="true"'))
                c.errors += browser.evaluate('window.zoQaErrors||[]')
            browser.call('Emulation.setScriptExecutionDisabled',{'value':True}); browser.navigate(url)
            c.check('No JS all source sections available',browser.evaluate('[...document.querySelectorAll(".reader-content>section.level2")].every(n=>n.getClientRects().length>0)'))
            browser.call('Emulation.setScriptExecutionDisabled',{'value':False})
        finally:
            if browser:
                try: browser.call('Browser.close')
                except Exception: pass
                browser.ws.close()
            try: process.wait(timeout=10)
            except subprocess.TimeoutExpired: process.terminate(); process.wait(timeout=10)
    protected=json.loads((output/'protected-before.json').read_text(encoding='utf-8'))
    changed=[n for n,h in protected.items() if not (REPO/n).is_file() or sha(REPO/n)!=h]
    c.check('All production assets and accepted references unchanged',[n for n in changed if n not in AUTHORIZED_RECORDS],[])
    c.check('No observed JS errors',c.errors,[])
    report={'checks':c.checks,'checker_sha256':sha(Path(__file__)),'scope':'G02 prototype Edge file://; not production or new mathematical audit',
            'limits':['No Safari/Firefox, real touch or screen reader','G02 has no separate source foundation/journal/checkpoint sections; none invented','Owner visual acceptance pending'],
            'temporary_browser_profile_removed':not Path(profile).exists(),'protected_files':len(protected)}
    report['authorized_internal_record_updates']=[{'path':n,'before_sha256':protected[n],'after_sha256':sha(REPO/n)} for n in changed if n in AUTHORIZED_RECORDS]
    dump(output/'qa-results.json',report)
    failed=[n for n in c.checks if not n['pass']]
    print(json.dumps({'checks':len(c.checks),'passed':len(c.checks)-len(failed),'failures':[n['name'] for n in failed]},ensure_ascii=False))
    return int(bool(failed))
