"""Publish the one current HTML tree. No render or dated acceptance record."""
import json
from pathlib import Path
import zo_publish as p
from zo_publish_current_course import verify_files


def course_pages():
    from zo_course_site_sources import context as c
    from zo_course_site_sources.guidance_content import GUIDES
    return sorted({x.as_posix() for x in [*c.PAGES.values(),c.FOUNDATION]} |
                  {(c.HOME/n).as_posix() for n in
                   ['chuyen-de.html','cach-hoc.html','da-luu.html',*[g['file'] for g in GUIDES]]})


def snapshot(root, target, pages=None, pdfs=None):
    from zo_course_site_sources import context as c
    from zo_html_dependencies import preview_files
    root=Path(root).resolve();docs=root/'docs';explicit=pages is not None
    known=set(course_pages())
    pages=sorted({p.safe_relative(name,'existing HTML page') for name in pages}) if explicit else sorted(known)
    selected_pdfs={p.safe_relative(name,'existing PDF') for name in (pdfs or [])}
    if not pages or any(not name.endswith('.html') for name in pages):
        raise p.ConfigError('Select existing HTML output paths.')
    record=json.loads((root/c.HOME/'_quy_trinh/ho_so/current_site_build.json').read_text('utf-8')) if known.intersection(pages) else {}
    for name in pages:
        file=docs/name
        if not file.is_file() or (name in known and record.get('outputs',{}).get(name)!=p.sha256(file)):
            raise p.ConfigError('Build the changed course HTML first: '+name)
    # Resolve this publication's actual files, not every historical file in docs.
    files=preview_files(root,[docs/name for name in [*pages,*selected_pdfs]])
    for file in list(files):
        if file.suffix.lower() in {'.ttf','.otf','.woff','.woff2'}:
            files.update(file.parent.glob('OFL*.txt'))
    canonical={}
    referenced_pdfs=set()
    for file in sorted(files):
        if file.is_symlink() or not file.resolve().is_relative_to(docs.resolve()):
            raise p.ConfigError('Course dependency outside canonical docs: '+str(file))
        name=file.relative_to(docs).as_posix()
        if file.suffix.lower()=='.pdf' and name not in selected_pdfs:referenced_pdfs.add(name)
        else:canonical[name]=p.sha256(file)
    before=p.tree_manifest(target,True)
    preserved={name:item['sha256'] for name,item in before['files'].items()
               if name.endswith('.pdf') and name not in selected_pdfs}
    pdf_hashes={name:canonical[name] for name in selected_pdfs}
    verify_files(root,pdf_hashes)
    if not referenced_pdfs<=set(preserved):
        raise p.ConfigError('New PDF requires an explicit PDF release: '+str(sorted(referenced_pdfs-set(preserved))))
    return {'mode':'built-pages' if explicit else 'course-html','pages':pages,'pdfs':pdf_hashes,'preserved_pdfs':preserved,
            'canonical_files':canonical,'render_performed':False,
            'new_content_review_performed':False,'owner_acceptance_inferred':False}


def verify_snapshot(root, seal):
    if seal.get('mode') not in {'course-html','built-pages'} or not isinstance(seal.get('pdfs'),dict):
        raise p.ConfigError('Invalid current HTML publication snapshot.')
    if seal['mode']=='course-html' and seal.get('pages')!=course_pages():
        raise p.ConfigError('Invalid course HTML inventory.')
    if seal['mode']=='built-pages' and (not seal.get('pages') or any(
            p.safe_relative(name,'existing HTML page')!=name or not name.endswith('.html') for name in seal['pages'])):
        raise p.ConfigError('Invalid selected HTML inventory.')
    verify_files(Path(root),{'docs/'+name:digest for name,digest in seal['canonical_files'].items()})
    verify_files(Path(root),seal['pdfs'])
    if any(seal['canonical_files'].get(name)!=digest for name,digest in seal['pdfs'].items()):
        raise p.ConfigError('Selected existing PDF differs between canonical and public locations.')
    if not set(seal['pages'])<=set(seal['canonical_files']):
        raise p.ConfigError('Current HTML snapshot omits a course page.')
    return seal
