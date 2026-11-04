"""Deploy the aggregate-only Cloudflare service using encrypted local credentials.

Run through scripts/zo_python.py. Tokens are never printed, put in arguments,
or written in plaintext. The temporary deployment token is not a Worker binding.
"""
from pathlib import Path
from datetime import datetime, timezone
import argparse, hashlib, json, re
import requests
from zo_site_views_secret import convert

ROOT=Path(__file__).resolve().parents[1]

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--worker',required=True)
    parser.add_argument('--subdomain',required=True)
    parser.add_argument('--report',type=Path,required=True)
    args=parser.parse_args()
    if any(not re.fullmatch(r'[a-z0-9-]+',v) for v in [args.worker,args.subdomain]):
        raise ValueError('Invalid Worker name or subdomain')
    config=json.loads((ROOT/'scripts/zo_site_views/config.json').read_text('utf-8'))
    account=config['account_id']
    if not re.fullmatch(r'[a-f0-9]{32}',account):raise ValueError('Invalid account')
    credential_dir=ROOT/'.local/site-views'
    deployment_token=convert((credential_dir/'deploy.dpapi').read_bytes(),decrypt=True).decode()
    analytics_token=convert((credential_dir/'analytics.dpapi').read_bytes(),decrypt=True).decode()
    session=requests.Session()
    session.headers.update(Authorization='Bearer '+deployment_token)
    base='https://api.cloudflare.com/client/v4/accounts/'+account
    def api(method,path,**kwargs):
        response=session.request(method,base+path,timeout=60,allow_redirects=False,**kwargs)
        if not response.ok:raise RuntimeError(f'Cloudflare {method} {path}: HTTP {response.status_code}')
        data=response.json()
        if not data.get('success'):raise RuntimeError('Cloudflare rejected '+method+' '+path+'; codes='+str([r.get('code') for r in data.get('errors',[])]))
        return data.get('result')
    namespaces=api('GET','/storage/kv/namespaces',params={'per_page':100})
    found=[row for row in namespaces if row['title']==args.worker]
    if len(found)>1:raise ValueError('Ambiguous KV namespace')
    namespace=(found[0] if found else api('POST','/storage/kv/namespaces',json={'title':args.worker}))['id']
    ledger_path='/storage/kv/namespaces/'+namespace+'/values/ledger'
    current=session.get(base+ledger_path,timeout=30,allow_redirects=False)
    identity=json.dumps(config,separators=(',',':'),ensure_ascii=False)
    if current.status_code==404:
        ledger=json.loads((credential_dir/'ledger.json').read_text('utf-8'))
        stamp=datetime.fromisoformat(ledger['updated_at'].replace('Z','+00:00'))
        if ledger['identity']!=identity or abs((datetime.now(timezone.utc)-stamp).total_seconds())>1200:
            raise ValueError('A fresh, matching Cloudflare ledger is required for bootstrap')
        if ledger['snapshot'].get('source')!='Cloudflare Web Analytics' or ledger['snapshot'].get('exclude_bots') is not True:
            raise ValueError('Bootstrap must contain the real filtered Cloudflare snapshot')
        api('PUT',ledger_path,data=json.dumps(ledger),headers={'Content-Type':'application/json'})
        bootstrapped=True
    elif current.ok:
        ledger=current.json()
        if ledger.get('identity')!=identity:raise ValueError('Existing ledger belongs to another configuration')
        bootstrapped=False
    else:raise RuntimeError('Cannot verify existing KV ledger')
    code=(ROOT/'scripts/zo_site_views/worker.mjs').read_bytes()
    metadata={'main_module':'worker.mjs','compatibility_date':'2026-11-01',
        'bindings':[{'type':'kv_namespace','name':'SITE_VIEWS','namespace_id':namespace},
                    {'type':'plain_text','name':'SITE_CONFIG','text':json.dumps(config)},
                    {'type':'secret_text','name':'CF_ANALYTICS_API_TOKEN','text':analytics_token}]}
    script='/workers/scripts/'+args.worker
    uploaded=api('PUT',script,files={'metadata':(None,json.dumps(metadata),'application/json'),
        'worker.mjs':('worker.mjs',code,'application/javascript+module')})
    api('POST',script+'/subdomain',json={'enabled':True,'previews_enabled':False})
    schedule=api('PUT',script+'/schedules',json=[{'cron':'*/5 * * * *'}])
    url='https://'+args.worker+'.'+args.subdomain+'.workers.dev/api/site-views'
    response=requests.get(url,headers={'Origin':'https://zomath.vn','Cache-Control':'no-cache'},timeout=30)
    response.raise_for_status();snapshot=response.json()
    if (response.headers.get('Access-Control-Allow-Origin')!='https://zomath.vn'
        or snapshot.get('source')!='Cloudflare Web Analytics' or snapshot.get('stale')
        or snapshot.get('hosts')!=config['hosts']):raise ValueError('Public endpoint verification failed')
    report={'deployed_at':datetime.now(timezone.utc).isoformat(),'account_id':account,'worker':args.worker,
        'endpoint':url,'namespace_id':namespace,'cron':'*/5 * * * *','code_sha256':hashlib.sha256(code).hexdigest(),
        'analytics_credential_storage':'Cloudflare encrypted secret binding; no token in report',
        'deployment_credential_storage':'Windows DPAPI; temporary token must be revoked after deployment',
        'kv_bootstrapped_from_fresh_cloudflare_ledger':bootstrapped,'snapshot':snapshot,
        'cors_verified':True,'scheduled_update_verified':False}
    target=(ROOT/args.report).resolve();target.relative_to(ROOT)
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n','utf-8')
    print(json.dumps({'endpoint':url,'total':snapshot['total'],'today':snapshot['today'],'cron':'*/5 * * * *','public_API_verified':True},ensure_ascii=False))

if __name__=='__main__':main()
