"""Build a bounded, reproducible HTML figure specimen, never production pages."""
from __future__ import annotations
import argparse
import hashlib
import html
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / 'content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g01'
PROFILE = ROOT / '_design/web_2027_mau_dung_chung/figure-profile-candidate'
GRAPH = ROOT / 'quy_trinh_xay_dung/cong_cu_do_thi_ham_so_zo_math'
VARIATION = ROOT / 'quy_trinh_xay_dung/cong_cu_bang_bien_thien_zo_math'
DEFAULT = ROOT / '_audit/zo_math_figure_profile_2026-10-08'


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def protect():
    paths = [PACKAGE / 'index.qmd', PACKAGE / 'du_lieu/bang_bien_thien.json',
             ROOT / 'docs/content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g01/index.html',
             ROOT / '_audit/zo_web_2027_g01_g02_doi_sanh_2026-10-08/g01-kit.html']
    for base in [PACKAGE / 'hinh', PACKAGE / 'giao_dien',
                 ROOT / '_design/ngon_ngu_thiet_ke_zo_math_0_4/06_nguon',
                 ROOT / '_design/ngon_ngu_thiet_ke_zo_math_0_4/07_mau_thi_giac']:
        paths += [p for p in base.rglob('*') if p.is_file()]
    return {p.relative_to(ROOT).as_posix(): sha(p) for p in paths}


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build(output, force=False, reuse_figures=False):
    output = output.resolve()
    if ROOT / '_audit' not in output.parents:
        raise ValueError('Đầu ra mẫu phải nằm dưới _audit, không ghi production.')
    if (output / 'index.html').exists() and not force:
        raise ValueError('Mẫu đã tồn tại; cần --force để tái sinh đúng phạm vi.')
    before = protect()
    output.mkdir(parents=True, exist_ok=True)
    assets = output / 'assets'; assets.mkdir(exist_ok=True)
    graph = load_module('graph04_specimen', GRAPH / 'zo_graph_build.py')
    sys.path.insert(0, str(VARIATION))
    variation = load_module('variation04_specimen', VARIATION / 'zo_variation_html.py')
    records = variation.load_data(PACKAGE / 'du_lieu/bang_bien_thien.json')
    fragments = variation.math_fragments(records)
    # Original TeX, JSON, vectors and production HTML are never written.
    generated = []
    if reuse_figures:
        previous = json.loads((output / 'manifest.json').read_text(encoding='utf-8'))
        graphic_inputs = [GRAPH / 'zo_graph_build.py', GRAPH / 'tex/zo_graph_v02.tex',
                          GRAPH / 'tex/zo_graph_v04.tex', GRAPH / 'mau/cover_cubic_04.tex',
                          PROFILE / 'absolute-value-labels.json']
        graphic_inputs += [PACKAGE / 'hinh' / f'do_thi_{n:02}.tex' for n in range(1,4)]
        previous_hashes = previous['source_hashes'] | previous['protected_hashes']
        if any(previous_hashes.get(p.relative_to(ROOT).as_posix()) != sha(p) for p in graphic_inputs):
            raise RuntimeError('Nguồn đồ thị đã đổi; không được dùng lại SVG cũ.')
        for name,digest in previous['generated'].items():
            asset = output / name
            if sha(asset) != digest:
                raise RuntimeError('Tài sản hình đã đổi: ' + name)
            generated.append(asset)
    for name in ([] if reuse_figures else ['do_thi_01', 'do_thi_02', 'do_thi_03']):
        print('Building', name, flush=True)
        args = graph.parse_args([str(PACKAGE / 'hinh' / (name + '.tex')), '--out-dir', str(assets),
                                 '--style', '0.4', '--check'] +
                                (['--label-layout', str(PROFILE / 'absolute-value-labels.json')] if name == 'do_thi_03' else []) +
                                (['--force'] if force else []))
        pdf, svg = graph.build(args)
        generated += [pdf, svg]
    for surface, name in ([] if reuse_figures else [('transparent-light', 'cover-light'), ('transparent-dark', 'cover-dark')]):
        variant_dir = output / name
        args = graph.parse_args([str(GRAPH / 'mau/cover_cubic_04.tex'), '--out-dir', str(variant_dir),
                                 '--style', '0.4', '--surface', surface, '--check'] + (['--force'] if force else []))
        pdf, svg = graph.build(args)
        target = assets / (name + '.svg'); shutil.copy2(svg, target)
        generated += [pdf, svg, target]
    for name in ['figure.css', 'specimen.js']:
        shutil.copy2(PROFILE / name, output / name)
    palette_path = ROOT / '_design/ngon_ngu_thiet_ke_zo_math_0_4/07_mau_thi_giac/design/color_system.json'
    palette = json.loads(palette_path.read_text(encoding='utf-8'))['palette']
    config = json.loads((PROFILE / 'frame-tokens.json').read_text(encoding='utf-8'))
    config['colors'] = {k: palette[v] for k, v in config['backgrounds'].items()}
    colors = ''.join(f'<label title="{key}" class="swatch"><input type="radio" name="frame-bg" value="{key}" '
                     f'{"checked" if key == "yellow-light" else ""} style="--swatch:{color}" aria-label="{key}"></label>'
                     for key, color in config['colors'].items())
    by_id = {r['id']: r for r in records}
    table = lambda rid: variation.render_record(by_id[rid], fragments)
    graph_figure = lambda n, caption: (f'<figure class="zo-figure-region"><div class="zo-figure-scroll" tabindex="0" '
        f'role="region" aria-label="{html.escape(caption)}; cuộn ngang khi cần">'
        f'<img src="assets/{n}.svg" alt="{html.escape(caption)}"></div>'
        f'<figcaption>{html.escape(caption)}</figcaption></figure>')
    # Extract real prose/math from the approved production snapshot, rather than
    # inventing lesson wording in the builder. Only clone paragraphs, not IDs.
    from bs4 import BeautifulSoup
    approved = BeautifulSoup((ROOT / 'docs/content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g01/index.html').read_text(encoding='utf-8'), 'html.parser')
    selected = []
    for p in approved.select('.reader-content p'):
        if p.find('math') and 'p(x)' in p.get_text(' ', strip=True).replace(' ', ''):
            selected.append(str(p))
        if len(selected) == 2:
            break
    if not selected:
        raise RuntimeError('Không tìm thấy nội dung p(x) thật trong G01; không tự bịa nội dung thay.')
    gallery = ''.join(f'<article class="table-case"><span class="role">Mẫu từ dữ liệu G01 · {r["id"]}</span>'
                      f'<h2>{html.escape(r["title"])}</h2>{variation.render_record(r, fragments)}</article>' for r in records)
    content = f'''<!doctype html><html lang="vi"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>ZO Math · Mẫu khung bìa, đồ thị và bảng 0.4</title>
<link rel="stylesheet" href="figure.css"><style>
@font-face{{font-family:Be;src:url('../../assets/fonts/BeVietnamPro_Regular.ttf')}}
@font-face{{font-family:Be;src:url('../../assets/fonts/BeVietnamPro_SemiBold.ttf');font-weight:600}}
@font-face{{font-family:Math;src:url('../../assets/fonts/STIXTwoMath.ttf')}}
*{{box-sizing:border-box}}body{{margin:0;background:#FFF9E9;color:#3E3A35;font:17px/1.8 Be,sans-serif}}
header{{background:white;border-bottom:1px solid #DFD7CA;padding:18px 32px;display:flex;gap:20px;align-items:center;justify-content:space-between}}
header strong{{font-size:16px}}header span,.note{{font-size:12px;color:#766F66}}a{{color:#BF4240;text-decoration:none}}
.hero{{padding:40px 32px;display:flex;flex-wrap:wrap;align-items:center;gap:32px;border-bottom:1px solid #DFD7CA}}
.hero-copy{{flex:1 1 280px;max-width:420px}}h1{{font-size:40px;line-height:1.25;color:#EF5350;margin:8px 0 22px}}h2{{font-size:24px;line-height:1.45;margin:6px 0 24px;font-weight:600}}
.role{{display:block;font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:#766F66;margin-bottom:10px}}
.authoring-tools{{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin:24px 0 12px;font-size:12px}}select{{font:inherit;color:inherit;padding:8px;border:1px solid #DFD7CA;background:white;border-radius:4px;max-width:100%}}
.swatch input{{appearance:none;width:24px;height:24px;background:var(--swatch);border:1px solid #9F968B;border-radius:50%;margin:0;vertical-align:middle;cursor:pointer}}.swatch input:checked{{outline:2px solid #3E3A35;outline-offset:3px}}:focus-visible{{outline:2px solid #3E3A35;outline-offset:4px}}
main{{width:calc(100% - 64px);max-width:816px;margin:32px 32px 64px}}.reading-region{{padding:32px;background:white;border-radius:6px;margin-bottom:28px;min-width:0;overflow-wrap:break-word}}p{{margin:0 0 20px}}.reading-region>:last-child{{margin-bottom:0}}
math{{font-family:Math,serif;font-size:1em}}annotation{{display:none}}math[display=block]{{display:block;overflow-x:auto;max-width:100%;padding:8px 0}}details summary{{cursor:pointer;font-size:15px}}.gallery{{margin-top:24px}}.table-case+.table-case{{margin-top:40px}}
@media(max-width:760px){{body{{font-size:16px}}header{{padding:14px 16px}}header span{{display:none}}.hero{{padding:26px 12px;gap:24px}}.hero-copy{{padding:0 22px;max-width:none}}h1{{font-size:30px}}h2{{font-size:21px}}main{{width:calc(100% - 24px);margin:24px 12px 40px}}.reading-region{{padding:26px 22px}}.authoring-tools{{gap:12px}}}}
</style><body class="figure-specimen"><header><strong>ZO Math</strong><span>Mẫu thử riêng · chưa thay G01 hiện hành</span><a href="#lesson">Xem hình trong bài ↓</a></header>
<section class="hero"><div class="hero-copy"><span class="role">Ôn thi Toán THPT 2027 · Hàm số</span><h1>Đơn điệu và cực trị</h1><p>Dấu đạo hàm, tính đơn điệu và cực trị</p>
<p class="note">Ảnh bìa trong suốt; màu và tỉ lệ thuộc khung chứa. Đây là bộ chọn cho người biên soạn, không phải thêm công cụ cho học sinh.</p>
<div class="authoring-tools"><select id="shape" aria-label="Dạng khung"><option value="square">Vuông</option><option value="portrait">Dọc</option><option value="landscape" selected>Ngang</option></select>
<select id="size" aria-label="Kích thước khung"><option value="small">Nhỏ</option><option value="large">Lớn</option></select>{colors}</div><p id="frame-description" class="note"></p></div>
<figure class="zo-cover-frame" style="--frame-width:480px;--frame-ratio:480/320;--frame-bg:#FFF9E9"><img src="assets/cover-light.svg" alt="Đồ thị p(x)=x³−3x+1 với A(−1;3), B(1;−1), C(0;1)."></figure></section>
<main id="lesson"><section class="reading-region"><span class="role">Đọc bảng và đối chiếu đồ thị · nội dung thật R1-G01</span><h2>Từ bảng biến thiên đến dáng điệu đồ thị</h2>{''.join(selected)}{table('BBT02')}{graph_figure('do_thi_02', 'Đồ thị p(x)=x³−3x+1, A(−1;3), B(1;−1), C(0;1).')}
<p class="note">Cỡ ký hiệu bảng bằng văn bản; nhãn đồ thị khoảng 17 px ở kích thước tự nhiên. Màn hình hẹp cuộn trong hình, không phóng đầy vùng đọc.</p></section>
<section class="reading-region"><span class="role">Tiếp tuyến ngang · không tự suy ra cực trị</span><h2>Đọc hình ở kích thước tự nhiên</h2>{graph_figure('do_thi_01','Đồ thị y=(x−1)³+2 và tiếp tuyến y=2 tại A(1;2).')}{table('BBT01')}</section>
<section class="reading-region"><span class="role">Điểm xác định và điểm loại · giữ nguyên dữ kiện</span><h2>Cùng dáng đồ thị, khác tập xác định</h2>{graph_figure('do_thi_03','Giữ hoặc loại điểm tại gốc trên đồ thị hàm giá trị tuyệt đối.')}{table('BBT12')}{table('BBT13')}</section>
<section class="reading-region"><span class="role">Đối chiếu toàn bộ dữ liệu · không đổi bài học</span><h2>13 bảng nguồn của G01</h2><details id="all-tables"><summary>Mở bộ bảng kiểm đầy đủ</summary><div class="gallery">{gallery}</div></details><p class="note">Bảng cố ý sai vẫn được giữ như nguồn. Bộ kiểm này không phải luồng học mới hoặc trang sản xuất.</p></section></main>
<script type="application/json" id="frame-config">{json.dumps(config, ensure_ascii=False)}</script><script src="specimen.js"></script></body></html>'''
    (output / 'index.html').write_text(content, encoding='utf-8', newline='\n')
    after = protect()
    changed = [name for name, digest in before.items() if after.get(name) != digest]
    if changed:
        raise RuntimeError('Nguồn được bảo vệ đã đổi: ' + ', '.join(changed))
    dependencies = [Path(__file__), PROFILE / 'frame-tokens.json', PROFILE / 'figure.css', PROFILE / 'specimen.js',
                    PROFILE / 'absolute-value-labels.json',
                    GRAPH / 'zo_graph_build.py', GRAPH / 'tex/zo_graph_v02.tex', GRAPH / 'tex/zo_graph_v04.tex',
                    GRAPH / 'mau/cover_cubic_04.tex', VARIATION / 'zo_variation_html.py', VARIATION / 'zo_variation_build.py', palette_path]
    manifest = {'status': 'built_not_owner_accepted_not_production', 'protected_hashes': before,
                'protected_unchanged': True, 'source_hashes': {p.relative_to(ROOT).as_posix():sha(p) for p in dependencies},
                'records': records, 'generated': {p.relative_to(output).as_posix():sha(p) for p in generated},
                'limits': ['No course PDF render or production render.', 'Not locked Design 0.5.',
                           'Transparent profile rejects open markers and pagecolor; labels need placement review.']}
    (output / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    print(output / 'index.html')


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=DEFAULT)
    parser.add_argument('--force', action='store_true')
    parser.add_argument('--reuse-figures', action='store_true', help='Tái dựng HTML nếu nguồn/hash SVG đã được xác minh không đổi.')
    args=parser.parse_args()
    build(args.output, args.force, args.reuse_figures)
