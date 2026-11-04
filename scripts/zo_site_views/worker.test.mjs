import {test} from 'node:test';
import assert from 'node:assert/strict';
import {update, handle, count} from './worker.mjs';
import fs from 'node:fs/promises';
const config = await fs.readFile(new URL('./config.json', import.meta.url), 'utf8');
function environment() {
  let state = null;
  return {SITE_CONFIG:config,CF_ANALYTICS_API_TOKEN:'test-only',SITE_VIEWS:{
    async get() {return state ? JSON.parse(state):null;}, async put(key,value){state=value;}
  }};
}
function data(value) {return async(url,options)=> {
  assert.equal(url,'https://api.cloudflare.com/client/v4/graphql');
  const body=JSON.parse(options.body),filter=body.variables.filter;
  assert.equal(filter.bot,0); assert.equal(filter.siteTag,JSON.parse(config).site_id);
  assert.deepEqual(filter.requestHost_in,JSON.parse(config).hosts);
  return Response.json({data:{viewer:{accounts:[{totals:[{count:value}]}]}}});
};}
test('repeated refresh replaces daily values rather than adding them twice',async()=>{
  const env=environment(),now=Date.parse('2026-11-04T07:00:00Z');
  assert.equal((await update(env,now,data(12))).total,24);
  assert.equal((await update(env,now+60000,data(13))).total,26);
});
test('failed refresh leaves every part of the last good ledger intact',async()=>{
  const env=environment(),now=Date.parse('2026-11-04T07:00:00Z');
  await update(env,now,data(12)); const before=await env.SITE_VIEWS.get();
  let requests=0;
  await assert.rejects(update(env,now+60000,async(...args)=> ++requests===1 ? data(20)(...args) : Response.json({errors:[{message:'private server detail'}]})));
  assert.deepEqual(await env.SITE_VIEWS.get(),before);
});
test('missing account, fractional/negative counts and GraphQL errors never become zero',async()=>{
  const env=environment(),cfg=JSON.parse(config);
  for(const payload of [{data:{viewer:{accounts:[]}}},{errors:[{}]},{data:{viewer:{accounts:[{totals:[{count:-1}]}]}}},{data:{viewer:{accounts:[{totals:[{count:1.5}]}]}}}]) {
    await assert.rejects(count(env,cfg,cfg.since,'2026-11-04T00:00:00Z',async()=>Response.json(payload)));
  }
});
test('long outage is rejected instead of silently losing history',async()=>{
  const env=environment();await assert.rejects(update(env,Date.parse('2027-11-04T00:00:00Z'),data(0)));
});
test('API exposes aggregate only, labels stale data and restricts origins/methods',async()=>{
  const env=environment();
  assert.equal((await handle(new Request('http://local/api/site-views'),env)).status,503);
  await update(env,Date.parse('2026-11-04T07:00:00Z'),data(12));
  const response=await handle(new Request('http://local/api/site-views',{headers:{Origin:'http://127.0.0.1:8877'}}),env);
  assert.equal(response.headers.get('Access-Control-Allow-Origin'),'http://127.0.0.1:8877');
  const text=await response.text();assert.ok(!text.includes('test-only'));assert.ok(!text.includes('account_id'));assert.ok(!text.includes('days'));
  assert.equal((await handle(new Request('http://local/api/site-views',{headers:{Origin:'https://unrelated.example'}}),env)).status,403);
  assert.equal((await handle(new Request('http://local/api/site-views',{method:'POST'}),env)).status,405);
});

test('today starts at Vietnamese midnight, not UTC midnight or a rolling 24 hours',async()=>{
  const env=environment(), filters=[];
  const result=await update(env,Date.parse('2026-11-04T07:30:00Z'),async(url,options)=>{
    filters.push(JSON.parse(options.body).variables.filter);
    return data(10)(url,options);
  });
  assert.equal(filters.at(-1).datetime_geq,'2026-11-03T17:00:00.000Z');
  assert.equal(result.today,10);assert.equal(result.day,'2026-11-04');
  assert.equal(result.day_timezone,'Asia/Ho_Chi_Minh');
});

test('at exact Vietnamese midnight today resets without losing the cumulative total',async()=>{
  const result=await update(environment(),Date.parse('2026-11-04T17:00:00Z'),data(10));
  assert.equal(result.today,0);assert.equal(result.day,'2026-11-05');assert.equal(result.total,20);
});
