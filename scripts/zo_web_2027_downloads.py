"""Scoped G01 utility presentation; preserve titles, descriptions, IDs and URLs."""
from pathlib import Path
import copy
import os
import shutil
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path('content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g01')
CSS = PACKAGE / 'giao_dien/downloads.css'

def apply(target, page, output_root):
    section = target.select_one('#tai-tai-lieu')
    cards = section.select('.r1-download-card, .r1-section-download-item')
    if len(cards) != 8:
        raise ValueError('Expected exactly eight real G01 PDF downloads')
    for card in cards:
        link = card.select_one('a[download]')
        title = card.select_one('h3, .r1-section-download-title')
        description = card.select_one('.r1-section-download-description') or card.select_one('p:not(.r1-download-card__meta)')
        if not (link and title and description):
            raise ValueError('Incomplete PDF card; refuse silent content removal')
        filename = link['href']
        if Path(filename).name != filename or not filename.endswith('.pdf'):
            raise ValueError('Unexpected PDF URL: ' + filename)
        pdf = ROOT / PACKAGE / filename
        pages = len(PdfReader(pdf).pages)
        if pages < 1:
            raise ValueError('Empty PDF: ' + filename)
        # Keep original title/description nodes (and their inline semantics).
        title = copy.deepcopy(title)
        title['class'] = title.get('class', []) + ['zo-pdf-title']
        description = copy.deepcopy(description)
        description['class'] = description.get('class', []) + ['zo-pdf-description']
        link = copy.deepcopy(link)
        link['class'] = ['zo-pdf-download__link', 'zo-pdf-download']
        link['aria-label'] = 'Tải PDF: ' + title.get_text(' ', strip=True)
        link.clear()
        icon = target.new_tag('svg', attrs={'viewBox':'0 0 24 24','aria-hidden':'true','focusable':'false'})
        icon.append(target.new_tag('path', attrs={'d':'M12 3v12m-4-4 4 4 4-4M5 16v5h14v-5','fill':'none','stroke':'currentColor','stroke-width':'1.7','stroke-linecap':'round','stroke-linejoin':'round'}))
        link.append(icon)
        link.append('Tải PDF')
        copy_node = target.new_tag('div', attrs={'class':'zo-pdf-copy'})
        copy_node.extend([title, description])
        status=target.new_tag('small',attrs={'class':'zo-pdf-version-note'})
        status.string='Bản PDF chưa đồng bộ với HTML này.'
        copy_node.append(status)
        metric = target.new_tag('div', attrs={'class':'zo-pdf-pages','data-pdf-pages':str(pages)})
        number = target.new_tag('strong'); number.string = str(pages)
        unit = target.new_tag('span'); unit.string = 'trang'
        metric.extend([number, unit])
        card.clear()
        card['class'] = card.get('class', []) + ['zo-pdf-card']
        card.extend([copy_node, metric, link])
    # This copy describes the actual downloads; do not imply current PDF parity.
    intro = section.select_one('p:has(strong)')
    for node in intro.find_all(string=True):
        if 'Số trang dưới đây' in str(node):
            node.replace_with(str(node).replace(
                'Số trang dưới đây được kiểm tra trực tiếp từ tệp PDF hiện hành.',
                'Số trang được đọc từ các tệp PDF đang có; các bản PDF này chưa được đồng bộ với HTML mới.'))
    trigger = target.select_one('.mobile-trigger')
    trigger['aria-label'] = 'Mở mục lục học liệu'
    trigger['title'] = 'Mở mục lục học liệu'
    icon = trigger.select_one('[aria-hidden=true]')
    icon.clear()
    svg = target.new_tag('svg', attrs={'viewBox':'0 0 24 24','aria-hidden':'true','focusable':'false'})
    svg.append(target.new_tag('path', attrs={'d':'M5 6h14M5 12h14M5 18h14','fill':'none','stroke':'currentColor','stroke-width':'1.7','stroke-linecap':'round'}))
    icon.append(svg)
    runtime = output_root / 'assets/zo_web_2027/g01-downloads.css'
    runtime.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(ROOT / CSS, runtime)
    target.head.append(target.new_tag('link', attrs={'rel':'stylesheet','href':os.path.relpath(runtime, page.parent).replace('\\','/')}))
