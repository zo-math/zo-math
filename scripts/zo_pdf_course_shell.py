"""Prepare the opt-in course PDF shell from the approved D0 source design.

Runs only inside an isolated zo_pdf build. Never reads historical HTML/PDF.
"""
from pathlib import Path
from datetime import datetime, timedelta, timezone
import shutil
import yaml
from zo_pdf_support import support_model, support_tex, tex


def prepare(root: Path, mirror: Path, source: Path, definition: dict) -> dict:
    from zo_qmd_config import discover_project_config
    config = discover_project_config(root, source.relative_to(root))
    shell = config.raw.get('extensions', {}).get('course_pdf_shell') if config else None
    if not shell:
        return {}
    if shell.get('reference') != 'D0_owner_approved_2026_10_14':
        raise ValueError('Unknown course print shell authority')
    front = source.read_text(encoding='utf-8').split('---', 2)[1]
    meta = yaml.safe_load(front)
    profile = yaml.safe_load((source.parent/'_quy_trinh/ho_so/index.yml').read_text(encoding='utf-8'))
    model = support_model()
    runtime = mirror/'assets/tex/course-runtime'
    runtime.mkdir(parents=True)
    d0 = root/'content/thpt/on_thi_toan_thpt/hoc_lieu/d0'
    for p in (d0/'giao_dien/pdf_fonts').iterdir():
        if p.is_file(): shutil.copy2(p, runtime/p.name)
    shutil.copy2(d0/'giao_dien/zo_logo_04.png', runtime/'zo-course-logo.png')
    shutil.copy2(model['logo_path'], runtime/'zo-course-support-logo.png')
    shutil.copy2(model['qr_path'], runtime/'zo-course-support-qr.jpg')
    from zo_course_cover import print_cover
    print_cover(root,source.parent.name,runtime/'zo-course-cover.pdf',allow_direction_approved=bool(shell.get('allow_direction_approved_preview')))
    now = datetime.now(timezone(timedelta(hours=7)))
    variant = definition['metadata']['subtitle'].split('—')[-1].strip()
    downloads = meta['r1-download-files'] + meta.get('r1-section-download-files', [])
    download = next((x for x in downloads if x['href']==definition['output']),None)
    if download is None:
        if not definition.get('description'):raise ValueError('PDF variant needs a source-owned description')
        download={'description':definition['description']}
    layout=None
    if shell.get('layout')=='course-print-v2':
        from zo_course_pdf_layout import model as print_model
        layout=print_model(root,source,next(k for k,v in config.raw['extensions']['pdf_variants'].items() if v['output']==definition['output']))
    if layout:
        shutil.copy2(root/'assets/tex/zo-course-print-layout.tex',runtime/'zo-course-print-layout.tex')
        (mirror/'assets/tex/zo-course-print-runtime.json').write_text(
            __import__('json').dumps(layout, ensure_ascii=False), encoding='utf-8')
    fields = {
        'zoPrintTitle': meta['title'], 'zoPrintPackage': profile['package']['id'],
        'zoPrintVersion': profile['package']['candidate_version'],
        'zoPrintVariant': variant, 'zoPrintDescription': download['description'],
        'zoPrintURL': definition['metadata']['zo-pdf-branding']['canonical-url'],
        'zoBuildDate': now.strftime('%d/%m/%Y'), 'zoBuildYear': str(now.year),
    }
    lines = [support_tex(model), r'\newif\ifzoCoursePrintVTwo', r'\zoCoursePrintVTwo'+('true' if layout else 'false')]
    lines += [r'\newif\ifzoPrintSupport', r'\zoPrintSupporttrue']
    lines += ['\\newcommand{\\'+k+'}{'+tex(str(v))+'}' for k,v in fields.items() if k!='zoPrintURL']
    # QR payloads must contain literal URL bytes, not TeX escapes for underscores.
    lines += [r'\edef\zoPrintURL{\detokenize{'+fields['zoPrintURL']+'}}']
    lines += [r'\newcommand{\zoPrintCoverTitle}{'+r'\\'.join(tex(x) for x in shell['cover_lines'])+'}',
              r'\newcommand{\zoPrintFontDir}{'+runtime.as_posix()+'/}',
              r'\definecolor{zoSupportHeading}{HTML}{'+model['heading_color'].lstrip('#')+'}']
    (runtime/'zo-course-pdf-metadata.tex').write_text('\n'.join(lines)+'\n', encoding='utf-8')
    # The D0-style cover owns rights and the QR; suppress the old extra cover.
    (mirror/'assets/tex/zo-pdf-rights.tex').write_text('% Replaced by course shell cover.\n', encoding='utf-8')
    shutil.copy2(root/'assets/tex/zo-course-pdf-end.tex', mirror/'assets/tex/zo-pdf-support.tex')
    if layout:
        ending=mirror/'assets/tex/zo-pdf-support.tex'
        ending.write_text('\\begingroup\\sffamily\n'+ending.read_text('utf-8')+'\n\\endgroup\n',encoding='utf-8')
    # Keep preamble order deterministic: the base defines block environments,
    # then the approved course shell replaces only the cover/header/footer.
    profile_path = mirror/'_quarto-pdf.yml'
    quarto_profile = yaml.safe_load(profile_path.read_text(encoding='utf-8'))
    if layout:
        quarto_profile['format']['pdf']['keep-tex']=True
        quarto_profile['format']['pdf']['latex-clean']=False
        quarto_profile['format']['pdf']['latex-min-runs']=4
        quarto_profile['format']['pdf']['latex-max-runs']=6
    quarto_profile['format']['pdf']['include-in-header'] = [
        'assets/tex/zo-pdf.tex', 'assets/tex/zo-course-pdf-shell.tex']
    profile_path.write_text(yaml.safe_dump(quarto_profile,allow_unicode=True,sort_keys=False),encoding='utf-8')
    return {'runtime': runtime, 'support_inputs': model['input_hashes'], 'layout': layout}
