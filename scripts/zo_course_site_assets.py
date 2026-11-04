"""Refresh shared non-content assets; refuse any other source or HTML drift."""
import json
from datetime import datetime, timezone

ALLOWED = {
    'scripts/zo_course_site.py', 'scripts/zo_course_site_assets.py',
    'scripts/zo_html_preview.py', 'scripts/zo_site_views_dev.py',
    'scripts/zo_course_site_sources/app.js',
    'scripts/zo_course_site_sources/presence.js',
    'scripts/zo_course_site_sources/learning-format.css',
}

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
    from zo_course_site_scope import page_inputs
    record = dict(prior, inputs=current)
    record['page_inputs'] = page_inputs(root, context, current, site.catalog_metadata(), prior['table_profiles'])
    record['pending_pages'] = {}
    record['assets'] = {p.relative_to(context.OUT).as_posix():site.sha(p) for p in context.ASSETS.rglob('*') if p.is_file()}
    record['shared_asset_refresh'] = {'at':datetime.now(timezone.utc).isoformat(),'changed':sorted(changed),'HTML_unchanged':True}
    site.save(site.CURRENT, record)
    from zo_course_site_protection import refresh
    refresh(root, context, record)
    site.save(root/report, record['shared_asset_refresh'])
    print('Shared assets refreshed; all existing HTML preserved')
    return 0
