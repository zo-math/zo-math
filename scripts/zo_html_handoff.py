"""Fresh, source-selected local HTML handoff; HTTP is not browser acceptance."""
from pathlib import Path
from datetime import datetime, timezone
import argparse, hashlib, json, re, uuid
from urllib.parse import urlsplit, unquote
from bs4 import BeautifulSoup
import zo_html_preview as preview
from zo_html_dependencies import preview_files

ROOT=preview.ROOT
MAX_AGE=600
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def now():return datetime.now(timezone.utc).timestamp()
def local(root,path):
 p=(Path(root)/path).resolve()
 if not p.is_relative_to(Path(root).resolve()) or not p.is_file():raise ValueError('Missing or outside repository: '+str(path))
 return p
def latest(root,authority):
 p=local(root,authority)
 # The operating document lists the current preview before historical entries.
 # Never infer freshness from an audit folder name or filesystem timestamp.
 match=re.search(r'http://127\.0\.0\.1:(\d+)/(_audit/[^\s)<>"\']+\.html)',p.read_text(encoding='utf-8'))
 if not match:raise ValueError('Authority has no explicit current localhost preview')
 return preview.page_path(root,unquote(match[2])),int(match[1])
def save(path,data):
 path=Path(path)
 if path.exists():raise ValueError('Use a NEW handoff report; retain previous evidence')
 path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def prepare(root,authority,report):
 root=Path(root).resolve();entry,port=latest(root,authority)
 state=preview.ensure_preview(root,entry,port)
 doc=BeautifulSoup(entry.read_text(encoding='utf-8'),'html.parser');pages={entry}
 for link in doc.select('a[href]'):
  u=urlsplit(link['href'])
  if u.scheme or u.netloc or not u.path:continue
  p=(entry.parent/unquote(u.path)).resolve()
  if p.is_relative_to(entry.parent) and p.suffix.lower()=='.html':pages.add(preview.page_path(root,p))
 files=preview_files(root,pages)
 for p in pages:
  d=BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser')
  # HTML permits omitted body tags; inspect learner text, not explicit syntax.
  content=BeautifulSoup(str(d.body or d.html or d),'html.parser')
  for ignored in content.select('head,script,style'):ignored.decompose()
  if len(content.get_text(' ',strip=True))<20:raise ValueError('Empty/error preview: '+str(p))
  for n in d.select('img[src],script[src],link[rel=stylesheet][href]'):
   u=urlsplit(n.get('src',n.get('href','')))
   if u.scheme or u.netloc or not u.path:continue
   target=(root/unquote(u.path).lstrip('/')).resolve() if u.path.startswith('/') else (p.parent/unquote(u.path)).resolve()
   files.add(local(root,target))
 origin=f'http://127.0.0.1:{port}/'
 from urllib.parse import quote
 records={p.relative_to(root).as_posix():{'sha256':sha(p),'url':origin+quote(p.relative_to(root).as_posix())} for p in files}
 for path,item in records.items():
  if not preview.matches(item['url'],item['sha256']):raise ValueError('HTTP does not serve current file: '+path)
 data={'schema_version':1,'nonce':str(uuid.uuid4()),'prepared_at':now(),'authority':str(Path(authority).as_posix()),'entry':entry.relative_to(root).as_posix(),'url':state['url'],'port':port,'pages':[p.relative_to(root).as_posix() for p in sorted(pages)],'files':records,'shortcut':preview.shortcut(root,entry,port),'handoff_ready':False,'browser_confirmation_required':True}
 save(report,data);return data
def verify_live(root,data,clock=None):
 age=(now() if clock is None else clock)-data['prepared_at']
 if not 0<=age<=MAX_AGE:raise ValueError('Handoff expired; prepare and observe again before delivery')
 entry,port=latest(root,data['authority'])
 if entry.relative_to(Path(root).resolve()).as_posix()!=data['entry'] or port!=data['port']:raise ValueError('Current preview changed; historical handoff rejected')
 for path,item in data['files'].items():
  if sha(local(root,path))!=item['sha256']:raise ValueError('Preview changed after preparation: '+path)
  if not preview.matches(item['url'],item['sha256']):raise ValueError('Server stopped or wrong HTTP content: '+path)
def confirm(root,prepared,evidence,output):
 data=json.loads(Path(prepared).read_text(encoding='utf-8'));verify_live(root,data)
 observed=json.loads(Path(evidence).read_text(encoding='utf-8'))
 if observed.get('nonce')!=data['nonce']:raise ValueError('Browser evidence belongs to another handoff')
 if not data['prepared_at']<=observed.get('observed_at',0)<=now():raise ValueError('Browser observation must follow preparation')
 required={data['entry']}
 if len(data['pages'])>1:required.add(next(p for p in data['pages'] if p!=data['entry']))
 seen=set();proof=[]
 for visit in observed.get('visits',[]):
  path=visit['page'];item=data['files'].get(path)
  if path not in data['pages'] or not item or visit.get('url')!=item['url']:raise ValueError('Browser URL is not a current declared page')
  snapshot=local(root,visit['snapshot']);shot=local(root,visit['screenshot']);text=snapshot.read_text(encoding='utf-8');title=visit.get('title','')
  if not title or title not in text or unquote(visit['url']).removeprefix('http://') not in unquote(text).replace('http://',''):raise ValueError('Snapshot must show the actual URL and page title')
  if any(s in text.lower() for s in ['err_connection_refused','err_empty_response','this site can’t be reached','không thể truy cập trang web']):raise ValueError('Browser shows an error')
  image=shot.read_bytes()
  if not (image.startswith(b'\x89PNG\r\n\x1a\n') or image.startswith(b'\xff\xd8\xff') and image.endswith(b'\xff\xd9')):raise ValueError('Actual PNG/JPEG browser screenshot required')
  if visit.get('visible_content_confirmed') is not True:raise ValueError('Browser content has not been observed')
  seen.add(path);proof.append(dict(visit,snapshot_sha256=sha(snapshot),screenshot_sha256=sha(shot)))
 if not required<=seen:raise ValueError('Observe entry and a real content page, not just the hub')
 data.update(handoff_ready=True,browser_confirmation_required=False,confirmed_at=now(),browser_evidence=proof,owner_acceptance=False,published=False)
 save(output,data);return data
def check(root,path):
 data=json.loads(Path(path).read_text(encoding='utf-8'))
 if data.get('handoff_ready') is not True or not data.get('browser_evidence'):raise ValueError('HTTP-only or browser-requested status is NOT handoff-ready')
 verify_live(root,data)
 for visit in data['browser_evidence']:
  for name in ['snapshot','screenshot']:
   if sha(local(root,visit[name]))!=visit[name+'_sha256']:raise ValueError('Browser evidence changed')
 return data
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('command',choices=['prepare','confirm','check']);p.add_argument('--authority');p.add_argument('--report',type=Path,required=True);p.add_argument('--evidence',type=Path);p.add_argument('--output',type=Path);a=p.parse_args()
 try:
  for dest in [a.report,a.output]:
   if dest is not None and not dest.resolve().is_relative_to(ROOT/'_audit'):raise ValueError('Handoff reports must live under repository/_audit')
  if a.command=='prepare':
   if not a.authority:raise ValueError('--authority required')
   d=prepare(ROOT,a.authority,a.report)
  elif a.command=='confirm':
   if not a.evidence or not a.output:raise ValueError('--evidence and --output required')
   d=confirm(ROOT,a.report,a.evidence,a.output)
  else:d=check(ROOT,a.report)
  print(json.dumps({k:d[k] for k in ['url','handoff_ready','browser_confirmation_required']},ensure_ascii=False));return 0
 except (ValueError,OSError,KeyError) as e:print(str(e),file=__import__('sys').stderr);return 1
if __name__=='__main__':raise SystemExit(main())
