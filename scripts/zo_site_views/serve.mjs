// Local API uses the exact Worker query/aggregation/response implementation.
import http from 'node:http';
import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {execFileSync} from 'node:child_process';
import {update, handle} from './worker.mjs';
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const stateDir = path.join(root, '.local/site-views');
await fs.mkdir(stateDir, {recursive:true});
const stateFile = path.join(stateDir, 'ledger.json');
const env = {SITE_CONFIG: await fs.readFile(new URL('./config.json', import.meta.url), 'utf8'),
  CF_ANALYTICS_API_TOKEN: process.env.CF_ANALYTICS_API_TOKEN || '',
  SITE_VIEWS: {
    async get(key, type) { try { const value = await fs.readFile(stateFile, 'utf8'); return type === 'json' ? JSON.parse(value) : value; } catch (e) { if (e.code === 'ENOENT') return null; throw e; } },
    async put(key, value) { await fs.writeFile(stateFile+'.tmp', value, {mode:0o600}); await fs.rename(stateFile+'.tmp', stateFile); }
  }};
if (!env.CF_ANALYTICS_API_TOKEN) {
  try { env.CF_ANALYTICS_API_TOKEN = execFileSync('python', ['-B','scripts/zo_python.py','-B','scripts/zo_site_views_secret.py','read'], {cwd:root,encoding:'utf8',windowsHide:true,stdio:['ignore','pipe','ignore']}).trim(); }
  catch { /* Remain unavailable until the owner supplies the scoped credential. */ }
}
let updating = false;
async function tick() {
  if (updating) return;
  updating = true;
  try { const value = await update(env); console.log(JSON.stringify({event:'updated',total:value.total,updated_at:value.updated_at})); }
  catch { console.error('Cloudflare refresh failed; retained previous aggregate.'); }
  finally { updating = false; }
}
const server = http.createServer(async (req, res) => {
  if (req.url === '/health' && req.method === 'GET') {
    res.writeHead(200, {'Content-Type':'application/json','Cache-Control':'no-store'});
    res.end('{"service":"zo-site-views"}'); return;
  }
  try {
    const response = await handle(new Request('http://127.0.0.1:8878'+req.url, {method:req.method,headers:req.headers}), env);
    res.writeHead(response.status, Object.fromEntries(response.headers)); res.end(await response.text());
  } catch { res.writeHead(503, {'Content-Type':'application/json'}); res.end('{"status":"unavailable"}'); }
});
server.listen(8878, '127.0.0.1', () => console.log('Site views local API: 127.0.0.1:8878'));
await tick();
setInterval(tick, 5 * 60000);
