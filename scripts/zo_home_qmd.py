"""Home-only native Markdown contract and DOM binding to the approved UI.

No editorial prose lives here. The binding removes Pandoc scaffolding only;
the resulting content still passes the shell's inventory-preservation guard.
"""
import re
from bs4 import Comment


def source_checks(text):
    body = re.split(r'\n---\s*\n', text, maxsplit=1)[-1]
    return {
        'Home editorial source native headings': bool(re.search(r'^# .+\{#home-title\}', body, re.M)) and all(re.search(r'^## .+\{#'+key+r'\}',body,re.M) for key in ['home-catalog-title','home-purpose','home-method-title','home-strands-title','home-service-title','home-trust-title','home-faq-title']),
        'Home native paragraphs and lists': bool(re.search(r'^- .+\*\*Bài học\*\*',body,re.M)) and '::: {.home-support-copy}' in body,
        'Home no raw HTML narrative or template': not re.search(r'```\{=html\}|</?(?:div|section|p|h[1-6]|details|summary)\b|\.html\.tpl|include _partials/chuong_trinh.qmd',body),
        'Home only three data component includes': re.findall(r'\{\{< include ([^ ]+) >\}\}',body) == ['_partials/home_countdown.qmd','_partials/home_catalog.qmd','_partials/home_strands.qmd'],
    }


def require_native_source(text):
    failed=[key for key,ok in source_checks(text).items() if not ok]
    if failed:raise ValueError('; '.join(failed))


def source_fixtures(text):
    checks={}
    for name,bad in {
        'wrapper-only QMD':'---\ntitle: Home\n---\n{{< include _partials/chuong_trinh.qmd >}}',
        'HTML renamed QMD':text+'\n```{=html}\n<p>Prose</p>\n```',
        'old template dependency':text+'\n{{< include giao_dien/trang_nha.html.tpl >}}',
    }.items():
        try:require_native_source(bad);rejected=False
        except ValueError:rejected=True
        checks['negative native source '+name]=rejected
    return checks


def normalize_native_dom(doc, root, source_text=''):
    """Bind native QMD attributes without inventing headings/copy/IDs."""
    support = doc.select_one('.home-support-copy')
    if support is None or len(support.find_all('p',recursive=False)) != 2:
        raise ValueError('Home QMD must own the two support-copy paragraphs')
    support_copy = [p.get_text(' ',strip=True) for p in support.find_all('p',recursive=False)]
    support.decompose()
    for node in root.select('[data-home-tag]'):
        name=node.attrs.pop('data-home-tag')
        if name not in ('section','nav','figure','details'):raise ValueError('Unsupported Home presentation tag '+name)
        node.name=name
        if name=='details':node.attrs={}
    explicit_heading_ids = set(re.findall(r'^#{1,6} .*?\{[^}\n]*#([^\s}]+)', source_text, re.M))
    for node in root.select('.home-qmd-group'):
        # Quarto can promote a leading heading ID onto its fenced div.
        # Return only source-declared IDs to the heading before removing scaffolding.
        group_id = node.get('id')
        heading = node.find(re.compile(r'^h[1-6]$'), recursive=False)
        if group_id in explicit_heading_ids and heading is not None and not heading.get('id'):
            heading['id'] = group_id
        node.name='div'
        classes=[c for c in node.get('class',[]) if c!='home-qmd-group']
        if classes:node['class']=classes
        else:node.attrs.pop('class',None)
        node.attrs.pop('id',None)
    for node in root.select('.home-paragraph'):
        if node.name!='span' or node.parent.name!='p':raise ValueError('Styled native paragraph is not standalone')
        node.parent['class']=[c for c in node.get('class',[]) if c!='home-paragraph']
        node.unwrap()
    for node in root.select('p'):
        children=[c for c in node.children if getattr(c,'name',None) or str(c).strip()]
        if len(children)==1 and getattr(children[0],'name',None)=='span' and any(c in children[0].get('class',[]) for c in ('role','home-method-verb','home-method-number')):
            node.unwrap()
        elif len(children)==1 and getattr(children[0],'name',None)=='a' and 'home-action' in children[0].get('class',[]):
            node.unwrap()
    for node in root.select('.home-year'):node.attrs.pop('class',None)
    for node in root.select('h1,h2,h3,h4,h5,h6'):
        if 'home-summary' in node.get('class',[]):node.name='summary';node.attrs={}
        else:
            anchored = node.get('id') if 'home-unanchored' not in node.get('class',[]) else None
            node.attrs={'id':anchored} if anchored else {}
            if node.name in ('h2','h3','h4','h5','h6'):node['class']=['anchored']
    for nav in root.select('.home-section-nav'):
        for p in nav.find_all('p',recursive=False):p.unwrap()
    # Pandoc/Quarto may wrap standalone Markdown images in figures/captions.
    # Preserve the explicit native image metadata, not those writer wrappers.
    journey=root.select_one('.home-journey')
    journey['class']=['home-journey','figure']
    images=[]
    for img in journey.select('img'):
        caption = img.find_parent('figure')
        caption = caption.find('figcaption') if caption and caption != journey else None
        alt = img.get('alt') or (caption.get_text(' ',strip=True) if caption else '')
        if not alt:raise ValueError('Native illustration alternate description missing')
        attrs={'src':img['src'],'alt':alt}
        attrs['class']=[c for c in img.get('class',[]) if c == 'journey-portrait']+['figure-img']
        for key in ['width','height']:
            value=img.get('data-home-'+key)
            if not value or not value.isdecimal():raise ValueError('Native illustration dimensions missing')
            attrs[key]=value
        if img.get('loading'):attrs['loading']=img['loading']
        img.extract();img.attrs=attrs;images.append(img)
    if len(images)!=1 or not images[0]['src'].endswith('hanh_trinh_nguoi_hoc_toan_3x4.png'):
        raise ValueError('Home requires the single desktop cover at every viewport')
    journey.clear()
    for img in images:journey.append(img)
    service=root.select_one('.home-service-illustration')
    if service is not None:
        image=service.select_one('img.home-service-art')
        if image is None or len(service.select('img'))!=1:
            raise ValueError('Service illustration must be one canonical image')
        caption=image.find_parent('figure')
        caption=caption.find('figcaption') if caption else None
        attrs={'src':image['src'],'alt':image.get('alt') or (caption.get_text(' ',strip=True) if caption else ''),'class':['home-service-art']}
        if not attrs['alt']:raise ValueError('Service illustration description missing')
        for key in ['width','height']:
            value=image.get('data-home-'+key)
            if not value or not value.isdecimal():raise ValueError('Service illustration dimensions missing')
            attrs[key]=value
        if image.get('loading'):attrs['loading']=image['loading']
        image.extract();image.attrs=attrs;service.clear();service.append(image)
    for node in root.select('a[href]'):
        if not re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:',node['href']):
            node['href']=node['href'].replace('\\','/')
    for comment in root.find_all(string=lambda s:isinstance(s,Comment) and str(s).strip().startswith('Generated data/UI component;')):
        comment.extract()
    return support_copy
