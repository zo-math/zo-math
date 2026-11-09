"""Validate printed-content equivalence without rewriting PDF build provenance.

The original build contract remains strict. This additional read-only check can
prove that a course PDF still represents the current printable source when the
only additions are validated HTML-only video disclosures. Every other source,
dependency (including external Graphics), variant, PDF byte and page count is
still checked against the original build record. No historical hash is changed.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
from html.parser import HTMLParser
from pathlib import Path

from bs4 import BeautifulSoup
import yaml
import zo_pdf_contract as contract

POLICY = 'course-qmd-without-download-page-counts-v1'
IMPORTS = '<link rel="stylesheet" href="giao_dien/video.css">\n<script src="giao_dien/video.js" defer></script>\n'
ASSETS = ('giao_dien/video.css', 'giao_dien/video.js')
HTML_ONLY = '::: {.content-visible when-format="html"}\n'


class _BalancedVideo(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []

    def handle_starttag(self, tag, attrs):
        if tag not in {'details', 'summary', 'div', 'p', 'a'}:
            raise ValueError('Unexpected element in HTML-only video')
        if len(dict(attrs)) != len(attrs):
            raise ValueError('Duplicate video attribute')
        allowed = {'class', 'id', 'data-youtube-id', 'data-scheduled-at'} if tag == 'details' else {
            'summary': {'class'}, 'div': {'class'}, 'p': {'class', 'role'},
            'a': {'href', 'target', 'rel'},
        }[tag]
        if set(dict(attrs)) - allowed:
            raise ValueError('Unexpected video attribute')
        self.stack.append(tag)

    def handle_endtag(self, tag):
        if not self.stack or self.stack.pop() != tag:
            raise ValueError('Unbalanced HTML-only video')

    def handle_data(self, data):
        if data.strip() and (not self.stack or self.stack[-1] not in {'summary', 'p', 'a'}):
            raise ValueError('Text outside video summary or notice')

    def handle_comment(self, data):
        raise ValueError('Unexpected comment in video')

    def handle_decl(self, decl):
        raise ValueError('Unexpected declaration in video')


def _video_id(fragment: str) -> str:
    parser = _BalancedVideo()
    parser.feed(fragment)
    parser.close()
    if parser.stack:
        raise ValueError('Unclosed video element')
    doc = BeautifulSoup(fragment, 'html.parser')
    roots = doc.find_all(recursive=False)
    if len(roots) != 1 or roots[0].name != 'details':
        raise ValueError('Expected one video disclosure')
    node = roots[0]
    ident, video = node.get('id', ''), node.get('data-youtube-id', '')
    if node.get('class') != ['zo-block', 'zo-block-gray', 'zo-learning-video'] or not re.fullmatch(r'video-[a-z0-9-]+', ident) or not re.fullmatch(r'[A-Za-z0-9_-]{11}', video):
        raise ValueError('Invalid video identity')
    if [n.name for n in node.find_all(recursive=False)] != ['summary', 'div']:
        raise ValueError('Invalid video structure')
    summary, body = node.find_all(recursive=False)
    if summary.get('class') != ['zo-block-title'] or body.get('class') != ['zo-block-body']:
        raise ValueError('Invalid video containers')
    links = node.select('a')
    players = node.select('div.zo-video-player')
    if len(links) != 1 or links[0].get('href') != 'https://www.youtube.com/shorts/' + video or links[0].get('target') != '_blank' or set(links[0].get('rel', [])) != {'noopener', 'noreferrer'} or len(players) != 1 or players[0].contents:
        raise ValueError('Invalid video player or fallback')
    return ident


def print_projection(text: str, *, main: bool = False) -> tuple[str, list[str]]:
    """Remove only recognized raw-HTML fences, never Markdown/code/LaTeX.

    Preserve every other character. A removed fence owns its following blank
    separator, so deleting the addition restores the original source bytes.
    Fences nested in an example/code fence are deliberately left untouched.
    """
    lines = text.splitlines(keepends=True)
    result, ids = [], []
    i, imports = 0, 0
    while i < len(lines):
        if lines[i] == HTML_ONLY:
            if lines[i+1:i+3] != ['\n', '```{=html}\n']:
                raise ValueError('HTML-only video must contain one raw HTML fence')
            j = i + 3
            while j < len(lines) and lines[j] != '```\n': j += 1
            if j == len(lines) or lines[j+1:j+3] != ['\n', ':::\n']:
                raise ValueError('Invalid HTML-only video boundary')
            fragment = ''.join(lines[i+3:j])
            if 'zo-learning-video' in fragment:
                ident = _video_id(fragment)
                if ident in ids: raise ValueError('Duplicate video ID')
                ids.append(ident)
            elif fragment == IMPORTS and main:
                imports += 1
            else:
                raise ValueError('Unrecognized content inside HTML-only video')
            i = j + 3
            if i < len(lines) and lines[i] == '\n': i += 1
            continue
        opening = re.fullmatch(r' {0,3}(`{3,}|~{3,})([^\n]*)\n?', lines[i])
        if not opening:
            result.append(lines[i]); i += 1; continue
        fence = opening[1]
        j = i + 1
        closing = re.compile(r' {0,3}' + re.escape(fence[0]) + '{' + str(len(fence)) + r',}[ \t]*\n?')
        while j < len(lines) and not closing.fullmatch(lines[j]):
            j += 1
        if j == len(lines):
            result.extend(lines[i:]); break
        fragment = ''.join(lines[i+1:j])
        if lines[i] == '```{=html}\n' and lines[j].rstrip('\n') == '```':
            if 'zo-learning-video' in fragment:
                raise ValueError('Video lacks the explicit HTML-only format guard')
        result.extend(lines[i:j+1]); i = j + 1
    projected = ''.join(result)
    if imports:
        if imports != 1: raise ValueError('Duplicate video imports')
        parts = projected.split('---', 2)
        if len(parts) != 3 or parts[0].strip(): raise ValueError('Missing QMD front matter')
        metadata = yaml.safe_load(parts[1])
        resources = metadata.get('resources', [])
        if not isinstance(resources, list) or any(resources.count(x) != 1 for x in ASSETS):
            raise ValueError('Video resources do not match imports')
        match = re.search(r'^resources:\n(?:  - [^\n]+\n)+', parts[1], re.M)
        if not match: raise ValueError('Unsupported video resources declaration')
        resources_text = match[0]
        for asset in ASSETS:
            resources_text = resources_text.replace('  - ' + asset + '\n', '')
        parts[1] = parts[1][:match.start()] + resources_text + parts[1][match.end():]
        projected = '---'.join(parts)
    return projected, ids


def inspect_print_state(root: Path, source: Path, *, variant: str = 'full') -> dict:
    root, source = root.resolve(), source.resolve()
    errors = contract.validate_canonical_pdf_provenance(root, source, variant=variant)
    report = {'status': 'stale' if errors else 'current', 'errors': errors, 'strict_build_errors': errors, 'web_only_videos': [], 'projected_inputs': []}
    if not errors: return report
    allowed = {'source record does not match the current QMD',
               'pipeline_inputs do not match the current dependency set and hashes',
               f'input fingerprint drift: {variant}'}
    if set(errors) - allowed: return report
    try:
        payload = contract._load_manifest(contract.canonical_pdf_provenance_path(root, source))
        state = copy.deepcopy(contract.canonical_variant_input_state(root, source, variant))
        if state['source'].get('hash_policy') != POLICY: return report
        projected, ids = print_projection(source.read_text('utf-8'), main=True)
        state['source']['sha256'] = contract.course_pdf_source_digest(projected)
        if ids: report['projected_inputs'].append(state['source']['path'])
        for item in state['pipeline_inputs']:
            if Path(item['path']).suffix != '.qmd': continue
            path = root / item['path']
            projected, more = print_projection(path.read_text('utf-8'))
            if more:
                item['sha256'] = hashlib.sha256(projected.encode('utf-8')).hexdigest()
                report['projected_inputs'].append(item['path'])
                ids.extend(more)
        if not ids or len(ids) != len(set(ids)): return report
        report['web_only_videos'] = ids
        if state['source'] != payload['source'] or state['pipeline_inputs'] != payload['pipeline_inputs']:
            return report
        fingerprint = contract._canonical_json_hash({
            'generator': contract.PDF_BUILD_GENERATOR, 'profile': contract.PDF_BUILD_PROFILE,
            'source': state['source'], 'pipeline_inputs': state['pipeline_inputs'],
            'variant': variant, 'variant_definition': state['variant_definition'],
        })
        record = next(v for v in payload['variants'] if v['name'] == variant)
        if fingerprint != record['input_fingerprint']: return report
        report.update(status='print-equivalent', errors=[], verified_inputs=len(state['pipeline_inputs']), input_fingerprint=fingerprint)
    except (ValueError, OSError, KeyError, TypeError, StopIteration) as exc:
        report['projection_error'] = str(exc)
    return report


def validate_pdf_print_provenance(root: Path, source: Path, *, variant: str = 'full') -> list[str]:
    return inspect_print_state(root, source, variant=variant)['errors']


def inspect_print_states(root: Path, source: Path) -> dict[str, dict]:
    """Share the input proof, but independently verify each registered PDF.

    The strict full-variant check already validates the complete registry,
    definitions and output paths. Do not repeat dependency discovery eight times.
    """
    root, source = root.resolve(), source.resolve()
    first = inspect_print_state(root, source)
    registry = contract._variant_registry(root, source)
    if first['errors']:
        return {name: copy.deepcopy(first) for name in registry}
    payload = contract._load_manifest(contract.canonical_pdf_provenance_path(root, source))
    records, _ = contract._record_map(payload)
    results = {'full': first}
    for name, definition in registry.items():
        if name == 'full': continue
        report = copy.deepcopy(first)
        record = records[name]
        fingerprint = contract._canonical_json_hash({
            'generator': contract.PDF_BUILD_GENERATOR, 'profile': contract.PDF_BUILD_PROFILE,
            'source': payload['source'], 'pipeline_inputs': payload['pipeline_inputs'],
            'variant': name, 'variant_definition': definition,
        })
        errors = []
        if record['input_fingerprint'] != fingerprint: errors.append(f'input fingerprint drift: {name}')
        output = root / record['output']['path']
        try:
            if contract.sha256_file(output) != record['output']['sha256']: errors.append(f'PDF hash drift: {name}')
            if contract.pdf_inventory(output) != record['inventory']: errors.append(f'PDF inventory drift: {name}')
        except (OSError, ValueError) as exc:
            errors.append(f'cannot validate PDF {name}: {exc}')
        report.update(errors=errors, input_fingerprint=fingerprint)
        if errors: report['status'] = 'stale'
        results[name] = report
    return results


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('--variant', default='full')
    parser.add_argument('--all', action='store_true', help='Verify every PDF using one shared input proof')
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    report = inspect_print_states(root, root / args.source) if args.all else inspect_print_state(root, root / args.source, variant=args.variant)
    if args.report:
        target = args.report.resolve()
        if not target.is_relative_to(root/'_audit'): parser.error('Report must be under _audit')
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(any(item['errors'] for item in report.values()) if args.all else bool(report['errors']))
