"""Live canonical inputs and portable routes for the 2027 course UI."""
from pathlib import Path
from urllib.parse import urlsplit, unquote
from datetime import datetime
import os,json,hashlib,shutil
import yaml
from bs4 import BeautifulSoup

ROOT=Path(__file__).resolve().parents[2]
BASE=Path('content/thpt/on_thi_toan_thpt')
HOME=BASE/'tot_nghiep_thpt/2027'
DATA=ROOT/HOME/'_data/chuong_trinh.yml'
DESIGN=Path(__file__).resolve().parent
OUT=ROOT/'docs'
ASSETS=OUT/'assets/course_site_2027'
KEYS=['d0','r1_g01','r1_g02','r1_g03','r1_g04','r1_g05','r2_g01','r2_g02']
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
        image=load_cover(ROOT,key,allow_direction_approved=key in {'r1_g05','r2_g01'})
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
def finish(text,page):
    doc=BeautifulSoup(text,'html.parser')
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
                dest=Path('assets/course_site_2027')/u.path
            if dest is not None:n[attr]=rel(dest,page)+('?' +u.query if u.query else '')+('#'+u.fragment if u.fragment else '')
    doc.body['data-zo-course-site']='r20-integrated-v1'
    # The course projection replaces Quarto's shell, including its shared footer.
    # Reuse the same analytics source and keep finish() safe to call twice.
    if doc.find(id='zo-web-analytics') is None:
        analytics=BeautifulSoup((ROOT/'assets/html/web-analytics.html').read_text('utf-8'),'html.parser')
        for node in list(analytics.contents):doc.body.append(node.extract())
    return str(doc)
