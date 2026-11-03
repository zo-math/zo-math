"""Regression checks for source changes previously invisible to course checks."""
import json
import hashlib
from pathlib import Path
import tempfile
from unittest.mock import patch
import zo_course_site as site
from zo_course_site_dependencies import python_sources


def main():
    temporary = site.ROOT / '_audit/course_source_cleanup_20261103/tests'
    temporary.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=temporary) as folder:
        root = Path(folder)
        (root / 'scripts').mkdir()
        (root / 'scripts/entry.py').write_text('from nested import helper\n', 'utf-8')
        (root / 'scripts/nested.py').write_text('import leaf\n', 'utf-8')
        (root / 'scripts/leaf.py').write_text('value = 1\n', 'utf-8')
        assert len(python_sources(root, ['scripts/entry.py'])) == 3
        from zo_course_site_output import prune
        out=root/'docs'
        assets=out/'assets/zo_web_2027'
        assets.mkdir(parents=True)
        (out/'lesson.html').write_text('<link rel="stylesheet" href="assets/zo_web_2027/used.css">', 'utf-8')
        (out/'other.html').write_text('<img src="assets/zo_web_2027/other.svg">', 'utf-8')
        (assets/'used.css').write_text('@font-face{src:url(font.ttf)}', 'utf-8')
        (assets/'font.ttf').write_bytes(b'font fixture')
        (assets/'OFL.txt').write_text('license fixture', 'utf-8')
        (assets/'other.svg').write_text('<svg/>', 'utf-8')
        (assets/'unused.js').write_text('retired fixture', 'utf-8')
        assert prune(root,out,[out/'lesson.html']) == ['docs/assets/zo_web_2027/unused.js']
        assert (assets/'other.svg').is_file() and (assets/'OFL.txt').is_file()
        from zo_web_2027_production import PACKAGE, runtime_source_checks
        package=root/PACKAGE
        (package/'giao_dien/assets/current').mkdir(parents=True)
        (package/'hinh').mkdir()
        (package/'giao_dien/html.json').write_text(json.dumps({'adapter':'g01-revision-source-v1'}),'utf-8')
        (package/'giao_dien/web_2027_figures.json').write_text(json.dumps({'graphs':['one'],'asset_directory':'giao_dien/assets/current'}),'utf-8')
        graph=package/'hinh/one.tex'
        graph.write_text('current graph source','utf-8')
        hashes={}
        for name in ['one.svg','one.pdf','cover-light.svg','cover-dark.svg']:
            asset=package/'giao_dien/assets/current'/name
            asset.write_text(name,'utf-8')
            hashes[name]=hashlib.sha256(asset.read_bytes()).hexdigest()
        manifest={'assets':hashes,'source_hashes':{graph.relative_to(root).as_posix():hashlib.sha256(graph.read_bytes()).hexdigest()}}
        (package/'giao_dien/assets/current/manifest.json').write_text(json.dumps(manifest),'utf-8')
        assert all(runtime_source_checks(root).values())  # no historical layout exists
        graph.write_text('changed current graph','utf-8')
        assert not all(runtime_source_checks(root).values())
    record = {'inputs': {'known': 'old'}, 'outputs': {}, 'assets': {}}
    for current, expected in [
        ({'known': 'old'}, []),
        ({'known': 'new'}, ['Changed input: known']),
        ({}, ['Changed input: known']),
        ({'known': 'old', 'added': 'digest'}, ['Changed input: added']),
    ]:
        with patch.object(site, 'live_inputs', return_value=current):
            assert site.freshness(record) == expected
    sources = site.live_inputs()
    for path in ['scripts/assets/revision-review-rounds.css',
                 'scripts/assets/revision-review-rounds.js',
                 'assets/html/web-analytics.html',
                 '_design/web_2027_mau_dung_chung/templates/support.html.tpl',
                 '_design/ngon_ngu_thiet_ke_zo_math_0_4/03_du_lieu/color_system.json']:
        assert path in sources, path
    assert not any('_audit/' in p or 'website_hoc_tap_2027/' in p for p in sources)
    print(json.dumps({'passed': True, 'source_files': len(sources)}))


if __name__ == '__main__':
    main()
