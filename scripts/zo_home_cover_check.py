"""Protect the complete Home cover library separately from its displayed image."""
import hashlib
import json
from pathlib import Path
import re
import struct


ROOT = Path(__file__).resolve().parents[1]
HOME = Path('content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027')
RATIOS = {'1x1', '3x4', '4x3', '9x16', '16x9'}


def check(root=ROOT):
    # Current assets have their own manifest. The original import receipt is
    # immutable and must not reject a replacement explicitly supplied by owner.
    manifest = root / HOME / 'giao_dien/bo_anh_bia.json'
    records = json.loads(manifest.read_text(encoding='utf-8'))['assets']
    expected = {f'hanh_trinh_nguoi_hoc_toan_{ratio}.png' for ratio in RATIOS}
    failures = []
    if len(records) != 5 or {Path(r['destination']).name for r in records} != expected:
        failures.append('Cover registry must retain exactly the five required formats')
    for record in records:
        path = root / record['destination']
        if not path.is_file():
            failures.append(f'Missing retained cover: {path.name}')
            continue
        data = path.read_bytes()
        if hashlib.sha256(data).hexdigest() != record['sha256'] or len(data) != record['bytes']:
            failures.append(f'Changed original cover: {path.name}')
        if (data[:8] != b'\x89PNG\r\n\x1a\n' or len(data) < 24
                or struct.unpack('>II', data[16:24]) != (record['width'], record['height'])):
            failures.append(f'Wrong cover dimensions: {path.name}')
    qmd = (root / HOME / 'index.qmd').read_text(encoding='utf-8')
    if re.findall(r'assets/illustrations/(hanh_trinh_nguoi_hoc_toan_\w+\.png)', qmd) != ['hanh_trinh_nguoi_hoc_toan_3x4.png']:
        failures.append('Displayed Home cover must remain the single 3x4 illustration')
    if 'hoc_truc_tiep_trao_doi.svg' in qmd:
        failures.append('Home references the obsolete service illustration')
    if (root / HOME / 'assets/illustrations/hoc_truc_tiep_trao_doi.svg').exists():
        failures.append('Obsolete service illustration remains in the active library')
    return failures


if __name__ == '__main__':
    errors = check()
    print(json.dumps({'passed': not errors, 'retained_formats': 5, 'failures': errors}, ensure_ascii=False))
    raise SystemExit(bool(errors))
