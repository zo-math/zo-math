"""Exercise preview reopening with real local servers, never rendering lessons."""
import functools
import hashlib
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import socket
import subprocess
import tempfile
import threading
import unittest
from unittest.mock import patch
from urllib.request import urlopen

import zo_html_preview as preview


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


class PreviewTests(unittest.TestCase):
    def setUp(self):
        audit = preview.ROOT / '_audit'
        audit.mkdir(exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(prefix='html-preview-test-', dir=audit)
        self.root = Path(self.temp.name).resolve()
        assert self.root.is_relative_to(audit.resolve())
        self.page = self.root / 'học liệu có dấu' / 'index.html'
        self.page.parent.mkdir()
        self.page.write_text('<html><link rel="stylesheet" href="style.css">Bản xem đúng</html>', encoding='utf-8')
        self.page.with_name('style.css').write_text('body{color:red}', encoding='utf-8')
        self.original = hashlib.sha256(self.page.read_bytes()).hexdigest()
        self.children = []
        popen = subprocess.Popen
        def spawn(*args, **kwargs):
            child = popen(*args, **kwargs)
            self.children.append(child)
            return child
        self.patch = patch.object(preview.subprocess, 'Popen', side_effect=spawn)
        self.patch.start()

    def tearDown(self):
        self.patch.stop()
        for child in self.children:
            if child.poll() is None:
                child.terminate()
            child.wait(timeout=5)
        self.temp.cleanup()

    def port(self):
        with socket.socket() as sock:
            sock.bind(('127.0.0.1', 0))
            return sock.getsockname()[1]

    def test_stopped_server_restarts_and_preserves_html_and_assets(self):
        port = self.port()
        first = preview.ensure_preview(self.root, self.page, port)
        self.assertTrue(first['server_started'])
        with urlopen(first['url'].replace('index.html', 'style.css')) as response:
            self.assertEqual(response.read(), b'body{color:red}')
        self.children[0].terminate(); self.children[0].wait(timeout=5)
        second = preview.ensure_preview(self.root, self.page, port)
        self.assertTrue(second['server_started'])
        self.assertNotEqual(first['pid'], second['pid'])
        self.assertEqual(hashlib.sha256(self.page.read_bytes()).hexdigest(), self.original)
        self.assertEqual(second['html_sha256'], self.original)

    def test_running_correct_server_is_reused(self):
        port = self.port()
        preview.ensure_preview(self.root, self.page, port)
        second = preview.ensure_preview(self.root, self.page, port)
        self.assertFalse(second['server_started'])
        self.assertEqual(len(self.children), 1)

    def test_occupied_port_with_wrong_content_is_not_taken_over(self):
        wrong = self.root / 'wrong'; wrong.mkdir()
        server = ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(QuietHandler, directory=str(wrong)))
        thread = threading.Thread(target=server.serve_forever, daemon=True); thread.start()
        try:
            with self.assertRaisesRegex(ValueError, 'nội dung khác'):
                preview.ensure_preview(self.root, self.page, server.server_port)
            self.assertTrue(preview.occupied(server.server_port))
            self.assertFalse(self.children)
        finally:
            server.shutdown(); server.server_close(); thread.join()

    def test_missing_page_does_not_start_server(self):
        with self.assertRaisesRegex(ValueError, 'Không tìm thấy'):
            preview.ensure_preview(self.root, self.root / 'missing.html', self.port())
        self.assertFalse(self.children)

    def test_escape_and_non_html_are_rejected(self):
        for page in [self.root.parent / 'outside.html', self.page.with_suffix('.css')]:
            with self.assertRaises(ValueError):
                preview.ensure_preview(self.root, page, self.port())
        self.assertFalse(self.children)

    def test_invalid_port_does_not_start_server(self):
        with self.assertRaises(ValueError):
            preview.ensure_preview(self.root, self.page, 65536)
        self.assertFalse(self.children)

    def test_shortcut_is_relative_repeatable_and_uses_both_bytecode_flags(self):
        launcher = Path(preview.shortcut(preview.ROOT, self.page, 8877))
        data = launcher.read_bytes()
        self.assertIn(b'python -B "%~dp0', data)
        self.assertIn(b'zo_python.py" -B ', data)
        self.assertIn(b'\r\n', data)
        self.assertNotIn(str(preview.ROOT).encode(), data)
        self.assertEqual(preview.shortcut(preview.ROOT, self.page, 8877), str(launcher))
        self.assertEqual(launcher.read_bytes(), data)
        launcher.write_text('owner content', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'không ghi đè'):
            preview.shortcut(preview.ROOT, self.page, 8877)


if __name__ == '__main__':
    unittest.main(verbosity=2)
