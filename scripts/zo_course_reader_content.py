"""Prepare validated learning content without constructing the retired page UI."""
from urllib.parse import unquote, urlsplit, urlunsplit
import os

from bs4 import BeautifulSoup

from zo_course_html import write
from zo_web_2027_preview import DESIGN04, KIT


def prepare_assets(builder):
    for name in ['reading-regions.css', 'r1-consistency.css']:
        builder.materialize(KIT / name, name)
    for name in ['BeVietnamPro_Regular.ttf', 'BeVietnamPro_SemiBold.ttf', 'STIXTwoMath.ttf',
                 'OFL_BeVietnamPro.txt', 'OFL_STIX.txt']:
        builder.materialize(DESIGN04 / 'assets' / name, 'assets/fonts/' + name)


def render(root, binding, settings, builder, page, output_root, cover_name, source):
    """Keep the semantic reader and the same source/DOM/asset validation gates."""
    from zo_course_labels import apply as apply_labels
    from zo_course_tables import apply as apply_tables
    from zo_course_presentation import html_checks, require
    from zo_web_2027_consistency import apply_editorial_policy

    document = BeautifulSoup(
        '<!doctype html><html lang="vi"><head><meta charset="utf-8">'
        '<title></title></head><body><nav class="breadcrumb"></nav>'
        '<figure class="hero-art"></figure><main></main></body></html>',
        'html.parser',
    )
    document.title.string = root['data-r1-title']
    document.body['class'] = ['zo-web-2027-production']
    document.body['data-zo-web-production'] = root['data-r1-code']
    document.body['data-zo-content-projection'] = 'current-reader-v1'
    home = output_root / 'content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/index.html'
    link = document.new_tag('a', href=builder.href(home))
    link.string = 'Khóa 2027'
    document.select_one('.breadcrumb').append(link)
    image = document.new_tag('img', src=cover_name, alt=settings['cover_alt'])
    document.select_one('.hero-art').append(image)
    document.main.append(root)
    for name in ['reading-regions.css', 'r1-consistency.css']:
        document.head.append(document.new_tag('link', rel='stylesheet', href=name))
    apply_labels(document, binding, {})
    for node in document.select('[src],link[href],a[href]'):
        attribute = 'src' if node.has_attr('src') else 'href'
        url = urlsplit(node[attribute])
        if url.scheme or url.netloc or not url.path:
            continue
        target = (builder.output / unquote(url.path)).resolve()
        if not target.is_relative_to(output_root):
            raise ValueError('Content dependency escapes output directory')
        relative = os.path.relpath(target, page.parent).replace('\\', '/')
        node[attribute] = urlunsplit(('', '', relative, url.query, url.fragment))
    apply_tables(document, source.parent.name, page, builder.output)
    if document.select('.figure-viewport img'):
        from zo_course_math_assets import apply_graph_display
        apply_graph_display(document, page, builder.output)
    else:
        css = KIT / 'figure-profile-candidate/production-figures.css'
        builder.materialize(css, css.name)
        relative_css = os.path.relpath(builder.output / css.name, page.parent).replace('\\', '/')
        document.head.append(document.new_tag('link', rel='stylesheet', href=relative_css))
    apply_editorial_policy(document)
    require(html_checks(document, source))
    write(page, document)
    print('Current reader content prepared; retired page template omitted.')
    return True
