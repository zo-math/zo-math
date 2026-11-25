"""Regression tests for scoped builds; fixtures never rebuild the course."""
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch
from bs4 import BeautifulSoup

from zo_course_site_sources import context as c
from zo_course_site_sections import Section, build_sections, declarations, digest, full_projection, project, render


class SectionTests(unittest.TestCase):
    def test_projection(self):
        html = '<main>\r\n<section id="one"><section>old</section></section>\r\n<div id="two">2</div></main>'
        page = c.OUT/'example.html'
        result, _ = project(html, {'one': '<p>mới</p>', 'two': '3'}, page)
        self.assertEqual(result, html.replace('<section>old</section>', '<p>mới</p>').replace('>2<','>3<'))
        for bad in ({'absent':'x'}, {'one':'<a href="#absent">x</a>'}, {'two':'<p id="one">x</p>'}):
            with self.assertRaises(ValueError):
                project(html, bad, page)
        with self.assertRaises(ValueError):
            project(html.replace('>old<',' id="old">old<'), {'one':'<p>mới</p>'}, page)

    def test_plain_markdown_and_math(self):
        body = render(Section(Path('example.qmd'), 'example', 'markdown', '**Tổng** $a+b$'))
        self.assertIn('<strong>Tổng</strong>', body)
        self.assertIn('<math', body)

    def test_long_mathml_line_preserves_the_entire_paragraph(self):
        prompt = 'Các biểu thức ' + ', '.join([r'$f(a)<f(b)$'] * 10) + ' có cùng ý nghĩa không?'
        body = render(Section(Path('example.qmd'), 'example', 'markdown', 'Đọc câu hỏi.\n\n' + prompt))
        paragraph = BeautifulSoup(body, 'html.parser').find_all('p')[1]
        self.assertTrue(paragraph.get_text().startswith('Các biểu thức '))
        self.assertEqual(len(paragraph.find_all('math')), 10)

    def test_overview_matches_full_projection_in_an_isolated_shell(self):
        page = c.PAGES['r1_g01']
        sections = declarations(c.ROOT/page.with_suffix('.qmd'))
        shell = ('<main><section id="tong-quan"></section>'
                 + ''.join(f'<section id="{key}"></section>' for key in
                           ('bai-hoc','phieu-luyen','tu-kiem-tra','on-lai','on-nen')) + '</main>')
        full, _ = full_projection(shell, {'tong-quan': sections['tong-quan']}, c.OUT/page)
        fragment = render(sections['tong-quan'])
        doc = BeautifulSoup(fragment, 'html.parser')
        links = doc.select('#overview-start nav li > a')
        self.assertEqual([a['href'] for a in links], ['#bai-hoc','#phieu-luyen','#tu-kiem-tra','#on-lai'])
        self.assertIsNone(doc.select_one('#overview-start details'))
        for link in links:
            self.assertTrue(link.strong.get_text(strip=True))
            self.assertTrue(link.br.next_sibling.strip())
        self.assertEqual(len(doc.select('#overview-goals li > strong')), 5)
        partial, _ = project(shell.replace('id="tong-quan">','id="tong-quan">old'),
                             {'tong-quan':fragment}, c.OUT/page)
        self.assertEqual(full, partial)

    def test_lesson_intro_keeps_the_link_target(self):
        page = c.PAGES['r1_g01']
        intro = declarations(c.ROOT/page.with_suffix('.qmd'))['dinh-huong-bai-hoc']
        fragment = BeautifulSoup(render(intro), 'html.parser')
        self.assertEqual(len(fragment.find_all('p', recursive=False)), 2)
        self.assertIsNotNone(fragment.select_one('#câu-hỏi-dẫn-đường'))
        self.assertIsNotNone(fragment.select_one('[data-lesson-intro-end]'))

    def test_shared_source_and_scope(self):
        with TemporaryDirectory(dir=c.ROOT/'_audit') as work:
            root = Path(work).resolve()
            home = c.BASE/'test'
            pages = {key: home/(key+'.html') for key in ('alpha','beta','gamma')}
            shared = root/home/'shared.qmd'
            shared.parent.mkdir(parents=True)
            shared.write_text('<!-- zo-section shared -->\nshared text\n<!-- /zo-section -->\n','utf-8')
            manifest = root/home/'_quy_trinh/ban_dang_duyet.json'
            manifest.parent.mkdir()
            manifest.write_text('{"files": []}', 'utf-8')
            current = root/'record.json'
            record = {'outputs': {}, 'page_inputs': {'unchanged': 'baseline'}}
            fixture = b'<section id="shared">old</section>\r\n<section id="local">old</section>'
            for key,page in pages.items():
                src = root/page.with_suffix('.qmd')
                src.write_text(('{{< include shared.qmd >}}\n' if key != 'gamma' else '')
                               + '<!-- zo-section local -->\n'+key+'\n<!-- /zo-section -->','utf-8')
                output = root/'docs'/page
                output.parent.mkdir(parents=True,exist_ok=True)
                output.write_bytes(fixture)
                record['outputs'][page.as_posix()] = digest(fixture)
            current.write_text(json.dumps(record),'utf-8')
            with patch.multiple(c, ROOT=root, HOME=home, OUT=root/'docs', DESIGN=root,
                                PAGES=pages, FOUNDATION=pages['gamma']), \
                 patch('zo_course_site_sections.render', side_effect=lambda s:'<p>'+s.markdown+'</p>'):
                report = root/'log.json'
                a = pages['alpha'].with_suffix('.qmd')
                result = build_sections([a], ['shared'], current, report)
                self.assertEqual(set(result['built']), {pages[k].as_posix() for k in ('alpha','beta')})
                self.assertEqual((root/'docs'/pages['gamma']).read_bytes(),fixture)
                self.assertEqual((root/'docs'/pages['beta']).read_bytes(),fixture.replace(b'>old<',b'><p>shared text</p><',1))
                self.assertEqual(json.loads(current.read_bytes())['page_inputs'],record['page_inputs'])
                build_sections([], [], current, report)
                self.assertFalse(build_sections([], [], current, report, plan=True)['sections'])
                shared.write_text(shared.read_text('utf-8').replace('shared text','revised'),'utf-8')
                plan = build_sections([a], [], current, report, plan=True)
                self.assertEqual(plan['sections'], {pages[k].as_posix():['shared'] for k in ('alpha','beta')})
                (root/'docs'/pages['beta']).write_bytes(b'untracked changes')
                before = (root/'docs'/pages['alpha']).read_bytes()
                with self.assertRaises(ValueError):
                    build_sections([a], [], current, report)
                self.assertEqual((root/'docs'/pages['alpha']).read_bytes(),before)


if __name__ == '__main__':
    unittest.main()
