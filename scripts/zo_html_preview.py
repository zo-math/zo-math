"""Reopen an existing local HTML preview without rendering or publishing."""
from __future__ import annotations

import argparse
import functools
import hashlib
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import time
from urllib.error import URLError
from urllib.parse import quote
from urllib.request import ProxyHandler, build_opener
import webbrowser

ROOT = Path(__file__).resolve().parents[1]
HTTP = build_opener(ProxyHandler({}))


def page_path(root, page):
    root = Path(root).resolve()
    target = Path(page)
    target = (root / target).resolve() if not target.is_absolute() else target.resolve()
    if not target.is_relative_to(root) or target.suffix.lower() not in {'.html', '.htm'}:
        raise ValueError('Bản xem phải là HTML nằm trong repository.')
    if not target.is_file():
        raise ValueError('Không tìm thấy HTML đã dựng: ' + str(target))
    return target


def occupied(port):
    try:
        with socket.create_connection(('127.0.0.1', port), timeout=.3):
            return True
    except OSError:
        return False


def matches(url, expected):
    try:
        with HTTP.open(url, timeout=2) as response:
            return response.status == 200 and hashlib.sha256(response.read()).hexdigest() == expected
    except (OSError, URLError):
        return False


def ensure_preview(root, page, port=8877):
    root = Path(root).resolve()
    target = page_path(root, page)
    if not 1 <= port <= 65535:
        raise ValueError('Cổng phải trong khoảng 1–65535.')
    url = f'http://127.0.0.1:{port}/' + quote(target.relative_to(root).as_posix())
    expected = hashlib.sha256(target.read_bytes()).hexdigest()
    if occupied(port):
        if not matches(url, expected):
            raise ValueError(f'Cổng {port} đang phục vụ nội dung khác hoặc chưa sẵn sàng; không tự dừng tiến trình đó.')
        return {'url': url, 'server_started': False, 'pid': None, 'html_sha256': expected}
    command = [sys.executable, '-B', str(Path(__file__).resolve()), '--serve-root', str(root), '--port', str(port)]
    options = {'creationflags': subprocess.CREATE_NO_WINDOW} if os.name == 'nt' else {'start_new_session': True}
    process = subprocess.Popen(command, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL, cwd=str(root), **options)
    try:
        for _ in range(50):
            if process.poll() is not None:
                raise ValueError('Máy chủ xem không khởi động được; kiểm tra cổng đang dùng.')
            if matches(url, expected):
                return {'url': url, 'server_started': True, 'pid': process.pid, 'html_sha256': expected}
            time.sleep(.1)
        raise ValueError('Máy chủ chưa sẵn sàng; chưa mở trình duyệt.')
    except Exception:
        if process.poll() is None:
            process.terminate()
            process.wait(timeout=5)
        raise


def shortcut(root, page, port):
    target = page_path(root, page)
    launcher = target.parent / 'Mo_ban_xem_HTML.cmd'
    repo = os.path.relpath(Path(root).resolve(), target.parent).replace('/', '\\')
    name = target.name
    # cmd expands percent signs even inside quoted paths; reject ambiguous names.
    if any(c in repo + name for c in '%!\r\n'):
        raise ValueError('Đường dẫn không phù hợp với tệp mở nhanh Windows.')
    content = ('@echo off\r\nsetlocal\r\n'
               f'python -B "%~dp0{repo}\\scripts\\zo_python.py" -B "%~dp0{repo}\\scripts\\zo_html_preview.py" '
               f'--page "%~dp0{name}" --port {port}\r\n'
               'if errorlevel 1 pause\r\nendlocal\r\n')
    if launcher.exists() and launcher.read_bytes() != content.encode('utf-8'):
        raise ValueError('Tệp mở nhanh đã có nội dung khác; không ghi đè: ' + str(launcher))
    launcher.write_bytes(content.encode('utf-8'))
    return str(launcher)


class PreviewHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--page', help='HTML đã dựng, tương đối từ repo hoặc đường dẫn tuyệt đối')
    parser.add_argument('--port', type=int, default=8877)
    parser.add_argument('--no-browser', action='store_true')
    parser.add_argument('--shortcut', action='store_true', help='Tạo tệp mở nhanh cạnh HTML, giữ cùng bản xem')
    parser.add_argument('--serve-root', type=Path, help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    try:
        if args.serve_root:
            root = args.serve_root.resolve()
            if not root.is_relative_to(ROOT):
                raise ValueError('Thư mục phục vụ phải nằm trong repository.')
            handler = functools.partial(PreviewHandler, directory=str(root))
            with ThreadingHTTPServer(('127.0.0.1', args.port), handler) as server:
                server.serve_forever()
            return 0
        if not args.page:
            parser.error('--page là bắt buộc')
        result = ensure_preview(ROOT, args.page, args.port)
        if args.shortcut:
            result['shortcut'] = shortcut(ROOT, args.page, args.port)
        if not args.no_browser:
            result['browser_requested'] = bool(webbrowser.open(result['url']))
        print(json.dumps(result, ensure_ascii=False))
        return 0
    except (ValueError, OSError) as exc:
        print(json.dumps({'error': str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
