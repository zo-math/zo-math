"""Local preview dependency closure, shared by handoff and day-close protection."""
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit
from bs4 import BeautifulSoup

def preview_files(root, entries):
    root=Path(root).resolve()
    pending=[Path(p).resolve() for p in entries]
    bundle_roots={p.parent for p in pending}
    seen=set()
    while pending:
        path=pending.pop()
        if path in seen:continue
        if not path.is_relative_to(root) or not path.is_file():
            raise ValueError('Missing or outside repository: '+str(path))
        if path.is_symlink() or any(p.is_symlink() for p in path.parents if p!=root):
            raise ValueError('Symlink in preview dependency: '+str(path))
        seen.add(path)
        refs=[]
        if path.suffix.lower() in {'.html','.htm'}:
            soup=BeautifulSoup(path.read_text(encoding='utf-8'),'html.parser')
            for node in soup.select('img[src],script[src],link[href],source[src],video[src],video[poster],audio[src],object[data],embed[src],iframe[src]'):
                for name in ('src','href','poster','data'):
                    if node.get(name):refs.append(node[name])
            for node in soup.select('[srcset]'):
                refs.extend(part.strip().split()[0] for part in node['srcset'].split(',') if part.strip())
            css='\n'.join([node.get_text() for node in soup.select('style')]+[node['style'] for node in soup.select('[style]')])
            refs.extend(re.findall(r'url\(\s*[\"\x27]?([^\)\"\x27]+)',css))
            for node in soup.select('a[href]'):
                value=node['href'];url=urlsplit(value)
                if url.scheme or url.netloc or not url.path:continue
                target=(root/unquote(url.path).lstrip('/')) if url.path.startswith('/') else path.parent/unquote(url.path)
                # Follow bundle navigation; also retain direct download files.
                # External site navigation does not turn a preview into a crawl.
                if target.suffix.lower() not in {'.html','.htm'} or any(path.is_relative_to(b) and target.resolve().is_relative_to(b) for b in bundle_roots):
                    refs.append(value)
        elif path.suffix.lower()=='.css':
            css=path.read_text(encoding='utf-8')
            refs.extend(re.findall(r'url\(\s*[\"\x27]?([^\)\"\x27]+)',css))
            refs.extend(re.findall(r'@import\s+[\"\x27]([^\"\x27]+)',css))
        elif path.suffix.lower() in {'.js','.mjs'}:
            js=path.read_text(encoding='utf-8')
            refs.extend(re.findall(r'''(?:from\s*|import\s*\(|new\s+URL\s*\()\s*["'](\.{1,2}/[^"']+)''',js))
        elif path.suffix.lower()=='.svg':
            import xml.etree.ElementTree as ET
            for node in ET.parse(path).getroot().iter():
                for key,value in node.attrib.items():
                    if key.split('}')[-1]=='href':refs.append(value)
        for value in refs:
            url=urlsplit(value.strip())
            if url.scheme or url.netloc or not url.path:continue
            target=(root/unquote(url.path).lstrip('/')) if url.path.startswith('/') else path.parent/unquote(url.path)
            pending.append(target.resolve())
    return seen
