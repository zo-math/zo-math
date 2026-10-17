"""Approved course navigation; scoped to the canonical 2027 learner catalog."""
from pathlib import Path
import hashlib
import os
import shutil
from bs4 import BeautifulSoup
import yaml

ROOT = Path(__file__).resolve().parents[1]
KIT = ROOT / '_design/web_2027_mau_dung_chung'
BASE = Path('content/thpt/on_thi_toan_thpt')
PAGES = {
    'home': (BASE / 'tot_nghiep_thpt/2027/index.html', 'Nhà khóa học'),
    'd0': (BASE / 'hoc_lieu/d0/index.html', 'Khảo sát đầu vào'),
    'g01': (BASE / 'hoc_lieu/r1_g01/index.html', 'Đơn điệu và cực trị'),
    'g02': (BASE / 'hoc_lieu/r1_g02/index.html', 'Giá trị lớn nhất và nhỏ nhất'),
    'g03': (BASE / 'hoc_lieu/r1_g03/index.html', 'Đường tiệm cận'),
}
ICONS = {
    'home': '<path d="m3 10 9-7 9 7v10a1 1 0 0 1-1 1h-5v-7H9v7H4a1 1 0 0 1-1-1Z"/>',
    'list': '<path d="M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01"/>',
    'top': '<path d="m6 10 6-6 6 6M12 4v17"/>',
}

def destinations(output_root, page, current=None):
    catalog = yaml.safe_load((ROOT / BASE / 'tot_nghiep_thpt/2027/_data/chuong_trinh.yml').read_text(encoding='utf-8'))
    if [p['id'] for p in catalog['packages']] != ['d0', 'r1_g01', 'r1_g02', 'r1_g03']:
        raise ValueError('Course navigation bindings must be updated for the current catalog')
    result = []
    entries=dict(PAGES)
    if current == "g04":
        entries["g04"]=(BASE / "hoc_lieu/r1_g04/index.html", "Khảo sát sự biến thiên và vẽ đồ thị của hàm số")
    for key, (relative, label) in entries.items():
        if not (ROOT / relative.with_suffix('.qmd')).is_file():
            raise ValueError(f'Missing canonical destination: {relative}')
        href = os.path.relpath(output_root / relative, page.parent).replace('\\', '/')
        if key in ('g01', 'g02', 'g03', 'g04'):
            href += '?r1-view=bat-dau#bat-dau'
        result.append((key, href, label))
    return result

def require(doc, page, output_root, key):
    header = doc.select_one('.site-top--course-navigation')
    if header is None or header.select('.course-link,.lab-link'):
        raise ValueError('Missing approved navigation or legacy toolbar link')
    controls = header.select('.course-tools > .course-action, .course-tools > details > summary')
    if [n.get('data-course-action') for n in controls] != ['home', 'list', 'top']:
        raise ValueError('Course controls must be Home / List / Top')
    if any(not n.get('aria-label') or len(n.select('svg')) != 1 for n in controls):
        raise ValueError('Course controls need accessible names and one icon')
    menu = header.select_one('details.zo-course-menu')
    if menu.has_attr('open') or not doc.select_one('#zo-course-top'):
        raise ValueError('Course menu must start closed and Top must have a target')
    actual = menu.select('nav a')
    expected = destinations(output_root, page, key)
    if [(n.get('data-course-page'), n.get('href'), n.get_text(strip=True)) for n in actual] != expected:
        raise ValueError('Course destinations differ from the approved catalog bindings')
    if [n.get('data-course-page') for n in actual if n.get('aria-current') == 'page'] != [key]:
        raise ValueError('Exactly the current course page must be marked')
    if controls[0].get('href') != expected[0][1] or controls[2].get('href') != '#zo-course-top':
        raise ValueError('Home or Top target is incorrect')
    if len(header.select('.appearance')) != 1 or header.select_one('.course-tools').find_next_sibling() != header.select_one('.appearance'):
        raise ValueError('Course tools must precede the existing appearance controls')

def apply(doc, page, output_root, runtime, key):
    protected = [str(n) for n in doc.select('main,.rail,footer.site-footer')]
    logo = str(doc.select_one('.site-top > a:first-child'))
    header = doc.select_one('.site-top')
    if header is None or header.select_one('.course-tools'):
        raise ValueError('Navigation requires one unadapted toolbar')
    for node in header.select('.course-link,.lab-link'):
        node.decompose()
    header['class'] = list(header.get('class', [])) + ['site-top--course-navigation']
    doc.body['data-zo-course-navigation'] = key
    anchor = doc.new_tag('span', id='zo-course-top', attrs={'aria-hidden': 'true'})
    header.insert_before(anchor)
    tools = doc.new_tag('nav', attrs={'class': 'course-tools', 'aria-label': 'Điều hướng toàn khóa học'})
    dest = destinations(output_root, page, key)
    for action, label, href in [('home', 'Nhà khóa học', dest[0][1]), ('list', 'Danh sách toàn khóa học', None), ('top', 'Về đầu trang', '#zo-course-top')]:
        node = doc.new_tag('summary' if action == 'list' else 'a', attrs={'class': 'course-action', 'aria-label': label, 'title': label, 'data-course-action': action})
        if href is not None:
            node['href'] = href
        svg = BeautifulSoup('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">' + ICONS[action] + '</svg>', 'html.parser').svg
        node.append(svg)
        if action == 'list':
            menu = doc.new_tag('details', attrs={'class': 'zo-course-menu'})
            menu.append(node)
            panel = doc.new_tag('nav', attrs={'class': 'course-panel', 'aria-label': 'Các trang trong khóa học'})
            for destkey, desthref, destlabel in dest:
                link = doc.new_tag('a', href=desthref, attrs={'data-course-page': destkey})
                if destkey == key:
                    link['aria-current'] = 'page'
                link.string = destlabel
                panel.append(link)
            menu.append(panel)
            tools.append(menu)
        else:
            tools.append(node)
    header.select_one('.appearance').insert_before(tools)
    resources = {}
    runtime.mkdir(parents=True, exist_ok=True)
    for name in ['course-navigation.css', 'course-navigation.js']:
        source = KIT / name
        target = runtime / name
        shutil.copyfile(source, target)
        href = os.path.relpath(target, page.parent).replace('\\', '/')
        if name.endswith('.css'):
            doc.head.append(doc.new_tag('link', rel='stylesheet', href=href))
        else:
            doc.body.append(doc.new_tag('script', src=href, defer=''))
        resources[name] = {'source': source.relative_to(ROOT).as_posix(), 'sha256': hashlib.sha256(source.read_bytes()).hexdigest()}
    # Keep font licenses in the referenced public asset closure.
    for license_name in ['OFL_BeVietnamPro.txt', 'OFL_STIX.txt']:
        license_file = runtime / 'assets/fonts' / license_name
        if not license_file.is_file():
            raise ValueError('Missing font license: ' + str(license_file))
        doc.head.append(doc.new_tag('link', rel='license', type='text/plain', href=os.path.relpath(license_file,page.parent).replace('\\','/')))
    require(doc, page, output_root, key)
    if protected != [str(n) for n in doc.select('main,.rail,footer.site-footer')] or logo != str(doc.select_one('.site-top > a:first-child')):
        raise ValueError('Course navigation must not change content, sidebar, footer, or logo')
    return resources
