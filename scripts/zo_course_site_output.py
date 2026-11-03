"""Remove unreferenced generated native assets after installing final HTML."""
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit
from bs4 import BeautifulSoup
from zo_html_dependencies import preview_files


def prune(root, output, pages):
    root, output = Path(root).resolve(), Path(output).resolve()
    generated = output / 'assets/zo_web_2027'
    if output != root / 'docs' or not generated.is_relative_to(output):
        raise ValueError('Cleanup is limited to generated course assets in docs')
    if not generated.is_dir():
        return []
    pages = {Path(p).resolve() for p in pages}
    keep = preview_files(root, pages)
    # Other website pages may still use a native asset; retain their direct
    # dependencies too, without crawling unrelated pages or changing them.
    extra = set()
    for path in output.rglob('*'):
        if not path.is_file() or path in pages or path.is_relative_to(generated):
            continue
        if path.suffix.lower() not in {'.html', '.css'}:
            continue
        text = path.read_text('utf-8')
        if 'zo_web_2027' not in text:
            continue
        if path.suffix.lower() == '.html':
            doc = BeautifulSoup(text, 'html.parser')
            refs = [n[a] for n in doc.select('[href],[src],[poster],[data]')
                    for a in ['href', 'src', 'poster', 'data'] if n.get(a)]
            refs.extend(part.strip().split()[0] for n in doc.select('[srcset]')
                        for part in n['srcset'].split(',') if part.strip())
            refs.extend(re.findall(r'''url\(\s*["']?([^\)"']+)''', text))
        else:
            refs = re.findall(r'''url\(\s*["']?([^\)"']+)''', text)
        for ref in refs:
            url = urlsplit(ref)
            if url.scheme or url.netloc or not url.path:
                continue
            target = ((output / unquote(url.path).lstrip('/')) if url.path.startswith('/')
                      else path.parent / unquote(url.path)).resolve()
            if target.is_relative_to(generated) and target.is_file():
                extra.add(target)
    if extra:
        keep.update(preview_files(root, extra))
    for font in list(keep):
        if font.suffix in {'.ttf', '.woff', '.woff2'}:
            keep.update(font.parent.glob('OFL*'))
    removed = []
    candidates = list(generated.rglob('*'))
    if any(p.is_symlink() or getattr(p.stat(), 'st_file_attributes', 0) & 0x400
           for p in [generated, *candidates]):
        raise ValueError('Refuse generated-asset cleanup through a reparse point')
    for path in candidates:
        if path.is_file() and path not in keep:
            removed.append(path.relative_to(root).as_posix())
            path.unlink()
    for path in sorted((p for p in candidates if p.is_dir()),
                       key=lambda p: len(p.parts), reverse=True):
        if not any(path.iterdir()):
            path.rmdir()
    return removed
