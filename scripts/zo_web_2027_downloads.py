"""Scoped G01 utility presentation; preserve titles, descriptions, IDs and URLs."""
from pathlib import Path
import copy
import os
import shutil
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path('content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g01')
CSS = PACKAGE / 'giao_dien/downloads.css'

def project_source_section(section, layout_attrs):
    """Use fresh download content and retain its approved reading presentation."""
    if section is None:
        raise ValueError('Missing current source download section')
    projected = copy.deepcopy(section)
    projected['class'] = list(dict.fromkeys(
        projected.get('class', []) + layout_attrs.get('class', [])))
    return projected


def download_region_coverage(section):
    """Every PDF card must sit inside an approved white reading region."""
    if section is None:
        return False
    cards = section.select('.zo-pdf-card')
    return bool(cards) and all(any('reading-region' in node.get('class', [])
        for node in [card, *card.parents] if getattr(node, 'attrs', None)) for card in cards)


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


def metadata_section(doc, *, create_missing=False):
    """A metadata-owned utility region; it adds no mathematical content."""
    section=doc.select_one("#tai-tai-lieu .reading-region")
    if section is not None:return section
    if not create_missing or doc.select_one("#tai-tai-lieu") is not None:
        raise ValueError("Missing source-owned download section")
    root=doc.select_one(".zo-on-thi-package.reader-content")
    if root is None:raise ValueError("Download utility requires the current source-owned reader")
    owner=doc.new_tag("section",id="tai-tai-lieu",attrs={"class":"level2","data-generated-from":"r1-download-files r1-section-download-files"})
    region=doc.new_tag("div",attrs={"class":"reading-region","data-reading-reason":"Metadata-owned PDF download utility"})
    title=doc.new_tag("h2");title.string="Tải tài liệu"
    intro=doc.new_tag("p");intro.string="Chọn bản phù hợp để đọc hoặc in. Số trang được đọc trực tiếp từ từng tệp PDF."
    region.extend([title,intro]);owner.append(region);root.append(owner);return region


def apply_from_metadata(doc, page, output_root, package, *, create_missing=False):
    """Use the existing download-card design for a newly registered package."""
    import yaml
    from zo_course_pdf_download_state import apply as apply_state
    source = ROOT / package / 'index.qmd'
    metadata = yaml.safe_load(source.read_text(encoding='utf-8').split('---', 2)[1])
    section = metadata_section(doc,create_missing=create_missing)
    doc.body['class'] = list(dict.fromkeys(doc.body.get('class', []) + ['zo-web-2027-production']))
    cards = doc.new_tag('div', attrs={'class':'r1-downloads'})
    section.append(cards)
    for item in metadata['r1-download-files'] + metadata['r1-section-download-files']:
        filename = item['href']
        pdf = source.parent / filename
        pages = len(PdfReader(pdf).pages)
        card = doc.new_tag('div', attrs={'class':'r1-download-card zo-pdf-card'})
        copy_node = doc.new_tag('div', attrs={'class':'zo-pdf-copy'})
        title = doc.new_tag('h3', attrs={'class':'zo-pdf-title'}); title.string = item['title']
        description = doc.new_tag('p', attrs={'class':'zo-pdf-description'}); description.string = item['description']
        note = doc.new_tag('small', attrs={'class':'zo-pdf-version-note'})
        copy_node.extend([title, description, note])
        metric = doc.new_tag('div', attrs={'class':'zo-pdf-pages','data-pdf-pages':str(pages)})
        number = doc.new_tag('strong'); number.string = str(pages)
        unit = doc.new_tag('span'); unit.string = 'trang'; metric.extend([number, unit])
        link = doc.new_tag('a', href=filename, download=item['download'], attrs={'class':'zo-pdf-download__link zo-pdf-download','aria-label':'Tải PDF: '+item['title']})
        icon = doc.new_tag('svg', attrs={'viewBox':'0 0 24 24','aria-hidden':'true','focusable':'false'})
        icon.append(doc.new_tag('path', attrs={'d':'M12 3v12m-4-4 4 4 4-4M5 16v5h14v-5','fill':'none','stroke':'currentColor','stroke-width':'1.7','stroke-linecap':'round','stroke-linejoin':'round'}))
        link.extend([icon, 'Tải PDF'])
        card.extend([copy_node, metric, link]); cards.append(card)
    css = output_root / 'assets/zo_web_2027/g01-downloads.css'
    css.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(ROOT / CSS, css)
    doc.head.append(doc.new_tag('link', rel='stylesheet', href=os.path.relpath(css,page.parent).replace('\\','/')))
    apply_state(doc, ROOT, package)
