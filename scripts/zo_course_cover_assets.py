"""Regenerate and compare approved cover bytes; never reapprove or replace them."""
from pathlib import Path
import tempfile,hashlib
from zo_graphics import load_graph

def verify_rebuild(root,source,surface,approved):
    root=Path(root);approved=Path(approved);source=Path(source)
    (root/'.quarto').mkdir(exist_ok=True)
    engine=load_graph('cover_dependency_verification',root)
    with tempfile.TemporaryDirectory(prefix='cover_exact_',dir=root/'.quarto') as temp:
        _,svg=engine.build(engine.parse_args([str(source),'--style','0.4','--surface',surface,'--check','--out-dir',temp]))
        if hashlib.sha256(svg.read_bytes()).digest()!=hashlib.sha256(approved.read_bytes()).digest():
            raise ValueError('Fresh cover differs from approved bytes; separate cover review required: '+str(approved))
