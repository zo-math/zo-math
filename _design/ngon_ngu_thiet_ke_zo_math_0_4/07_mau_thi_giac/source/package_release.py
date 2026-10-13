from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parents[1];out=R.parent/'ZO_Math_Bo_kiem_thu_0_4.zip'
def keep(p):
 rel=p.relative_to(R)
 if '__pycache__' in p.parts or p.suffix in ['.aux','.log','.pyc']:return False
 if rel.parts[0]=='qa':return p.suffix=='.json' or p.name=='design_board.png' or (len(rel.parts)>2 and rel.parts[1] in ['pdf_editions','guide_0_4'] and p.suffix=='.png')
 if p.name.endswith('_template.html'):return False
 if rel.parts[:2]==('source','tex') and p.suffix=='.pdf':return False
 if p.name=='manifest.json':return False
 return True
files=[p for p in sorted(R.rglob('*')) if p.is_file() and keep(p)]
manifest={'version':'0.4','files':[{'path':str(p.relative_to(R)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files]}
(R/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2));files.append(R/'manifest.json')
with zipfile.ZipFile(out.with_suffix('.tmp'), 'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in files:z.write(p,'ZO_Math_0_4/'+str(p.relative_to(R)))
with zipfile.ZipFile(out.with_suffix('.tmp')) as z:
 assert z.testzip() is None
 for row in manifest['files']:assert hashlib.sha256(z.read('ZO_Math_0_4/'+row['path'])).hexdigest()==row['sha256']
out.with_suffix('.tmp').replace(out);print(json.dumps({'files':len(files),'zip_bytes':out.stat().st_size,'zip_sha256':hashlib.sha256(out.read_bytes()).hexdigest()}))
