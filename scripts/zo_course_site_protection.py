"""Generate protection from the current course build, never from old receipts."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from zo_html_dependencies import preview_files


def refresh(root, context, record, evidence=()):
    root = Path(root).resolve()
    authority = context.HOME / '_quy_trinh/03_dieu_hanh_chuong_trinh.md'
    pages = [context.OUT / p for p in record['outputs']]
    files = preview_files(root, pages)
    files.update(root / p for p in record['inputs'])
    files.add(root / authority)
    files.add(root / context.HOME / '_quy_trinh/ho_so/current_site_build.json')
    for name in evidence:
        path=(root/Path(name)).resolve()
        if not path.is_relative_to(root) or not path.is_file():
            raise ValueError('Missing or outside current handoff evidence: '+str(name))
        files.add(path)
    for page in pages:
        shortcut = page.parent / 'Mo_ban_xem_HTML.cmd'
        if shortcut.is_file():
            files.add(shortcut)
    # Existing learner PDFs remain protected even when not linked by a card.
    for key in context.KEYS:
        folder = root / context.BASE / 'hoc_lieu' / key
        files.update(folder.glob('*.pdf'))
    data = {
        'schema_version': 1, 'id': '2027-CURRENT-SOURCE',
        'status': 'pending_owner_review',
        'updated_at': datetime.now(timezone.utc).isoformat(),
        'authority': authority.as_posix(),
        'entrypoints': [p.relative_to(root).as_posix() for p in sorted(pages)],
        'files': [{'path': p.relative_to(root).as_posix(),
                   'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
                  for p in sorted(files)],
        'owner_acceptance': False, 'published': False,
    }
    from zo_graphics import graphics_root
    graphics = graphics_root(root)
    external = {p for name in ['geometry', 'graph', 'variation']
                for p in (graphics/name).rglob('*')
                if p.is_file() and '__pycache__' not in p.parts
                and p.suffix in {'.py', '.tex', '.json', '.yml', '.yaml', '.sty'}}
    external.update(graphics.glob('zo_*.py'))
    data['external_dependencies'] = [
        {'path': p.relative_to(graphics).as_posix(),
         'sha256': hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(external)]
    path = root / context.HOME / '_quy_trinh/ban_dang_duyet.json'
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', 'utf-8')
    return data
