"""Regression of handoff gates; fixtures are not browser acceptance."""
import json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import zo_html_handoff as h

class HandoffTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory(dir=h.ROOT/'_audit',prefix='handoff-test-');self.root=Path(self.tmp.name);self.folder=self.root/'_audit/current';self.folder.mkdir(parents=True)
  self.entry=self.folder/'index.html';self.page=self.folder/'lesson.html';self.page.write_text('<html><head><title>Lesson</title></head><body>Actual learner content and mathematics</body></html>')
  self.entry.write_text('<html><head><title>Review</title></head><body>Current review entry <a href="lesson.html">Lesson</a></body></html>')
  self.authority=self.root/'03.md';self.authority.write_text('[Current](http://127.0.0.1:8877/_audit/current/index.html)\n[Old](http://127.0.0.1:8877/_audit/old/index.html)')
  self.http=patch.object(h.preview,'matches',return_value=True);self.http.start()
  self.server=patch.object(h.preview,'ensure_preview',return_value={'url':'http://127.0.0.1:8877/_audit/current/index.html'});self.server.start()
  self.prepared=self.root/'prepared.json';self.d=h.prepare(self.root,'03.md',self.prepared)
  self.evidence=self.root/'evidence.json';visits=[]
  for p,title in [(self.entry,'Review'),(self.page,'Lesson')]:
   rel=p.relative_to(self.root).as_posix();url=self.d['files'][rel]['url'];snapshot=p.with_suffix('.txt');snapshot.write_text(url+'\n'+title+'\nVisible content');shot=p.with_suffix('.png');shot.write_bytes(b'\x89PNG\r\n\x1a\nfixture')
   visits.append({'page':rel,'url':url,'title':title,'snapshot':snapshot.relative_to(self.root).as_posix(),'screenshot':shot.relative_to(self.root).as_posix(),'visible_content_confirmed':True})
  self.ev={'nonce':self.d['nonce'],'observed_at':h.now(),'visits':visits};self.write_evidence()
 def write_evidence(self):self.evidence.write_text(json.dumps(self.ev))
 def tearDown(self):self.http.stop();self.server.stop();self.tmp.cleanup()
 def confirm(self):return h.confirm(self.root,self.prepared,self.evidence,self.root/'confirmed.json')
 def test_prepare_is_not_ready(self):
  self.assertFalse(self.d['handoff_ready'])
  with self.assertRaisesRegex(ValueError,'NOT handoff-ready'):h.check(self.root,self.prepared)
 def test_transitive_css_font_and_download_are_sealed(self):
  runtime=self.root/'_audit/runtime';runtime.mkdir()
  (runtime/'main.css').write_text('@import "inner.css";')
  (runtime/'inner.css').write_text('@font-face{src:url(font.woff2)}')
  (runtime/'font.woff2').write_bytes(b'font')
  (runtime/'book.pdf').write_bytes(b'%PDF-fixture')
  self.page.write_text('<html><head><title>Lesson</title><link rel="stylesheet" href="../runtime/main.css"></head><body>Actual learner content <a href="../runtime/book.pdf">Download</a></body></html>')
  data=h.prepare(self.root,'03.md',self.root/'with-dependencies.json')
  for name in ['main.css','inner.css','font.woff2','book.pdf']:
   self.assertIn('_audit/runtime/'+name,data['files'])
  (runtime/'font.woff2').unlink()
  with self.assertRaisesRegex(ValueError,'Missing'):h.verify_live(self.root,data)
 def test_valid_omitted_body_tag(self):
  self.entry.write_text('<!doctype html><html><meta charset="utf-8"><title>Review</title><h1>A real current review page</h1><p>Visible learner content</p></html>')
  self.assertFalse(h.prepare(self.root,'03.md',self.root/'other.json')['handoff_ready'])
 def test_empty_document_rejected(self):
  self.page.write_text('<html><head><title>Only a title should not pass as lesson content</title></head><body></body></html>')
  with self.assertRaisesRegex(ValueError,'Empty/error preview'):h.prepare(self.root,'03.md',self.root/'other.json')
 def test_confirm_then_live_check(self):
  self.assertTrue(self.confirm()['handoff_ready']);self.assertTrue(h.check(self.root,self.root/'confirmed.json')['handoff_ready'])
 def test_stopped_server_rejected_even_after_confirmation(self):
  self.confirm()
  with patch.object(h.preview,'matches',return_value=False):
   with self.assertRaisesRegex(ValueError,'Server stopped'):h.check(self.root,self.root/'confirmed.json')
 def test_old_preview_rejected(self):
  self.authority.write_text('[New](http://127.0.0.1:8877/_audit/new/index.html)');p=self.root/'_audit/new/index.html';p.parent.mkdir();p.write_bytes(self.entry.read_bytes())
  with self.assertRaisesRegex(ValueError,'Current preview changed'):self.confirm()
 def test_expired_rejected(self):
  with self.assertRaisesRegex(ValueError,'expired'):h.verify_live(self.root,self.d,self.d['prepared_at']+601)
 def test_changed_html_rejected(self):
  self.page.write_text('Changed')
  with self.assertRaisesRegex(ValueError,'changed after preparation'):self.confirm()
 def test_only_hub_rejected(self):
  self.ev['visits']=self.ev['visits'][:1];self.write_evidence()
  with self.assertRaisesRegex(ValueError,'real content page'):self.confirm()
 def test_wrong_browser_url_rejected(self):
  self.ev['visits'][1]['url']='http://127.0.0.1:8877/old.html';self.write_evidence()
  with self.assertRaisesRegex(ValueError,'Browser URL'):self.confirm()
 def test_browser_error_rejected(self):
  p=self.root/self.ev['visits'][0]['snapshot'];p.write_text(p.read_text()+' ERR_CONNECTION_REFUSED')
  with self.assertRaisesRegex(ValueError,'shows an error'):self.confirm()
 def test_missing_screenshot_rejected(self):
  (self.root/self.ev['visits'][0]['screenshot']).unlink()
  with self.assertRaises(ValueError):self.confirm()
 def test_jpeg_browser_screenshot_supported(self):
  for visit in self.ev['visits']:(self.root/visit['screenshot']).write_bytes(b'\xff\xd8\xfffixture\xff\xd9')
  self.assertTrue(self.confirm()['handoff_ready'])
 def test_other_session_evidence_rejected(self):
  self.ev['nonce']='old';self.write_evidence()
  with self.assertRaisesRegex(ValueError,'another handoff'):self.confirm()
 def test_old_observation_rejected(self):
  self.ev['observed_at']=self.d['prepared_at']-1;self.write_evidence()
  with self.assertRaisesRegex(ValueError,'follow preparation'):self.confirm()
 def test_modified_browser_proof_rejected(self):
  self.confirm();(self.root/self.ev['visits'][0]['snapshot']).write_text('Changed evidence')
  with self.assertRaisesRegex(ValueError,'evidence changed'):h.check(self.root,self.root/'confirmed.json')
 def test_no_overwrite_of_historical_report(self):
  with self.assertRaisesRegex(ValueError,'NEW handoff report'):h.prepare(self.root,'03.md',self.prepared)
if __name__=='__main__':unittest.main(verbosity=2)
