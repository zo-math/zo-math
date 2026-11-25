"""Refresh shared non-content assets; refuse any other source or HTML drift."""
import json
from datetime import datetime, timezone
from pathlib import Path

ALLOWED = {
    'scripts/zo_course_site.py', 'scripts/zo_course_site_assets.py',
    'scripts/zo_html_preview.py', 'scripts/zo_site_views_dev.py',
    'scripts/zo_course_site_sources/app.js',
    'scripts/zo_course_site_sources/presence.js',
    'scripts/zo_course_site_sources/learning-format.css',
}


def refresh_reader_catalog(site, source):
    """Update navigation and its data without regenerating learning content."""
    from zo_course_site_sections import build_lock
    from zo_course_site_protection import refresh

    root, context = site.ROOT, site.c
    page = source.with_suffix('.html')
    name = page.as_posix()
    config = source.parent / 'giao_dien/html.json'
    allowed = {'scripts/zo_course_site.py', 'scripts/zo_course_site_assets.py',
               'scripts/zo_course_site_sources/context.py',
               'scripts/zo_course_site_sources/README.md', config.as_posix()}
    with build_lock(root/'.quarto/course-site-sections.lock'):
        prior = json.loads(site.CURRENT.read_text('utf-8'))
        _, current, pending, _ = site.scope_state(prior)
        if set(pending.get(name, [])) - allowed:
            raise ValueError(f'Other reader inputs changed: {pending[name]}')
        target = context.OUT / page
        if site.sha(target) != prior['outputs'].get(name):
            raise ValueError(f'Expected the verified current HTML: {name}')
        before = target.read_bytes()
        after = context.limit_reader_catalog(before.decode('utf-8'), page).encode('utf-8')
        target.write_bytes(after)
        try:
            result = site.local_check([target])
            if result['failures']:
                raise ValueError(str(result['failures']))
        except Exception:
            target.write_bytes(before)
            raise
        prior['inputs'] = site.live_inputs()
        prior['outputs'][name] = site.sha(target)
        prior['page_inputs'][name] = current[name]
        prior['pending_pages'] = {key: reasons for key, reasons in pending.items() if key != name}
        site.save(site.CURRENT, prior)
        refresh(root, context, prior)
        return result

def apply(site, report):
    root, context = site.ROOT, site.c
    prior = json.loads(site.CURRENT.read_text('utf-8'))
    current = site.live_inputs()
    changed = {p for p in set(current) | set(prior['inputs']) if current.get(p) != prior['inputs'].get(p)}
    if not changed <= ALLOWED:
        raise ValueError('Non-asset source changes require normal render: '+str(sorted(changed-ALLOWED)))
    pending = site.scope_state(prior)[2]
    unrendered = {name for causes in pending.values() for name in causes} - ALLOWED
    if unrendered:
        raise ValueError('Previously pending content requires normal render: '+str(sorted(unrendered)))
    for name, digest in prior['outputs'].items():
        if site.sha(context.OUT/name) != digest:
            raise ValueError('HTML changed: '+name)
    for name, digest in prior['assets'].items():
        if site.sha(context.OUT/name) != digest:
            raise ValueError('Previous asset changed outside builder: '+name)
    # No HTML is parsed, rewritten or adopted as native render input.
    site.install_assets()
    from zo_course_site_output import normalize_lines
    normalized=normalize_lines(root,context.OUT,[p for p in context.ASSETS.rglob('*') if p.is_file()])
    from zo_course_site_scope import page_inputs
    record = dict(prior, inputs=current)
    record['page_inputs'] = page_inputs(root, context, current, site.catalog_metadata(), prior['table_profiles'])
    record['pending_pages'] = {}
    record['assets'] = {p.relative_to(context.OUT).as_posix():site.sha(p) for p in context.ASSETS.rglob('*') if p.is_file()}
    record['shared_asset_refresh'] = {'at':datetime.now(timezone.utc).isoformat(),'changed':sorted(changed),'HTML_unchanged':True,'normalized_asset_line_endings':normalized}
    site.save(site.CURRENT, record)
    from zo_course_site_protection import refresh
    refresh(root, context, record)
    site.save(root/report, record['shared_asset_refresh'])
    print('Shared assets refreshed; all existing HTML preserved')
    return 0
