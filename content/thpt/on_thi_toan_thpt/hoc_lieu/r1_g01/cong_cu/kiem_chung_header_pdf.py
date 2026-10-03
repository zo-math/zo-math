"""Running-header regression on actual PDF text coordinates.

Use through scripts/zo_python.py. No PDF is modified; report has every page.
Poppler bbox is preferred; pypdf coordinates provide a deterministic fallback
when the pdftotext binary is absent, crashes, or lacks ``-bbox`` support.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import xml.etree.ElementTree as ET
from pypdf import PdfReader

TITLE = 'Đơn điệu và cực trị'
LABELS = ('Bản đầy đủ', 'Bản học và bài tập')


def _inspect_poppler(path: Path, label: str) -> dict:
    run = subprocess.run(['pdftotext', '-bbox', str(path), '-'], capture_output=True, check=True)
    root = ET.fromstring(run.stdout)
    pages = root.findall('.//{*}page')
    reader = PdfReader(path)
    findings = []
    for number, page in enumerate(pages, 1):
        words = [{**{k: float(v) for k, v in w.attrib.items()}, 'text': w.text or ''}
                 for w in page.findall('.//{*}word')]
        header = sorted([w for w in words if w['yMax'] < 80], key=lambda w: (round(w['yMin']), w['xMin']))
        text = ' '.join(w['text'] for w in header)
        if number == 1:
            findings.append({'page': number, 'cover': True, 'variant_label': label in reader.pages[0].extract_text(), 'ok': label in reader.pages[0].extract_text()})
            continue
        if number == len(pages) and not header:
            # The shared template deliberately gives the closing support page
            # the plain style, as in the pre-fix PDFs; it has no running header.
            closing = reader.pages[-1].extract_text()
            ok = 'Bảo trợ ZO Math' in closing and 'BAO TRO ZO MATH' in closing
            findings.append({'page': number, 'closing_plain': True, 'ok': ok})
            continue
        ys = [w['yMin'] for w in header]
        body = [w for w in words if 80 <= w['yMin'] < float(page.attrib['height'])-60]
        sizes = []
        def font_size(t, cm, tm, font, size):
            if t.strip() and tm[5] > float(page.attrib['height'])-80:
                sizes.append(size)
        reader.pages[number-1].extract_text(visitor_text=font_size)
        # One physical line with the entire, unchanged title and brand. No label.
        ok = (text == 'ZO Math '+TITLE and bool(ys) and max(ys)-min(ys) < 2
              # Shared A4 layout: the one-line box ends before 50 pt from
              # the top. Retaining the rejected extra 5 pt fails this bound.
              and max(w['yMax'] for w in header) <= 50
              and all(9 <= s <= 12 for s in sizes) and bool(sizes)
              and min(w['xMin'] for w in header) >= 50
              and max(w['xMax'] for w in header) <= float(page.attrib['width'])-50
              and all(header[i]['xMax'] <= header[i+1]['xMin']+.2 for i in range(len(header)-1))
              and not any(label in text for label in LABELS))
        findings.append({'page': number, 'ok': ok, 'text': text, 'words': header,
                         'y_span': max(ys)-min(ys) if ys else None, 'font_sizes': sorted(set(sizes)),
                         'body_top': min((w['yMin'] for w in body), default=None)})
    return {'file': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'pages': len(pages), 'ok': all(p['ok'] for p in findings),
            'coordinate_engine': 'poppler-bbox', 'headers': findings}


def _inspect_pypdf(path: Path, label: str, fallback_reason: str) -> dict:
    reader = PdfReader(path)
    findings = []
    for number, page in enumerate(reader.pages, 1):
        page_text = page.extract_text() or ''
        if number == 1:
            findings.append({
                'page': number, 'cover': True,
                'variant_label': label in page_text,
                'ok': label in page_text,
            })
            continue

        height = float(page.mediabox.height)
        chunks = []

        def text_chunk(text, cm, tm, font, size):
            clean = ' '.join(text.split())
            if not clean:
                return
            top_baseline = height - float(tm[5])
            chunks.append({
                'text': clean, 'x': float(tm[4]), 'top_baseline': top_baseline,
                'font_size': float(size),
            })

        page.extract_text(visitor_text=text_chunk)
        top_chunks = [item for item in chunks if item['top_baseline'] < 80]
        header = sorted(
            [item for item in top_chunks
             if item['text'].startswith('ZO Math')
             or any(candidate in item['text'] for candidate in LABELS)],
            key=lambda item: (round(item['top_baseline'], 2), item['x']),
        )
        if number == len(reader.pages) and not header:
            ok = 'Bảo trợ ZO Math' in page_text and 'BAO TRO ZO MATH' in page_text
            findings.append({'page': number, 'closing_plain': True, 'ok': ok})
            continue

        text = ' '.join(item['text'] for item in header)
        y_values = [item['top_baseline'] for item in header]
        sizes = [item['font_size'] for item in header]
        ok = (
            text == 'ZO Math ' + TITLE
            and bool(header)
            and max(y_values) - min(y_values) < 2
            and max(y_values) <= 50
            and all(9 <= size <= 12 for size in sizes)
            and min(item['x'] for item in header) >= 50
            and len(header) == 1
            and not any(candidate in text for candidate in LABELS)
        )
        findings.append({
            'page': number, 'ok': ok, 'text': text,
            'chunks': header,
            'y_span': max(y_values) - min(y_values) if y_values else None,
            'font_sizes': sorted(set(sizes)),
        })
    return {
        'file': str(path),
        'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
        'pages': len(reader.pages),
        'ok': all(item['ok'] for item in findings),
        'coordinate_engine': 'pypdf-fallback',
        'fallback_reason': fallback_reason,
        'headers': findings,
    }


def inspect_pdf(path: Path, label: str) -> dict:
    try:
        return _inspect_poppler(path, label)
    except (FileNotFoundError, subprocess.CalledProcessError, ET.ParseError) as exc:
        return _inspect_pypdf(path, label, f'{type(exc).__name__}: {exc}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('full', type=Path)
    parser.add_argument('student', type=Path)
    parser.add_argument('--report', type=Path, required=True)
    args = parser.parse_args()
    result = [inspect_pdf(args.full, LABELS[0]), inspect_pdf(args.student, LABELS[1])]
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps([{k:v for k,v in r.items() if k!='headers'} for r in result],ensure_ascii=False))
    raise SystemExit(0 if all(r['ok'] for r in result) else 1)
