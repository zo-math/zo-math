"""Canonical r20 presentation of freshly rendered course sources."""
from pathlib import Path
from html import escape as esc
from urllib.parse import urlsplit, unquote, quote
import json, shutil, sys
from bs4 import BeautifulSoup
import yaml
from functools import lru_cache
from datetime import datetime
from . import context as c
from .context import DESIGN, PAGES, KEYS, OUT, sha, native_ref as resolved_ref, catalog, presence_data
from .guidance_content import GUIDES
from .learning_pages import guide_hub, guide_article
from .reader_overview import overview_content, overview_aliases


ICONS = {
 'arrow':'M5 12h14m-6-6 6 6-6 6', 'back':'M19 12H5m6-6-6 6 6 6',
 'book':'M12 5v15m0-15C8 2 4 3 2 4v15c3-1 7-1 10 1 3-2 7-2 10-1V4c-3-1-7-2-10 1Z',
 'pen':'m15 4 5 5M4 20l4-1L21 6l-5-5L3 14l-1 8Z',
 'check':'m8 12 3 3 6-7M9 3H5v18h14V3h-4M9 1h6v4H9Z',
 'repeat':'M20 8A8 8 0 0 0 6 5L3 8m0-5v5h5m-4 8a8 8 0 0 0 14 3l3-3m0 5v-5h-5',
 'bookmark':'M6 3h12v18l-6-4-6 4Z', 'search':'M21 21l-5-5M18 10a8 8 0 1 1-16 0 8 8 0 0 1 16 0Z',
 'grid':'M3 3h7v7H3Zm11 0h7v7h-7ZM3 14h7v7H3Zm11 0h7v7h-7Z',
 'menu':'M4 6h16M4 12h16M4 18h16', 'close':'m6 6 12 12M6 18 18 6',
 'help':'M9 8a3 3 0 1 1 5 2c-2 1-2 2-2 3m0 4h.01M22 12A10 10 0 1 1 2 12a10 10 0 0 1 20 0Z',
 'focus':'M9 3H3v6m12-6h6v6M3 15v6h6m12-6v6h-6',
 'clock':'M12 7v5l3 2m7-2A10 10 0 1 1 2 12a10 10 0 0 1 20 0Z',
 'download':'M12 3v12m-5-5 5 5 5-5M3 15v6h18v-6',
 'chevron':'m9 5 7 7-7 7', 'spark':'m12 2 3 7 7 3-7 3-3 7-3-7-7-3 7-3Z',
}
def icon(name):
    return f'<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.65" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="{ICONS[name]}"/></svg>'

def btn(href,text,style='primary',name='arrow',extra=''):
    return f'<a class="button {style}" href="{esc(href)}" {extra}>{esc(text)}{icon(name)}</a>'

def header(active='course', reader=False):
    if reader:active='topics'
    return f'''<a class="skip-link" href="#main-content">Đến nội dung</a>
<header class="site-header"><a class="brand" href="index.html" aria-label="ZO Math · Khóa 2027"><img src="logo.svg" alt="ZO Math" width="117" height="32"></a>
<nav class="global-nav" aria-label="Điều hướng khóa học"><a href="index.html" {'aria-current="page"' if active=='course' else ''}>Khóa 2027</a><a href="chuyen-de.html" {'aria-current="page"' if active=='topics' else ''}>Chuyên đề</a><a href="cach-hoc.html" {'aria-current="page"' if active=='guide' else ''}>Cách học</a></nav>
<div class="header-controls"><a class="header-saved" href="da-luu.html" aria-label="Học liệu đã lưu" {'aria-current="page"' if active=='saved' else ''}>{icon('bookmark')}<span>Đã lưu</span><span class="saved-count" hidden>0</span></a><button class="icon-button appearance-open" data-open-presence="appearance" aria-label="Tùy chọn giao diện" title="Tùy chọn giao diện">{icon("grid")}</button></div></header>'''

def footer():
    config=yaml.safe_load((c.ROOT/'_quarto.yml').read_text('utf-8'))
    center=config['website']['page-footer']['center']
    import re
    info=''.join('<a href="'+esc(c.rel(Path(href.lstrip('/')).with_suffix('.html')),quote=True)+'">'+esc(label)+'</a>' for label,href in re.findall(r'\[([^\]]+)\]\(([^)]+)\)',center))
    social=''.join('<a href="'+esc(a['href'],quote=True)+'">'+esc(a.get('title',''))+'</a>' for a in BeautifulSoup(center,'html.parser').select('a[href]'))
    copyright=re.search(r'©\s*\d{4}\s+ZO Math',center)
    assert copyright and info and social,'Canonical footer missing'
    return '<footer class="site-footer" aria-label="Chân trang ZO Math"><div class="footer-inner"><nav aria-label="Thông tin ZO Math">'+info+'</nav><nav class="footer-social" aria-label="Kết nối ZO Math">'+social+'</nav><p class="footer-copyright">'+copyright.group()+' · Học liệu miễn phí</p></div></footer>'

def document(title,body,kind='home',data=None,css=None):
    source=c.ROOT/c.PAGE.with_suffix('.qmd')
    if not source.is_file():source=c.ROOT/c.PAGES['home'].with_suffix('.qmd')
    metadata=yaml.safe_load(source.read_text('utf-8').split('---',2)[1])
    robots='noindex,nofollow' if metadata.get('draft',False) else 'index,follow'
    extra=''.join(f'<link rel="stylesheet" href="{esc(h)}">' for h in (css or []))
    payload=json.dumps(dict(data or {},presence=presence_data()),ensure_ascii=False).replace('</','<\\/')
    return f'''<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="{robots}"><title>{esc(title)} · ZO Math</title>{extra}<link rel="stylesheet" href="zo-colors.css"><link rel="stylesheet" href="site.css"><link rel="stylesheet" href="course-redesign.css"><link rel="stylesheet" href="learning-redesign.css"><link rel="stylesheet" href="guidance.css"><link rel="stylesheet" href="review-rounds.css"><link rel="stylesheet" href="learning-format.css"></head><body class="site-{kind} zo-web-2027-production" data-page="{kind}">{body}{presence_shell()}<div class="toast" role="status" aria-live="polite" hidden></div><script id="page-data" type="application/json">{payload}</script><script src="app.js" defer></script><script src="presence.js" defer></script><script src="review-rounds.js" defer></script></body></html>'''


def time_readout():
    units=[('days','ngày'),('hours','giờ'),('minutes','phút'),('seconds','giây')]
    return '<div class="exam-readout" role="timer" aria-live="off">'+''.join(f'<div class="exam-unit"><strong data-{key}>—</strong><span>{label}</span></div>' for key,label in units)+'</div>'


def hero_clock(show_caption=True):
    p=presence_data()
    caption='<span class="exam-caption">THI TỐT NGHIỆP THPT 2027</span>' if show_caption else ''
    return f'''<section class="exam-hero-clock" id="exam-hero-clock" aria-label="Đếm ngược ngày thi"><div class="exam-heading">{caption}<h2>Đếm ngược ngày thi</h2><button class="exam-date" data-open-presence="timer">Ngày tạm tính · {p['date']} {icon('chevron')}</button></div>{time_readout()}<span class="exam-paused" hidden>Đã tạm dừng cập nhật</span></section>'''


def appearance_panel():
    choices=[('red-1','Đỏ nhạt'),('red-2','Đỏ'),('yellow-1','Vàng nhạt'),('yellow-2','Vàng'),('gray-2','Xám nhạt'),('gray-3','Xám')]
    controls=''.join(f'<label class="theme-choice"><input type="radio" name="canvas" value="{key}" aria-label="{label}" {"checked" if key=="gray-3" else ""}><span class="theme-color" style="--swatch:var(--zo-{key})"></span><span>{label}</span></label>' for key,label in choices)
    return '<section data-presence-panel="appearance" hidden><p>Chọn màu nền quanh trang. Phần đọc luôn giữ nền trắng.</p><fieldset class="theme-options"><legend>Màu nền</legend>'+controls+'</fieldset><label class="exam-auto"><input type="checkbox" id="grayscale"> Sắc xám</label><p class="presence-timer-note">Lựa chọn được lưu trên trình duyệt này.</p></section>'


def presence_shell():
    p=presence_data()
    clock=''.join(f'<span class="presence-unit"><strong data-{key}>—</strong><span>{label}</span></span>' for key,label in [('days','ngày'),('hours','giờ'),('minutes','phút'),('seconds','giây')])
    return f'''<aside class="course-presence" id="course-presence" aria-label="Đồng hồ và bảo trợ"><div class="presence-study-tools"></div><button class="presence-time" data-open-presence="timer" aria-label="Đếm ngược ngày thi. Mở thông tin ngày thi" title="Thông tin ngày thi"><span class="presence-count">{clock}</span><small class="exam-paused" hidden>Đã tạm dừng</small></button><button class="presence-support" data-open-presence="support" aria-label="Bảo trợ ZO Math. Mở mã QR lớn" title="Mở mã QR bảo trợ"><img class="presence-qr" src="{p['qr']}" alt="" width="64" height="64"><span class="presence-support-label"><span>Bảo trợ</span><strong>ZO Math</strong></span></button><div class="presence-save"></div></aside>
<dialog id="presence-dialog" class="presence-dialog" aria-labelledby="presence-dialog-title"><div class="presence-dialog-head"><h2 id="presence-dialog-title">Bảo trợ ZO Math</h2><button class="icon-button" data-close-presence aria-label="Đóng bảng tiện ích">{icon('close')}</button></div><section data-presence-panel="support"><p>{esc(p['invitation'])}</p><img class="dialog-qr" src="{p['qr']}" alt="Mã QR Vietcombank để bảo trợ ZO Math" width="256" height="256"><dl class="presence-bank"><div><dt>Ngân hàng</dt><dd>{esc(p['bank'])}</dd></div><div><dt>Chủ tài khoản</dt><dd>{esc(p['owner'])}</dd></div><div><dt>Số tài khoản</dt><dd>{esc(p['account'])}</dd></div><div><dt>Nội dung chuyển khoản</dt><dd>{esc(p['memo'])}</dd></div></dl><div class="presence-actions"><button class="button primary" data-copy-account>Sao chép số tài khoản</button><a class="button secondary" href="{p['qr']}" download="QR-bao-tro-ZO-Math.jpg">Lưu QR {icon('download')}</a></div><p class="presence-copy-status" role="status"></p></section><section data-presence-panel="timer" hidden>{time_readout()}<p class="exam-target">{p['date']} · Giờ Việt Nam</p><p><strong>Ngày tạm tính.</strong> {esc(p['notice'])}</p><a class="text-link" href="{esc(p['source'])}" target="_blank" rel="noopener">Xem lịch thi năm 2026 {icon('arrow')}</a><label class="exam-auto"><input type="checkbox" id="exam-auto" checked> Tự động cập nhật thời gian</label><p class="presence-timer-note">Khi bật lại, đồng hồ cập nhật theo thời gian hiện tại.</p></section>{appearance_panel()}</dialog>'''

def snapshot_stats(root):
    return {'text':sha_text(root.get_text()),'math':[str(m) for m in root.select('math')],
            'ids':[n['id'] for n in root.select('[id]')],
            'headings':[(n.name,n.get_text()) for n in root.select('h1,h2,h3,h4,h5,h6')],
            'images':len(root.select('img')),'tables':len(root.select('table'))}

def sha_text(text):
    import hashlib
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

MODES=[('bai-hoc','Bài học','Hiểu ý tưởng và cách làm','book'),('phieu-luyen','Luyện tập','Tự làm, đối chiếu, sửa lỗi','pen'),
       ('tu-kiem-tra','Kiểm tra','Thử sức trong một lượt tự làm','check'),('on-lai','Ôn lại','Gọi lại kiến thức sau một khoảng nghỉ','repeat')]

def card(p):
    # The registry selects approved card artwork independently of lesson/PDF covers.
    from zo_topic_art import card_art
    artwork = card_art(c.ROOT, p['id'])
    if artwork is not None:
        p = dict(p, cover=c.rel(Path('assets/course_site_2027/illustrations') / (p['id'] + '.png')),
                 coverAlt=artwork[1])
    actions=''.join(f'<a class="topic-activity" data-activity="{key}" href="{p["url"]}#{key}">{icon(ic)}<span>{label}</span>{icon("arrow")}</a>' for key,label,hint,ic in MODES)
    overview=btn(p['url']+'#tong-quan','Tổng quan','primary topic-overview-entry',extra='data-overview')
    return f'''<article class="course-card topic-card" data-course="{p['id']}" data-group="{p['group']}" aria-labelledby="title-{p['id']}"><figure class="topic-art"><img src="{p['cover']}" alt="{esc(p['coverAlt'])}" loading="lazy"></figure><button class="save-course icon-button" data-save="{p['id']}" aria-label="Lưu chuyên đề {esc(p['title'])}" aria-pressed="false">{icon('bookmark')}</button><div class="topic-body"><h3 id="title-{p['id']}">{esc(p['title'])}</h3><p>{esc(p['summary'])}</p>{overview}<nav class="topic-activities" aria-label="Các phần của {esc(p['title'])}">{actions}</nav></div></article>'''

def home(items):
    source=c.OUT/PAGES['home']
    original=c.fresh('home')
    def fragment(selector):
        node=BeautifulSoup(str(original.select_one(selector)),'html.parser').find()
        assert node is not None,selector
        for element in [node]+node.select('[src],[href]'):
            for attr in ['src','href']:
                if element.get(attr):element[attr]=resolved_ref(element[attr],source)
        return node
    title=original.select_one('#home-title').decode_contents()
    lead=original.select_one('.home-lead').decode_contents()
    art=fragment('.home-journey img')
    intro=fragment('.home-video-copy');intro['class']=['course-intro-copy']
    video=fragment('.home-video-media')
    video.append(intro.select_one('.home-video-audience').extract())
    scope=fragment('#tám-mạch');scope['class']=['course-section','course-scope']
    for badge in scope.select('.home-topic-number'):badge.decompose()
    service=fragment('#hoc-truc-tiep');service['class']=['course-section','course-service']
    benefits=service.select_one('dl');benefits['class']=['service-benefits']
    for term in list(benefits.select('dt')):
        definition=term.find_next_sibling('dd');row=original.new_tag('div')
        term.insert_before(row);row.append(term.extract());row.append(definition.extract())
    faq=fragment('#cau-hoi-thuong-gap');faq['class']=['course-section','course-faq']
    support=fragment('#ung-ho');support['class']=['course-section','course-support']
    support.select_one('h3').name='h2'
    journey=fragment('#lo-trinh-on-thi')
    journey.select_one('#cach-hoc')['href']='cach-hoc.html'
    for link in journey.select('a[href]'):
        if urlsplit(link['href']).path.endswith('/d0/index.html'):link['data-course-page']='d0'
    for area in [service,journey]:
        for link in area.select('a.button,a.text-link'):
            link.append(BeautifulSoup(icon('arrow'),'html.parser'))
    body=header()+f'''<main id="main-content" class="home-main course-home home-editorial"><span id="hoc-lieu-hien-co" hidden></span><span id="chuyen-de" hidden></span><section class="hero exam-hero"><div class="hero-copy"><h1 id="home-title">{title}</h1><p class="hero-lead">{lead}</p><div class="hero-actions">{btn('chuyen-de.html','Chuyên đề')}{btn('#hoc-truc-tiep','Học trực tiếp','secondary','book')}</div></div><figure class="course-hero-art">{art}</figure></section>{hero_clock(show_caption=False)}
<nav class="course-section-nav" aria-label="Trong trang Khóa 2027"><a href="#gioi-thieu-khoa">Giới thiệu</a><a href="#tám-mạch">Nội dung chương trình</a><a href="#lo-trinh-on-thi">Lộ trình ôn thi</a><a href="#hoc-truc-tiep">Học trực tiếp</a><a href="#cau-hoi-thuong-gap">Câu hỏi thường gặp</a><a href="#ung-ho">Bảo trợ</a></nav>
<section id="recent-reading" class="resume-strip" aria-label="Vị trí đọc gần nhất" hidden></section>
<section id="gioi-thieu-khoa" class="course-section course-introduction">{intro}<div class="course-intro-media">{video}</div></section>
{scope}
{journey}
{service}{faq}{support}</main>'''+footer()
    return document('Ôn thi Toán THPT 2027',body,data={'catalog':items})

def topics(items):
    strands=yaml.safe_load(c.DATA.read_text('utf-8'))['program']['strands']
    groups=[]
    for strand in strands:
        members=[p for p in items if p['id']!='d0' and p['group']==strand['id']]
        if not members:
            continue
        tone=' shaded' if len(groups)%2 else ''
        heading='strand-'+strand['id'].lower()
        groups.append(f'<section class="topic-strand{tone}" aria-labelledby="{heading}"><h2 id="{heading}">{esc(strand["title"])}</h2><div class="topic-grid">'+''.join(card(p) for p in members)+'</div></section>')
    rows=''.join(groups)
    search=f'<label class="catalog-search">{icon("search")}<span class="visually-hidden">Tìm chuyên đề</span><input id="course-search" type="search" placeholder="Tìm chuyên đề…" autocomplete="off"></label>'
    body=header('topics')+f'''<main id="main-content" class="catalog-page"><div class="topics-introduction"><header class="catalog-heading"><h1>Chuyên đề</h1></header></div>
<aside class="catalog-diagnostic"><div><h2>Khảo sát đầu vào</h2><p>{esc(next(p['summary'] for p in items if p['id']=='d0'))}</p></div>{btn('d0.html#khai-bao-pham-vi','Làm khảo sát','secondary')}</aside>
<section id="recent-reading" class="resume-strip" aria-label="Vị trí đọc gần nhất" hidden></section>
<section class="catalog" id="chuyen-de" aria-labelledby="catalog-title"><h2 id="catalog-title" class="visually-hidden">Danh sách chuyên đề</h2><div class="catalog-toolbar"><div class="catalog-filters" role="group" aria-label="Lọc chuyên đề"><button data-filter="all" aria-pressed="true">Tất cả</button><button data-filter="R1" aria-pressed="false">Hàm số</button><button data-filter="R2" aria-pressed="false">Thống kê</button></div>{search}</div><p id="filter-status" class="visually-hidden" role="status"></p><div class="topic-strands">{rows}</div><div id="no-courses" class="empty-state" hidden><h3>Chưa tìm thấy chuyên đề phù hợp</h3><p>Thử một từ ngắn hơn hoặc chọn “Tất cả”.</p><button id="clear-search" class="button secondary">Xóa bộ lọc</button></div></section>
</main>'''+footer()
    return document('Chuyên đề',body,'topics',data={'catalog':items})

def side_nav(p,items):
    main=[('tong-quan','Tổng quan','grid')]+[(k,t,ic) for k,t,h,ic in MODES]
    if p['id']=='d0':main=[('tong-quan','Tổng quan','grid'),('bat-dau','Bắt đầu','book'),('khai-bao-pham-vi','Chọn phạm vi','pen'),('khao-sat','Khảo sát','check'),('doc-ket-qua','Đọc kết quả','repeat'),('chon-mach','Chọn mạch học','arrow')]
    def links(rows):return ''.join(f'<a href="#{k}" data-view="{k}">{icon(ic)}<span>{t}</span></a>' for k,t,ic in rows)
    support='' if p['id']=='d0' else '<span class="nav-label">KHI CẦN HỖ TRỢ</span>'+links([('on-nen','Ôn nền','book'),('sua-loi','Sửa lỗi','help'),('loi-giai','Lời giải','check')])+'<span class="nav-label">GHI CHÉP</span>'+links([('nhat-ky','Nhật kí','pen')])
    docs='' if p['id']=='d0' else '<span class="nav-label">TRA CỨU</span>'+links(([('tai-tai-lieu','Tải PDF','download')] if p['has_pdf'] else [])+[('nguon','Nguồn tài liệu','book')])
    all_courses=''.join(f'<a href="{x["url"]}" data-course-page="{x["id"]}" {"aria-current=page" if x["id"]==p["id"] else ""}>{esc(x["title"])}</a>' for x in items)
    return f'<div class="nav-inner"><div class="nav-course"><strong>{esc(p["title"])}</strong></div><nav class="lesson-nav" aria-label="Các phần của chuyên đề"><span class="nav-label">{"KHẢO SÁT ĐẦU VÀO" if p["id"]=="d0" else "HỌC VÀ LUYỆN TẬP"}</span>{links(main)}{support}{docs}<a href="#toan-van" data-view="toan-van">{icon("book")}<span>Đọc toàn văn</span></a></nav><details class="course-switcher"><summary>Chuyển chuyên đề</summary><nav aria-label="Các chuyên đề">{all_courses}</nav></details></div>'

def reader(p,items):
    source=c.OUT/PAGES[p['id']];doc=c.fresh(p['id'])
    content=doc.select_one('.reader-content');before=snapshot_stats(content)
    for node in content.select('[src],[href],[poster],[data]'):
        for attr in ['src','href','poster','data']:
            if node.get(attr):node[attr]=resolved_ref(node[attr],source)
    # Only URL rebasing is allowed inside the published learning content.
    after=snapshot_stats(content)
    assert before==after,p['id']+' content changed'
    css=[]
    for n in doc.select('link[rel=stylesheet]'):
        name=Path(urlsplit(n['href']).path).name
        if name in {'reading-regions.css','production-figures.css','course-tables.css','r1-consistency.css','g01-downloads.css','downloads.css'}:
            css.append(resolved_ref(n['href'],source))
    overview=overview_content(p,content,icon,btn)
    returnbar=f'<div class="context-return" id="context-return" hidden>{icon("back")}<div><small>ĐANG MỞ HỖ TRỢ</small><strong id="origin-label"></strong></div><button id="return-to-task">Quay lại chỗ đang làm {icon("arrow")}</button></div>'
    body=header(reader=True)+f'''<div class="reader-shell"><aside class="reader-sidebar" id="reader-sidebar"><button class="icon-button mobile-nav-close" aria-label="Đóng nội dung chuyên đề">{icon('close')}</button>{side_nav(p,items)}</aside><div class="nav-scrim" hidden></div><main id="main-content" class="reader-main"><div class="reader-breadcrumb"><a href="chuyen-de.html#chuyen-de">Chuyên đề</a>{icon('chevron')}<span>{esc(p['title'])}</span></div><header class="lesson-heading"><div class="eyebrow red">{'KHẢO SÁT ĐẦU VÀO' if p['id']=='d0' else 'HÀM SỐ VÀ ĐỒ THỊ' if p['group']=='R1' else 'THỐNG KÊ VÀ DỮ LIỆU'}</div><h1>{esc(p['title'])}</h1><p>{esc(p['summary'])}</p></header><div class="reader-tools"><span id="current-view-label">Tổng quan</span><div><button class="icon-button" id="save-position" aria-label="Lưu chỗ đang đọc" title="Lưu chỗ đang đọc">{icon('bookmark')}</button><button class="icon-button" id="text-size" aria-label="Tăng cỡ chữ" title="Cỡ chữ lớn">A<span class="small-a">A</span></button><button class="icon-button" id="focus-mode" aria-label="Bật chế độ tập trung" aria-pressed="false" title="Chế độ tập trung">{icon('focus')}</button></div></div>{returnbar}<div class="reading-layout"><div class="reading-column"><section id="tong-quan" class="course-overview">{overview}</section>{str(content)}</div><aside class="reading-outline"><span class="nav-label">TRONG PHẦN NÀY</span><nav id="page-outline" aria-label="Mục lục phần đang đọc"></nav><div class="outline-help"><span>{icon('help')} {'Cần hướng dẫn?' if p['id']=='d0' else 'Cần ôn kiến thức?'}</span><p>Mở hỗ trợ, rồi quay lại đúng chỗ em đang làm.</p>{'<a href="#on-nen">Ôn nền '+icon('arrow')+'</a><a href="#sua-loi">Sửa lỗi '+icon('arrow')+'</a>' if p['id']!='d0' else '<a href="#bat-dau">Đọc hướng dẫn '+icon('arrow')+'</a>'}</div></aside></div></main></div><div class="mobile-reader-bar"><button id="mobile-contents">{icon('menu')} Nội dung</button><span id="mobile-view">Tổng quan</span><button id="mobile-save" aria-label="Lưu chỗ đang đọc">{icon('bookmark')}</button></div><button class="button secondary exit-focus" hidden>{icon('back')} Thoát tập trung</button><dialog id="support-gate"><form method="dialog"><button class="icon-button dialog-close" value="cancel" aria-label="Đóng">{icon('close')}</button><span class="eyebrow">GIỮ ĐÚNG LƯỢT TỰ LÀM</span><h2>Em đã kết thúc lượt kiểm tra?</h2><p>Hãy giữ nguyên bài làm ban đầu trước khi xem hỗ trợ. Phần làm sau khi xem không tính vào kết quả tự làm.</p><div class="dialog-actions"><button class="button primary" value="end">Đã kết thúc, mở hỗ trợ {icon('arrow')}</button><button class="button secondary" value="cancel">Tiếp tục tự làm</button></div></form></dialog>'''
    body=body.replace(str(content),'<div id="toan-van">'+str(content)+'</div>',1)
    body=body.replace('<dialog id="support-gate">','<dialog id="support-gate" aria-labelledby="support-gate-title">')
    body=body.replace('<h2>Em đã kết thúc lượt kiểm tra?</h2>','<h2 id="support-gate-title">Em đã kết thúc lượt kiểm tra?</h2>')
    data={'course':p,'catalog':items,'modes':[{'id':k,'title':t} for k,t,h,ic in MODES],
          'overviewAliases':overview_aliases(p['id'])}
    return document(p['title'],body+footer(),'reader',data,css),{'id':p['id'],'math_count':len(before['math']),'ids':len(before['ids']),'images':before['images'],'tables':before['tables'],'content_unchanged':True,'text_sha256':before['text']}

def saved(items):
    body=header('saved')+f'''<main id="main-content" class="utility-main"><h1>Học liệu đã lưu</h1><p class="utility-intro">Chuyên đề và vị trí đọc em đã đánh dấu trên trình duyệt này.</p><div id="saved-list"></div><div id="saved-empty" class="empty-state">{icon('bookmark')}<h2>Chưa có học liệu được lưu</h2><p>Chọn biểu tượng đánh dấu trên chuyên đề hoặc ngay trong bài học.<br>Những chỗ em muốn quay lại sẽ ở đây.</p>{btn('chuyen-de.html#chuyen-de','Chọn chuyên đề')}</div><p class="local-note">Dấu lưu chỉ ở trình duyệt này, chưa đồng bộ giữa các thiết bị.</p></main>'''+footer()
    return document('Học liệu đã lưu',body,'saved',{'catalog':items})

def guide():
    body=header('guide')+guide_hub(GUIDES,icon,btn)+footer()
    return document('Cách học',body,'guide')

def detailed_guide(g,items):
    return document(g['title'],header('guide')+guide_article(g,GUIDES,items,icon,btn)+footer(),'guidance')

