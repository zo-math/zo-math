"""Per-output build evidence: partial work never certifies untouched pages."""
import hashlib
import json
from pathlib import Path

TABLES = '_design/web_2027_mau_dung_chung/profiles/course-tables.json'


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, default=str).encode()).hexdigest()


def catalog_view(metadata):
    return {key: {'title': value.get('title'),
                  'has_pdf': bool(value.get('r1-download-files') or value.get('r1-section-download-files'))}
            for key, value in metadata.items() if key != 'home'}


def table_view(tables, key):
    return dict(shared={k: v for k, v in tables.items() if k != 'pages'},
                page=tables.get('pages', {}).get(key))


def page_inputs(root, context, inputs, metadata, tables=None):
    """Split file ownership; retain shared dependencies and explicit includes/assets."""
    from zo_course_editorial import closure
    root = Path(root)
    pages = {**context.PAGES, 'foundation': context.FOUNDATION}
    owners = {key: page.with_suffix('.qmd') for key, page in pages.items()}
    covers = set()
    for key, source in owners.items():
        cover = root / source.parent / 'giao_dien/anh_bia.json'
        if cover.is_file():
            covers.add(cover.relative_to(root).as_posix())
            covers.add((source.parent / json.loads(cover.read_text('utf-8'))['image']).as_posix())
    result = {}
    for key, source in owners.items():
        explicit = set()
        for file, body in closure(root / source, root).items():
            explicit.add(file.relative_to(root).as_posix())
            import re
            for ref in re.findall(r'(?:src=["\']|\]\()([^"\'\s)>]+)', body):
                if '://' in ref: continue
                target = (file.parent / ref.split('#', 1)[0].split('?', 1)[0]).resolve()
                if target.is_relative_to(root) and target.suffix.lower() not in {'.html', '.qmd', ''}:
                    explicit.add(target.relative_to(root).as_posix())
        selected = {}
        for name, value in inputs.items():
            path = Path(name)
            owner = next((k for k, s in owners.items()
                          if path == s or (k != 'home' and s.name == 'index.qmd' and path.is_relative_to(s.parent))), None)
            # Other lessons' prose and private assets are not dependencies.
            if owner is not None and owner != key and name not in explicit and name not in covers:
                continue
            # Shared foundation QMD is needed only by actual includes, not by a hyperlink.
            if path.suffix == '.qmd' and name not in explicit:
                continue
            if name == TABLES and tables is not None:
                selected['@table-profile'] = digest(table_view(tables, key))
            else:
                selected[name] = value
        selected['@catalog'] = digest(catalog_view(metadata))
        result[pages[key].as_posix()] = selected
    from zo_course_site_sources.guidance_content import GUIDES
    for name in ['chuyen-de.html', 'cach-hoc.html', 'da-luu.html', *[g['file'] for g in GUIDES]]:
        result[(context.HOME / name).as_posix()] = dict(result[context.PAGES['home'].as_posix()])
    return result


def baseline(root, context, record, current_inputs, current_tables):
    if 'page_inputs' in record:
        return record['page_inputs']
    # Legacy evidence can be split only when the old table bytes are known.
    tables = record.get('table_profiles')
    if tables is None and record.get('inputs', {}).get(TABLES) == current_inputs.get(TABLES):
        tables = current_tables
    return page_inputs(root, context, record.get('inputs', {}),
                       record.get('catalog_metadata', {}), tables)


def merge_evidence(previous, current, rendered):
    merged = dict(previous)
    for page in rendered:
        if page in current:
            merged[page] = current[page]
    return merged


def stale_pages(previous, current):
    return {page: sorted(k for k in set(previous.get(page, {})) | set(values)
                         if previous.get(page, {}).get(k) != values.get(k))
            for page, values in current.items() if previous.get(page) != values}
