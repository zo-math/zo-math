"""G02 opt-in shell from a fresh canonical render, without audit HTML inputs."""
from __future__ import annotations
import json
import os
from pathlib import Path
import shutil
from urllib.parse import urlsplit, unquote, urlunsplit

from bs4 import BeautifulSoup
from zo_web_2027_home import HomeBuilder
from zo_web_2027_preview import PreviewBuilder, REPO, sha
from zo_web_2027_g02 import build
from zo_web_2027_g02_payloads import apply, build_vectors
from zo_r1_g01_labels import apply as apply_labels, remove_redundant_labels

PACKAGE = Path('content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g02')
MARKER = 'zo-web-2027-g02'


def align_reading_roles(doc):
    """Remove contextual scaffolding that G01 does not render as extra labels.

    Typed task/knowledge/checkpoint labels remain; they identify real units.
    All original anchors and content stay in their owning reading region.
    """
    for node in doc.select('[data-zo-type="task"][data-zo-function="function.warmup"], [data-zo-type="task"][data-zo-function="function.self_check"]'):
        heading = node.find(['h3','h4','h5'])
        if heading:
            value = heading.get_text(' ', strip=True)
            heading.name = 'p'
            heading.clear()
            title = doc.new_tag('span', attrs={'class':'r1-task-label'})
            title.string = value
            label = heading.find_previous_sibling(attrs={'data-reading-label':True})
            if label:
                heading.append(label.extract())
            heading.append(title)
        else:
            title = node.select_one(':scope > p > strong')
            if title:
                title['class'] = title.get('class', []) + ['r1-task-label']
    for paper in doc.select('.reader-content .reading-region'):
        label = paper.find(attrs={'data-reading-label': True}, recursive=False)
        if not label:
            continue
        heading = paper.find(['h2', 'h3', 'h4', 'h5', 'h6'])
        duplicate = heading and label.get_text(' ', strip=True).casefold() == heading.get_text(' ', strip=True).casefold()
        foundation = paper.find_parent(id='on-nen') and label.get_text(' ', strip=True).casefold() == 'ôn nền'
        answer_group = paper.find_parent(id='loi-giai') and heading and heading.get_text(' ', strip=True) == 'Bài học' and label.get_text(' ', strip=True).casefold() == 'lời giải'
        warmup = paper.find_parent(id='ba-câu-khởi-động') and bool(paper.select('[data-zo-function="function.warmup"]'))
        if duplicate or foundation or answer_group or warmup:
            label.decompose()


class G02Builder(HomeBuilder):
    def __init__(self, output_root):
        super().__init__(output_root / 'assets/zo_web_2027/g02/g02-reading.html', output_root)
        self.runtime = self.output

    def common_assets(self):
        PreviewBuilder.common_assets(self)


def adapt(path, output_root):
    original = BeautifulSoup(path.read_text(encoding='utf-8'), 'html.parser')
    if MARKER not in original.body.get('class', []):
        raise ValueError('G02 opt-in marker missing; refuse rollback to the legacy shell')
    if original.body.has_attr('data-zo-web-production'):
        return False
    from zo_math_notation import require_source, require_runtime_css
    require_source(REPO / PACKAGE / 'index.qmd')
    require_runtime_css(REPO / '_design/web_2027_mau_dung_chung/web-shell.css')
    from zo_web_2027_backlog_check import require_source as require_structure_source
    require_structure_source(REPO/PACKAGE/'index.qmd',json.loads((REPO/PACKAGE/'giao_dien/he_nhan.json').read_text(encoding='utf-8')))
    builder = G02Builder(output_root)
    builder.output.mkdir(parents=True, exist_ok=True)
    doc = build(builder.output, path, builder=builder)
    # Rebuild only the graph SVG display assets from canonical TeX. Intermediate
    # graph PDFs stay in the output tree; no learning-package PDF is rebuilt.
    vectors=build_vectors(builder.output)
    payloads = apply(builder.output / 'g02-reading.html', builder.output, document=doc)
    apply_labels(doc, REPO / PACKAGE / 'giao_dien/he_nhan.json')
    align_reading_roles(doc)
    remove_redundant_labels(doc)
    from zo_web_2027_fallback_nav import apply as apply_fallback
    apply_fallback(doc)
    doc.body['class'].append(MARKER)
    doc.body['data-zo-web-production'] = 'R1-G02'
    doc.select_one('.lab-link').string = 'ZO Math'
    for note in doc.select('.prototype-note'):
        note.decompose()
    # The shared builder authors links relative to its private asset directory.
    # Rebase every local resource exactly once to the actual package page.
    for node in doc.select('[src],link[href],a[href]'):
        key = 'src' if node.has_attr('src') else 'href'
        url = urlsplit(node[key])
        if url.scheme or url.netloc or not url.path:
            continue
        destination = (builder.output / unquote(url.path)).resolve()
        if not destination.is_relative_to(output_root.resolve()):
            raise ValueError('G02 dependency escapes output root: ' + node[key])
        node[key] = urlunsplit(('', '', os.path.relpath(destination, path.parent).replace('\\', '/'), url.query, url.fragment))
    ids = [n['id'] for n in doc.select('[id]')]
    from zo_course_tables import apply as apply_tables
    apply_tables(doc, 'r1_g02', path, builder.output)
    from zo_web_2027_backlog_check import require as require_structure
    require_structure(doc,json.loads((REPO/PACKAGE/'giao_dien/he_nhan.json').read_text(encoding='utf-8')))
    builder.resources['course-tables.css'] = {'source': '_design/web_2027_mau_dung_chung/course-tables.css', 'sha256': sha(REPO / '_design/web_2027_mau_dung_chung/course-tables.css')}
    if len(ids) != len(set(ids)) or doc.select('details[open]'):
        raise ValueError('G02 duplicate anchors or initially open disclosure')
    from zo_web_2027_navigation import apply as apply_course_navigation
    builder.resources.update(apply_course_navigation(doc,path,output_root,builder.output,'g02'))
    from zo_course_pdf_download_state import apply as apply_pdf_state
    apply_pdf_state(doc,REPO,PACKAGE)
    from zo_web_2027_consistency import apply_editorial_policy
    apply_editorial_policy(doc)
    from zo_course_html import write
    write(path, doc)
    report = {'package': 'R1-G02', 'source': (PACKAGE / 'index.qmd').as_posix(),
        'source_sha256': sha(REPO / PACKAGE / 'index.qmd'), 'html_sha256': sha(path),
        'canonical_render': True, 'payloads': payloads, 'vectors':vectors, 'learning_pdf_built': False,
        'published': False, 'resources': builder.resources}
    report_path = os.environ.get('ZO_WEB_2027_G02_REPORT')
    if report_path:
        target = Path(report_path).resolve()
        if not target.is_relative_to(REPO / '_audit'):
            raise ValueError('G02 report must stay in the audit directory')
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return True
