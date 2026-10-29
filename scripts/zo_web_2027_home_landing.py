"""Native editorial QMD + generated data widgets; fresh Quarto input only."""
from pathlib import Path
import copy
import html
import json
import os
from datetime import datetime, date, timedelta
from bs4 import BeautifulSoup
from zo_web_2027_preview import REPO, KIT, DESIGN04, template, sha, BRAND_THOUGHT, inventory

COURSE = Path('content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027')


def countdown_source(program):
    """One canonical date; reference is explicitly NOT an official 2027 schedule."""
    config = program['exam_countdown']
    status = config['status']
    target = datetime.fromisoformat(config['target'])
    reference = datetime.fromisoformat(config['reference'])
    date.fromisoformat(config['verified_on'])
    if status not in ('reference', 'official') or target.year != program['year']:
        raise ValueError('Invalid countdown status or course year')
    if target.utcoffset() != timedelta(hours=7) or reference.utcoffset() != timedelta(hours=7):
        raise ValueError('Exam timestamps require explicit Vietnam offset +07:00')
    if status == 'reference' and (reference.year != target.year-1 or reference.replace(year=target.year) != target):
        raise ValueError('Provisional target must match the verified previous-year reference')
    if not config['source_url'].startswith('https://'):
        raise ValueError('Exam schedule needs a verified HTTPS source')
    label = 'Đếm ngược từ' if status == 'reference' else 'Lịch thi chính thức:'
    notice = (f'Ngày và giờ này được tạm lấy theo lịch thi Toán năm {reference.year}, chưa phải lịch thi chính thức năm {target.year}.'
              if status == 'reference' else 'Theo lịch thi Toán chính thức của Bộ Giáo dục và Đào tạo.')
    stamp = target.strftime('%H:%M ngày %d/%m/%Y')
    return f'''<section class="home-countdown" data-countdown-target="{html.escape(config['target'], quote=True)}" data-countdown-status="{status}" aria-label="Đếm ngược tới mốc thi Toán">
      <div class="countdown-heading"><span>Thời gian không chờ em</span><svg class="countdown-dial" viewBox="0 0 48 48" aria-hidden="true" focusable="false"><circle cx="24" cy="24" r="20"/><circle class="countdown-sweep" cx="24" cy="24" r="20" pathLength="60"/><path d="M24 12v12l8 4"/></svg></div>
      <div class="countdown-readout" role="timer" aria-live="off" hidden>
        <div class="countdown-days"><strong data-time="days">—</strong><span>ngày còn lại</span></div>
        <div class="countdown-hms"><div><strong data-time="hours">—</strong><span>giờ</span></div><b aria-hidden="true">:</b><div><strong data-time="minutes">—</strong><span>phút</span></div><b aria-hidden="true">:</b><div><strong data-time="seconds">—</strong><span>giây</span></div></div>
      </div>
      <p class="countdown-date">{label} <time datetime="{html.escape(config['target'], quote=True)}">{stamp}</time>, giờ Việt Nam.</p>
      <p class="countdown-notice">{notice} <a href="{html.escape(config['source_url'], quote=True)}">Xem nguồn.</a></p>
      <p class="countdown-fallback">Bật JavaScript để xem đồng hồ cập nhật từng giây.</p>
      <p class="countdown-ended" role="status" hidden></p>
    </section>'''


def render_components(program, packages):
    source = (REPO / COURSE / program['home_editorial_source']).resolve()
    if source != (REPO / COURSE / 'index.qmd').resolve():
        raise ValueError('Home editorial source must be the native index.qmd')
    from zo_home_qmd import require_native_source
    require_native_source(source.read_text(encoding='utf-8'))
    from zo_web_2027_navigation import PAGES
    if [p.ref_id for p in packages] != [relative.parent.name for key,(relative,_) in PAGES.items() if key!='home']:
        raise ValueError('Home catalog must follow canonical D0 G01 G02 G03 order')
    cards = []
    for p in packages:
        category = 'survey' if p.ref_id == 'd0' else ('statistics' if p.ref_id.startswith('r2_') else 'functions')
        from zo_course_cover import load_cover
        asset=load_cover(REPO,p.ref_id,allow_direction_approved=p.html_only or p.display_status=='Bản xem trước')
        cover='/' + asset.relative_to(REPO).as_posix()
        if not (REPO / cover.lstrip('/')).is_file():
            raise ValueError('Missing canonical catalog cover ' + cover)
        entry = p.html_url + ('' if p.html_only else '?r1-view=bat-dau#bat-dau')
        cards.append(f'''<article class="home-card" data-package-id="{p.ref_id}" data-category="{category}"><div class="home-card-content">
          <img src="{cover}" alt="" width="420" height="240" loading="lazy">
          <div class="home-card-copy"><span class="role">{html.escape(p.display_status)}</span>
          <h3 id="home-card-title-{p.ref_id}">{html.escape(p.title)}</h3><p>{html.escape(p.summary)}</p>
          <a class="home-card-action" id="home-card-action-{p.ref_id}" href="{entry}" aria-labelledby="home-card-action-{p.ref_id} home-card-title-{p.ref_id}">{'Làm khảo sát' if p.html_only else 'Mở tài liệu'} <span aria-hidden="true">→</span></a></div></div></article>''')
    strands = ''.join(f'<div data-strand-id="{html.escape(s["id"], quote=True)}"><span class="home-topic-number" aria-hidden="true">{i:02d}</span><h3>{html.escape(s["title"])}</h3></div>' for i,s in enumerate(program['strands'],1))
    tools = '''<div class="home-catalog-tools" hidden>
      <div class="home-filters" role="group" aria-label="Lọc học liệu"><button type="button" data-filter="all" aria-pressed="true">Tất cả</button><button type="button" data-filter="survey" aria-pressed="false">Khảo sát</button><button type="button" data-filter="functions" aria-pressed="false">Hàm số</button><button type="button" data-filter="statistics" aria-pressed="false">Thống kê</button></div>
      <label class="home-search">Tìm học liệu<input type="search" id="home-search" placeholder="Tên chủ đề muốn ôn" autocomplete="off"></label>
    </div>'''
    fragments = {'countdown': countdown_source(program), 'strands': strands,
                 'catalog': tools+'\n<div class="home-catalog">'+'\n'.join(cards)+'</div>\n<p class="home-filter-status" role="status" aria-live="polite" hidden></p>'}
    return {f'home_{name}.qmd': '<!-- Generated data/UI component; edit YAML or generator, not this file. -->\n\n```{=html}\n'+value+'\n```\n'
            for name,value in fragments.items()}


def build(builder):
    raw = BeautifulSoup(builder.page.read_text(encoding='utf-8'), 'html.parser')
    root = raw.select_one('.home-landing-content')
    if root is None:
        raise ValueError('Editorial Home profile requires fresh editorial source; refuse old layout')
    from zo_home_qmd import normalize_native_dom
    editorial_text = (REPO / builder.profile['editorial_source']).read_text(encoding='utf-8')
    support_copy = normalize_native_dom(raw, root, editorial_text)
    original = inventory(root)
    content = copy.deepcopy(root)
    builder.common_assets()
    for name in ['site-footer.css', 'course-home-landing.css', 'course-home-landing.js']:
        builder.materialize(KIT / name, name)
    builder.normalize_links(content, builder.page)
    footer, footer_info = builder.site_footer()
    support = BeautifulSoup(template('support.html', support_href=builder.href(builder.output_root / 'content/support/donate.html'), prototype_note=''), 'html.parser')
    support.select_one('.prototype-note').decompose()
    support.select_one('.support-region')['class'] = ['support-region', 'home-paper', 'home-support']
    # Home-only approved copy; keep the shared support template, bank and QR intact.
    support.select_one('.support-content > p').string = support_copy[0]
    support.select_one('.r1-support-link a').string = support_copy[1]
    styles = ['reading-regions.css', 'web-shell.css', 'appearance-inline.css', 'site-footer.css', 'course-home-landing.css']
    result = template('page.html', title=html.escape(builder.profile['title']), body_class='course-home home-editorial zo-web-2027-home',
        home_href=builder.href(builder.page), breadcrumb='', drawer_title='Trong trang Nhà', navigation=builder.navigation(),
        appearance=builder.appearance(), hero='', content=str(content), support=str(support), site_footer=footer,
        styles='\n'.join(f'<link rel="stylesheet" href="{builder.runtime_hrefs[n]}">' for n in styles),
        scripts='\n'.join(f'<script src="{builder.runtime_hrefs[n]}"></script>' for n in ['site-ui.js', 'course-home-landing.js']), brand_thought=html.escape(BRAND_THOUGHT))
    doc = BeautifulSoup(result, 'html.parser')
    doc.title.string = builder.profile['title'] + ' — ZO Math'
    doc.body['data-zo-web-production'] = 'course-home'
    doc.html['data-zo-preferences'] = 'zo-web-2027-preview-v1'
    doc.select_one('.breadcrumb').decompose()
    trigger = doc.select_one('.mobile-trigger')
    trigger['class'].append('mobile-trigger--icon')
    trigger['aria-label'] = 'Mở mục lục trang Nhà'
    # Only shell-owned shorthand asset URLs need rebasing; content is already canonical.
    for node in doc.select('img[src],link[href]'):
        key = 'src' if node.has_attr('src') else 'href'
        if node[key] in builder.runtime_hrefs:
            node[key] = builder.runtime_hrefs[node[key]]
    from zo_course_tables import apply as apply_tables
    apply_tables(doc, 'home', builder.page, builder.runtime)
    builder.resources['course-tables.css'] = {'source':'_design/web_2027_mau_dung_chung/course-tables.css', 'sha256':sha(KIT / 'course-tables.css')}
    from zo_web_2027_navigation import apply
    builder.resources.update(apply(doc, builder.page, builder.output_root, builder.runtime, 'home'))
    if inventory(doc.select_one('.home-landing-content')) != original:
        raise ValueError('Shell adapter changed canonical editorial text, IDs, headings or math')
    from zo_course_html import write
    write(builder.page, doc)
    data = REPO / COURSE / '_data/chuong_trinh.yml'
    editorial = REPO / builder.profile['editorial_source']
    return {'layout': 'editorial-home-2027', 'source_inventory': original,
        'canonical_data': data.relative_to(REPO).as_posix(), 'canonical_data_sha256': sha(data),
        'component_sha256': {path:sha(REPO/path) for path in builder.profile['component_sources']},
        'editorial_source': editorial.relative_to(REPO).as_posix(),
        'editorial_sha256': sha(editorial), 'profile_sha256': sha(KIT / 'profiles/course-home.json'),
        'resources': builder.resources, 'links': builder.links, 'footer': footer_info,
        'implementation_sha256': {name:sha(REPO/'scripts'/name) for name in ['zo_build_on_thi.py','zo_web_2027_home.py','zo_web_2027_home_landing.py','zo_home_qmd.py']},
        'html_sha256': sha(builder.page), 'reference_only_not_runtime': True}
