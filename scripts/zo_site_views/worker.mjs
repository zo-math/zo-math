// Only aggregate counts leave this service. The API token is a server secret.
export const QUERY = `query SiteViews($account: string!, $filter: AccountRumPageloadEventsAdaptiveGroupsFilter_InputObject!) {
  viewer { accounts(filter: {accountTag: $account}) {
    totals: rumPageloadEventsAdaptiveGroups(limit: 1, filter: $filter) { count }
  } }
}`;
const DAY = 86400000;
const iso = t => new Date(t).toISOString();
export function settings(env) {
  const cfg = JSON.parse(env.SITE_CONFIG);
  if (!/^[a-f0-9]{32}$/.test(cfg.account_id) || !/^[a-f0-9]{32}$/.test(cfg.site_id)
      || !Array.isArray(cfg.hosts) || !cfg.hosts.length || cfg.hosts.some(h => !/^[a-z0-9.-]+$/.test(h))
      || !Number.isFinite(Date.parse(cfg.since)) || !cfg.since.endsWith('T00:00:00Z')) throw Error('Invalid configuration');
  return cfg;
}
export async function count(env, cfg, start, end, fetcher = fetch) {
  if (!env.CF_ANALYTICS_API_TOKEN) throw Error('Missing analytics credential');
  const response = await fetcher('https://api.cloudflare.com/client/v4/graphql', {
    method: 'POST', headers: {'Content-Type': 'application/json', Authorization: `Bearer ${env.CF_ANALYTICS_API_TOKEN}`},
    body: JSON.stringify({query: QUERY, variables: {account: cfg.account_id, filter: {
      datetime_geq: start, datetime_lt: end, siteTag: cfg.site_id, requestHost_in: cfg.hosts, bot: 0
    }}}), signal: AbortSignal.timeout(20000)
  });
  if (!response.ok) throw Error('Analytics HTTP failure');
  const result = await response.json();
  if (result.errors?.length) throw Error('Analytics query rejected');
  const accounts = result.data?.viewer?.accounts;
  if (!Array.isArray(accounts) || accounts.length !== 1 || !Array.isArray(accounts[0].totals)) throw Error('Incomplete analytics response');
  const rows = accounts[0].totals;
  if (rows.length > 1) throw Error('Unexpected aggregation');
  const value = rows.length === 0 ? 0 : rows[0].count;
  if (!Number.isSafeInteger(value) || value < 0) throw Error('Invalid analytics count');
  return value;
}
export async function update(env, now = Date.now(), fetcher = fetch) {
  const cfg = settings(env), identity = JSON.stringify(cfg);
  const previous = await env.SITE_VIEWS.get('ledger', 'json');
  if (previous && previous.identity !== identity) throw Error('Ledger configuration changed');
  const since = Date.parse(cfg.since), today = Math.floor(now / DAY) * DAY;
  if (since > now) throw Error('Start date is in the future');
  const last = previous ? Date.parse(previous.updated_at) : since;
  // Never silently replace an all-time total with a rolling retention window.
  if (now - last > 170 * DAY) throw Error('Analytics history gap requires reconciliation');
  const start = previous ? Math.max(since, Math.floor(last / DAY) * DAY - 7 * DAY) : since;
  const days = {...previous?.days};
  for (let t = start; t <= today; t += DAY) {
    const end = Math.min(t + DAY, now);
    if (end > t) days[iso(t).slice(0, 10)] = await count(env, cfg, iso(t), iso(end), fetcher);
  }
  const total = Object.values(days).reduce((a, b) => a + b, 0);
  if (!Number.isSafeInteger(total)) throw Error('Total exceeds safe integer range');
  const vietnamOffset = 7 * 3600000;
  const dayStart = Math.floor((now + vietnamOffset) / DAY) * DAY - vietnamOffset;
  const todayCount = now > dayStart ? await count(env, cfg, iso(Math.max(since, dayStart)), iso(now), fetcher) : 0;
  const ledger = {identity, days, updated_at: iso(now)};
  const snapshot = {schema_version: 1, source: 'Cloudflare Web Analytics', metric: 'page_views',
    scope: 'website', hosts: cfg.hosts, total, today: todayCount, day: iso(now+vietnamOffset).slice(0,10),
    day_timezone: 'Asia/Ho_Chi_Minh', since: cfg.since, updated_at: ledger.updated_at, exclude_bots: true};
  // One write publishes the whole successful refresh; failed requests preserve the last good value.
  await env.SITE_VIEWS.put('ledger', JSON.stringify({...ledger, snapshot}));
  return snapshot;
}
const origins = new Set(['https://zomath.vn', 'https://www.zomath.vn', 'http://127.0.0.1:8877', 'http://localhost:8877']);
export async function handle(request, env) {
  const url = new URL(request.url), origin = request.headers.get('Origin');
  const headers = {'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store', 'X-Content-Type-Options': 'nosniff', 'Vary': 'Origin'};
  if (origin && !origins.has(origin)) return new Response('{}', {status: 403, headers});
  if (origin) headers['Access-Control-Allow-Origin'] = origin;
  if (url.pathname !== '/api/site-views') return new Response('{}', {status: 404, headers});
  if (request.method !== 'GET') return new Response('{}', {status: 405, headers});
  const saved = await env.SITE_VIEWS.get('ledger', 'json');
  if (!saved?.snapshot || saved.identity !== JSON.stringify(settings(env))) return new Response(JSON.stringify({status: 'unavailable'}), {status: 503, headers});
  const stale = Date.now() - Date.parse(saved.updated_at) > 20 * 60000;
  return new Response(JSON.stringify({...saved.snapshot, stale}), {headers});
}
export default {
  fetch: handle,
  async scheduled(event, env) { await update(env); }
};
