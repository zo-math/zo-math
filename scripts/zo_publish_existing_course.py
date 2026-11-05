"""Publish an explicit snapshot as requested, without recertifying its content.

Public policy, source Git, backup, exact-byte seals and deployment guards remain
in the normal publisher. PDFs can only be inherited unchanged from public Git.
"""
import json
from pathlib import Path
import zo_publish as p
from zo_publish_current_course import verify_files

AUTHORITY=Path('content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/_quy_trinh/ho_so/uy_quyen_phat_hanh_ban_hien_co_20261105.json')

def verify_existing(root):
    from zo_course_site_sources import context as c
    from zo_course_site_sources.guidance_content import GUIDES
    if root.resolve()!=c.ROOT.resolve():
        raise p.ConfigError('Existing course release requires the canonical checkout.')
    auth=json.loads((root/AUTHORITY).read_text('utf-8'))
    permission=auth.get('authorization',{})
    if not all(permission.get(k) is True for k in ['commit','push','publication','existing_outputs_without_new_content_review']):
        raise p.ConfigError('Explicit authorization for existing products is missing.')
    if not permission.get('verbatim_user_request') or auth.get('pdf_policy')!='inherit-unchanged-public':
        raise p.ConfigError('Existing-products release must retain public PDFs.')
    expected={x.as_posix() for x in [*c.PAGES.values(),c.FOUNDATION]}
    expected|={(c.HOME/n).as_posix() for n in ['chuyen-de.html','cach-hoc.html','da-luu.html',*[g['file'] for g in GUIDES]]}
    if set(auth['pages'])!=expected:
        raise p.ConfigError('Existing course page inventory differs.')
    verify_files(root,auth['sealed_files'])
    pdfs=auth['pdfs']
    for name,digest in pdfs.items():
        if not name.startswith('content/thpt/on_thi_toan_thpt/hoc_lieu/') or not name.endswith('.pdf'):
            raise p.ConfigError('Invalid inherited course PDF: '+name)
        if auth['sealed_files'].get(name)!=digest or auth['sealed_files'].get('docs/'+name)!=digest:
            raise p.ConfigError('Inherited PDF is not sealed in both canonical locations: '+name)
    raw={'files':{name[5:]:{'sha256':digest} for name,digest in auth['sealed_files'].items() if name.startswith('docs/')}}
    missing=[]
    assets=p.asset_dependencies(root/'docs',raw,sorted(expected),missing)
    if missing:raise p.ConfigError('Missing publication assets: '+str(missing))
    selected=expected|set(pdfs)|assets
    for name in selected:
        if auth['sealed_files'].get('docs/'+name)!=raw['files'][name]['sha256']:
            raise p.ConfigError('Unsealed existing product: '+name)
    return {'mode':'existing-course','pages':sorted(expected),'pdfs':pdfs,
            'inherited_pdfs':pdfs,'canonical_files':{name:raw['files'][name]['sha256'] for name in selected},
            'authorization_sha256':p.sha256(root/AUTHORITY),'owner_acceptance_inferred':False,
            'new_content_review_performed':False}
