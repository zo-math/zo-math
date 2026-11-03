"""Source closure for the current course, including native render dependencies."""
import ast
from pathlib import Path


def python_sources(root, entries):
    root = Path(root).resolve()
    pending = [root / p for p in entries]
    seen = set()
    while pending:
        path = pending.pop().resolve()
        if path in seen:
            continue
        seen.add(path)
        tree = ast.parse(path.read_text(encoding='utf-8-sig'), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                modules = [n.name for n in node.names]
            elif isinstance(node, ast.ImportFrom):
                modules = [node.module or '']
            else:
                continue
            for name in modules:
                locations = [path.parent, root / 'scripts', root]
                for parent in locations:
                    candidate = parent.joinpath(*name.split('.')).with_suffix('.py')
                    if candidate.is_file() and candidate.is_relative_to(root):
                        pending.append(candidate)
                        break
    return seen


def build_sources(root, context):
    from zo_course_editorial import closure
    root = Path(root).resolve()
    files = {context.DATA}
    files.update(python_sources(root, [
        'scripts/zo_course_site.py', 'scripts/zo_qmd.py',
        'scripts/zo_check_repo.py', 'scripts/zo_quarto.py',
    ]))
    # The native renderer is an active part of this build, not a fallback.
    for directory in [context.DESIGN, root / '_design/web_2027_mau_dung_chung',
                      root / 'scripts/assets', root / 'assets/lua',
                      root / 'assets/html', root / 'assets/tex',
                      root / 'assets/css', root / 'assets/js', root / 'assets/fonts',
                      root / 'assets/logo', root / context.BASE / '_templates']:
        files.update(p for p in directory.rglob('*') if p.is_file()
                     and '__pycache__' not in p.parts)
    files.update(p for p in root.glob('_quarto*.y*ml') if p.is_file())
    files.update(root.glob('*.scss'))
    files.add(root / '_language.yml')
    design = root / '_design/ngon_ngu_thiet_ke_zo_math_0_4'
    files.add(design / '03_du_lieu/color_system.json')
    for name in ['BeVietnamPro_Regular.ttf', 'BeVietnamPro_SemiBold.ttf',
                 'STIXTwoMath.ttf', 'OFL_BeVietnamPro.txt', 'OFL_STIX.txt']:
        files.add(design / '07_mau_thi_giac/assets' / name)
    files.add(design / '07_mau_thi_giac/logos/horizontal_color.svg')
    files.add(root / 'assets/images/qr_bao_tro_zo_math_vietcombank.jpg')
    for page in [*context.PAGES.values(), context.FOUNDATION]:
        source = root / page.with_suffix('.qmd')
        files.update(closure(source, root))
        for parent in source.parents:
            if not parent.is_relative_to(root):
                break
            for name in ['_metadata.yml', '_metadata.yaml']:
                if (parent / name).is_file():
                    files.add(parent / name)
        # Source-owned assets and contracts; generated review/build receipts
        # are excluded to avoid making the source depend on its own output.
        for name in ['giao_dien', 'hinh', 'du_lieu', 'noi_dung', 'cong_cu', 'assets']:
            files.update(p for p in (source.parent / name).rglob('*')
                         if p.is_file() and '__pycache__' not in p.parts)
        contracts = source.parent / '_quy_trinh'
        for pattern in ['*.json', '*.yml', '*.yaml']:
            files.update(p for p in contracts.glob(pattern)
                         if p.name != 'ban_dang_duyet.json')
        files.update(p for p in contracts.rglob('*.yml')
                     if 'lich_su' not in p.parts)
        files.update(p for p in contracts.rglob('*.yaml')
                     if 'lich_su' not in p.parts)
    return files
