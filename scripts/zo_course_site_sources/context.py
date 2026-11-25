"""Live canonical inputs and portable routes for the 2027 course UI."""
from pathlib import Path
from urllib.parse import urlsplit, unquote
from datetime import datetime
import os,json,hashlib,shutil,re
import yaml
from bs4 import BeautifulSoup

ROOT=Path(__file__).resolve().parents[2]
BASE=Path('content/thpt/on_thi_toan_thpt')
HOME=BASE/'tot_nghiep_thpt/2027'
DATA=ROOT/HOME/'_data/chuong_trinh.yml'
DESIGN=Path(__file__).resolve().parent
OUT=ROOT/'docs'
ASSETS=OUT/'assets/course_site_2027'
# During the editorial rollout, these files must coexist with the public
# versions still used by pages awaiting migration.
ROLLOUT_ASSETS={'app.js','course-redesign.css','learning-format.css'}
KEYS=['d0','r1_g01','r1_g02','r1_g03','r1_g04','r1_g05','r2_g01','r2_g02',
      'r3_g01','r3_g02','r3_g03','r3_g04','r3_g05','r3_g06','r3_g07','r3_g08','r3_g09','r3_g10','r3_g11','r3_g12','r3_g13','r3_g14','r3_g15','r3_g16','r3_g17','r3_g18','r3_g19','r4_g01','r4_g02','r4_g03','r4_g04','r4_g05','r4_g06','r5_g01','r5_g02','r5_g03','r5_g04','r5_g05','r5_g06','r5_g07','r5_g08','r5_g09']
PAGES={key:BASE/'hoc_lieu'/key/'index.html' for key in KEYS}
PAGES['home']=HOME/'index.html'
FOUNDATION=BASE/'hoc_lieu/_dung_chung/nen/so_gan_dung_sai_so.html'
FRESH={}
PAGE=PAGES['home']
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rel(path,page=None):return os.path.relpath(OUT/path,(OUT/(page or PAGE)).parent).replace('\\','/')
def fresh(key):
    if key not in FRESH:raise ValueError('Fresh successful QMD render required: '+key)
    return BeautifulSoup(FRESH[key],'html.parser')
def native_ref(value,page):
    # Reader and Home keep their canonical locations, so native links stay valid.
    return value
def catalog():
    from zo_course_cover import load_cover
    config=yaml.safe_load(DATA.read_text('utf-8'))
    refs={r['id']:r for r in config['packages']}
    if set(KEYS)-set(refs):raise ValueError('Course catalog missing a current package')
    items=[]
    for key in KEYS:
        folder=ROOT/BASE/'hoc_lieu'/key
        meta=yaml.safe_load((folder/'index.qmd').read_text('utf-8').split('---',2)[1])
        image=load_cover(ROOT,key,allow_direction_approved=key in {'r1_g05','r2_g01','r3_g07'})
        cover=json.loads((folder/'giao_dien/anh_bia.json').read_text('utf-8'))
        dest=ASSETS/'covers'/(key+image.suffix)
        dest.parent.mkdir(parents=True,exist_ok=True)
        if not dest.exists() or sha(dest)!=sha(image):shutil.copyfile(image,dest)
        items.append(dict(id=key,code=key.replace('_','-').upper(),title=meta['title'],summary=refs[key]['summary'],group='D0' if key=='d0' else key[:2].upper(),url=rel(PAGES[key]),cover=rel(dest.relative_to(OUT)),coverAlt=cover.get('alt',meta['title']),has_pdf=bool(meta.get('r1-download-files') or meta.get('r1-section-download-files'))))
    return items
def presence_data():
    cfg=yaml.safe_load(DATA.read_text('utf-8'))['program']['exam_countdown']
    doc=BeautifulSoup((ROOT/'_design/web_2027_mau_dung_chung/templates/support.html.tpl').read_text('utf-8'),'html.parser')
    fields={d.get_text(' ',strip=True):d.find_next_sibling('dd').get_text(' ',strip=True) for d in doc.select('dt')}
    target=cfg['target']
    return dict(target=target,status=cfg['status'],date=datetime.fromisoformat(target).strftime('%H:%M · %d/%m/%Y'),notice='Ngày thi năm 2027 chưa được xác nhận; mốc này dùng để tham khảo khi lập kế hoạch ôn tập.',source=cfg['source_url'],qr=rel(Path('assets/course_site_2027/qr.jpg')),invitation=doc.select_one('.support-content > p').get_text(' ',strip=True),bank=fields['Ngân hàng'],account=fields['Số tài khoản'],owner=fields['Chủ tài khoản'],memo=fields['Nội dung chuyển khoản'])

def editorial_assets(page):
    config=ROOT/page.parent/'giao_dien/html.json'
    if not config.is_file() or not json.loads(config.read_text('utf-8')).get('versioned_course_assets'):
        return {}
    assets={}
    for name in sorted(ROLLOUT_ASSETS):
        contents=(DESIGN/name).read_bytes().replace(b'\r\n',b'\n')
        digest=hashlib.sha256(contents).hexdigest()[:16]
        path=Path(name)
        # The same directory preserves relative URLs inside stylesheets.
        target=ASSETS/f'{path.stem}.{digest}{path.suffix}'
        target.parent.mkdir(parents=True,exist_ok=True)
        if not target.exists():
            target.write_bytes(contents)
        elif target.read_bytes()!=contents:
            raise ValueError(f'Versioned course asset does not match its source: {target}')
        assets[name]=target.relative_to(OUT)
    return assets

def limit_reader_catalog(text,page):
    config=ROOT/page.parent/'giao_dien/html.json'
    keys=json.loads(config.read_text('utf-8')).get('reader_catalog') if config.is_file() else None
    if keys is None:return text
    owner=next((key for key, path in PAGES.items() if path==page),None)
    if not isinstance(keys,list) or owner not in keys or len(keys)!=len(set(keys)) or not set(keys)<=set(KEYS):
        raise ValueError(f'Invalid public reader catalog for {page}')
    menu=r'<details class="course-switcher">.*?</details>'
    data=r'(<script id="page-data" type="application/json">)(.*?)(</script>)'
    def trim_menu(match):
        return re.sub(r'<a\b[^>]*data-course-page="([^"]+)"[^>]*>.*?</a>',
                      lambda link:link[0] if link[1] in keys else '',match[0],flags=re.S)
    def trim_data(match):
        payload=json.loads(match[2]);items=payload['catalog']
        if set(keys)-{item['id'] for item in items}:
            raise ValueError(f'Missing entries in the reader catalog for {page}')
        payload['catalog']=[item for item in items if item['id'] in keys]
        return match[1]+json.dumps(payload,ensure_ascii=False).replace('</','<\\/')+match[3]
    text,menus=re.subn(menu,trim_menu,text,flags=re.S)
    text,blocks=re.subn(data,trim_data,text,flags=re.S)
    if (menus,blocks)!=(1,1):raise ValueError(f'Expected one reader catalog for {page}')
    return text

def finish(text,page):
    doc=BeautifulSoup(text,'html.parser')
    versions=editorial_assets(page)
    routes={'index.html':PAGES['home'],**{k+'.html':PAGES[k] for k in KEYS}}
    for name in ['chuyen-de.html','cach-hoc.html','da-luu.html','cach-hoc-bai-hoc.html','cach-hoc-luyen-tap.html','cach-hoc-kiem-tra.html','cach-hoc-on-lai.html']:
        routes[name]=HOME/name
    from .guidance_content import GUIDES
    for guide in GUIDES:routes[guide['file']]=HOME/guide['file']
    for n in doc.select('[href],[src]'):
        # Native learning URLs are already relative to this very same location.
        if n.find_parent(class_='reader-content'):continue
        for attr in ['href','src']:
            value=n.get(attr)
            if not value:continue
            u=urlsplit(value)
            if u.scheme or u.netloc or not u.path:continue
            dest=routes.get(unquote(u.path))
            if u.path in ['site.css','course-redesign.css','learning-redesign.css','guidance.css','learning-format.css','zo-colors.css','app.js','presence.js','review-rounds.js','review-rounds.css','foundation-return.js','logo.svg']:
                dest=versions.get(u.path,Path('assets/course_site_2027')/u.path)
            if dest is not None:n[attr]=rel(dest,page)+('?' +u.query if u.query else '')+('#'+u.fragment if u.fragment else '')
    doc.body['data-zo-course-site']='r20-integrated-v1'
    # The course projection replaces Quarto's shell, including its shared footer.
    # Reuse the same analytics source and keep finish() safe to call twice.
    if doc.find(id='zo-web-analytics') is None:
        analytics=BeautifulSoup((ROOT/'assets/html/web-analytics.html').read_text('utf-8'),'html.parser')
        for node in list(analytics.contents):doc.body.append(node.extract())
    return limit_reader_catalog(str(doc),page)
