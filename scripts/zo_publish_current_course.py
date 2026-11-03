"""Publish the current integrated course under explicit release authorization.

This is separate from historical owner-acceptance receipts. It requires fresh
canonical build evidence, current PDF provenance and a sealed technical review.
"""
from pathlib import Path
import json
import zo_publish as p

AUTHORITY=Path('content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/_quy_trinh/ho_so/uy_quyen_phat_hanh_hien_hanh.json')

def verify_files(root, records):
    for name,digest in records.items():
        relative=p.safe_relative(name,'reviewed course file');file=root/relative
        if file.is_symlink() or not file.resolve().is_relative_to(root.resolve()) or not file.is_file() or p.sha256(file)!=digest:
            raise p.ConfigError('Reviewed course file changed or missing: '+name)

def verify_current(root):
    import zo_course_site as site
    from zo_course_site_sources import context as c
    from zo_course_site_sources.guidance_content import GUIDES
    from zo_publish_pdfs import selected_pdfs,validate_pdfs
    import yaml
    if root.resolve()!=c.ROOT.resolve():raise p.ConfigError('Current course release requires the canonical checkout.')
    auth=json.loads((root/AUTHORITY).read_text('utf-8'))
    a=auth.get('authorization',{})
    if not all(a.get(k) is True for k in ['commit','push','publication']) or not a.get('user_message_id') or not a.get('verbatim_user_request'):
        raise p.ConfigError('Explicit current course release authorization is missing.')
    if auth.get('technical_review')!='completed':raise p.ConfigError('Current course technical review is incomplete.')
    expected={x.as_posix() for x in [*c.PAGES.values(),c.FOUNDATION]}
    expected|={(c.HOME/n).as_posix() for n in ['chuyen-de.html','cach-hoc.html','da-luu.html',*[g['file'] for g in GUIDES]]}
    if set(auth['pages'])!=expected:raise p.ConfigError('Current course release page inventory differs.')
    build=json.loads(site.CURRENT.read_text('utf-8'))
    errors=site.freshness(build)
    if not build.get('complete') or set(build['outputs'])!=expected or errors:
        raise p.ConfigError('Current course build is stale/incomplete: '+str(errors[:10]))
    checks=site.local_check([c.OUT/name for name in sorted(expected)])
    if checks['failures']:raise p.ConfigError('Current course links failed: '+str(checks['failures']))
    sources=[]
    for key,page in c.PAGES.items():
        if key=='home':continue
        cfg=root/page.parent/'_quy_trinh/cau_hinh_san_xuat_qmd.yml'
        variants=(yaml.safe_load(cfg.read_text('utf-8')).get('extensions',{}).get('pdf_variants',{}) if cfg.is_file() else {})
        if key=='d0' or variants:sources.append(page.with_suffix('.qmd').as_posix())
    pdf_records=selected_pdfs(root,sources)
    _,config=p.load_config(root,'publish_public.yml')
    errors=validate_pdfs(root,pdf_records,config)
    if errors:raise p.ConfigError('Current course PDF provenance failed: '+str(errors[:8]))
    pdfs={x['path']:p.sha256(root/x['path']) for x in pdf_records}
    if set(auth['pdfs'])!=set(pdfs):raise p.ConfigError('Reviewed PDF inventory differs.')
    verify_files(root,auth['reviewed_files'])
    needed={'docs/'+name for name in expected|set(pdfs)}|set(pdfs)
    if not needed<=set(auth['reviewed_files']):raise p.ConfigError('Review seal omits a course product.')
    raw=p.tree_manifest(c.OUT);missing=[]
    assets=p.asset_dependencies(c.OUT,raw,sorted(expected),missing)
    if missing:raise p.ConfigError('Missing current course assets: '+str(missing))
    selected=expected|set(pdfs)|assets
    for name in selected:
        if auth['reviewed_files'].get('docs/'+name)!=raw['files'][name]['sha256']:
            raise p.ConfigError('Unreviewed current course asset: '+name)
    for name,digest in pdfs.items():
        if p.sha256(c.OUT/name)!=digest:raise p.ConfigError('PDF download differs from canonical source: '+name)
    return {'mode':'current-course','pages':sorted(expected),'pdfs':pdfs,
            'canonical_files':{name:raw['files'][name]['sha256'] for name in selected},
            'authorization_sha256':p.sha256(root/AUTHORITY),
            'build_record_sha256':p.sha256(site.CURRENT),'owner_acceptance_inferred':False}
