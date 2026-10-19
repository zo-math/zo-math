"""Discover active review manifests independently of manual cleanup flags."""
import hashlib,json
from pathlib import Path

def active_manifests(root):
    root=Path(root).resolve();result=[]
    for path in sorted((root/'content').glob('**/_quy_trinh/ban_dang_duyet.json')):
        if '_audit' in path.relative_to(root).parts or 'lich_su' in path.relative_to(root).parts:continue
        if path.is_symlink() or not path.resolve().is_relative_to(root):raise ValueError('Unsafe review manifest: '+str(path))
        data=json.loads(path.read_text('utf-8'))
        if data.get('status')=='pending_owner_review':
            if not data.get('files') or not data.get('entrypoints'):raise ValueError('Active review has no protected files/entrypoints')
            for entry in data['files']:
                rel=Path(entry['path']);target=(root/rel).resolve()
                if rel.is_absolute() or '..' in rel.parts or not target.is_relative_to(root) or not target.is_file():raise ValueError('Missing/unsafe active review file: '+str(rel))
                if target.is_symlink() or any(p.is_symlink() for p in target.parents if p!=root):raise ValueError('Symlink in active review')
                if entry.get('sha256') and hashlib.sha256(target.read_bytes()).hexdigest()!=entry['sha256']:raise ValueError('Active review file changed: '+str(rel))
            if data.get('external_dependencies'):
                from zo_graphics import graphics_root
                tool=graphics_root(root)
                for entry in data['external_dependencies']:
                    external_path=(tool/entry['path']).resolve()
                    if not external_path.is_relative_to(tool) or not external_path.is_file() or external_path.is_symlink():raise ValueError('Missing/unsafe external graphics source: '+str(external_path))
                    if hashlib.sha256(external_path.read_bytes()).hexdigest()!=entry['sha256']:raise ValueError('External graphics source changed since review: '+str(external_path))
            names={entry['path'] for entry in data['files']}
            if not set(data['entrypoints'])<=names:raise ValueError('Review entrypoint absent from protected inventory')
            result.append(path)
    authority=Path('content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/_quy_trinh/03_dieu_hanh_chuong_trinh.md')
    if (root/authority).is_file():
        from zo_html_handoff import latest
        entry,_=latest(root,authority)
        protected=set()
        for path in result:
            protected.update(json.loads(path.read_text('utf-8'))['entrypoints'])
        if entry.relative_to(root).as_posix() not in protected:
            raise ValueError('Current operating HTML preview has no active protection manifest')
    return result
