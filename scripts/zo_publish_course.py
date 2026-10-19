"""Release the approved canonical course outputs, preserving all other pages.

No historical render, alternate product location, or PDF provenance exemption.
"""
from __future__ import annotations
import json
from datetime import datetime, timezone
from pathlib import Path
from xml.etree import ElementTree as ET
from bs4 import BeautifulSoup
import zo_publish as p
from zo_publish_pages import Timings, finish, merge_indexes, allowed

RECORD = Path('content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/_quy_trinh/ho_so_dong_bo_sau_bang_20261019.json')


def verify_approved(root):
    import yaml
    import zo_web_2027_bundle as bundle
    from zo_review_protection import active_manifests
    from zo_pdf_contract import validate_canonical_pdf_provenance
    from zo_web_2027_d0 import pdf_download
    if root.resolve() != bundle.ROOT.resolve():
        raise p.ConfigError('Approved course verification requires the canonical source checkout.')
    record = json.loads((root/RECORD).read_text(encoding='utf-8'))
    if record.get('owner_acceptance') != 'approved':
        raise p.ConfigError('Current course products have no owner acceptance.')
    manifests = [json.loads(x.read_text(encoding='utf-8')) for x in active_manifests(root)]
    pages = sorted(path.as_posix() for path in bundle.PAGES.values())
    if not any(m['status'] == 'owner_approved' and {'docs/'+x for x in pages} <= set(m['entrypoints']) for m in manifests):
        raise p.ConfigError('All six current HTML pages must have approved protection.')
    bundle.check_current(root/'docs')
    pdfs = {}
    for key, page in bundle.PAGES.items():
        source = root/page.with_suffix('.qmd')
        if key == 'home':
            continue
        if key == 'd0':
            pdf_download(root, page.parent, 'index.pdf')
            variants = {'full': {'output': 'index.pdf'}}
        else:
            config = yaml.safe_load((source.parent/'_quy_trinh/cau_hinh_san_xuat_qmd.yml').read_text(encoding='utf-8'))
            variants = config['extensions']['pdf_variants']
        for variant, definition in variants.items():
            relative = (page.parent/definition['output']).as_posix()
            if key != 'd0':
                errors = validate_canonical_pdf_provenance(root, source, variant=variant)
                if errors:
                    raise p.ConfigError('Stale course PDF '+relative+': '+str(errors))
            digest = p.sha256(root/relative)
            if not (root/'docs'/relative).is_file() or p.sha256(root/'docs'/relative) != digest:
                raise p.ConfigError('Canonical PDF download differs: '+relative)
            pdfs[relative] = digest
    if len(pdfs) != 33:
        raise p.ConfigError('Incomplete current PDF variant inventory.')
    return {'pages': pages, 'pdfs': pdfs, 'record_sha256': p.sha256(root/RECORD),
            'canonical_files': record['canonical_html_build']['files']}


def require_exact_products(tree, docs, pages, pdfs):
    for name in pages:
        if not (tree/name).is_file() or p.sha256(tree/name) != p.sha256(docs/name):
            raise p.ConfigError('Approved HTML bytes changed: '+name)
    for name, digest in pdfs.items():
        if not (tree/name).is_file() or p.sha256(tree/name) != digest:
            raise p.ConfigError('Approved PDF bytes changed: '+name)


def selected_indexes(rendered, pages, config):
    """Derive only selected index records from the exact approved HTML."""
    records = []
    sitemap = ET.Element('urlset', xmlns='http://www.sitemaps.org/schemas/sitemap/0.9')
    for name in pages:
        doc = BeautifulSoup((rendered/name).read_text(encoding='utf-8'), 'html.parser')
        reading = doc.select_one('.home-landing-content, .reader-content')
        if reading is None:
            raise p.ConfigError('Missing canonical reader: '+name)
        for node in reading.select('script,style,nav'):
            node.decompose()
        title = doc.title.get_text(' ', strip=True) if doc.title else name
        records.append({'href': name, 'title': title, 'section': '', 'text': reading.get_text(' ', strip=True)})
        url = ET.SubElement(sitemap, 'url')
        ET.SubElement(url, 'loc').text = 'https://'+config['custom_domain']['cname']+'/'+name
    p.write_text_lf(rendered/'search.json', json.dumps(records, ensure_ascii=False, indent=2)+'\n')
    p.write_text_lf(rendered/'sitemap.xml', ET.tostring(sitemap, encoding='unicode')+'\n')


def candidate(target, docs, rendered, destination, pages, pdfs, config, approved_files=None):
    before = p.tree_manifest(target, True)
    raw = p.tree_manifest(docs)
    missing = []
    dependencies = p.asset_dependencies(docs, raw, pages, missing)
    if missing:
        raise p.ConfigError('Missing canonical dependencies: '+str(sorted(set(missing))))
    selected = set(pages) | set(pdfs) | dependencies
    for name in selected:
        if approved_files is not None and approved_files.get(name) != raw['files'][name]['sha256']:
            raise p.ConfigError('Unsealed canonical dependency: '+name)
        if not allowed(name, config):
            raise p.ConfigError('Canonical dependency not public: '+name)
    rendered.mkdir(parents=True)
    p.copy_manifest(docs, rendered, {'files': {name: raw['files'][name] for name in selected}})
    selected_indexes(rendered, pages, config)
    destination.mkdir(parents=True)
    p.copy_manifest(target, destination, before)
    p.copy_manifest(rendered, destination, p.tree_manifest(rendered))
    merge_indexes(target, rendered, destination, pages, config)
    manifest = p.tree_manifest(destination)
    indexes = p.normalize_public_indexes(destination, manifest, config)
    manifest = p.tree_manifest(destination)
    difference = p.exact_diff(before, manifest)
    issues = list(indexes['issues'])
    issues.extend({'type': 'output-scope', 'path': x} for x in difference['add']+difference['update']+difference['delete'] if x not in selected | {'search.json', 'sitemap.xml'})
    changed_assets = set(difference['update'])-set(pages)-{'search.json','sitemap.xml'}
    for name in before['files']:
        if changed_assets and name.endswith('.html') and name not in pages:
            shared = p.asset_dependencies(target, before, [name]) & changed_assets
            if shared:
                issues.append({'type': 'shared-asset-needs-pages', 'path': name, 'assets': sorted(shared)})
    policy = p.build_manifest(destination, config)
    issues.extend(policy['issues'])
    if {name: {'sha256': item['sha256'], 'size': item['size']} for name, item in policy['files'].items()} != manifest['files']:
        issues.append({'type': 'candidate-manifest-mismatch'})
    validation = p.validate_public(destination, manifest, config)
    issues.extend(validation['issues'])
    issues.extend(p.changed_trailing_whitespace(target, destination, manifest))
    require_exact_products(destination, docs, pages, pdfs)
    return {'manifest': manifest, 'manifest_sha256': p.manifest_digest(manifest), 'diff': difference,
            'target_before_manifest': before, 'target_after_manifest': manifest,
            'validation': validation, 'issues': issues, 'selected_outputs': sorted(selected)}


def validate_receipt(root, target, config, payload):
    seal = verify_approved(root)
    if payload['approved_course']['approval_seal'] != seal:
        raise p.ConfigError('Approved canonical source/output changed after prepare.')
    paths = payload['prepare_paths']
    public, backup, rendered = (root/paths[k] for k in ['public_dir','backup_dir','render_dir'])
    for tree in [target, public, backup, rendered]:
        if p.scan_symlinks(tree, tree == target):
            raise p.ConfigError('Symlink in approved publication tree.')
    if p.tree_manifest(public) != payload['manifest'] or p.tree_manifest(target, True) != payload['manifest']:
        raise p.ConfigError('Approved publication tree changed after prepare.')
    if p.tree_manifest(backup) != payload['target_before_manifest'] or p.tree_manifest(rendered) != payload['approved_course']['render_manifest']:
        raise p.ConfigError('Publication backup or sealed input changed after prepare.')
    require_exact_products(target, root/'docs', seal['pages'], seal['pdfs'])
    policy = p.build_manifest(target, config, True)
    if policy['issues'] or set(policy['files']) != set(payload['manifest']['files']):
        raise p.ConfigError('Approved publication policy mismatch.')
    if any(name not in payload['manifest']['files'] for name in config['required_files']):
        raise p.ConfigError('Missing required public file.')
    result = p.validate_public(target, payload['manifest'], config)
    if result['issues'] or p.changed_trailing_whitespace(backup, target, payload['manifest']):
        raise p.ConfigError('Approved publication validation failed: '+str(result['issues']))
    return result


def prepare(root, target, config_path, config, args, source_state, target_state):
    clock = Timings()
    issues = [{'type': 'source-git', 'message': x} for x in source_state['issues']]
    issues.extend({'type': 'target-git', 'message': x} for x in target_state['issues'])
    if issues:
        raise p.ConfigError(str(issues))
    if p.scan_symlinks(target, True):
        raise p.ConfigError('Symlink in public worktree.')
    report = root/config['prepare']['report_file']
    if report.exists() and json.loads(report.read_text(encoding='utf-8')).get('exit_code') == 0:
        raise p.ConfigError('An existing successful prepare must be validated or published first.')
    seal = verify_approved(root)
    stage = root/config['prepare']['staging_dir']
    if stage.exists():
        raise p.ConfigError('Existing publication stage; refusing to overwrite it.')
    before = p.tree_manifest(target, True)
    payload = {'schema_version': p.REPORT_SCHEMA_VERSION, 'mode': 'prepare', 'config_version': config['version'],
               'config_sha256': p.sha256(config_path), 'config': config_path.relative_to(root).as_posix(),
               'timestamp_utc': datetime.now(timezone.utc).isoformat(), 'repo_root': str(root), 'publish_worktree': str(target),
               'source': source_state, 'target': target_state}
    stage.mkdir(parents=True)
    keep = False
    try:
        p.copy_manifest(target, stage/'backup', before)
        if p.tree_manifest(stage/'backup') != before:
            raise p.RestoreError('Publication backup mismatch.')
        result = candidate(target, root/'docs', stage/'render', stage/'public', seal['pages'], seal['pdfs'], config, seal['canonical_files'])
        payload.update(result)
        payload['prepare_paths'] = {key: f'{config["prepare"]["staging_dir"]}/{folder}' for key, folder in [('render_dir','render'),('public_dir','public'),('backup_dir','backup')]}
        payload['prepare_paths'].update(staging_dir=config['prepare']['staging_dir'], report_file=config['prepare']['report_file'])
        payload['approved_course'] = {'version': 1, 'approval_seal': seal, 'render_manifest': p.tree_manifest(stage/'render'), 'render_performed': False}
        if verify_approved(root) != seal or p.tree_manifest(target, True) != before:
            raise p.ConfigError('Source, approval or public tree changed during prepare.')
        if not result['issues']:
            try:
                p.sync_exact(stage/'public', target, result['manifest'], result['diff'])
                if p.tree_manifest(target, True) != result['manifest'] or p.git_text(target, 'diff', '--cached', '--name-only', safe=target):
                    raise p.RestoreError('Prepared tree/index does not match approved plan.')
            except Exception:
                p.restore_from_backup(target, stage/'backup', before)
                raise
            keep = True
        return finish(root, args, config, payload, clock)
    finally:
        if not keep and stage.exists() and p.tree_manifest(target, True) == before:
            p.safe_remove_tree(stage, root/'_audit')
