"""Notation and lesson-outline gate for canonical 2027 learning packages.

Reject defects; never silently rewrite mathematics or generated HTML.
The user confirmed these notation rules on 2026-10-11.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re
from zo_latex_delimiters import delimiter_errors, self_test as delimiter_self_test

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'content/thpt/on_thi_toan_thpt/hoc_lieu'
MATH = re.compile(r'\$\$(.*?)\$\$|(?<!\\)\$([^$\n]+)\$', re.S)
INCLUDE = re.compile(r'\{\{<\s*include\s+([^>]+?)\s*>\}\}')
RADICAL_SELECTOR = '.reader-content math[display=inline] msqrt:not(mfrac msqrt,msup msqrt,msub msqrt,msubsup msqrt,mroot msqrt):has(msup):not(:has(mfrac,msqrt,mroot,mtable,msub,msubsup,mover,munder,munderover))'
RADICAL_GEOMETRY = r'''(()=>{const rect=n=>{let r=n.getBoundingClientRect();return {x:r.x,y:r.y,right:r.right,bottom:r.bottom,height:r.height,width:r.width}};
 return [...document.querySelectorAll('.reader-content msqrt')].filter(n=>n.getClientRects().length&&!n.closest('[hidden]')).map(n=>{
 const r=rect(n),c=n.firstElementChild,cr=rect(c),s=getComputedStyle(n),cs=getComputedStyle(c),p=getComputedStyle(n.parentElement);
 return {tex:n.closest('math').querySelector('annotation')?.textContent,balanced:n.matches('''+json.dumps(RADICAL_SELECTOR)+r'''),
 signSize:parseFloat(s.fontSize),contentSize:parseFloat(cs.fontSize),parentSize:parseFloat(p.fontSize),font:s.fontFamily,
 sign:r,content:cr,transform:s.transform,overflow:s.overflow,mathDisplay:getComputedStyle(n.closest('math')).display};})})()'''


def radical_geometry_errors(records: list[dict]) -> list[str]:
    errors = []
    for n in records:
        if not n['balanced']:continue
        size = n['parentSize']; r=n['sign']; c=n['content']
        if abs(n['contentSize']-size)>.03:errors.append('Radicand text size changed: '+n['tex'])
        if abs(n['signSize']/size-.8)>.01:errors.append('Radical sign compensation missing: '+n['tex'])
        # A taller radicand may legitimately need a larger sign; bound only
        # the lower overhang, not the height of every mathematical expression.
        # STIX has discrete radical variants; short x/numerals may leave up
        # to .6em below their ink. The reported Cambria defect exceeds .8em.
        if r['bottom']-c['bottom']>.6*size:errors.append('Excessive radical lower overhang: '+n['tex'])
        if c['height']<=1.4*size and r['height']>1.7*size:errors.append('Oversized simple radical: '+n['tex'])
        if r['y']>c['y']+.5 or r['bottom']<c['bottom']-.5:errors.append('Radicand not contained by radical: '+n['tex'])
        if n['transform']!='none' or n['overflow']!='visible':errors.append('Radical is squashed or clipped: '+n['tex'])
        if n['mathDisplay'] not in ['math','inline math']:errors.append('Radical left native inline layout: '+n['tex'])
    return errors


def math_errors(text: str) -> list[dict]:
    errors = []
    # Only math-mode expressions are scanned for slash/apostrophe: units such
    # as m/s and external URLs in prose are not mathematical fractions.
    for match in MATH.finditer(text):
        formula = match[1] if match[1] is not None else match[2]
        line = text.count('\n', 0, match.start()) + 1
        for error in delimiter_errors(formula):
            errors.append({'line':line, 'rule':error['rule'], 'formula':formula,
                           'expression':error['expression']})
        if '/' in formula:
            errors.append({'line': line, 'rule': 'fraction-requires-frac', 'formula': formula})
        if "'" in formula or '′' in formula:
            errors.append({'line': line, 'rule': 'derivative-requires-prime', 'formula': formula})
        if '√' in formula or re.search(r'\\sqrt(?!\s*(?:\[[^]]+\]\s*)?\{)', formula):
            errors.append({'line': line, 'rule': 'root-requires-braced-sqrt', 'formula': formula})
    blank = lambda m: re.sub(r'[^\n]', ' ', m[0])
    masked = MATH.sub(blank, text)
    masked = re.sub(r'^---\s*\n.*?\n---\s*\n', blank, masked, count=1, flags=re.S)
    masked = re.sub(r'(?m)^!\[.*$', blank, masked)  # Preserve original line numbers.
    for match in re.finditer(r'(?<![\w/.-])[A-Za-z](?:\^\\prime|\x27)?\([A-Za-z0-9 +;-]+\)\s*[=<>]|√|\\(?:frac|sqrt)\s*\{', masked):
        errors.append({'line': masked.count('\n', 0, match.start())+1, 'rule':'formula-outside-math-mode', 'formula':match[0]})
    return errors


def outline_errors(text: str) -> list[dict]:
    match = re.search(r'^## Bài học[^\n]*\n(.*?)(?=^## |\Z)', text, re.M | re.S)
    if not match:
        return [{'rule': 'lesson-missing'}]
    errors = []; major = 0; minor = 0
    for line in match[1].splitlines():
        heading = re.match(r'^(#{3,4})\s+(.*?)(?:\s+\{.*)?$', line)
        if not heading:
            continue
        level, title = heading.groups(); title = title.strip()
        # Structural opening/closure and independently numbered task groups
        # are not knowledge-section numbers. Do not reset task numbers.
        if title in ['Khởi động', 'Khép lại bài học'] or title.startswith(('Nhiệm vụ ', 'Gợi mở ', 'Tự kiểm tra ')):
            continue
        if level == '###':
            major += 1; minor = 0
            expected = f'{major}. '
        elif major:
            minor += 1; expected = f'{major}.{minor}. '
        else:
            continue
        if not title.startswith(expected):
            errors.append({'rule':'lesson-section-number','expected':expected,'heading':title})
    return errors


def source_errors(path: Path) -> list[dict]:
    result = []; visited = set()
    def visit(item):
        item = item.resolve()
        if item in visited: return
        visited.add(item)
        if not item.is_relative_to(BASE):
            raise ValueError('Unexpected include outside learning packages: '+str(item))
        text = item.read_text(encoding='utf-8')
        for error in math_errors(text):
            result.append({'path':item.relative_to(ROOT).as_posix(), **error})
        for ref in INCLUDE.findall(text):visit(item.parent/ref.strip())
    visit(path)
    for error in outline_errors(path.read_text(encoding='utf-8')):
        result.append({'path':path.relative_to(ROOT).as_posix(), **error})
    return result


def require_source(path: Path) -> None:
    errors = source_errors(path)
    if errors:
        raise ValueError('ZO Math notation/outline gate failed:\n'+json.dumps(errors,ensure_ascii=False,indent=2))


def runtime_css_errors(css: str) -> list[str]:
    blocks = re.findall(r'\.reader-content\s+math\[display\s*=\s*[\"\x27]?inline[\"\x27]?\]\s*\{([^}]+)\}', css)
    if len(blocks) != 1:
        return ['Expected one explicit inline MathML rule in shared shell']
    properties = dict(re.findall(r'([\w-]+)\s*:\s*([^;]+)', blocks[0]))
    expected = {'display':'inline math', 'vertical-align':'baseline', 'overflow':'visible'}
    errors = ['Inline MathML '+k+' must be '+v for k,v in expected.items() if properties.get(k,'').strip()!=v]
    errors += ['Inline MathML must not clip '+k for k in ['overflow-x','overflow-y'] if k in properties and properties[k].strip()!='visible']
    return errors


def display_css_errors(css: str) -> list[str]:
    """Keep display MathML native and centered; retain local horizontal scrolling."""
    blocks = re.findall(r'math\[display\s*=\s*["\x27]?block["\x27]?\]\s*\{([^}]+)\}', css)
    if len(blocks) != 1:
        return ['Expected one native display MathML rule']
    properties = dict(re.findall(r'([\w-]+)\s*:\s*([^;]+)', blocks[0]))
    expected = {'display':'block math', 'overflow-x':'auto', 'max-width':'100%'}
    errors = ['Display MathML '+k+' must be '+v for k,v in expected.items() if properties.get(k,'').strip()!=v]
    if properties.get('text-align','').strip() in {'left','right','start','end'}:
        errors.append('Display MathML must retain native centering')
    return errors


def require_runtime_css(path: Path) -> None:
    errors = runtime_css_errors(path.read_text(encoding='utf-8'))
    errors += radical_css_errors(path.read_text(encoding='utf-8'))
    errors += math_font_errors(path.with_name('reading-regions.css').read_text(encoding='utf-8'))
    errors += display_css_errors(path.with_name('reading-regions.css').read_text(encoding='utf-8'))
    if errors:
        raise ValueError('ZO Math inline layout gate failed: '+ '; '.join(errors))


def math_font_errors(css: str) -> list[str]:
    faces = re.findall(r'@font-face\s*\{([^}]+)\}', css)
    valid = [n for n in faces if re.search(r'font-family\s*:\s*ZOMath\s*;', n)
             and 'assets/fonts/STIXTwoMath.ttf' in n]
    rules = re.findall(r'(?<![\w-])math\s*\{([^}]+)\}', css)
    errors = []
    if len(valid) != 1:errors.append('Declare STIX Two Math once with non-generic alias ZOMath')
    if not any(re.search(r'font-family\s*:\s*ZOMath\s*,\s*math\s*;', n) for n in rules):
        errors.append('Select the explicit STIX face before generic math fallback')
    return errors


def radical_css_errors(css: str) -> list[str]:
    errors = []
    for selector, expected in [(RADICAL_SELECTOR, '.8em'),(RADICAL_SELECTOR+'>*', '1.25em')]:
        rules = re.findall(re.escape(selector)+r'\s*\{([^}]+)\}', css)
        if len(rules) != 1 or not re.search(r'font-size\s*:\s*'+re.escape(expected)+r'\s*(?:;|$)', rules[0]):
            errors.append('Missing balanced inline-power radical rule: '+selector)
        if any(re.search(r'transform\s*:|overflow\s*:\s*hidden|vertical-align\s*:', n) for n in rules):
            errors.append('Do not squash, clip or shift radicals')
    return errors


def self_test() -> dict:
    checks = {
        'reject slash fraction':bool(math_errors('$1/x$')),
        'reject apostrophe derivative':bool(math_errors("$f'(x)$")),
        'reject raw root':bool(math_errors('$√x$')),
        'reject unbraced root':bool(math_errors(r'$\sqrt x$')),
        'reject untyped expression':bool(math_errors('Cho f(x)=x+1.')),
        'accept canonical notation':not math_errors(r'$f^\prime(x)=\frac{1}{\sqrt{x}}$'),
        'accept units and URLs':not math_errors('Tốc độ 3 m/s. https://example.com/a/b'),
        'reject missing lesson number':bool(outline_errors('## Bài học {#bai-hoc}\n### Hàm số {#ham-so}\n')),
        'reject unanchored lesson number':bool(outline_errors('## Bài học {#bai-hoc}\n### Hàm số\n')),
        'reject skipped subsection number':bool(outline_errors('## Bài học {#bai-hoc}\n### 1. Hàm số {#a}\n#### 1.2. Miền {#b}\n')),
        'preserve task numbering':not outline_errors('## Bài học {#bai-hoc}\n### 1. Hàm số {#a}\n#### Nhiệm vụ 02 {#q}\n#### 1.1. Miền {#b}\n'),
        'reject old math CSS':bool(runtime_css_errors('.reader-content math[display=inline]{display:inline-block;vertical-align:middle;overflow:hidden}')),
        'accept native math CSS':not runtime_css_errors('.reader-content math[display=inline]{display:inline math;vertical-align:baseline;overflow:visible}'),
        'reject generic custom font alias':bool(math_font_errors('@font-face{font-family:Math;src:url(STIXTwoMath.ttf)} math{font-family:Math,serif}')),
        'accept explicit STIX face':not math_font_errors('@font-face{font-family:ZOMath;src:url(assets/fonts/STIXTwoMath.ttf)} math{font-family:ZOMath,math;}'),
        'reject missing radical compensation':bool(radical_css_errors(RADICAL_SELECTOR+'{font-size:.8em}')),
        'accept balanced inline radical':not radical_css_errors(RADICAL_SELECTOR+'{font-size:.8em}'+RADICAL_SELECTOR+'>*{font-size:1.25em}'),
        'reject squashed radical':bool(radical_css_errors(RADICAL_SELECTOR+'{font-size:.8em;transform:scaleY(.8)}'+RADICAL_SELECTOR+'>*{font-size:1.25em}')),
    }
    checks.update(delimiter_self_test())
    return checks


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('paths',type=Path,nargs='*')
    parser.add_argument('--self-test',action='store_true')
    parser.add_argument('--report',type=Path)
    args=parser.parse_args()
    paths=args.paths or [BASE/p/'index.qmd' for p in ['r1_g01','r1_g02']]
    errors=[e for p in paths for e in source_errors(p.resolve())]
    fixtures=self_test() if args.self_test else {}
    css_errors=runtime_css_errors((ROOT/'_design/web_2027_mau_dung_chung/web-shell.css').read_text(encoding='utf-8'))
    css_errors+=radical_css_errors((ROOT/'_design/web_2027_mau_dung_chung/web-shell.css').read_text(encoding='utf-8'))
    css_errors+=math_font_errors((ROOT/'_design/web_2027_mau_dung_chung/reading-regions.css').read_text(encoding='utf-8'))
    css_errors+=display_css_errors((ROOT/'_design/web_2027_mau_dung_chung/reading-regions.css').read_text(encoding='utf-8'))
    result={'errors':errors,'css_errors':css_errors,'negative_fixtures':fixtures,'passed':not errors and not css_errors and all(fixtures.values()),'scope':[str(p) for p in paths]}
    if args.report:
        target=args.report.resolve()
        if not target.is_relative_to(ROOT/'_audit'):raise ValueError('Audit reports only')
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2));return 0 if result['passed'] else 1


if __name__=='__main__':raise SystemExit(main())
