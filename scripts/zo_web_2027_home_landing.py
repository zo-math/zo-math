"""Editorial Home only: canonical template + real catalog, fresh Quarto input."""
from pathlib import Path
from string import Template
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
    label = 'Tạm tính đến' if status == 'reference' else 'Lịch thi chính thức:'
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
      <p class="countdown-notice">{notice} <a href="{html.escape(config['source_url'], quote=True)}">Xem lịch thi dùng để tính</a></p>
      <p class="countdown-fallback">Bật JavaScript để xem đồng hồ cập nhật từng giây.</p>
      <p class="countdown-ended" role="status" hidden></p>
    </section>'''


def render_source(program, packages):
    source = (REPO / COURSE / program['home_editorial_source']).resolve()
    if not source.is_relative_to(REPO / COURSE / 'giao_dien') or source.suffix != '.tpl':
        raise ValueError('Unsafe editorial source')
    if [p.ref_id for p in packages] != ['d0', 'r1_g01', 'r1_g02']:
        raise ValueError('Home catalog must follow canonical D0 G01 G02 order')
    cards = []
    for p in packages:
        category = 'survey' if p.ref_id == 'd0' else 'functions'
        cover = (f'/content/thpt/on_thi_toan_thpt/hoc_lieu/{p.ref_id}/giao_dien/assets/figures_0_4/cover-light.svg'
                 if p.ref_id != 'd0' else '/' + (DESIGN04 / 'logos/stack_color.svg').relative_to(REPO).as_posix())
        if not (REPO / cover.lstrip('/')).is_file():
            raise ValueError('Missing canonical catalog cover ' + cover)
        entry = p.html_url + ('' if p.html_only else '?r1-view=bat-dau#bat-dau')
        cards.append(f'''<article class="home-card" data-package-id="{p.ref_id}" data-category="{category}"><a class="home-card-link" href="{entry}" aria-labelledby="home-card-title-{p.ref_id}">
          <img src="{cover}" alt="" width="420" height="240" loading="lazy">
          <div class="home-card-copy"><span class="role">{html.escape(p.display_status)}</span>
          <h3 id="home-card-title-{p.ref_id}">{html.escape(p.title)}</h3><p>{html.escape(p.summary)}</p>
          <span class="home-card-action">{'Làm khảo sát' if p.html_only else 'Mở tài liệu'} <span aria-hidden="true">→</span></span></div></a></article>''')
    strands = ''.join(f'<div data-strand-id="{html.escape(s["id"], quote=True)}"><h3>{html.escape(s["title"])}</h3></div>' for s in program['strands'])
    values = {k: html.escape(program[k]) for k in ['audience', 'deployment', 'start', 'roadmap_note']}
    values.update(cards='\n'.join(cards), strands=strands, countdown=countdown_source(program))
    return Template(source.read_text(encoding='utf-8')).substitute(values)


def build(builder):
    raw = BeautifulSoup(builder.page.read_text(encoding='utf-8'), 'html.parser')
    root = raw.select_one('.home-landing-content')
    if root is None:
        raise ValueError('Editorial Home profile requires fresh editorial source; refuse old layout')
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
    support.select_one('.support-content > p').string = 'Nếu tài liệu hữu ích với bạn, bạn có thể ủng hộ ZO Math tiếp tục biên soạn và chia sẻ.'
    support.select_one('.r1-support-link a').string = 'Xem thông tin ủng hộ'
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
    builder.page.write_text(str(doc), encoding='utf-8')
    data = REPO / COURSE / '_data/chuong_trinh.yml'
    partial = REPO / COURSE / '_partials/chuong_trinh.qmd'
    editorial = REPO / builder.profile['editorial_source']
    return {'layout': 'editorial-home-2027', 'source_inventory': original,
        'canonical_data': data.relative_to(REPO).as_posix(), 'canonical_data_sha256': sha(data),
        'partial_sha256': sha(partial), 'editorial_source': editorial.relative_to(REPO).as_posix(),
        'editorial_sha256': sha(editorial), 'profile_sha256': sha(KIT / 'profiles/course-home.json'),
        'resources': builder.resources, 'links': builder.links, 'footer': footer_info,
        'implementation_sha256': {name:sha(REPO/'scripts'/name) for name in ['zo_build_on_thi.py','zo_web_2027_home.py','zo_web_2027_home_landing.py']},
        'html_sha256': sha(builder.page), 'reference_only_not_runtime': True}
