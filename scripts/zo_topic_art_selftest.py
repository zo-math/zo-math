"""Regression checks for approval, path and byte-preservation boundaries."""
from pathlib import Path
from tempfile import TemporaryDirectory
import hashlib
import json
import unittest
from PIL import Image
import zo_topic_art as art


class ArtworkBoundary(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.folder = self.root/'content/thpt/on_thi_toan_thpt/hoc_lieu/example/hinh/v1'
        self.folder.mkdir(parents=True)
        self.master = self.folder/'approved.png'
        image = Image.new('RGBA', (40, 24))
        image.putpixel((20, 12), (239, 83, 80, 255))
        image.save(self.master)
        self.manifest = dict(package='example', approval={'status':'approved'}, alt='Example',
                             master=dict(file='approved.png',sha256=art.sha(self.master),dimensions=[40,24]), variants={})
        self.registry = dict(schema_version=1,formats={'1x1':[100,100]},
                             packages={'example':{'manifest':(self.folder/'manifest.json').relative_to(self.root).as_posix()}})
        (self.root/art.REGISTRY).parent.mkdir(parents=True)
        self.save()

    def save(self):
        (self.folder/'manifest.json').write_text(json.dumps(self.manifest),'utf-8')
        (self.root/art.REGISTRY).write_text(json.dumps(self.registry),'utf-8')

    def test_master_tamper_refused(self):
        self.master.write_bytes(self.master.read_bytes()+b'changed')
        with self.assertRaisesRegex(ValueError,'master changed'):
            art.export(self.root,build=True)

    def test_unapproved_master_refused(self):
        self.manifest['approval']['status']='pending_owner_review'
        self.save()
        with self.assertRaisesRegex(ValueError,'not been approved'):
            art.export(self.root,build=True)

    def test_registry_escape_refused(self):
        self.registry['packages']['example']['manifest']='../outside.json'
        self.save()
        with self.assertRaisesRegex(ValueError,'escapes repository'):
            art.export(self.root,build=True)

    def test_pending_recomposition_never_inherits_master_approval(self):
        self.manifest['variant_sources']={'1x1':dict(file='approved.png',sha256=art.sha(self.master),dimensions=[40,24],approval='pending_owner_review')}
        self.save()
        original=self.master.read_bytes()
        art.export(self.root,build=True)
        data=json.loads((self.folder/'manifest.json').read_text('utf-8'))
        self.assertEqual(data['variants']['1x1']['artwork_approval'],'pending_owner_review')
        self.assertEqual(self.master.read_bytes(),original)
        art.export(self.root)

    def test_changed_export_cannot_be_silently_rebuilt(self):
        art.export(self.root,build=True)
        image=self.folder/'example-minh-hoa-1x1.png'
        image.write_bytes(image.read_bytes()+b'changed')
        with self.assertRaisesRegex(ValueError,'changed outside exporter'):
            art.export(self.root,build=True)


if __name__=='__main__':
    unittest.main()
