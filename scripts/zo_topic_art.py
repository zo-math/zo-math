"""Versioned, approved topic artwork: export exact-ratio transparent PNGs."""
from pathlib import Path
import argparse
import hashlib
import json
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = Path('content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/_data/minh_hoa_chuyen_de.json')


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def local(root, name):
    path = (Path(root) / name).resolve()
    if not path.is_relative_to(Path(root).resolve()):
        raise ValueError('Artwork path escapes repository: ' + str(name))
    return path


def load_registry(root=ROOT):
    registry = json.loads((Path(root) / REGISTRY).read_text('utf-8'))
    if registry['schema_version'] != 1:
        raise ValueError('Unsupported topic-art registry')
    return registry


def load_master(root, package, registry=None):
    registry = registry or load_registry(root)
    path = local(root, registry['packages'][package]['manifest'])
    folder = Path(root) / 'content/thpt/on_thi_toan_thpt/hoc_lieu' / package / 'hinh'
    if not path.is_relative_to(folder.resolve()):
        raise ValueError('Artwork must be owned by its package')
    manifest = json.loads(path.read_text('utf-8'))
    if manifest['package'] != package or manifest['approval']['status'] != 'approved':
        raise ValueError('Topic artwork has not been approved: ' + package)
    image = (path.parent / manifest['master']['file']).resolve()
    if not image.is_relative_to(path.parent) or sha(image) != manifest['master']['sha256']:
        raise ValueError('Approved topic master changed: ' + package)
    with Image.open(image) as im:
        if im.mode != 'RGBA' or list(im.size) != manifest['master']['dimensions']:
            raise ValueError('Wrong topic master mode or dimensions: ' + package)
        if im.getchannel('A').getextrema() != (0, 255):
            raise ValueError('Topic artwork must retain transparent background')
    return path, manifest, image


def card_art(root, package):
    """None means retain the existing cover; registered artwork must validate."""
    registry = load_registry(root)
    if package not in registry['packages']:
        return None
    _, manifest, image = load_master(root, package, registry)
    return image, manifest['alt']


def export(root=ROOT, packages=None, build=False):
    root = Path(root)
    registry = load_registry(root)
    selected = packages or list(registry['packages'])
    if len(selected) != len(set(selected)):
        raise ValueError('Select unique packages')
    checked = []
    for package in selected:
        path, manifest, original = load_master(root, package, registry)
        before = sha(original)
        records = {}
        with Image.open(original) as opened:
            image = opened.copy()
        requested = manifest.get('requested_formats', list(registry['formats']))
        if set(requested) - set(registry['formats']):
            raise ValueError('Unknown requested artwork format')
        for ratio, size in registry['formats'].items():
            if ratio not in requested:
                continue
            width, height = size
            rw, rh = map(int, ratio.split('x'))
            if width * rh != height * rw:
                raise ValueError('Inexact aspect ratio: ' + ratio)
            source = manifest.get('variant_sources', {}).get(ratio)
            if source:
                variant_source = (path.parent / source['file']).resolve()
                if not variant_source.is_relative_to(path.parent) or sha(variant_source) != source['sha256']:
                    raise ValueError('Recomposed variant source changed: ' + ratio)
                with Image.open(variant_source) as opened:
                    frame = opened.copy()
                if frame.mode != 'RGBA' or list(frame.size) != source['dimensions']:
                    raise ValueError('Wrong recomposed source dimensions/mode: ' + ratio)
                approval = source['approval']
                if approval not in {'pending_owner_review', 'approved'}:
                    raise ValueError('Unknown recomposed variant approval: ' + ratio)
                composition = 'recomposed_for_ratio'
            else:
                frame = image
                approval = 'inherited_from_unchanged_master'
                composition = 'unchanged'
            margin = manifest.get('export_margin_px', 0)
            if not isinstance(margin, int) or not 0 <= margin < min(width, height) / 2:
                raise ValueError('Invalid transparent export margin')
            scale = min((width - 2 * margin) / frame.width, (height - 2 * margin) / frame.height, 1)
            fitted = (max(1, round(frame.width * scale)), max(1, round(frame.height * scale)))
            # Premultiply alpha for resampling: no dark fringes on transparency.
            resized = frame.convert('RGBa').resize(fitted, Image.Resampling.LANCZOS).convert('RGBA')
            canvas = Image.new('RGBA', size, (0, 0, 0, 0))
            offset = ((width - fitted[0]) // 2, (height - fitted[1]) // 2)
            canvas.paste(resized, offset)
            output = path.parent / f'{package}-minh-hoa-{ratio}.png'
            if build:
                if output.exists() and ratio in manifest.get('variants', {}):
                    expected = manifest['variants'][ratio]['sha256']
                    if sha(output) != expected:
                        raise ValueError('Variant changed outside exporter: ' + str(output))
                elif output.exists():
                    raise ValueError('Refuse to overwrite unregistered variant: ' + str(output))
                canvas.save(output, format='PNG', optimize=True)
            if not output.is_file():
                raise ValueError('Missing variant: ' + str(output))
            with Image.open(output) as actual:
                if actual.mode != 'RGBA' or actual.size != tuple(size):
                    raise ValueError('Wrong variant size/mode: ' + str(output))
                if actual.tobytes() != canvas.tobytes():
                    raise ValueError('Variant does not preserve the approved master: ' + str(output))
                if actual.getpixel((0, 0))[3] != 0 or actual.getchannel('A').getextrema() != (0, 255):
                    raise ValueError('Variant lost transparent background: ' + str(output))
            records[ratio] = dict(file=output.name, dimensions=size, bytes=output.stat().st_size,
                                  sha256=sha(output), fitted_dimensions=list(fitted), offset=list(offset),
                                  method='contain_without_crop_or_upscale_on_transparent_canvas',
                                  artwork_approval=approval, composition=composition,
                                  source_file=source['file'] if source else manifest['master']['file'])
            if not build and manifest.get('variants', {}).get(ratio) != records[ratio]:
                raise ValueError('Variant manifest mismatch: ' + str(output))
        if sha(original) != before:
            raise ValueError('Original was modified during export')
        if build:
            manifest['variants'] = records
            manifest['exporter'] = 'scripts/zo_topic_art.py'
            path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', 'utf-8')
        checked.append(dict(package=package, variants=len(records), master_unchanged=True))
    return checked


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['build', 'check'])
    parser.add_argument('--package', action='append', help='Registered package; default all registered artwork')
    args = parser.parse_args()
    try:
        print(json.dumps({'passed': True, 'packages': export(packages=args.package, build=args.command == 'build')}, ensure_ascii=False))
        return 0
    except (ValueError, KeyError, OSError) as error:
        print(json.dumps({'passed': False, 'error': str(error)}, ensure_ascii=False))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
