"""Refresh shared non-content assets; refuse any other source or HTML drift."""
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ALLOWED = {
    'scripts/zo_course_site.py', 'scripts/zo_course_site_assets.py',
    'scripts/zo_html_preview.py', 'scripts/zo_site_views_dev.py',
    'scripts/zo_course_site_sources/app.js',
    'scripts/zo_course_site_sources/presence.js',
    'scripts/zo_course_site_sources/learning-format.css',
}


def refresh_presence_copy(site, report):
    """Regenerate the canonical QR dialog script without touching page HTML."""
    return refresh_asset(site, report, 'presence.js', lambda _: site.c.presence_script())


def refresh_style_section(site, report, layout, source=None):
    """Apply one declared style section without adopting unrelated CSS changes."""
    from zo_course_site_sections import SECTION_ASSETS, section_style

    names = SECTION_ASSETS.get(layout, ())
    if len(names) != 1 or not names[0].endswith('.css'):
        raise ValueError(f'Expected one stylesheet for the selected section: {layout}')
    name = names[0]

    def render(before):
        source = (site.c.DESIGN/name).read_bytes().replace(b'\r\n', b'\n')
        current = section_style(source, layout)
        if not current:
            raise ValueError(f'Missing stylesheet section: {layout}')
        old = section_style(before, layout)
        return before.replace(old, current, 1) if old else before + b'\n' + current + b'\n'

    if source is None:
        return refresh_asset(site, report, name, render)
    return refresh_versioned_stylesheet(site, report, source.with_suffix('.html'), name, render)


def refresh_versioned_stylesheet(site, report, page, name, render):
    return refresh_versioned_reader_asset(site, report, page, name, render)


def refresh_versioned_reader_asset(site, report, page, name, render):
    """Replace one reader asset binding without reserializing the current HTML."""
    from bs4 import BeautifulSoup
    from zo_course_site_sections import build_lock, digest, publish_changes

    root, context = site.ROOT, site.c
    report = (root / report).resolve()
    if not report.is_relative_to(root / '_audit'):
        raise ValueError('Asset reports belong under _audit')
    output = context.OUT / page
    name_path = Path(name)
    script = name_path.suffix == '.js'
    selector = 'script[src]' if script else 'link[rel="stylesheet"][href]'
    attribute = 'src' if script else 'href'
    tag = 'script' if script else 'link'
    pattern = re.compile(rf'{re.escape(name_path.stem)}\.([0-9a-f]{{16}}){re.escape(name_path.suffix)}')
    manifest = root / context.HOME / '_quy_trinh/ban_dang_duyet.json'

    def encode(data, prior):
        value = json.dumps(data, indent=2, ensure_ascii=False) + '\n'
        return (value.replace('\n', '\r\n') if b'\r\n' in prior else value).encode('utf-8')

    with build_lock(root / '.quarto/course-site-sections.lock'):
        before = output.read_bytes()
        current_bytes = site.CURRENT.read_bytes()
        record = json.loads(current_bytes)
        if digest(before) != record['outputs'].get(page.as_posix()):
            raise ValueError(f'HTML differs from its recorded output: {page}')
        doc = BeautifulSoup(before.decode('utf-8'), 'html.parser')
        links = [link[attribute] for link in doc.select(selector)
                 if pattern.fullmatch(Path(link[attribute]).name)]
        if len(links) != 1:
            raise ValueError(f'Expected one versioned {name} binding: {page}')
        href, = links
        previous = (output.parent / href).resolve()
        if previous.parent != context.ASSETS.resolve():
            raise ValueError(f'Unexpected reader asset location: {href}')
        prior_asset = previous.read_bytes()
        if digest(prior_asset) != record['assets'].get(previous.relative_to(context.OUT).as_posix()):
            raise ValueError(f'Reader asset differs from its recorded output: {href}')
        payload = render(prior_asset)
        payload_hash = digest(payload)
        target = context.ASSETS / f'{name_path.stem}.{payload_hash[:16]}{name_path.suffix}'
        asset = target.relative_to(context.OUT).as_posix()
        prefix = rf'''(<{tag}\b[^>]*\b{attribute}\s*=\s*["'])'''.encode()
        old_binding = re.compile(prefix + re.escape(href.encode()) + rb'''(["'])''')
        after, count = old_binding.subn(lambda match: match[1] + href.replace(previous.name, target.name).encode()
                                        + match[2], before)
        if count != 1:
            raise ValueError(f'Expected one reader asset reference in the HTML source: {page}')
        if not target.exists():
            with target.open('xb') as file:
                file.write(payload)
        if target.read_bytes() != payload:
            raise ValueError(f'Versioned reader asset differs from its content digest: {target}')
        record['assets'][asset] = payload_hash
        record['outputs'][page.as_posix()] = digest(after)
        next_record = encode(record, current_bytes)
        manifest_bytes = manifest.read_bytes()
        protection = json.loads(manifest_bytes)
        entries = {entry['path']: entry for entry in protection['files']}
        for path, sha in ((target, payload_hash), (output, digest(after)), (site.CURRENT, digest(next_record))):
            relative = path.relative_to(root).as_posix()
            entries[relative] = dict(path=relative, sha256=sha)
        protection['files'] = [entries[key] for key in sorted(entries, key=Path)]
        publish_changes({output: (before, after), site.CURRENT: (current_bytes, next_record),
                         manifest: (manifest_bytes, encode(protection, manifest_bytes))})
    report.parent.mkdir(parents=True, exist_ok=True)
    result = {'page': page.as_posix(), 'asset': asset, 'sha256': payload_hash, 'updated': before != after}
    report.write_bytes(encode(result, b''))
    print(json.dumps(result, ensure_ascii=False))


def refresh_asset(site, report, name, render):
    from zo_course_site_sections import build_lock, digest, publish_changes

    root, context = site.ROOT, site.c
    report = (root / report).resolve()
    if not report.is_relative_to(root / '_audit'):
        raise ValueError('Asset reports belong under _audit')
    target = context.ASSETS / name
    asset = target.relative_to(context.OUT).as_posix()
    manifest = root / context.HOME / '_quy_trinh/ban_dang_duyet.json'

    def encode(data):
        return (json.dumps(data, ensure_ascii=False, indent=2) + '\n').encode('utf-8')

    with build_lock(root / '.quarto/course-site-sections.lock'):
        before = target.read_bytes()
        current_bytes = site.CURRENT.read_bytes()
        record = json.loads(current_bytes)
        if digest(before) != record['assets'].get(asset):
            raise ValueError(f'Asset differs from its recorded output: {asset}')
        after = render(before)
        record['assets'][asset] = digest(after)
        manifest_bytes = manifest.read_bytes()
        protection = json.loads(manifest_bytes)
        paths = {target.relative_to(root).as_posix(): digest(after),
                 site.CURRENT.relative_to(root).as_posix(): digest(encode(record))}
        for entry in protection['files']:
            if entry['path'] in paths:
                entry['sha256'] = paths.pop(entry['path'])
        if paths:
            raise ValueError('Missing asset or current build in the protection manifest')
        publish_changes({target: (before, after),
                         site.CURRENT: (current_bytes, encode(record)),
                         manifest: (manifest_bytes, encode(protection))})
    report.parent.mkdir(parents=True, exist_ok=True)
    result = {'asset': asset, 'sha256': digest(after), 'updated': before != after, 'HTML_unchanged': True}
    report.write_bytes(encode(result))
    print(json.dumps(result, ensure_ascii=False))


def refresh_reader_catalog(site, source):
    """Update navigation, its data and asset URLs without rendering content."""
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
        text = context.limit_reader_catalog(before.decode('utf-8'), page)
        installed = context.editorial_assets(page, installed_hashes=prior['assets'])
        for original, versioned in installed.items():
            unversioned = context.rel(context.ASSETS.relative_to(context.OUT) / original, page)
            new_url = context.rel(versioned, page)
            attribute = 'src' if original.endswith('.js') else 'href'
            tag = 'script' if attribute == 'src' else 'link'
            binding = re.compile(rf'''(<{tag}\b[^>]*\b{attribute}=["']){re.escape(unversioned)}(["'])''')
            text, count = binding.subn(lambda match: match[1] + new_url + match[2], text)
            if count:
                prior['assets'][versioned.as_posix()] = site.sha(context.OUT / versioned)
        after = text.encode('utf-8')
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


def refresh_reader_nav_labels(site, report):
    """Project shared navigation and reader labels into the current course."""
    from zo_course_site_sections import build_lock, digest, publish_changes
    from zo_course_site_sources import build

    root, context = site.ROOT, site.c
    report = (root / report).resolve()
    if not report.is_relative_to(root / '_audit'):
        raise ValueError('Reader label reports belong under _audit')
    nav = re.compile(rb'<nav\b[^>]*\bclass="lesson-nav"[^>]*>.*?</nav>', re.DOTALL)
    label = re.compile(rb'<span class="nav-label">([^<]*)</span>')
    full_text = re.compile(rb'(<a\b[^>]*data-view="toan-van"[^>]*>.*?<span>)[^<]*(</span>\s*</a>)', re.DOTALL)
    app_binding = re.compile(rb'(<script\b[^>]*\bsrc=")([^"]*/app(?:\.[0-9a-f]{16})?\.js)(")')
    app_label = re.compile(rb"'toan-van':'[^']*'")
    title = build.FULL_TEXT_LABEL.encode()
    runtime_source = context.DESIGN / 'app.js'
    runtime_name = runtime_source.relative_to(root).as_posix()
    manifest_path = root / context.HOME / '_quy_trinh/ban_dang_duyet.json'
    source = Path(build.__file__).resolve()
    source_name = source.relative_to(root).as_posix()

    def encode(record, previous):
        value = json.dumps(record, ensure_ascii=False, indent=2) + '\n'
        return (value.replace('\n', '\r\n') if b'\r\n' in previous else value).encode()

    with build_lock(root / '.quarto/course-site-sections.lock'):
        record_bytes = site.CURRENT.read_bytes()
        record = json.loads(record_bytes)
        old_source = record['inputs'][source_name]
        new_source = site.sha(source)
        old_runtime_source = record['inputs'][runtime_name]
        new_runtime_source = site.sha(runtime_source)
        changes = {}
        bindings = {}
        new_assets = {}
        updated = []
        unverified = {}
        for key in context.KEYS:
            name = context.PAGES[key].as_posix()
            file = context.OUT / name
            before = file.read_bytes()
            recorded = record['outputs'].get(name)
            if not recorded or b'data-zo-course-site=' not in before:
                raise ValueError(f'Expected current course HTML: {name}')
            actual = digest(before)
            if actual != recorded:
                unverified[name] = {'recorded': recorded, 'before': actual}
            current = list(nav.finditer(before))
            if len(current) != 1:
                raise ValueError(f'Expected one lesson navigation: {name}')
            expected = nav.search(build.side_nav({'id': key, 'title': '', 'has_pdf': False}, []).encode())
            labels = label.findall(expected[0])
            spans = list(label.finditer(current[0].group()))
            if len(spans) != len(labels):
                raise ValueError(f'Reader group structure differs: {name}')
            after_nav = current[0].group()
            for item, text in reversed(list(zip(spans, labels))):
                start, end = item.span(1)
                after_nav = after_nav[:start] + text + after_nav[end:]
            after_nav, count = full_text.subn(lambda match: match[1] + title + match[2], after_nav)
            if count != 1:
                raise ValueError(f'Expected one full-text navigation link: {name}')
            after = before[:current[0].start()] + after_nav + before[current[0].end():]

            scripts = list(app_binding.finditer(after))
            if len(scripts) != 1:
                raise ValueError(f'Expected one reader script: {name}')
            script, = scripts
            previous = (file.parent / script[2].decode()).resolve()
            if previous.parent != context.ASSETS.resolve():
                raise ValueError(f'Unexpected reader script: {previous}')
            if previous not in bindings:
                prior = previous.read_bytes()
                asset = previous.relative_to(context.OUT).as_posix()
                if digest(prior) != record['assets'].get(asset):
                    raise ValueError(f'Reader script differs from its recorded output: {asset}')
                payload, count = app_label.subn(b"'toan-van':'" + title + b"'", prior)
                if count != 1:
                    raise ValueError(f'Expected one full-text runtime label: {asset}')
                if payload == prior or previous.name == 'app.js':
                    target = previous
                    if payload != prior:
                        changes[target] = prior, payload
                else:
                    target = previous.with_name(f'app.{digest(payload)[:16]}.js')
                    new_assets[target] = payload
                record['assets'][target.relative_to(context.OUT).as_posix()] = digest(payload)
                bindings[previous] = target
            target = bindings[previous]
            if target != previous:
                start, end = script.span(2)
                after = after[:start] + script[2].removesuffix(previous.name.encode()) + target.name.encode() + after[end:]
            if after != before:
                changes[file] = before, after
                record['outputs'][name] = digest(after)
                updated.append(name)
        if changes:
            record['inputs'][source_name] = new_source
            record['inputs'][runtime_name] = new_runtime_source
            for page, inputs in record['page_inputs'].items():
                if page not in unverified:
                    if inputs.get(source_name) == old_source:
                        inputs[source_name] = new_source
                    if inputs.get(runtime_name) == old_runtime_source:
                        inputs[runtime_name] = new_runtime_source
            record['pending_pages'] = site.scope_state(record)[2]
            record['reader_nav_labels'] = {'pages_updated': updated, 'prior_html_mismatches': unverified}
            changes[site.CURRENT] = record_bytes, encode(record, record_bytes)
            manifest_bytes = manifest_path.read_bytes()
            manifest = json.loads(manifest_bytes)
            entries = {item['path']: item for item in manifest['files']}
            protected = {file: after for file, (_, after) in changes.items()}
            protected.update(new_assets)
            protected.update({source: source.read_bytes(), runtime_source: runtime_source.read_bytes()})
            for file, content in protected.items():
                name = file.relative_to(root).as_posix()
                entries[name] = {'path': name, 'sha256': digest(content)}
            manifest['files'] = [entries[name] for name in sorted(entries, key=Path)]
            manifest['updated_at'] = datetime.now(timezone.utc).isoformat()
            changes[manifest_path] = manifest_bytes, encode(manifest, manifest_bytes)
            for file, payload in new_assets.items():
                if not file.exists():
                    with file.open('xb') as stream:
                        stream.write(payload)
                if file.read_bytes() != payload:
                    raise ValueError(f'Versioned reader script differs from its content digest: {file}')
            publish_changes(changes)
    result = {'readers_checked': len(context.KEYS), 'pages_updated': updated, 'prior_html_mismatches': unverified}
    report.parent.mkdir(parents=True, exist_ok=True)
    site.save(report, result)
    print(f"Reader navigation labels: {len(updated)} updated, {len(context.KEYS)} checked")

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
