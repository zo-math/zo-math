"""Start/reuse the local, loopback-only Analytics API for HTML previews."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import time
from urllib.error import URLError
from urllib.request import ProxyHandler, build_opener

ROOT = Path(__file__).resolve().parents[1]

def ensure():
    state = ROOT / '.local/site-views'
    if not (state/'analytics.dpapi').is_file() and not os.environ.get('CF_ANALYTICS_API_TOKEN'):
        return False
    http = build_opener(ProxyHandler({}))
    def ready():
        try:
            with http.open('http://127.0.0.1:8878/health', timeout=1) as response:
                return json.load(response).get('service') == 'zo-site-views'
        except (OSError, ValueError, URLError):
            return False
    if ready():
        return True
    node = shutil.which('node')
    if node is None:
        raise ValueError('Node.js is required for the local Cloudflare counter')
    state.mkdir(parents=True, exist_ok=True)
    with (state/'server.log').open('ab') as log:
        child = subprocess.Popen([node, str(ROOT/'scripts/zo_site_views/serve.mjs')], cwd=ROOT,
            stdin=subprocess.DEVNULL, stdout=log, stderr=log,
            **({'creationflags':subprocess.CREATE_NO_WINDOW} if os.name=='nt' else {'start_new_session':True}))
    for _ in range(30):
        if ready():
            return True
        if child.poll() is not None:
            raise ValueError('Local Analytics API could not start; inspect .local/site-views/server.log')
        time.sleep(.1)
    raise ValueError('Local Analytics API did not become ready')

if __name__ == '__main__':
    print(json.dumps({'local_api_ready':ensure()}))
