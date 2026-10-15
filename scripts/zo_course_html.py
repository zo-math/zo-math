"""Deterministic serialization for the course's generated HTML."""
from pathlib import Path

def write(path: Path, document) -> None:
    # BeautifulSoup may retain CRLF from an imported layout text node. Collapse
    # it before writing; platform translation must not introduce another CR.
    text = str(document).replace('\r\n', '\n').replace('\r', '\n')
    text = '\n'.join(line.rstrip(' \t') for line in text.split('\n'))
    with path.open('w', encoding='utf-8', newline='\n') as stream:
        stream.write(text)
