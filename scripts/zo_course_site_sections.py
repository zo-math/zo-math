"""Render named QMD fragments and replace only the corresponding HTML interiors."""
from collections import Counter
from contextlib import contextmanager
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
import hashlib
import os
import re
import subprocess
import sys
from tempfile import TemporaryDirectory
from urllib.parse import unquote, urlsplit

from bs4 import BeautifulSoup
from zo_course_editorial import closure
from zo_course_site_sources import context as c


SECTION_ASSETS = {
    'overview': ('learning-format.css',),
    'lesson-intro': ('learning-format.css', 'app.js'),
    'lesson-activity': ('learning-format.css',),
}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def section_style(css, layout):
    start = f'/* zo-section-style {layout} */'.encode()
    end = b'/* /zo-section-style */'
    if start not in css:
        return b''
    body, marker, _ = css.split(start, 1)[1].partition(end)
    if css.count(start) != 1 or not marker or b'/* zo-section-style ' in body:
        raise ValueError('Ambiguous CSS section: ' + layout)
    return start + body + end


@dataclass(frozen=True)
class Section:
    owner: Path
    target: str
    layout: str
    markdown: str
    includes: tuple = ()

    def signature(self):
        renderer = Path(__file__).read_bytes()
        if self.layout == 'overview':
            from zo_course_site_sources.build import ICONS, icon
            renderer += ''.join(icon(key) for key in sorted(ICONS)).encode()
        for name in SECTION_ASSETS.get(self.layout, ()):
            data = (c.DESIGN/name).read_bytes()
            renderer += section_style(data, self.layout) if name.endswith('.css') else data
        return digest(b'\0'.join((self.markdown.encode(), self.layout.encode(), renderer)))


def declarations(source, root=None, *, output=None):
    """Follow actual course includes, so one shared source has all its consumers."""
    found = {}
    sources = closure(source, root or c.ROOT)
    include_line = re.compile(r'(?m)^ *\{\{<\s*include\s+([^>]+?)\s*>\}\} *$')
    def expand(markdown, owner, chain, used):
        def substitute(match):
            path = (owner.parent / match[1].strip().strip('"')).resolve()
            if path in chain or path not in sources:
                raise ValueError('Invalid or cyclic fragment include: ' + str(path))
            used.add(path)
            return expand(sources[path], path, chain | {path}, used)
        return include_line.sub(substitute, markdown)
    for owner, text in sources.items():
        active = None
        fence = None
        lines = text.splitlines(keepends=True)
        for index, line in enumerate(lines):
            stripped = line.strip()
            code = re.match(r'^ {0,3}(\x60{3,}|~{3,})', line)
            if fence:
                if stripped == fence or (stripped.startswith(fence) and set(stripped) == {fence[0]}):
                    fence = None
                continue
            if code:
                fence = code[1]
                continue
            if stripped == '<!-- /zo-section -->' and active:
                start, target, layout, destination = active
                if destination != output:
                    active = None
                    continue
                markdown = ''.join(lines[start:index]).strip()
                if target in found or not markdown:
                    raise ValueError(f'Duplicate or empty section {target} in {source}')
                used = set()
                markdown = expand(markdown, owner, {owner}, used)
                found[target] = Section(owner, target, layout, markdown, tuple(sorted(used)))
                active = None
            elif re.match(r'<!--\s*/?zo-section\b', stripped):
                marker = re.fullmatch(r'<!-- zo-section ([\w.-]+)(?: (markdown|overview|lesson-intro|lesson-activity))?(?: output=([\w-]+\.html))? -->', stripped)
                if not marker or active:
                    raise ValueError(f'Invalid or nested section at {owner}:{index + 1}')
                active = (index + 1, marker[1], marker[2] or 'markdown', marker[3])
        if active:
            raise ValueError(f'Unclosed section {active[1]} in {owner}')
    return found


def overview(doc):
    """Project the QMD introduction, linked choices, goals and prerequisite."""
    from zo_course_site_sources.build import icon, MODES
    from html import escape
    *intro, choose, choices, goals, table, prior = [n for n in doc.children if n.name]
    if (not intro or any(p.name != 'p' for p in intro)
            or (choose.name, choices.name, goals.name, prior.name) != ('p','ul','p','p')):
        raise ValueError('Overview needs an introduction, choices, goals and prerequisites')
    rows = table.select('tbody > tr')
    symbols = {target: symbol for target, _, _, symbol in MODES}
    # Align the drawn left edges to the book at x=2 in the 24-unit icon grid.
    left_offsets = {'check': 3, 'repeat': 1}
    actions = []
    help_heading = choose.select_one('[data-choice-help]')
    definitions = []
    seen = set()
    for row in choices.find_all('li', recursive=False):
        link = row.find('a', href=True)
        if link is None or link['href'][1:] not in symbols or not link['href'].startswith('#'):
            raise ValueError('Unknown overview navigation link')
        href = link['href']
        if href in seen:
            raise ValueError('Duplicate overview navigation link: ' + href)
        seen.add(href)
        label = link.decode_contents()
        link.extract()
        description = row.decode_contents().strip().removeprefix('—').strip()
        symbol = symbols[href[1:]]
        leading_icon = icon(symbol, size=17, viewbox_x=left_offsets.get(symbol, 0))
        caption = f'<br>{description}'
        if help_heading:
            definitions.append(f'<div><dt>{label}</dt><dd>{description}</dd></div>')
            caption = ''
        actions.append(f'<li><a href="{href}"><span><strong style="display:inline-flex;align-items:center;gap:11px">'
                       f'{leading_icon}<span>{label}</span></strong>'
                       f'{caption}</span>{icon("arrow")}</a></li>')
    if len(actions) != len(symbols) or not rows or prior.find('strong') is None:
        raise ValueError('Incomplete overview')
    items = []
    # Reuse the course guidance link colors for running text only. Navigation
    # cards already expose their own pointer and keyboard states.
    for node in [*intro, table, prior]:
        for link in node.select('a[href]'):
            link.wrap(doc.new_tag('span', attrs={'class': 'guidance-section', 'style': 'display:contents'}))
    for row in rows:
        cells = row.find_all(['td', 'th'], recursive=False)
        if len(cells) != 2:
            raise ValueError('Each overview goal needs a label and a self-check')
        items.append('<li>' + cells[1].decode_contents() + '</li>')
    prior_title = prior.strong.extract().get_text(strip=True).rstrip('.')
    def group(anchor, title, body):
        return (f'<section class="topic-overview-section" id="{anchor}">'
                f'<h2>{escape(title)}</h2>{body}</section>')
    navigation = '<nav aria-label="Chọn phần học"><ul class="topic-outline">' + ''.join(actions) + '</ul></nav>'
    if help_heading:
        question = escape(help_heading['data-choice-help'])
        navigation += (f'<details class="overview-choice-help"><summary>{question}</summary>'
                       + '<dl>' + ''.join(definitions) + '</dl></details>')
    return ('<section class="overview-introduction" id="overview-introduction" data-reading-scale aria-label="Giới thiệu chuyên đề">'
            + ''.join(map(str, intro)) + '</section>'
            + group('overview-start', choose.get_text(strip=True), navigation)
            + group('overview-goals', goals.get_text(strip=True),
                    '<ul class="overview-goals" style="row-gap:.65em">' + ''.join(items) + '</ul>')
            + group('overview-prerequisites', prior_title, '<p>' + prior.decode_contents().strip() + '</p>'))


def render(section):
    if '{{<' in section.markdown or re.search(r'(?m)^\s*(?:\x60{3,}|~{3,})\s*\{[a-zA-Z]', section.markdown):
        raise ValueError(f'{section.target}: executable cells and Quarto shortcodes require native processing')
    command = [sys.executable, '-B', str(c.ROOT/'scripts/zo_python.py'), '-B',
               str(c.ROOT/'scripts/zo_quarto.py'), 'pandoc', '-f', 'markdown',
               '-t', 'html5', '--mathml', '--wrap=none']
    # Read the output file to avoid truncating long MathML lines in Quarto's stdout relay.
    scratch = c.ROOT / '.quarto'
    scratch.mkdir(exist_ok=True)
    with TemporaryDirectory(dir=scratch) as folder:
        output = Path(folder) / 'fragment.html'
        result = subprocess.run([*command, '-o', str(output)], input=section.markdown, text=True,
                                encoding='utf-8', cwd=c.ROOT, capture_output=True, check=False)
        if result.returncode:
            raise ValueError(f'{section.target}: {result.stderr.strip()}')
        doc = BeautifulSoup(output.read_text(encoding='utf-8'), 'html.parser')
    if section.layout == 'lesson-activity':
        title = doc.select_one('p:first-child > strong:only-child')
        if title is None:
            raise ValueError(f'{section.target}: expected a bold activity title')
        title['class'] = ['zo-task-title']
    raw = overview(doc) if section.layout == 'overview' else str(doc).strip()
    if section.layout == 'lesson-intro':
        raw += '<span hidden data-lesson-intro-end></span>'
    return str(BeautifulSoup(raw, 'html.parser'))


class Locations(HTMLParser):
    """Find exact source offsets without reserializing the surrounding page."""
    def __init__(self, text, targets):
        super().__init__(convert_charrefs=False)
        self.lines = [0] + [m.end() for m in re.finditer('\n', text)]
        self.targets = targets
        self.ids = Counter()
        self.spans = {}
        self.active = None
        self.feed(text)
        self.close()
        if self.active or set(targets) != self.spans.keys():
            raise ValueError('Missing or unclosed section: ' + str(set(targets) - self.spans.keys()))

    def source_position(self):
        line, column = self.getpos()
        return self.lines[line - 1] + column

    def handle_starttag(self, tag, attrs):
        key = dict(attrs).get('id')
        if key:
            self.ids[key] += 1
        if key in self.targets:
            if self.active or key in self.spans or tag not in {'section','article','div','main','aside','nav','details'}:
                raise ValueError(f'Ambiguous, nested or invalid HTML target: {key}')
            self.active = (key, tag, self.source_position() + len(self.get_starttag_text()))
            self.depth = 1
        elif self.active and tag == self.active[1]:
            self.depth += 1

    def handle_endtag(self, tag):
        if self.active and self.active[1] == tag:
            self.depth -= 1
            if not self.depth:
                key, _, start = self.active
                self.spans[key] = (start, self.source_position())
                self.active = None


def project(text, fragments, output):
    if not fragments:
        return text, {}
    index = Locations(text, fragments)
    ids = index.ids.copy()
    evidence = {}
    links = []
    for key, (start, end) in index.spans.items():
        before = text[start:end]
        old = BeautifulSoup(before, 'html.parser')
        new = BeautifulSoup(fragments[key], 'html.parser')
        old_ids = Counter(n['id'] for n in old.select('[id]'))
        new_ids = Counter(n['id'] for n in new.select('[id]'))
        if old_ids.keys() - new_ids.keys():
            raise ValueError(f'{key}: removing existing anchors needs migration: {old_ids.keys() - new_ids.keys()}')
        ids.subtract(old_ids)
        ids.update(new_ids)
        links.extend(n[attr] for attr in ('href','src','poster') for n in new.select(f'[{attr}]'))
        evidence[key] = {'previous': digest(before.encode()), 'html': digest(fragments[key].encode())}
        evidence[key]['ids'] = list(new_ids)
    for key, data in evidence.items():
        if any(ids[i] != 1 for i in data.pop('ids')):
            raise ValueError(f'{key}: duplicate HTML anchor')
    for value in links:
        url = urlsplit(value)
        if url.scheme or url.netloc:
            continue
        if not url.path and url.fragment and ids[unquote(url.fragment)] != 1:
            raise ValueError('Missing or ambiguous target: ' + value)
        if url.path:
            path = (c.OUT / unquote(url.path).lstrip('/') if url.path.startswith('/')
                    else output.parent / unquote(url.path)).resolve()
            if not path.is_relative_to(c.OUT) or not path.is_file():
                raise ValueError('Missing local section resource: ' + value)
    for key, (start, end) in sorted(index.spans.items(), key=lambda pair: pair[1][0], reverse=True):
        text = text[:start] + fragments[key] + text[end:]
    return text, evidence


@contextmanager
def build_lock(path):
    """An OS lock is released even if a concurrent builder is interrupted."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('a+b') as stream:
        if not stream.tell():
            stream.write(b'0')
            stream.flush()
        stream.seek(0)
        if os.name == 'nt':
            import msvcrt
            msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
        else:
            import fcntl
            fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
        yield


def publish_changes(changes):
    """Stage all writes first, compare original bytes and roll back a failed batch."""
    from tempfile import NamedTemporaryFile
    staged = {}
    applied = []
    def stage(path, data):
        with NamedTemporaryFile(dir=path.parent, delete=False) as temporary:
            temporary.write(data)
            return Path(temporary.name)
    try:
        for path, (before, after) in changes.items():
            if before != after:
                staged[path] = stage(path, after)
        for path, temp in staged.items():
            if path.read_bytes() != changes[path][0]:
                raise ValueError(f'File changed during section build: {path}')
            os.replace(temp, path)
            applied.append(path)
    except BaseException:
        for path in reversed(applied):
            before, after = changes[path]
            if path.read_bytes() == after:
                os.replace(stage(path, before), path)
        raise
    finally:
        for temp in staged.values():
            temp.unlink(missing_ok=True)


def build_sections(pages, targets, current, report, plan=False, *, prepare=None):
    import json
    from datetime import datetime, timezone
    from zo_course_solution_prompts import project_solution_prompts
    current_bytes = current.read_bytes()
    record = json.loads(current_bytes)
    manifest_path = c.ROOT/c.HOME/'_quy_trinh/ban_dang_duyet.json'
    manifest_bytes = manifest_path.read_bytes()
    manifest = json.loads(manifest_bytes)
    owners = {page: page.with_suffix('.qmd') for page in [*c.PAGES.values(), c.FOUNDATION]}
    if 'home' in c.PAGES:
        for name in record['outputs']:
            page = Path(name)
            if page.parent == c.HOME and page not in owners:
                owners[page] = c.PAGES['home'].with_suffix('.qmd')
    def page_sections(page):
        source = owners[page]
        destination = page.name if page != source.with_suffix('.html') else None
        return declarations(c.ROOT/source, output=destination)
    catalog = {page: page_sections(page) for page in owners}
    selected_pages = {page for page, source in owners.items() if not pages or source in pages}
    selections = {(s.owner, s.target) for page in selected_pages for s in catalog[page].values()
                  if not targets or s.target in targets}
    missing = set(targets) - {key for _, key in selections}
    if missing:
        raise ValueError(f'No QMD section binding for {sorted(missing)} in the requested scope')
    if not selections and pages:
        raise ValueError('These QMD sources have no independently renderable sections')
    history = record.setdefault('section_builds', {})
    for page in selected_pages:
        removed = history.get(page.as_posix(), {}).keys() - catalog[page].keys()
        if removed and not targets:
            raise ValueError(f'{page}: removed section bindings require an explicit migration: {sorted(removed)}')
    history_changed = False
    changed_includes = set()
    for page in selected_pages:
        for key, section in catalog[page].items():
            if (section.owner, key) in selections:
                prior = history.get(page.as_posix(), {}).get(key, {}).get('includes', {})
                for path in section.includes:
                    if prior.get(path.relative_to(c.ROOT).as_posix()) != digest(path.read_bytes()):
                        changed_includes.add(path)
    pending = {}
    for page, sections in catalog.items():
        for key, section in sections.items():
            if (section.owner, key) not in selections and changed_includes.isdisjoint(section.includes):
                continue
            previous = history.get(page.as_posix(), {}).get(key, {})
            signature = section.signature()
            if previous.get('input') != signature or targets:
                pending.setdefault(page, {})[key] = (section, signature)
    result = {'sections': {p.as_posix(): list(s) for p,s in pending.items()}, 'built': {},
              'full_pages_built': 0}
    if plan:
        return result
    changes = {}
    cache = {}
    protected = set()
    layouts = {section.layout for values in pending.values() for section, _ in values.values()}
    for layout in sorted(layouts):
        for name in SECTION_ASSETS.get(layout, ()):
            source = c.DESIGN/name
            output = c.ASSETS/name
            key = output.relative_to(c.OUT).as_posix()
            before, after = changes.get(output, (output.read_bytes(), output.read_bytes()))
            if digest(before) != record['assets'].get(key):
                raise ValueError('Asset differs from its recorded output: ' + key)
            data = source.read_bytes().replace(b'\r\n', b'\n')
            if name.endswith('.css'):
                old = section_style(after, layout)
                new = section_style(data, layout)
                if old:
                    after = after.replace(old, new, 1)
                elif new:
                    after += b'\n' + new + b'\n'
            else:
                after = data
            changes[output] = before, after
            protected.update((source, output))
    for output, (before, after) in changes.items():
        key = output.relative_to(c.OUT).as_posix()
        record['assets'][key] = digest(after)
        if after != before:
            result.setdefault('updated_assets', []).append(key)
            if output.suffix == '.css':
                result['updated_stylesheet'] = key
    for page, candidates in pending.items():
        output = c.OUT/page
        before = output.read_bytes()
        name = page.as_posix()
        if digest(before) != record['outputs'].get(name):
            raise ValueError('HTML differs from its recorded output: ' + name)
        fragments = {}
        for key, (section, signature) in candidates.items():
            if signature not in cache:
                cache[signature] = render(section)
            fragments[key] = cache[signature]
            protected.update([section.owner, *section.includes])
        baseline = before.decode('utf-8')
        if prepare is not None:
            baseline = prepare(page, baseline)
        after, proof = project(baseline, fragments, output)
        after = project_solution_prompts(after)
        encoded = after.encode('utf-8')
        changes[output] = before, encoded
        record['outputs'][name] = digest(encoded)
        for key, (section, signature) in candidates.items():
            entry = section_evidence(section, signature, proof[key]['html'])
            history_changed |= history.setdefault(name, {}).get(key) != entry
            history[name][key] = entry
        result['built'][name] = proof
        protected.add(output)
    def encoded_json(data, before):
        value = json.dumps(data, indent=2, ensure_ascii=False) + '\n'
        return (value.replace('\n','\r\n') if b'\r\n' in before else value).encode()
    if history_changed or any(before != after for before, after in changes.values()):
        for page, candidates in pending.items():
            latest = page_sections(page)
            if any(latest.get(key) != section or section.signature() != signature
                   for key, (section, signature) in candidates.items()):
                raise ValueError('QMD changed during section build: ' + page.as_posix())
        next_record = encoded_json(record, current_bytes)
        changes[current] = current_bytes, next_record
        protected.add(current)
        protected.update(p for p in (c.ROOT/'scripts/zo_course_site_sections.py',
                         c.ROOT/'scripts/zo_course_site.py', c.DESIGN/'build.py',
                         c.ROOT/'scripts/zo_course_solution_prompts.py',
                         c.DESIGN/'overview_content.py', c.DESIGN/'README.md') if p.is_file())
        entries = {entry['path']: entry for entry in manifest['files']}
        for path in sorted(protected):
            name = path.relative_to(c.ROOT).as_posix()
            data = changes[path][1] if path in changes else path.read_bytes()
            entries[name] = dict(path=name, sha256=digest(data))
        manifest['files'] = [entries[name] for name in sorted(entries, key=Path)]
        manifest.update(status='pending_owner_review', owner_acceptance=False,
                        updated_at=datetime.now(timezone.utc).isoformat())
        changes[manifest_path] = manifest_bytes, encoded_json(manifest, manifest_bytes)
        with build_lock(c.ROOT/'.quarto/course-site-sections.lock'):
            publish_changes(changes)
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return result


def section_evidence(section, signature, html_digest):
    return {'input': signature, 'html': html_digest,
            'source': section.owner.relative_to(c.ROOT).as_posix(),
            'includes': {p.relative_to(c.ROOT).as_posix(): digest(p.read_bytes()) for p in section.includes}}


def full_projection(text, sections, output):
    from zo_course_solution_prompts import project_solution_prompts
    fragments = {key: render(section) for key, section in sections.items()}
    result, proof = project(text, fragments, output)
    return project_solution_prompts(result), {key: section_evidence(section, section.signature(), proof[key]['html'])
                    for key, section in sections.items()}
