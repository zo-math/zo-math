"""Store the local Analytics credential encrypted for the current Windows user.

This file never logs the token. `read` is only consumed by the local API child.
"""
import argparse
import ctypes
from ctypes import wintypes
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / '.local/site-views/analytics.dpapi'

class Blob(ctypes.Structure):
    _fields_ = [('size', wintypes.DWORD), ('data', ctypes.POINTER(ctypes.c_byte))]

def convert(data, decrypt=False):
    buffer = ctypes.create_string_buffer(data)
    source = Blob(len(data), ctypes.cast(buffer, ctypes.POINTER(ctypes.c_byte)))
    target = Blob()
    if decrypt:
        ok = ctypes.windll.crypt32.CryptUnprotectData(ctypes.byref(source), None, None, None, None, 1, ctypes.byref(target))
    else:
        ok = ctypes.windll.crypt32.CryptProtectData(ctypes.byref(source), 'ZO Math Analytics', None, None, None, 1, ctypes.byref(target))
    if not ok:
        raise RuntimeError('Windows credential encryption failed')
    try:
        return ctypes.string_at(target.data, target.size)
    finally:
        ctypes.windll.kernel32.LocalFree(target.data)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['store', 'read'])
    args = parser.parse_args()
    if args.command == 'store':
        secret = sys.stdin.buffer.read().strip()
        if len(secret) < 20 or len(secret) > 512 or any(chr(c).isspace() for c in secret):
            raise ValueError('Invalid credential')
        TARGET.parent.mkdir(parents=True, exist_ok=True)
        TARGET.write_bytes(convert(secret))
    else:
        sys.stdout.buffer.write(convert(TARGET.read_bytes(), decrypt=True))
