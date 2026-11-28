"""Check the source and DOM conventions of newly integrated course readers."""
from pathlib import Path
import json
import re
import xml.etree.ElementTree as ET

import yaml
from bs4 import BeautifulSoup

CONTRACT = 'course-reading-v1'
LEGACY_PACKAGES = {'d0', 'r1_g01', 'r1_g02', 'r1_g03', 'r1_g04', 'r1_g05', 'r2_g01', 'r2_g02'}


def enabled(source):
    binding = Path(source).parent / 'giao_dien/html.json'
    return binding.is_file() and json.loads(binding.read_text('utf-8')).get('presentation_contract') == CONTRACT


def source_checks(source, root, text=None):
    source = Path(source)
    if not enabled(source):
        if source.parent.parent.name == 'hoc_lieu' and source.parent.name not in LEGACY_PACKAGES:
            return {'presentation contract required for new package': False}
        return {}
    text = source.read_text('utf-8') if text is None else text
    metadata = yaml.safe_load(text.split('---', 2)[1])
    title = metadata['title']
    data = yaml.safe_load((Path(root) / 'content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/_data/chuong_trinh.yml').read_text('utf-8'))
    package = next(p for p in data['packages'] if p['id'] == source.parent.name)
    lesson = text.split('## Bài học', 1)[1].split('## Luyện tập', 1)[0]
    activities = re.findall(r'^:::.*\.(?:zo-learning-task|zo-learning-example)[^\n]*', lesson, re.M)
    returns = re.findall(r'[^\n]*\[Xem đề bài\]\(#[^)]+\)[^\n]*', text)
    figures = BeautifulSoup(text, 'html.parser').select('figure[data-zo-role="context-illustration"]')
    def geometry_scale_matches(figure):
        scale = re.fullmatch(r'--figure-width: (\d+\.\d+)em', figure.get('style', ''))
        image = figure.find('img')
        if scale is None or image is None:
            return False
        svg_path = (source.parent / image['src']).resolve()
        if not svg_path.is_relative_to((source.parent / 'hinh').resolve()):
            return False
        svg = ET.parse(svg_path).getroot()
        return abs(float(scale[1]) - float(svg.attrib['width']) / 10) < 0.001
    return {
        'presentation title has no dash': not re.search(r'[-–—]', title),
        'presentation has one title without subtitle': 'subtitle' not in metadata,
        'presentation summary explains content': package['summary'].strip(' .') != title.strip(' .'),
        'presentation activities use shared prose style': bool(activities) and all('.zo-lesson-activity' in a for a in activities),
        'presentation return actions are separate paragraphs': bool(returns) and all(re.fullmatch(r'\[Xem đề bài\]\(#[^)]+\)\.', line.strip()) for line in returns),
        'presentation geometry uses explicit reading scale': all('zo-geometry-figure' in f.get('class', []) and geometry_scale_matches(f) and f.find('figcaption') for f in figures),
    }


def html_checks(document, source):
    if not enabled(source):
        return {}
    reader = document.select_one('.reader-content')
    if reader is None:
        return {'presentation reader exists': False}
    activities = reader.select('#bai-hoc .zo-learning-task, #bai-hoc .zo-learning-example')
    returns = [a for a in reader.select('a[href]') if a.get_text(' ', strip=True) == 'Xem đề bài']
    figures = reader.select('figure[data-zo-role="context-illustration"]')
    return {
        'presentation HTML activities use shared prose style': all('zo-lesson-activity' in a.get('class', []) for a in activities),
        'presentation HTML return actions occupy own paragraph': all(a.parent.name == 'p' and a.parent.get_text(' ', strip=True).strip(' .') == 'Xem đề bài' for a in returns),
        'presentation HTML geometry captions and scale survive': all('zo-geometry-figure' in f.get('class', []) and f.find('figcaption') and '--figure-width:' in f.get('style', '') for f in figures),
    }


def require(checks):
    failed = [name for name, passed in checks.items() if not passed]
    if failed:
        raise ValueError('Course presentation: ' + ', '.join(failed))
