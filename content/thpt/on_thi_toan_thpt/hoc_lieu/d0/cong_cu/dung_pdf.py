"""Build only D0 PDF from its canonical QMD; never render or overwrite HTML."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import re
from collections import Counter
from datetime import datetime, timedelta, timezone

from pypdf import PdfReader

PACKAGE = Path(__file__).resolve().parents[1]
ROOT = PACKAGE.parents[4]
SOURCE = PACKAGE / 'index.qmd'
OUTPUT = PACKAGE / 'index.pdf'
RECEIPT = PACKAGE / '_quy_trinh/pdf_build.json'
SUPPORT = ROOT / 'content/support/donate.qmd'
SUPPORT_QR = ROOT / 'content/support/images/qr_bao_tro_zo_math_vietcombank.jpg'
sys.path.insert(0, str(ROOT / 'scripts'))
from zo_pdf_support import support_model, support_tex


def print_metadata(mirror):
    """Use the same live HTML support component as the approved layout."""
    model = support_model()
    profile = json.loads((PACKAGE / 'cong_cu/d0_print_profile.json').read_text(encoding='utf-8'))
    from zo_course_cover import print_cover
    print_cover(ROOT,'d0',mirror/PACKAGE.relative_to(ROOT)/'giao_dien/d0_cover.pdf',allow_direction_approved=True)
    fields = {}
    now = datetime.now(timezone(timedelta(hours=7)))
    fields.update(zoBuildDate=now.strftime('%d/%m/%Y'), zoBuildYear=str(now.year))
    sizes=[]
    PdfReader(PACKAGE/'hinh/hinh_hop.pdf').pages[0].extract_text(
        visitor_text=lambda text,cm,tm,font,size: sizes.append(round(size,5)) if text.strip() else None)
    label_pt=Counter(sizes).most_common(1)[0][0]
    figure_scale=profile['typography']['body_pt']*72/72.27/label_pt
    fields['zoFigureScale']=f'{figure_scale:.7f}'
    fields.update(zoBodySize=str(profile['typography']['body_pt']),
                  zoBodyLeading=str(profile['typography']['body_leading_pt']),
                  zoTaskSize=str(profile['typography']['task_title_pt']),
                  zoSectionSize=str(profile['typography']['section_title_pt']))
    heading=model['heading_color'].lstrip('#')
    if not re.fullmatch(r'[0-9a-fA-F]{6}',heading):raise ValueError('Support color is not hexadecimal')
    directory = mirror / PACKAGE.relative_to(ROOT) / 'giao_dien'
    (directory / 'd0_pdf_metadata.tex').write_text(
        support_tex(model)+'\n'+'\n'.join('\\newcommand{\\' + key + '}{' + value + '}' for key, value in fields.items())
        + '\n\\definecolor{zoSupportHeading}{HTML}{'+heading+'}\n', encoding='utf-8')
    shutil.copy2(model['qr_path'], directory / 'd0_support_qr.jpg')
    from zo_course_table_roles import contract, function_profile, table_rows
    table_contract=contract(ROOT);table_specs={}
    for entry in table_contract['pages']['d0']:
        ident=entry['selector'][1:].split()[0]
        rows=table_rows(SOURCE.read_text('utf-8'),ident)
        spec=function_profile(entry,table_contract) or entry
        widths=spec.get('widths') or [100/len(rows[0])]*len(rows[0])
        table_specs[ident]={'widths':widths,'center':list(range(1,len(widths)+1)) if entry['kind'] in {'values','frequency','matrix','sign'} else [c+1 for c in entry.get('center_body_columns',[])], 'right':spec.get('right_columns',[])}
    (directory/'d0_tables.json').write_text(json.dumps(table_specs,ensure_ascii=False),encoding='utf-8')
    shutil.copy2(model['logo_path'], directory / 'd0_support_stack.png')
    return {'date':fields['zoBuildDate'],'figure_label_pt':profile['typography']['body_pt'],
            'support_fields':model['fields'],'support_source_hashes':model['input_hashes']}


def inputs():
    paths = [SOURCE, Path(__file__), ROOT/'scripts/zo_pdf_support.py', PACKAGE / 'cong_cu/d0.lua',
             PACKAGE / 'cong_cu/d0_pdf.lua', PACKAGE / 'cong_cu/d0_print.lua',
             PACKAGE / 'cong_cu/d0_print_profile.json', PACKAGE / 'giao_dien/d0_pdf.tex',
             PACKAGE / 'giao_dien/d0_pdf_end.tex', ROOT / '_quarto.yml',
             ROOT / 'scripts/zo_quarto.py', ROOT / 'scripts/zo_python.py',
             ROOT / 'assets/lua/zo_learning_components.lua',
             ROOT / 'assets/lua/zo_variation_qmd.lua', ROOT/'assets/lua/zo_course_print.lua']
    paths += [PACKAGE / '_quy_trinh/pdf_source_delta.json',
              PACKAGE / '_quy_trinh/d0_bai00_logic_delta.json',
              PACKAGE / '_quy_trinh/cau_hinh_san_xuat_qmd.yml',
              PACKAGE / '_quy_trinh/ho_so/index.yml',
              PACKAGE / '_quy_trinh/dieu_chinh_sau_duyet.json',
              PACKAGE / '_quy_trinh/d0_editorial_comparison_delta.json',
              PACKAGE / '_quy_trinh/d0_numbering_delta.json',
              PACKAGE / '_quy_trinh/d0_presentation_comparison_delta.json',
              PACKAGE / 'cong_cu/kiem_chung_da_duyet.py',
              ROOT / 'scripts/zo_d0_presentation.py']
    paths += list((PACKAGE / 'giao_dien/pdf_fonts').glob('*'))
    paths += [path for path in (ROOT / '_design/web_2027_mau_dung_chung').rglob('*') if path.is_file()]
    paths += list((ROOT / 'content/thpt/on_thi_toan_thpt/hoc_lieu').glob('r*_g*/giao_dien/he_nhan.json'))
    paths += [PACKAGE / 'giao_dien/zo_logo_04.png',
              PACKAGE / 'du_lieu/bang_bien_thien.json', PACKAGE / 'hinh/bbt01.pdf',
              PACKAGE / 'hinh/hinh_hop.pdf', ROOT/'scripts/zo_course_cover.py', PACKAGE/'giao_dien/anh_bia.json', PACKAGE/'giao_dien/assets/bia_khao_sat.svg']
    model=support_model()
    paths += [ROOT / name for name in model['input_hashes']]
    return {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in paths}


def isolated_project(directory):
    """LuaLaTeX writes intermediate index.pdf beside QMD; contain it here."""
    mirror = directory / 'project'
    mirror.mkdir()
    for source in ROOT.iterdir():
        if source.is_file():
            shutil.copy2(source, mirror / source.name)
    ignored = shutil.ignore_patterns('_audit', '__pycache__', '.quarto', '*_files')
    for relative in (Path('assets'), Path('scripts'),
                     Path('_design/web_2027_mau_dung_chung'), PACKAGE.relative_to(ROOT)):
        shutil.copytree(ROOT / relative, mirror / relative, ignore=ignored)
    for source in (ROOT / 'content/thpt/on_thi_toan_thpt/hoc_lieu').glob('r*_g*/giao_dien/he_nhan.json'):
        target = mirror / source.relative_to(ROOT)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    for parent in PACKAGE.parents:
        if parent == ROOT:
            break
        for name in ('_metadata.yml', '_metadata.yaml'):
            source = parent / name
            if source.is_file():
                target = mirror / source.relative_to(ROOT)
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, target)
    return mirror


def main():
    sys.path.insert(0, str(PACKAGE / 'cong_cu'))
    from kiem_chung_da_duyet import verify_source
    verify_source()
    before = inputs()
    build = ROOT / '.quarto/d0_pdf_build'
    build.mkdir(parents=True, exist_ok=True)
    temporary = Path(tempfile.mkdtemp(prefix='render_', dir=build))
    replacement = OUTPUT.with_name('.index.pdf.replacement')
    try:
        mirror = isolated_project(temporary)
        metadata = print_metadata(mirror)
        command = [sys.executable, str(mirror / 'scripts/zo_python.py'), '-B',
                   str(mirror / 'scripts/zo_quarto.py'), 'render',
                   SOURCE.relative_to(ROOT).as_posix(), '--to', 'pdf',
                   '--output-dir', '.quarto/pdf_output']
        environment = os.environ.copy()
        quarto = shutil.which("quarto", path=environment.get("PATH"))
        if quarto is not None:
            environment["ZO_QUARTO_EXECUTABLE"] = quarto
        completed = subprocess.run(command, cwd=mirror, env=environment)
        if completed.returncode:
            return completed.returncode
        candidates = list((mirror / '.quarto/pdf_output').rglob('index.pdf'))
        if len(candidates) != 1:
            raise ValueError('Expected exactly one rendered D0 PDF')
        pdf = PdfReader(candidates[0])
        if not pdf.pages or pdf.metadata.title != 'Khảo sát đầu vào':
            raise ValueError('PDF has no pages or incorrect title metadata')
        if before != inputs():
            raise ValueError('Inputs changed during render; output was not replaced')
        shutil.copy2(candidates[0], replacement)
        replacement.replace(OUTPUT)
        receipt = {'schema_version': 1, 'source': SOURCE.relative_to(ROOT).as_posix(),
                   'command': 'python scripts/zo_python.py -B '
                   'content/thpt/on_thi_toan_thpt/hoc_lieu/d0/cong_cu/dung_pdf.py',
                   'inputs_sha256': before, 'pages': len(pdf.pages),
                   'output': OUTPUT.relative_to(ROOT).as_posix(),
                   'output_sha256': hashlib.sha256(OUTPUT.read_bytes()).hexdigest(),
                   'print_metadata': metadata,
                   'owner_acceptance': 'pending', 'publication': 'pending'}
        RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print(f'PDF: {OUTPUT} ({len(pdf.pages)} pages)')
        return 0
    finally:
        if replacement.exists():
            replacement.unlink()
        shutil.rmtree(temporary)
        if not any(build.iterdir()):
            build.rmdir()


if __name__ == '__main__':
    raise SystemExit(main())
