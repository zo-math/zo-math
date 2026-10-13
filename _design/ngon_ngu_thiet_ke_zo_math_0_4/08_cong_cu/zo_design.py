#!/usr/bin/env python3
"""Read-only inspector for the portable ZO Math design handoff. Python 3.9+."""
from pathlib import Path
import argparse,hashlib,json,re,sys
from urllib.parse import unquote
ROOT=Path(__file__).resolve().parents[1]
MUTABLE={'09_nhat_ki','_audit'}
REFERENCE={'06_nguon','07_mau_thi_giac'}
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def read_json(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def resolved(root,rel):
 p=(root/rel).resolve()
 if not p.is_relative_to(root.resolve()):raise ValueError('Đường dẫn ra ngoài bộ: '+rel)
 return p

def check(root=ROOT):
 errors=[];checks=0
 def require(ok,msg):
  nonlocal checks
  checks+=1
  if not ok:errors.append(msg)
 def load(rel):
  try:return read_json(root/rel)
  except (ValueError,OSError) as e:require(False,rel+': '+str(e));return None
 meta=load('03_du_lieu/bo_ban_giao.json');rules=load('03_du_lieu/quy_tac.json');sources=load('03_du_lieu/nguon.json');labels=load('03_du_lieu/trang_thai.json');targets=load('03_du_lieu/ho_so_ap_dung.json');colors=load('03_du_lieu/color_system.json');task=load('09_nhat_ki/cong_viec_hien_tai.json');assets=load('03_du_lieu/tai_san.json');manifest=load('08_cong_cu/manifest.json')
 if not all(x is not None for x in [meta,rules,sources,labels,targets,colors,task,assets,manifest]):return {'ok':False,'checks':checks,'errors':errors}
 for key in ['entry','rules','sources','active_task']:
  try:require(resolved(root,meta[key]).is_file(),'Thiếu tuyến đọc: '+key)
  except (ValueError,KeyError) as e:require(False,str(e))
 srcids={x['id'] for x in sources};ruleids={x['id'] for x in rules}
 require(len(srcids)==len(sources),'Trùng ID nguồn');require(len(ruleids)==len(rules),'Trùng ID quy tắc')
 require(len([s for s in sources if s.get('kind')=='provided_original'])==30,'Không đủ 30 đầu vào gốc')
 for s in sources:
  try:
   p=resolved(root,s['path']);require(p.is_file(),'Thiếu nguồn '+s['id'])
   if p.is_file() and s.get('sha256'):require(sha(p)==s['sha256'],'Nguồn gốc đã đổi: '+s['path'])
  except (ValueError,KeyError) as e:require(False,str(e))
 for r in rules:
  require(r.get('status') in labels,'Trạng thái không hợp lệ: '+r['id'])
  require(bool(r.get('scope')) and bool(r.get('limit')),'Thiếu phạm vi/giới hạn: '+r['id'])
  require(bool(r.get('evidence')) and all(e in srcids for e in r.get('evidence',[])),'Căn cứ thiếu/không tồn tại: '+r['id'])
 for t in targets['targets']:
  try:require(resolved(root,t['guide']).is_file(),'Thiếu hướng dẫn: '+t['id'])
  except ValueError as e:require(False,str(e))
  require(all(i in ruleids for i in t['rule_ids']),'Quy tắc đích không tồn tại: '+t['id'])
 require(task.get('target') in {t['id'] for t in targets['targets']},'Nhiệm vụ chỉ tới sản phẩm không có')
 try:require(resolved(root,task['guide']).is_file(),'Nhiệm vụ thiếu tuyến đọc')
 except (ValueError,KeyError) as e:require(False,str(e))
 for family,n in [('red',7),('yellow',7),('gray',9)]:
  expected={f'{family}-{i}' for i in range(1,n+1)}
  require({k for k in colors['palette'] if k.startswith(family+'-')}==expected,'Token không liên tiếp: '+family)
 require(len(colors['palette'])==23,'Sai số mã màu')
 for name,h in [('Đỏ ZO','#EF5350'),('Vàng ZO','#FFCA28'),('Xám ZO','#3E3A35')]:
  a=colors['anchors'].get(name,{})
  require(a.get('hex')==h and colors['palette'].get(a.get('token'))==h,'Màu gốc sai: '+name)
 require(len(set(colors['backgrounds']))==6 and all(x in colors['palette'] for x in colors['backgrounds']),'Sáu nền không hợp lệ')
 for a in assets:
  try:require(resolved(root,a['path']).is_file(),'Thiếu tài sản: '+a['path'])
  except ValueError as e:require(False,str(e))
 # Only authored operational documents: historical links are preserved verbatim.
 for p in root.rglob('*.md'):
  rel=p.relative_to(root)
  if rel.parts[0] in REFERENCE|MUTABLE:continue
  s=re.sub(r'```[\s\S]*?```','',p.read_text(encoding='utf-8'))
  for m in re.finditer(r'\[[^\]\n]*\]\(([^)\n]+)\)',s):
   link=m.group(1).strip().split(' "')[0]
   if re.match(r'^(https?://|mailto:|#)',link):continue
   link=unquote(link.split('#')[0])
   q=(p.parent/link).resolve()
   require(q.is_relative_to(root.resolve()) and q.exists(),'Liên kết hỏng trong '+str(rel)+': '+link)
 for x in manifest['files']:
  try:
   p=resolved(root,x['path']);require(p.is_file(),'Manifest thiếu tệp: '+x['path'])
   if p.is_file():require(p.stat().st_size==x['bytes'] and sha(p)==x['sha256'],'Khác bản phát hành: '+x['path'])
  except (ValueError,KeyError) as e:require(False,str(e))
 return {'ok':not errors,'checks':checks,'errors':errors,'limits':['Chỉ kiểm cấu trúc/nguồn/hash; không chứng nhận thiết kế, quyền duyệt hay tích hợp.','Liên kết trong nguồn lịch sử có thể trỏ ra ngoài bộ; xem mục lục và ghi chú thiếu.','09_nhat_ki và _audit được phép thay đổi; không khóa hash như tài nguyên phát hành.']}

def main():
 if hasattr(sys.stdout,'reconfigure'):sys.stdout.reconfigure(encoding='utf-8')
 ap=argparse.ArgumentParser(description=__doc__);sp=ap.add_subparsers(dest='command',required=True)
 sp.add_parser('check');sp.add_parser('status');find=sp.add_parser('find');find.add_argument('query')
 args=ap.parse_args()
 if args.command=='check':
  r=check();print(json.dumps(r,ensure_ascii=False,indent=2));return 0 if r['ok'] else 1
 if args.command=='status':
  m=read_json(ROOT/'03_du_lieu/bo_ban_giao.json');t=read_json(ROOT/'09_nhat_ki/cong_viec_hien_tai.json')
  print(json.dumps({'bo_ban_giao':m['package_version'],'mau_thiet_ke':m['design_specimen_version'],'cong_viec':t},ensure_ascii=False,indent=2));return 0
 found=[p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file() and not {'__pycache__','_audit'}&set(p.relative_to(ROOT).parts) and args.query.casefold() in p.relative_to(ROOT).as_posix().casefold()]
 for p in sorted(found)[:80]:print(p)
 print('Tổng:',len(found),'; hiển thị tối đa 80.');return 0 if found else 1
if __name__=='__main__':raise SystemExit(main())
