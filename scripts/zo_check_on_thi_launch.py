#!/usr/bin/env python3
"""Kiểm tra ứng viên ra mắt cục bộ Ôn thi Toán THPT 2027."""

from __future__ import annotations

import argparse
import copy
import functools
import hashlib
import http.server
import importlib.util
import json
import re
import subprocess
import shutil
import sys
import tempfile
import threading
import xml.etree.ElementTree as ET
from dataclasses import replace
from pathlib import Path
from typing import Any, Callable

import yaml
from bs4 import BeautifulSoup

from zo_pdf_contract import validate_canonical_pdf_provenance


ROOT = Path(__file__).resolve().parents[1]
PROGRAM = ROOT / "content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027"
R1 = ROOT / "content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g01"
DOCS = ROOT / "docs"


def load_builder():
    path = ROOT / "scripts/zo_build_on_thi.py"
    spec = importlib.util.spec_from_file_location("zo_build_on_thi", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Không nạp được trình sinh")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def expect_failure(action: Callable[[], Any]) -> bool:
    try:
        action()
    except (ValueError, OSError, KeyError, TypeError):
        return True
    return False


def yaml_file(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    return value if isinstance(value, dict) else {}


def html_page(path: Path) -> BeautifulSoup:
    return BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")


def hrefs(page: BeautifulSoup) -> list[str]:
    return [str(tag.get("href", "")) for tag in page.select("a[href]")]


def css_selectors(text: str) -> list[str]:
    """Lấy selector ở mọi cấp, bỏ qua phần khai báo và at-rule."""
    selectors: list[str] = []
    cursor = 0
    while cursor < len(text):
        opening = text.find("{", cursor)
        if opening < 0:
            break
        prelude = text[cursor:opening].strip()
        depth = 1
        closing = opening + 1
        while closing < len(text) and depth:
            if text[closing] == "{":
                depth += 1
            elif text[closing] == "}":
                depth -= 1
            closing += 1
        if depth:
            raise ValueError("CSS có khối chưa đóng")
        body = text[opening + 1:closing - 1]
        if prelude.startswith("@media"):
            selectors.extend(css_selectors(body))
        elif not prelude.startswith("@"):
            selectors.append(prelude)
        cursor = closing
    return selectors


def cover_measurements(builder, svg: str) -> list[dict[str, Any]]:
    metrics = builder.FontMetrics(builder.FONT_METRICS_PATH)
    root = ET.fromstring(svg)
    lines = []
    for node in root.findall('.//{http://www.w3.org/2000/svg}text'):
        for line in node:
            size = float(node.attrib['font-size'])
            x = float(line.attrib['x'])
            width = metrics.width(line.text or '', size)
            lines.append({'text':line.text, 'width':width, 'limit':1128-x,
                          'fill':node.attrib['fill'], 'fits':width <= 1128-x})
    return lines


def fixture_checks(builder, data, packages, audit: Path):
    checks, details = {}, {}
    with tempfile.TemporaryDirectory(prefix='fixtures-', dir=audit) as temporary:
        temp = Path(temporary)
        refs = copy.deepcopy(data)
        first = packages[0]
        refs['packages'] = [{'id':first.ref_id}, {'id':'r1_g02'}]
        refs['latest_package'] = first.ref_id
        # Real temporary QMD/profile inputs traverse the normal loader and build.
        for ref in refs['packages']:
            dest = temp/'packages'/ref['id']
            (dest/builder.PROFILE_NAME).parent.mkdir(parents=True)
            metadata = builder.qmd_metadata(first.qmd)
            profile = builder.load_yaml(first.qmd.parent/builder.PROFILE_NAME)
            if ref['id'] != first.ref_id:
                metadata['title'] = 'Giá trị lớn nhất, giá trị nhỏ nhất và tiệm cận'
                profile['package']['id'] = 'R1-G02'
            (dest/'index.qmd').write_text('---\n'+yaml.safe_dump(metadata,allow_unicode=True)+'---\n',encoding='utf-8')
            (dest/builder.PROFILE_NAME).write_text(yaml.safe_dump(profile,allow_unicode=True),encoding='utf-8')
            for name in first.pdfs:
                shutil.copyfile(first.qmd.parent/name, dest/name)
        builder.build(data=refs,package_root=temp/'packages',output_root=temp/'output')
        base = temp/'output'/builder.PROGRAM_ROOT.relative_to(ROOT)
        partial = (base/'_partials/chuong_trinh.qmd').read_text(encoding='utf-8')
        refs_in_partial = re.findall(r'!\[[^]]*\]\(([^)]+)\)',partial)
        assets = [{'href':href,'exists':(base/href).is_file()} for href in refs_in_partial]
        actual = sorted(p.name for p in (base/'assets/bia').glob('*.svg'))
        checks['fixture_second_package_full_build'] = (
            partial.count('data-package-id=') == 2 and all(x['exists'] for x in assets)
            and actual == ['chuong_trinh.svg',f'{first.ref_id}.svg','r1_g02.svg']
        )
        details['two_packages'] = {'latest':refs['latest_package'],'assets':assets,'generated':actual}
        checks['fixture_second_build_unchanged'] = not builder.build(
            check=True,data=refs,package_root=temp/'packages',output_root=temp/'output')
        measured = {p.name:cover_measurements(builder,p.read_text(encoding='utf-8'))
                    for p in (base/'assets/bia').glob('*.svg')}
        details['cover_lines'] = measured
        checks['fixture_all_svg_lines_fit'] = all(line['fits'] for lines in measured.values() for line in lines)

        metrics = builder.FontMetrics(builder.FONT_METRICS_PATH)
        normal = metrics.wrap(first.title,68,1056,3,field='package.title')
        near = ' '.join(['Toán']*5)
        near_limit = metrics.width(near,68)+.001
        wrapped = metrics.wrap(near+' Toán',68,near_limit,2,field='package.title')
        checks['fixture_normal_wrap'] = ' '.join(normal)==first.title and all(metrics.width(s,68)<=1056 for s in normal)
        checks['fixture_near_limit_wrap'] = wrapped==[near,'Toán']
        rejected = {}
        for label,text in [('first_token','W'*27),('wrapped_last','Tên '+'W'*27),('wrapped_middle','Tên '+'W'*27+' Toán')]:
            try:
                metrics.wrap(text,68,1056,3,field='package.title')
                rejected[label] = None
            except builder.BuildError as exc:
                rejected[label] = str(exc)
        checks['fixture_long_tokens_fail'] = all(rejected.values())
        details['wrap'] = {'normal':normal,'near_limit':near_limit,'wrapped':wrapped,'rejected':rejected}

        original = builder.THEME_PATH.read_text(encoding='utf-8')
        colors = builder.theme_colors()
        # Synthetic mutation is confined to the temporary fixture, never the theme.
        mutated = re.sub(r'(?m)^(\$red-10:\s*)[^;]+;',r'\g<1>#123456 !default;',original)
        mutated = re.sub(r'(?m)^(\$gray-300:\s*)[^;]+;',r'\g<1>#654321 !default;',mutated)
        theme = temp/'fixture.scss'
        theme.write_text(mutated,encoding='utf-8')
        changed = builder.theme_colors(theme)
        builder.build(data=refs,package_root=temp/'packages',theme_path=theme,output_root=temp/'mutated')
        changed_base = temp/'mutated'/builder.COVER_ROOT.relative_to(ROOT)
        changes = {p.name:cover_measurements(builder,p.read_text(encoding='utf-8')) for p in changed_base.glob('*.svg')}
        checks['fixture_theme_mutation_reaches_svg'] = changed['primary']!=colors['primary'] and all(
            any(line['fill']==changed['primary'] for line in lines) for lines in changes.values())
        changed_partial=(temp/'mutated'/builder.PARTIAL_ROOT.relative_to(ROOT)/'chuong_trinh.qmd').read_text(encoding='utf-8')
        checks['fixture_theme_mutation_reaches_local_css'] = (
            changed['gray-300']!=colors['gray-300']
            and f'--zo-on-thi-gray-300: {changed["gray-300"]}' in changed_partial)
        details['token_mutation'] = {'token':'red-10','before':colors['primary'],'after':changed['primary'],
                                   'css_property':'--bs-primary','svg_files':list(changes),
                                   'local_token':'gray-300','local_before':colors['gray-300'],
                                   'local_after':changed['gray-300']}
        for label,text in {
            'missing':re.sub(r'(?m)^\$red-10:[^\n]*\n','',original),
            'duplicate':original+'\n$red-10: #123456;\n',
            'unresolved':re.sub(r'(?m)^\$red-10:[^\n]*', '$red-10: $not_registered;',original),
            'expression':re.sub(r'(?m)^\$red-10:[^\n]*', '$red-10: mix($white, $black);',original),
        }.items():
            theme.write_text(text,encoding='utf-8')
            checks[f'fixture_token_{label}_fails'] = expect_failure(lambda:builder.theme_colors(theme))
    details['temporary_fixtures_removed'] = not Path(temporary).exists()
    return checks, details


# Browser-only assertions: DOM presence is not evidence that a heading is visible.
# Keep this runner local; it never uses a personal browser profile.
BROWSER_CHECK = r'''
import fs from 'node:fs';
import path from 'node:path';
import {spawn} from 'node:child_process';
const cfg=JSON.parse(process.argv[1]), sleep=ms=>new Promise(r=>setTimeout(r,ms));
const child=spawn(cfg.chrome,['--headless=new','--remote-debugging-port=0',`--user-data-dir=${cfg.profile}`,'--no-first-run','--no-default-browser-check','--disable-background-networking','--disable-component-update','--disable-sync','about:blank'],{windowsHide:true,stdio:'ignore'});
let ws,seq=0;const pending=new Map(), checks={}, states=[];
const call=(method,params={})=>new Promise((resolve,reject)=>{const id=++seq;pending.set(id,{resolve,reject});ws.send(JSON.stringify({id,method,params}));});
const evaluate=async expression=>{const r=await call('Runtime.evaluate',{expression,returnByValue:true,awaitPromise:true});if(r.exceptionDetails)throw Error(JSON.stringify(r.exceptionDetails));return r.result.value;};
const key=async()=>{await call('Input.dispatchKeyEvent',{type:'keyDown',key:'Tab',code:'Tab',windowsVirtualKeyCode:9});await call('Input.dispatchKeyEvent',{type:'keyUp',key:'Tab',code:'Tab',windowsVirtualKeyCode:9});};
const rgb=hex=>'rgb('+hex.slice(1).match(/../g).map(s=>parseInt(s,16)).join(', ')+')';
const measure=`(() => {
 const visibility=e=>{const r=e.getBoundingClientRect(), ancestors=[];for(let n=e;n;n=n.parentElement){const c=getComputedStyle(n);if(c.display==='none'||['hidden','collapse'].includes(c.visibility)||Number(c.opacity)===0)ancestors.push({tag:n.tagName,classes:n.className,display:c.display,visibility:c.visibility,opacity:c.opacity});}return {text:e.textContent.trim(),visible:ancestors.length===0&&[r.x,r.y,r.width,r.height].every(Number.isFinite)&&r.width>0&&r.height>0,blockedBy:ancestors,box:{x:r.x,y:r.y,width:r.width,height:r.height},color:getComputedStyle(e).color};};
 const root=getComputedStyle(document.documentElement), title=document.querySelector('#title-block-header h1');
 const h1=[...document.querySelectorAll('h1')].map(visibility);
 const images=[...document.querySelectorAll('main img')].map(e=>({src:e.getAttribute('src'),loaded:e.complete&&e.naturalWidth>0}));
 const palette=Object.fromEntries(${JSON.stringify(Object.keys(cfg.tokens))}.map(p=>[p,root.getPropertyValue(p).trim()]));
 const localColors=[...document.querySelectorAll('[data-on-thi-colors]')].map(e=>Object.fromEntries(${JSON.stringify(cfg.localNames)}.map(name=>[name,getComputedStyle(e).getPropertyValue('--zo-on-thi-'+name).trim()])));
 return {title:title?visibility(title):null,h1,images,palette,localColors,headerBottom:document.querySelector('#quarto-header')?.getBoundingClientRect().bottom||0,overflow:document.documentElement.scrollWidth-document.documentElement.clientWidth,links:[...document.querySelectorAll('main a[href]')].map(e=>e.getAttribute('href'))};
})()`;
try {
 child.on('error',error=>{process.stderr.write(String(error));});
 const active=path.join(cfg.profile,'DevToolsActivePort');
 for(let i=0;i<100&&!fs.existsSync(active);i++){if(child.exitCode!==null)throw Error('Chrome exited before CDP startup');await sleep(100);}
 const port=fs.readFileSync(active,'utf8').split('\n')[0];
 const tabs=await(await fetch(`http://127.0.0.1:${port}/json/list`)).json();
 ws=new WebSocket(tabs.find(t=>t.type==='page').webSocketDebuggerUrl);
 ws.addEventListener('message',event=>{const m=JSON.parse(event.data),p=pending.get(m.id);if(p){pending.delete(m.id);m.error?p.reject(Error(JSON.stringify(m.error))):p.resolve(m.result);}});
 await new Promise((resolve,reject)=>{ws.addEventListener('open',resolve,{once:true});ws.addEventListener('error',reject,{once:true});});
 await call('Page.enable');await call('Runtime.enable');await call('Emulation.setFocusEmulationEnabled',{enabled:true});
 for(const width of [1440,430,390]) {
  await call('Emulation.setDeviceMetricsOverride',{width,height:900,deviceScaleFactor:1,mobile:width<500});
  for(const javascript of [true,false]) for(const [name,route] of Object.entries(cfg.routes)) {
   await call('Emulation.setScriptExecutionDisabled',{value:!javascript});
   await call('Page.navigate',{url:cfg.base+route});
   for(let i=0;i<100;i++){await sleep(100);if(await evaluate('document.readyState==="complete"'))break;}
   await evaluate("document.querySelectorAll('img').forEach(e=>e.loading='eager');document.fonts.ready");await sleep(150);
   const state=await evaluate(measure), id=`${name}_${width}_${javascript?'js':'no_js'}`;
   const scoped=['program','gateway'].includes(name);
   checks[id+'_heading']=state.h1.filter(h=>h.visible).length===1&&(!scoped||(state.title?.visible&&state.title.box.y>=state.headerBottom-.5));
   checks[id+'_overflow']=state.overflow<=1;
   checks[id+'_images']=state.images.every(i=>i.loaded);
   checks[id+'_theme_tokens']=Object.entries(cfg.tokens).every(([k,v])=>cfg.localNames.includes(k.replace('--bs-',''))||state.palette[k]?.toLowerCase()===v)
     &&(name==='thpt'||state.localColors.length>0)&&state.localColors.every(c=>cfg.localNames.every(n=>c[n]===cfg.tokens['--bs-'+n]));
   if(scoped) checks[id+'_title_color']=state.title.color===rgb(cfg.tokens['--bs-primary']);
   await evaluate("document.querySelector('link[href*=zo_on_thi]')?.setAttribute('disabled','')");
   const without=await evaluate(measure);
   await evaluate("document.querySelector('link[href*=zo_on_thi]')?.removeAttribute('disabled')");
   checks[id+'_scope_control']=scoped?(name!=='program'||!without.title?.visible):JSON.stringify(state.h1.map(h=>h.visible))===JSON.stringify(without.h1.map(h=>h.visible));
   if(scoped) {
    await evaluate("document.body.setAttribute('tabindex','-1');document.body.focus({preventScroll:true})");
    for(let i=0;i<100;i++){await key();if(await evaluate("!!document.activeElement.closest('.zo-on-thi')"))break;}
    state.focus=await evaluate("(() => {const e=document.activeElement,c=getComputedStyle(e);return {inside:!!e.closest('.zo-on-thi'),visible:e.matches(':focus-visible'),color:c.outlineColor,width:c.outlineWidth,offset:c.outlineOffset,style:c.outlineStyle};})()");
    checks[id+'_focus']=state.focus.inside&&state.focus.visible&&state.focus.color===rgb(cfg.tokens['--bs-gray-700'])&&state.focus.width==='2px'&&state.focus.offset==='2px'&&state.focus.style==='solid';
    await evaluate('document.activeElement.blur();document.body.removeAttribute("tabindex");scrollTo(0,0)');
   }
   if(name==='program') {
    const mutation=cfg.mutation;
    await evaluate(`document.documentElement.style.setProperty('--bs-primary',${JSON.stringify(mutation)})`);
    state.mutatedTitleColor=(await evaluate(measure)).title.color;
    checks[id+'_token_mutation_reaches_css']=state.mutatedTitleColor===rgb(mutation);
    await evaluate("document.documentElement.style.removeProperty('--bs-primary')");
   }
   const shot=await call('Page.captureScreenshot',{format:'png',fromSurface:true});
   fs.writeFileSync(path.join(cfg.audit,id+'.png'),Buffer.from(shot.data,'base64'));
   states.push({id,javascript,width,...state});
  }
 }
 console.log(JSON.stringify({checks,states,input:'CDP; mobile viewports simulated'}));
} finally {
 try{ws?.close()}catch{}
 if(child.exitCode===null){const exit=new Promise(resolve=>child.once('exit',resolve));child.kill();await exit;}
 await sleep(400);
}
'''


def browser_checks(site: Path, audit: Path, builder, mutation: str):
    class QuietHandler(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *args):
            pass
    chrome = shutil.which('chrome') or next((str(p) for p in (
        Path('C:/Program Files/Google/Chrome/Application/chrome.exe'),
        Path('C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'),
    ) if p.is_file()), None)
    if not chrome:
        raise RuntimeError('Cần Chrome/Edge để kiểm tra H1 bằng computed style; không thay bằng kiểm tra DOM')
    colors = builder.theme_colors()
    with http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(QuietHandler,directory=str(site))) as server:
        thread=threading.Thread(target=server.serve_forever,daemon=True)
        thread.start()
        try:
            with tempfile.TemporaryDirectory(prefix='browser-cache-',dir=audit) as profile:
                config={'chrome':chrome,'profile':profile,'audit':str(audit),'base':f'http://127.0.0.1:{server.server_port}',
                        'tokens':{prop:colors[name] for prop,name in builder.CSS_COLOR_TOKENS.items()},
                        'localNames':list(builder.LOCAL_COLOR_TOKENS),
                        'mutation':mutation, 'routes':{
                            'program':'/content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/index.html',
                            'gateway':'/content/thpt/on_thi_toan_thpt/index.html',
                            'home':'/index.html', 'thpt':'/content/thpt/index.html'}}
                result=subprocess.run(['node','--input-type=module','-e',BROWSER_CHECK,json.dumps(config)],
                                      capture_output=True,text=True,encoding='utf-8',timeout=240)
                if result.returncode:
                    raise RuntimeError(f'Browser checker failed: {result.stderr[-3000:]}')
                report=json.loads(result.stdout)
                report['temporary_profile_removed']=True
        finally:
            server.shutdown()
            thread.join()
    (audit/'browser.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    return report


def main_checks(site: Path, run_r1: bool, audit: Path) -> tuple[dict[str, bool], dict[str, Any]]:
    builder = load_builder()
    data = builder.load_yaml(builder.DATA_PATH)
    program, packages, latest = builder.load_model(data)
    checks: dict[str, bool] = {}
    details: dict[str, Any] = {
        "package": latest.code,
        "package_title": latest.title,
        "package_version": latest.version,
        "package_status": latest.display_status,
        "pdfs": list(latest.pdfs),
        "source_sha256": {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                          for p in (builder.DATA_PATH,builder.THEME_PATH,ROOT/'assets/css/zo_on_thi.css',
                                    ROOT/'scripts/zo_build_on_thi.py',Path(__file__))},
    }
    r1_source = R1 / "index.qmd"
    r1_registry = yaml_file(R1 / "_quy_trinh/cau_hinh_san_xuat_qmd.yml").get("extensions", {}).get("pdf_variants", {})
    provenance = {
        name: validate_canonical_pdf_provenance(ROOT, r1_source, variant=name)
        for name in r1_registry
    } if isinstance(r1_registry, dict) else {"registry": ["pdf_variants is not a mapping"]}
    checks["r1_pdf_provenance_current"] = (
        len(provenance) == 8 and all(not errors for errors in provenance.values())
    )
    details["r1_pdf_provenance"] = provenance

    checks["data_valid"] = not expect_failure(lambda: builder.validate_data(data))
    checks["generated_outputs_current"] = not expect_failure(lambda: builder.build(check=True))
    checks["package_sources_exact"] = (
        latest.code == "R1-G01"
        and latest.title == "Kết nối hàm số, bảng biến thiên và đồ thị"
        and latest.version == "1.2"
        and latest.production == "accepted"
        and latest.publication == "pending"
        and len(latest.pdfs) == 8
        and all((latest.qmd.parent / name).is_file() for name in latest.pdfs)
    )

    home_source = (ROOT / "index.qmd").read_text(encoding="utf-8")
    home_partial = builder.HOME_PARTIAL.read_text(encoding="utf-8")
    program_partial = (builder.PARTIAL_ROOT / "chuong_trinh.qmd").read_text(encoding="utf-8")
    edition_partial = (builder.PARTIAL_ROOT / "an_ban.qmd").read_text(encoding="utf-8")
    checks["home_generated_latest_only"] = (
        latest.title not in home_source
        and latest.code not in home_source
        and home_source.count("_on_thi_2027_trang_chu.md") == 1
        and home_partial.count("Khám phá chương trình →") == 1
        and len(re.findall(r"\[[^]]+\]\([^)]+\)", home_partial)) == 1
    )
    checks["edition_gateway_exact"] = (
        edition_partial.count(".zo-on-thi-gateway__edition") == 1
        and program["title"] in edition_partial
        and "R1-G01" not in edition_partial
    )
    checks["program_content_contract"] = all(
        text in program_partial
        for text in (
            "#hoc-lieu-hien-co", "## Dành cho ai?", "## Chương trình giúp em làm gì?",
            "## Học theo cách nào?", "## Lộ trình", "## Tám mạch",
            "## Học liệu hiện có", "## Bắt đầu từ đâu?", "## Trạng thái triển khai",
            "Khảo sát đầu vào D0", "Có thể học", "?r1-view=cach-hoc", "Mở khảo sát →",
        )
    ) and all(f"**R{i}**" in program_partial for i in range(1, 9))
    checks["d0_entry_and_no_future_packages"] = (
        program_partial.count("data-package-id=") == len(packages)
        and program_partial.count('data-package-id="d0"') == 1
        and program_partial.count(
            "[Khảo sát đầu vào D0](/content/thpt/on_thi_toan_thpt/hoc_lieu/d0/index.html)"
        ) == 1
        and program_partial.count(
            "[Mở khảo sát →](/content/thpt/on_thi_toan_thpt/hoc_lieu/d0/index.html)"
        ) == 1
        and "hiện chưa được cung cấp công khai tại trang này" not in program_partial
        and all(code not in program_partial for code in ("R2-G01", "R3-G01"))
    )

    root_config = yaml_file(ROOT / "_quarto.yml")
    profile_text = (ROOT / "_quarto-on-thi-preview.yml").read_text(encoding="utf-8")
    navbar = root_config.get("website", {}).get("navbar", {}).get("left", [])
    pho_thong = next((x for x in navbar if x.get("text") == "Phổ Thông"), {})
    sidebars = root_config.get("website", {}).get("sidebar", [])
    on_thi = next((x for x in sidebars if x.get("id") == "on-thi"), {})
    sidebar_hrefs = [x.get("href") for x in on_thi.get("contents", [])]
    checks["navbar_and_shared_sidebar"] = (
        any(x.get("text") == "Ôn thi Toán THPT" and x.get("href") == "content/thpt/on_thi_toan_thpt/index.qmd" for x in pho_thong.get("menu", []))
        and sidebar_hrefs == [
            "content/thpt/on_thi_toan_thpt/index.qmd",
            "content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/index.qmd",
            "content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g01/index.qmd",
        ]
        and "sidebar:" not in profile_text
    )

    r1_source = (R1 / "index.qmd").read_text(encoding="utf-8")
    r1_profile = yaml_file(R1 / "_quy_trinh/ho_so/index.yml")
    checks["r1_program_backlink_and_pending"] = (
        "[Ôn thi Toán THPT 2027](../../tot_nghiep_thpt/2027/index.qmd)" in r1_source
        and r1_profile.get("workflow", {}).get("publication") == "pending"
        and "published" not in (R1 / "_quy_trinh/ho_so/index.yml").read_text(encoding="utf-8")
    )
    governed_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (
            ROOT / "content/thpt/on_thi_toan_thpt/index.qmd",
            PROGRAM / "index.qmd",
            builder.DATA_PATH,
        )
    )
    checks["no_fake_publication_claim"] = (
        "https://zomath.vn/content/thpt/on_thi_toan_thpt" not in governed_text
        and not re.search(r"ngày (?:công bố|xuất bản)", governed_text, re.I)
        and "đã xuất bản" not in governed_text.lower()
    )

    css = (ROOT / "assets/css/zo_on_thi.css").read_text(encoding="utf-8")
    selectors = css_selectors(re.sub(r"/\*.*?\*/", "", css, flags=re.S))
    checks["css_component_scoped"] = (
        all(".zo-on-thi" in selector for selector in selectors)
        and not any(term in css for term in ("linear-gradient", "box-shadow", "animation:"))
        and not re.search(r'#[0-9a-fA-F]{3,8}\b|rgba?\(',css)
        and all(f'var({prop})' in css for prop in builder.CSS_COLOR_TOKENS)
    )

    cover_checks = []
    colors=builder.theme_colors()
    details['token_bindings']={prop:{'scss':'$'+name,'value':colors[name],
                                   'css_reference':f'var({prop})'}
                              for prop,name in builder.CSS_COLOR_TOKENS.items()}
    details['svg_lines']={}
    for cover in (builder.COVER_ROOT / "chuong_trinh.svg", builder.COVER_ROOT / "r1_g01.svg"):
        text = cover.read_text(encoding="utf-8")
        root = ET.fromstring(text)
        lines=cover_measurements(builder,text)
        details['svg_lines'][cover.name]=lines
        cover_checks.append(
            root.attrib.get("viewBox") == "0 0 1200 900"
            and "data:font/woff2;base64," in text
            and "data:image/svg+xml;base64," in text
            and not re.search(r'(?:href|src)="https?://', text)
            and "Ôn thi Toán THPT" in text
            and "…" not in text
            and "data-safe-area=\"72\"" in text
            and "data-grid-columns=\"6\"" in text
            and all(line['fits'] and line['fill'] in colors.values() for line in lines)
            and root.find('{http://www.w3.org/2000/svg}rect').attrib['fill']==colors['white']
        )
    checks["covers_self_contained"] = all(cover_checks)

    more_checks, details['fixtures'] = fixture_checks(builder,data,packages,audit)
    checks.update(more_checks)
    duplicate = copy.deepcopy(data)
    duplicate["packages"].append(copy.deepcopy(duplicate["packages"][0]))
    missing = copy.deepcopy(data)
    missing["packages"][0]["id"] = "missing_package"
    missing["latest_package"] = "missing_package"
    bad_latest = copy.deepcopy(data)
    bad_latest["latest_package"] = "not_registered"
    long_package = replace(packages[0], title="Tên học liệu " * 80)
    checks["fixture_duplicate_id_fails"] = expect_failure(lambda: builder.validate_data(duplicate))
    checks["fixture_missing_ref_fails"] = expect_failure(lambda: builder.load_model(missing))
    checks["fixture_bad_latest_fails"] = expect_failure(lambda: builder.validate_data(bad_latest))
    checks["fixture_long_title_fails"] = expect_failure(lambda: builder.render_covers(program, [long_package]))

    rendered = {
        "home": site / "index.html",
        "thpt": site / "content/thpt/index.html",
        "gateway": site / "content/thpt/on_thi_toan_thpt/index.html",
        "program": site / "content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/index.html",
        "r1": site / "content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g01/index.html",
    }
    checks["rendered_pages_exist"] = all(path.is_file() for path in rendered.values())
    details['html_sha256']={name:hashlib.sha256(path.read_bytes()).hexdigest()
                           for name,path in rendered.items() if path.is_file()}
    if checks["rendered_pages_exist"]:
        pages = {name: html_page(path) for name, path in rendered.items()}
        feature = pages["home"].select_one("[data-on-thi-home-feature]")
        checks["rendered_home_single_cta"] = feature is not None and len(feature.select("a")) == 1
        checks["rendered_no_js_content"] = all(
            phrase in pages["program"].get_text(" ", strip=True)
            for phrase in ("Dành cho ai?", "Học theo cách nào?", "Bắt đầu từ đâu?", latest.title)
        ) and latest.title in pages["home"].get_text(" ", strip=True)
        checks["rendered_routes"] = (
            any("tot_nghiep_thpt/2027/index.html" in href for href in hrefs(pages["home"]))
            and any("on_thi_toan_thpt/index.html" in href for href in hrefs(pages["thpt"]))
            and any("tot_nghiep_thpt/2027/index.html" in href for href in hrefs(pages["gateway"]))
            and any("r1_g01/index.html?r1-view=cach-hoc" in href for href in hrefs(pages["program"]))
            and any("hoc_lieu/d0/index.html" in href for href in hrefs(pages["program"]))
            and any("tot_nghiep_thpt/2027/index.html" in href for href in hrefs(pages["r1"]))
        )
        checks["rendered_program_heading_shape"] = (
            len(pages["program"].select("main h1")) == 1
            and len(pages["program"].select("main h3")) == len(packages)
            and not pages["program"].select("main details, main table")
        )
        checks["rendered_local_resources"] = all(
            not str(tag.get(attr, "")).startswith(("http://", "https://"))
            for page in pages.values()
            for tag, attr in [(node, "src") for node in page.select("main [src]")]
        )
        checks['rendered_resources_exist'] = all(
            (site/str(node['src']).lstrip('/')).is_file() if str(node['src']).startswith('/')
            else (rendered[name].parent/str(node['src'])).is_file()
            for name,page in pages.items() for node in page.select('main img[src]')
            if not str(node['src']).startswith(('data:','https:','http:'))
        )
    else:
        for name in ("rendered_home_single_cta", "rendered_no_js_content", "rendered_routes", "rendered_program_heading_shape", "rendered_local_resources"):
            checks[name] = False

    if run_r1 and rendered["r1"].is_file():
        result = subprocess.run(
            [sys.executable, str(R1 / "cong_cu/kiem_chung.py"), str(rendered["r1"])],
            cwd=ROOT, text=True, encoding="utf-8", capture_output=True,
        )
        checks["r1_checker_current"] = result.returncode == 0
        details["r1_checker_tail"] = (result.stdout + result.stderr)[-1200:]
    else:
        checks["r1_checker_current"] = not run_r1
    return checks, details


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site", type=Path, default=DOCS)
    parser.add_argument("--skip-r1", action="store_true")
    parser.add_argument("--audit-dir", type=Path, default=ROOT/'_audit/on_thi_launch')
    args = parser.parse_args()
    try:
        audit=args.audit_dir.resolve()
        if not audit.is_relative_to(ROOT/'_audit'):
            raise ValueError('Audit phải nằm trong _audit của repository')
        audit.mkdir(parents=True,exist_ok=True)
        checks, details = main_checks(args.site.resolve(), not args.skip_r1, audit)
        browser=browser_checks(args.site.resolve(),audit,load_builder(),details['fixtures']['token_mutation']['after'])
        checks.update(browser['checks'])
    except Exception as exc:  # checker phải báo gọn mọi lỗi hợp đồng
        print(json.dumps({"passed": False, "error": str(exc)}, ensure_ascii=False, indent=2))
        return 1
    result = {"passed": all(checks.values()), "checks": checks, "details": details}
    (audit/'checker.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
