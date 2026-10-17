"""Connect this content repository to the standalone ZO Math Graphics tool."""
from __future__ import annotations
import os
import importlib.util
from pathlib import Path
import subprocess
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]

def graphics_root(repo_root: Path | None = None) -> Path:
    """The environment override propagates into isolated source mirrors."""
    configured = os.environ.get('ZO_MATH_GRAPHICS_ROOT')
    path = Path(configured).expanduser() if configured else (repo_root or REPO_ROOT).resolve().parent / 'zo_math_graphics'
    path = path.resolve()
    if '_audit' in {p.casefold() for p in path.parts}:
        raise ValueError('Graphics production tool must not be loaded from _audit')
    if not (path / 'zo_geometry.py').is_file():
        raise FileNotFoundError('Missing ZO Math Graphics at ' + str(path) + '; set ZO_MATH_GRAPHICS_ROOT if installed elsewhere')
    return path

def geometry_paths(repo_root: Path | None = None) -> dict[str, Path]:
    base = graphics_root(repo_root)
    return {'compiler': base / 'geometry/zo_geometry.py',
            'checker': base / 'geometry/zo_geometry_check.py',
            'style': base / 'assets/tex/zo-geometry-styles.tex',
            'cli': base / 'zo_geometry.py'}

def graph_path(path: Path, repo_root: Path | None = None) -> Path:
    """Resolve the stable manifest namespace without rewriting existing receipts."""
    repo = (repo_root or REPO_ROOT).resolve()
    path = Path(path).resolve()
    for directory, destination in [('cong_cu_do_thi_ham_so_zo_math', 'graph'),
                                   ('cong_cu_bang_bien_thien_zo_math', 'variation')]:
        legacy = repo / 'quy_trinh_xay_dung' / directory
        if path.is_relative_to(legacy):
            return graphics_root(repo) / destination / path.relative_to(legacy)
    return path

def _graph_api(repo_root: Path | None = None):
    path = graphics_root(repo_root) / 'zo_graph.py'
    spec = importlib.util.spec_from_file_location('zo_graph_external_api', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def load_graph(name='zo_graph_external', repo_root: Path | None = None):
    return _graph_api(repo_root).load_graph(repo_root or REPO_ROOT, name)

def load_variation(path: Path, name='zo_variation_external', repo_root: Path | None = None):
    if graph_path(path, repo_root) != graphics_root(repo_root) / 'variation/zo_variation_build.py':
        raise ValueError('Unknown variation engine: ' + str(path))
    return _variation_api(repo_root).load_variation(name)

def lesson_layout(repo_root: Path | None = None):
    return load_graph("zo_graph_layout_profile", repo_root).lesson_layout()


def set_lesson_graph_size(image, svg: Path, repo_root: Path | None = None):
    import xml.etree.ElementTree as ET
    profile = lesson_layout(repo_root)
    width = float(ET.parse(svg).getroot().attrib["viewBox"].split()[2])
    image["style"] = f"--figure-em:{width/profile['web_svg_bp_per_em']:.5f}em"
    image["data-zo-graph-layout"] = profile["id"]
    image["data-zo-graph-role"] = "lesson"


def _variation_api(repo_root: Path | None = None):
    path = graphics_root(repo_root) / 'zo_variation.py'
    spec = importlib.util.spec_from_file_location('zo_variation_external_api', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def load_variation_html(name='zo_variation_html_external', repo_root: Path | None = None):
    return _variation_api(repo_root).load_html(name)

def main(argv=None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if not args or args[0] not in {'geometry', 'geometry-check', 'geometry-test', 'graph', 'graph-test', 'variation'}:
        print('Usage: zo_graphics.py geometry ... | geometry-check ... | geometry-test ... | graph <source.tex> ... | graph-test | variation ...', file=sys.stderr)
        return 2
    try:
        base = graphics_root()
        script = {'geometry': base / 'zo_geometry.py', 'geometry-check': base / 'geometry/zo_geometry_check.py',
                  'geometry-test': base / 'tests/zo_geometry_selftest.py',
                  'graph': base / 'zo_graph.py', 'graph-test': base / 'graph/kiem_thu/kiem_tra_cong_cu.py',
                  'variation': base / 'zo_variation.py'}[args[0]]
    except (FileNotFoundError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    forwarded = args[1:]
    return subprocess.run([sys.executable, '-B', str(script), *forwarded], check=False).returncode

if __name__ == '__main__':
    raise SystemExit(main())
