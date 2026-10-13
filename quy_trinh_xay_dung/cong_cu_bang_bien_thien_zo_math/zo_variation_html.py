"""Opt-in Design 0.4 native HTML renderer; legacy SVG/Lua path is unchanged."""
from __future__ import annotations

import html
import shutil
import subprocess
from bs4 import BeautifulSoup
from zo_variation_build import load_data, math_token, validate_record


def math_fragments(records):
    tokens = sorted({math_token(value) for record in records for row in record['rows'] for value in row
                     if value and math_token(value).startswith('$')} | {r'$\parallel$'})
    pandoc = shutil.which('pandoc')
    if not pandoc:
        raise RuntimeError('Thiếu Pandoc; không thay toán bằng chuỗi Unicode giả.')
    result = subprocess.run([pandoc, '-f', 'markdown', '-t', 'html5', '--mathml'],
                            input='\n\n'.join(tokens), text=True, encoding='utf-8',
                            capture_output=True, check=True)
    paragraphs = BeautifulSoup(result.stdout, 'html.parser').find_all('p', recursive=False)
    if len(paragraphs) != len(tokens) or any(not p.find('math') for p in paragraphs):
        raise RuntimeError('Pandoc không giữ đúng ánh xạ ô toán.')
    return {token: p.decode_contents() for token, p in zip(tokens, paragraphs)}


def render_record(record, fragments):
    validate_record(record)
    rid = html.escape(record['id'], quote=True)
    title = html.escape(record['title'])
    excluded = set(record.get('excluded_columns', []))
    rows = []
    for r, row in enumerate(record['rows']):
        cells = []
        for c, value in enumerate(row):
            excluded_cell = r > 0 and c in excluded
            shown = '∥' if excluded_cell else value
            token = math_token(shown)
            content = fragments[token] if token.startswith('$') else html.escape(shown)
            tag = 'th' if r == 0 or c == 0 else 'td'
            attrs = (' scope="col"' if r == 0 else ' scope="row"') if tag == 'th' else ''
            classes = []
            if '↗' in shown or '↘' in shown or '→' in shown:
                classes.append('trend')
            if excluded_cell:
                classes.append('excluded')
                attrs += f' aria-label="{html.escape(value, quote=True)}"'
            if classes:
                attrs += f' class="{" ".join(classes)}"'
            width = record.get('column_min_widths_mm', {}).get(str(c))
            if width:
                attrs += f' style="min-width:{float(width):g}mm"'
            attrs += f' data-source-value="{html.escape(value, quote=True)}"'
            cells.append(f'<{tag}{attrs}>{content}</{tag}>')
        rows.append('<tr>' + ''.join(cells) + '</tr>')
    table = (f'<table class="zo-variation-native" data-bbt="{rid}" '
             f'data-intentional-error="{str(bool(record.get("intentional_error"))).lower()}">'
             f'<caption class="sr-only">{title}</caption><thead>{rows[0]}</thead>'
             f'<tbody>{"".join(rows[1:])}</tbody></table>')
    return (f'<figure class="zo-figure-region" data-source-bbt="{rid}">'
            f'<div class="zo-figure-scroll" tabindex="0" role="region" aria-label="{title}; cuộn ngang khi cần">'
            f'{table}</div><figcaption>{title}.</figcaption></figure>')
