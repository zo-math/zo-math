"""Single-render page releases, sealed artifact reuse, and pre-publication validation.

The published tree is the baseline. Unselected pages and PDFs keep their exact
published bytes. Full rebuilds remain available in zo_publish --full-render.
"""
from __future__ import annotations
import copy
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import sys
import tempfile
import time
from urllib.parse import unquote, urlsplit
from xml.etree import ElementTree as ET
import zo_publish as p

VERSION = 1
D0_PDF = 'content/thpt/on_thi_toan_thpt/hoc_lieu/d0/index.pdf'
D0_PAGE = 'content/thpt/on_thi_toan_thpt/hoc_lieu/d0/index.html'


class Timings:
    def __init__(self):
        self.started = time.perf_counter()
        self.values = {}

    @contextmanager
    def phase(self, name):
        start = time.perf_counter()
        try:
            yield
        finally:
            self.values[name] = round(time.perf_counter()-start, 6)

    def report(self):
        return {**self.values, 'total_seconds': round(time.perf_counter()-self.started, 6)}


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    p.write_text_lf(path, json.dumps(value, ensure_ascii=False, indent=2)+'\n')


def allowed(name, config):
    return (p.path_allowed(name,config['allowlist']['files'],config['allowlist']['globs'])
            and not p.path_denied(name,config['denylist']['paths'],config['denylist']['globs']))


def tool_sha(path):
    # Python source is equivalent across Git LF and Windows CRLF checkouts.
    return hashlib.sha256(path.read_bytes().replace(b'\r\n',b'\n')).hexdigest()


def selected_sources(root, pages):
    result = []
    if not pages:
        raise p.ConfigError('Page release requires at least one --page.')
    for page in sorted(set(pages)):
        name = p.safe_relative(page, 'page')
        if not name.endswith('.html'):
            raise p.ConfigError('--page must be a site-relative .html path.')
        source = next((root / (name[:-5]+ext) for ext in ('.qmd', '.Rmd', '.rmd')
                       if (root/(name[:-5]+ext)).is_file()), None)
        if source is None:
            raise p.ConfigError('Missing source for '+name)
        if source.is_symlink() or not source.resolve().is_relative_to(root.resolve()):
            raise p.ConfigError('Unsafe page source: '+name)
        result.append(source.relative_to(root).as_posix())
    return result


def preflight(root, pages, config, target=None):
    """Cheap checks before any Quarto process; output validation still runs later."""
    sources = selected_sources(root, pages)
    issues = []
    for page in pages:
        if not allowed(page, config):
            issues.append({'type':'page-not-public', 'path':page})
    for name in sources:
        text = (root/name).read_text(encoding='utf-8')
        for ref in re.findall(r'''(?:src|poster)\s*=\s*["']([^"']+)["']''', text):
            url = urlsplit(ref)
            if url.scheme or url.netloc or not url.path:
                continue
            path = root/url.path.lstrip('/') if url.path.startswith('/') else (root/name).parent/unquote(url.path)
            if not path.resolve().is_relative_to(root.resolve()) or '_audit' in path.resolve().parts:
                issues.append({'type':'unsafe-source-resource','path':name,'value':ref})
            elif not path.is_file():
                issues.append({'type':'missing-source-resource','path':name,'value':ref})
    if target is not None:
        manifest=p.tree_manifest(target, True)
        missing=[]
        p.asset_dependencies(target,manifest,[x for x in pages if x in manifest['files']],missing)
        issues.extend({'type':'missing-published-dependency','path':x} for x in sorted(set(missing)))
    return {'sources':sources,'pages':sorted(set(pages)),'issues':issues}


def input_fingerprints(root,only_ignored=False):
    tracked={};dirty=set()
    if not only_ignored:
        for entry in p.git_text(root,'ls-files','--stage','-z').split('\0'):
            if not entry:continue
            metadata,name=entry.split('\t',1)
            mode,blob,stage=metadata.split()
            if stage!='0':raise p.ConfigError('Unmerged build input: '+name)
            tracked[name]=blob
        dirty=set(p.git_text(root,'diff','--name-only','HEAD','-z').split('\0'))
    names=list(tracked)
    ignored=p.git(root,'ls-files','--others','--ignored','--exclude-standard','-z')
    if ignored.returncode:raise p.ConfigError('Cannot inventory ignored inputs.')
    for name in ignored.stdout.split('\0'):
        if not name or Path(name).parts[0] in p.RENDER_SUPPORT_EXCLUDED_ROOTS:continue
        parts=Path(name).parts
        if any(x in parts for x in ['.Rproj.user','.ipynb_checkpoints','__pycache__']) or name.lower().endswith(('.pyc','.pyo')):continue
        names.append(name)
    inputs={}
    for name in sorted(set(filter(None,names))):
        if Path(name).parts[0] in {'.git','_audit','.quarto','docs','tmp'}:continue
        file=root/name
        if file.is_symlink():raise p.ConfigError('Symlink source dependency: '+name)
        if not file.is_file():inputs[name]=None
        elif name in tracked and name not in dirty:inputs[name]='git-blob:'+tracked[name]
        else:inputs[name]=p.sha256(file)
    return inputs


def fingerprint(root, pages, config, tool_root=None, d0_pdf=False, pdfs=None):
    """Conservative dependency key: all tracked bytes and permitted ignored inputs.

    This intentionally invalidates on unrelated tracked source changes rather
    than guessing dependencies of arbitrary Python/R hooks. Commit metadata
    alone does not invalidate it. No docs/audit/generated cache is an input.
    """
    tool_root=tool_root or Path(__file__).resolve().parents[1]
    inputs=input_fingerprints(root)
    tools={name:tool_sha(tool_root/'scripts'/name)
           for name in ['zo_publish.py','zo_publish_pages.py','zo_quarto.py','zo_python.py']}
    if pdfs:
        tools['zo_publish_pdfs.py']=tool_sha(tool_root/'scripts/zo_publish_pdfs.py')
    version=p.run(['quarto','--version'],root)
    if version.returncode:
        raise p.MissingToolError('Cannot identify Quarto version.')
    data={'version':VERSION,'pages':sorted(set(pages)),'d0_pdf':d0_pdf,'inputs':inputs,'tools':tools,
          'selected_pdfs':pdfs or [],
          'config':config,'python':sys.version,'quarto':version.stdout.strip(),
          'packages':sorted((d.metadata.get('Name',''),d.version) for d in importlib.metadata.distributions()),
          'environment':{k:os.environ.get(k) for k in ['QUARTO_PROFILE','QUARTO_PYTHON','RETICULATE_PYTHON','ZO_MATH_GRAPHICS_ROOT','ZO_OFFICIAL_BUILD']}}
    encoded=json.dumps(data,sort_keys=True,ensure_ascii=False).encode()
    return {'key':hashlib.sha256(encoded).hexdigest(),'inputs':inputs,'tools':tools,
            'quarto':data['quarto'],'python':data['python'],'policy':'conservative-all-tracked-and-approved-ignored'}


def render_pages(root, destination, sources, tool_root=None):
    """One real Quarto invocation per selected source; always use fresh output."""
    tools=tool_root or root
    logs=[]
    (root/'.quarto').mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='page-render-',dir=root/'.quarto') as tmp:
        output=Path(tmp)/'render';output.mkdir()
        for source in sources:
            command=[sys.executable,str(tools/'scripts/zo_python.py'),'-B',str(tools/'scripts/zo_quarto.py'),
                     'render',source,'--to','html','--output-dir',output.relative_to(root).as_posix()]
            result=p.run(command,root,environment=p.render_subprocess_environment())
            logs.append({'command':command,'exit_code':result.returncode,'stdout':result.stdout,'stderr':result.stderr})
            if result.returncode:
                raise RuntimeError('Page render failed: '+result.stderr[-5000:])
        shutil.copytree(output,destination)
    return {'source_count':len(sources),'invocations':logs,'exit_code':0}


def cache_eligible(root,sources):
    """Do not reuse executed/opaque documents without an execution input contract."""
    pending=list(sources);seen=set()
    include=re.compile(r'''\{\{<\s*include\s+(?:"([^"]+)"|'([^']+)'|([^\s>]+))\s*>\}\}''')
    while pending:
        name=pending.pop()
        if name in seen:continue
        seen.add(name);file=root/name
        if not file.is_file() or not file.resolve().is_relative_to(root.resolve()):return False
        text=file.read_text(encoding='utf-8')
        if re.search(r'^\s*`{3,}\s*\{(?![=.#])',text,re.M) or re.search(r'`\{(?:r|python)\}',text):return False
        for match in include.finditer(text):
            reference=next(x for x in match.groups() if x is not None)
            dependency=(file.parent/reference).resolve()
            if not dependency.is_relative_to(root.resolve()):return False
            pending.append(dependency.relative_to(root.resolve()).as_posix())
        # Unknown shortcodes may depend on external/volatile state.
        if '{{<' in include.sub('',text):return False
    return True


def artifact(root, pages, config, destination, cache_root, timings, tool_root=None, d0_pdf=False, pdfs=None):
    check=preflight(root,pages,config)
    if check['issues']:
        raise p.ConfigError(json.dumps(check['issues'],ensure_ascii=False))
    with timings.phase('fingerprint'):
        seal=fingerprint(root,pages,config,tool_root,d0_pdf,pdfs)
    reusable=cache_eligible(root,check['sources'])
    cache_root.mkdir(parents=True,exist_ok=True)
    cached=cache_root/seal['key']
    with timings.phase('artifact'):
        if reusable and cached.exists():
            if p.scan_symlinks(cached):
                raise p.ConfigError('Unsafe artifact cache.')
            receipt=json.loads((cached/'receipt.json').read_text(encoding='utf-8'))
            if receipt['fingerprint']!=seal or p.tree_manifest(cached/'render')!=receipt['manifest']:
                raise p.ConfigError('Artifact cache hash mismatch; refusing reuse.')
            shutil.copytree(cached/'render',destination)
            return {'cache_hit':True,'cache_eligible':True,'fingerprint':seal,'render':{'source_count':0,'exit_code':0}}
        with tempfile.TemporaryDirectory(prefix='artifact-',dir=cache_root) as temporary:
            temp=Path(temporary)
            render=render_pages(root,temp/'raw',check['sources'],tool_root)
            # Hooks must not silently rewrite a fingerprinted source.
            if fingerprint(root,pages,config,tool_root,d0_pdf,pdfs)!=seal:
                raise p.ConfigError('Source inputs changed during page render.')
            # A new page may link a canonical PDF that Quarto did not copy.
            # Supply verified PDFs before resolving the HTML dependencies.
            for record in pdfs or []:
                target=temp/'raw'/record['path']
                target.parent.mkdir(parents=True,exist_ok=True)
                shutil.copyfile(root/record['path'],target)
            raw_manifest=p.tree_manifest(temp/'raw')
            missing=[]
            keep=set(pages)|p.asset_dependencies(temp/'raw',raw_manifest,pages,missing)
            if d0_pdf:
                if pages != [D0_PAGE] or D0_PDF not in raw_manifest['files']:
                    raise p.ConfigError('D0 PDF missing from the scoped HTML render.')
                keep.add(D0_PDF)
            keep.update(record['path'] for record in pdfs or [])
            if missing:raise p.ConfigError('Missing artifact dependencies: '+str(sorted(set(missing))))
            keep.update(x for x in ['search.json','sitemap.xml'] if x in raw_manifest['files'])
            p.copy_manifest(temp/'raw',temp/'render',{'files':{x:raw_manifest['files'][x] for x in keep}})
            p.safe_remove_tree(temp/'raw',cache_root)
            receipt={'fingerprint':seal,'manifest':p.tree_manifest(temp/'render')}
            save(temp/'receipt.json',receipt)
            # A cache entry is immutable: publish once after hashing all files.
            if reusable:shutil.copytree(temp,cached)
            shutil.copytree(temp/'render',destination)
    return {'cache_hit':False,'cache_eligible':reusable,'fingerprint':seal,'render':render}


def page_for_record(record, config):
    targets=p.search_navigation_targets(record)
    if not targets:return None
    raw=targets[0][1]
    if not isinstance(raw,str):return None
    url=urlsplit(raw)
    if url.netloc and url.netloc!=config['custom_domain']['cname']:return None
    path=unquote(url.path).lstrip('/')
    if path.endswith('/'):path+='index.html'
    return path


def merge_indexes(target, rendered, candidate, pages, config):
    """Replace selected search/sitemap entries, preserving other entries verbatim."""
    selected=set(pages)
    if (target/'search.json').is_file():
        old=json.loads((target/'search.json').read_text(encoding='utf-8'))
        if not (rendered/'search.json').is_file():
            raise p.ConfigError('Scoped render omitted search.json; cannot safely update search.')
        new=json.loads((rendered/'search.json').read_text(encoding='utf-8'))
        replacements=[x for x in new if page_for_record(x,config) in selected]
        # Quarto may legitimately exclude a page with search: false.
        merged=[];inserted=False
        for record in old:
            if page_for_record(record,config) in selected:
                if not inserted:merged.extend(replacements);inserted=True
            else:merged.append(record)
        if not inserted:merged.extend(replacements)
        if merged!=old:save(candidate/'search.json',merged)
    if (target/'sitemap.xml').is_file():
        if not (rendered/'sitemap.xml').is_file():
            raise p.ConfigError('Scoped render omitted sitemap.xml.')
        old=ET.parse(target/'sitemap.xml');new=ET.parse(rendered/'sitemap.xml')
        def location(node):
            item=next((x for x in node if x.tag.rsplit('}',1)[-1]=='loc'),None)
            return page_for_record({'href':item.text},config) if item is not None else None
        replacements={location(x):x for x in new.getroot() if location(x) in selected}
        if not selected.issubset(replacements):
            raise p.ConfigError('Scoped render omitted selected sitemap entry.')
        oldroot=old.getroot();changed=False
        for index,node in enumerate(list(oldroot)):
            key=location(node)
            if key in replacements:
                replacement=replacements.pop(key)
                if ET.tostring(node)!=ET.tostring(replacement):
                    oldroot.remove(node);oldroot.insert(index,copy.deepcopy(replacement));changed=True
        for replacement in replacements.values():oldroot.append(copy.deepcopy(replacement));changed=True
        if changed:
            namespace=oldroot.tag[1:].split('}')[0] if oldroot.tag.startswith('{') else ''
            if namespace:ET.register_namespace('',namespace)
            p.write_text_lf(candidate/'sitemap.xml',ET.tostring(oldroot,encoding='unicode')+'\n')


def inherited_pdf_issues(public, manifest, before, d0_pdf=False, pdfs=None):
    names=set(before['files'])|set(manifest['files'])
    selected={record['path'] for record in pdfs or []}
    return [{'type':'page-release-pdf-change','path':name}
            for name in sorted(names) if name.lower().endswith('.pdf')
            and not (d0_pdf and name == D0_PDF)
            and name not in selected
            and before['files'].get(name)!=manifest['files'].get(name)]


def d0_pdf_issues(candidate, source):
    """Permit one replaced PDF only when its canonical bytes and inputs are current."""
    receipt_path=source/'content/thpt/on_thi_toan_thpt/hoc_lieu/d0/_quy_trinh/pdf_build.json'
    try:
        receipt=json.loads(receipt_path.read_text(encoding='utf-8'))
        digest=receipt['output_sha256']
        inputs=receipt['inputs_sha256']
        if not inputs or p.sha256(source/D0_PDF)!=digest or p.sha256(candidate/D0_PDF)!=digest:
            raise ValueError('D0 PDF bytes or receipt differ')
        for name,wanted in inputs.items():
            safe=p.safe_relative(name,'D0 PDF input')
            file=(source/safe).resolve()
            if not file.is_relative_to(source.resolve()) or not file.is_file() or p.sha256(file)!=wanted:
                raise ValueError('D0 PDF input is stale: '+name)
        from pypdf import PdfReader
        if not isinstance(receipt.get('pages'),int) or receipt['pages']<1 or len(PdfReader(candidate/D0_PDF).pages)!=receipt['pages']:
            raise ValueError('D0 PDF page count differs from its build receipt')
    except (OSError,KeyError,ValueError,TypeError) as exc:
        return [{'type':'d0-pdf-provenance','path':D0_PDF,'message':str(exc)}]
    return []


def validate_candidate(candidate, manifest, config, before, d0_pdf=False, source=None, pdfs=None):
    issues=inherited_pdf_issues(candidate,manifest,before,d0_pdf,pdfs)
    if d0_pdf:
        issues.extend(d0_pdf_issues(candidate,source or Path(__file__).resolve().parents[1]))
    if pdfs:
        from zo_publish_pdfs import validate_pdfs
        issues.extend(validate_pdfs(source or Path(__file__).resolve().parents[1],pdfs,config,candidate))
    difference=p.exact_diff(before,manifest)
    changed=set(difference['add']+difference['update'])
    if difference['delete']:
        issues.extend({'type':'page-release-deletion','path':x} for x in difference['delete'])
    result=p.validate_public(candidate,manifest,config,historical_comparison_only=True,content_paths=changed)
    result['issues'].extend(issues)
    result['validated_content_paths']=sorted(changed)
    result['inherited_pdf_count']=sum(x.lower().endswith('.pdf') for x in manifest['files'])
    return result


def candidate(target, rendered, destination, pages, config, d0_pdf=False, source=None, pdfs=None):
    if pdfs:
        from zo_publish_pdfs import selected_pdfs
        expected=selected_pdfs(source,selected_sources(source,pages),evidence=False)
        identity=lambda record:{k:record.get(k) for k in ('source','path','variant','contract')}
        if list(map(identity,pdfs))!=expected:
            raise p.ConfigError('PDF outputs must belong to exactly the selected pages.')
    before=p.tree_manifest(target,True)
    raw=p.tree_manifest(rendered)
    for name in pages:
        if name not in raw['files']:raise p.ConfigError('Missing rendered page: '+name)
    missing=[]
    dependencies=p.asset_dependencies(rendered,raw,pages,missing)
    if missing:raise p.ConfigError('Missing rendered dependencies: '+', '.join(sorted(set(missing))))
    selected=set(pages)|dependencies
    if pdfs:
        selected_pdf_paths={record['path'] for record in pdfs}
        for name in dependencies:
            if name.lower().endswith('.pdf') and name not in selected_pdf_paths:
                if name not in before['files']:
                    raise p.ConfigError('New linked PDF is outside selected sources: '+name)
                selected.discard(name)  # Keep the published PDF, even if a hook copied another version.
    for record in pdfs or []:
        if record['path'] not in raw['files']:
            raise p.ConfigError('Missing selected PDF: '+record['path'])
        selected.add(record['path'])
    if d0_pdf:
        if pages != [D0_PAGE] or D0_PDF not in raw['files']:
            raise p.ConfigError('D0 PDF scope or render output differs.')
        selected.add(D0_PDF)
    for name in selected:
        if not allowed(name,config):raise p.ConfigError('Dependency not allowlisted: '+name)
    destination.mkdir(parents=True)
    p.copy_manifest(target,destination,before)
    p.copy_manifest(rendered,destination,{'files':{x:raw['files'][x] for x in selected}})
    merge_indexes(target,rendered,destination,pages,config)
    # Index normalization only needs the complete file-name set. Inherited
    # bytes are verified once below, rather than rehashed after every step.
    manifest={'files':{**before['files'],**{x:raw['files'][x] for x in selected}}}
    p.normalize_changed_html_whitespace(target,destination,pages)
    indexes=p.normalize_public_indexes(destination,manifest,config)
    manifest=p.tree_manifest(destination)
    diff=p.exact_diff(before,manifest)
    issues=list(indexes['issues'])
    allowed_outputs=selected|{'search.json','sitemap.xml'}
    issues.extend({'type':'output-scope','path':x} for x in diff['add']+diff['update']+diff['delete'] if x not in allowed_outputs)
    issues.extend(p.changed_trailing_whitespace(target,destination,manifest))
    policy=p.build_manifest(destination,config)
    issues.extend(policy['issues'])
    if set(policy['files'])!=set(manifest['files']):issues.append({'type':'candidate-manifest-mismatch'})
    # Asset replacement can affect unselected pages even if their HTML stays
    # unchanged. Block it instead of silently widening the release.
    selected_pdf_paths={record['path'] for record in pdfs or []}
    changed_assets=set(diff['update'])-set(pages)-{'search.json','sitemap.xml'}-selected_pdf_paths
    if changed_assets:
        for name in before['files']:
            if name.endswith('.html') and name not in pages:
                shared=p.asset_dependencies(target,before,[name])&changed_assets
                if shared:issues.append({'type':'shared-asset-needs-pages','path':name,'assets':sorted(shared)})
    validation=validate_candidate(destination,manifest,config,before,d0_pdf,source,pdfs)
    issues.extend(validation['issues'])
    return {'manifest':manifest,'manifest_sha256':p.manifest_digest(manifest),'diff':diff,
            'target_before_manifest':before,'validation':validation,'issues':issues,
            'referenced_asset_dependencies':sorted(dependencies),'index_normalization':indexes}


def validate_receipt(root,target,config,payload,check_source=True,source_root=None):
    """Read-only final gate, shared by validate and publish; no remote mutation."""
    paths=payload['prepare_paths'];public=root/paths['public_dir'];backup=root/paths['backup_dir']
    if p.scan_symlinks(target,True) or p.scan_symlinks(public) or p.scan_symlinks(backup):
        raise p.ConfigError('Symlink in prepared tree.')
    if p.tree_manifest(public)!=payload['manifest'] or p.tree_manifest(target,True)!=payload['manifest']:
        raise p.ConfigError('Prepared artifact or public worktree drift.')
    if p.tree_manifest(backup)!=payload['target_before_manifest']:
        raise p.ConfigError('Prepared backup drift.')
    seal=payload['page_release']['fingerprint']
    if payload['page_release']['version']!=VERSION:raise p.ConfigError('Unsupported page receipt version.')
    tool_root=Path(__file__).resolve().parents[1]
    for name,digest in seal['tools'].items():
        if payload.get('committed_source') and name in {'zo_python.py','zo_quarto.py'}:
            continue  # Render launchers belong to the pinned committed tree.
        if tool_sha(tool_root/'scripts'/name)!=digest:raise p.ConfigError('Publication tool changed since prepare: '+name)
    if check_source:
        # Committed source is checked by its immutable Git tree in publish_site.
        # The dependency seal also includes permitted ignored inputs, which must
        # not silently change between prepare and publish.
        if payload.get('committed_source'):
            if p.git_text(root,'rev-parse','HEAD')!=payload['source']['commit']:
                raise p.ConfigError('Committed source changed after prepare.')
            tracked_names=set(p.git_text(root,'ls-files','-z').split('\0'))
            expected={k:v for k,v in seal['inputs'].items() if k not in tracked_names}
            actual=input_fingerprints(root,only_ignored=True)
        else:
            expected=seal['inputs'];actual=input_fingerprints(root)
        if actual!=expected:raise p.ConfigError('Source dependency set or bytes changed after prepare.')
    pdfs=payload['page_release'].get('pdfs',[])
    if pdfs:
        from zo_publish_pdfs import selected_pdfs
        wanted=selected_pdfs(source_root or root,selected_sources(source_root or root,payload['page_release']['pages']),evidence=False)
        identity=lambda record:{k:record[k] for k in ('source','path','variant','contract')}
        if list(map(identity,pdfs))!=wanted:
            raise p.ConfigError('Selected PDFs no longer match selected pages.')
    result=validate_candidate(target,payload['manifest'],config,payload['target_before_manifest'],
                              payload['page_release'].get('d0_pdf',False),source_root or root,pdfs)
    if result['issues']:raise p.ConfigError(json.dumps(result['issues'],ensure_ascii=False))
    if p.changed_trailing_whitespace(backup,target,payload['manifest']):
        raise p.ConfigError('Prepared whitespace check failed.')
    policy=p.build_manifest(target,config,True)
    if policy['issues'] or set(policy['files'])!=set(payload['manifest']['files']):
        raise p.ConfigError('Prepared policy boundary mismatch.')
    for name in config['required_files']:
        if name not in payload['manifest']['files']:raise p.ConfigError('Missing required file: '+name)
    return result


def validate_only(root,config_path,config):
    start=time.perf_counter()
    _,payload=p.load_prepare_report(root,config_path,config)
    target=p.find_publish_worktree(root,config['target_branch'])
    source=p.git_state(root,config['source_branch'],f"origin/{config['source_branch']}")
    issues=p.source_mode_issues(source,bool(payload.get('committed_source')))
    if issues or source['commit']!=payload['source']['commit']:
        raise p.ConfigError('Source state changed after prepare: '+str(issues))
    if p.git_text(target,'rev-parse','HEAD',safe=target)!=payload['target']['commit']:
        raise p.ConfigError('Public HEAD changed after prepare.')
    if p.git_text(target,'diff','--cached','--name-only',safe=target):
        raise p.ConfigError('Public index is not empty.')
    if payload.get('committed_source'):
        with p.detached_source_tree(root,root/'.quarto/_zpv',payload['source']['commit'],root/'.quarto') as snapshot:
            p.validate_committed_prepared_tree(root,target,config,payload,snapshot)
    else:
        p.validate_prepared_tree(root,target,config,payload)
    print(json.dumps({'mode':'validate','passed':True,'rendered_pages':0,
                      'pushed':False,'mutated':False,'seconds':time.perf_counter()-start}))
    return 0


def changed_global_inputs(root, baseline):
    changed=p.git_text(root,'diff','--name-only',baseline,'HEAD').splitlines()
    return [name for name in changed if (
        (PurePosixPath(name).name.startswith('_quarto') and name.endswith(('.yml','.yaml')))
        or name.startswith(('_extensions/','filters/','assets/html/'))
        or name.endswith('.scss')
    )]


def require_page_scope(root,target,allow_global_inputs=False):
    baseline=p.published_source_commit(root,target)
    global_paths=changed_global_inputs(root,baseline)
    if global_paths and not allow_global_inputs:
        raise p.ConfigError('Global build inputs changed; use prepare --full-render: '+', '.join(global_paths))
    return baseline


def prepare(root,target,config_path,config,args,source_state,target_state):
    clock=Timings()
    stage=root/config['prepare']['staging_dir']
    if stage.exists():
        raise p.ConfigError('Existing prepare artifact: validate/publish or explicitly discard it first; receipt preserved.')
    issues=[{'type':'source-git','message':x} for x in p.source_mode_issues(source_state,args.committed_source)]
    issues.extend({'type':'target-git','message':x} for x in target_state['issues'])
    issues.extend({'type':'target-symlink','path':x} for x in p.scan_symlinks(target,True))
    payload={'schema_version':p.REPORT_SCHEMA_VERSION,'mode':'prepare','config_version':config['version'],
             'config_sha256':p.sha256(config_path),'config':config_path.relative_to(root).as_posix(),
             'timestamp_utc':datetime.now(timezone.utc).isoformat(),'repo_root':str(root),'publish_worktree':str(target),
             'source':source_state,'target':target_state,'manifest':{},'diff':{},'validation':{},'issues':issues}
    if issues:return finish(root,args,config,payload,clock)
    with clock.phase('scope_preflight'):
        allow_global_inputs=getattr(args,'allow_global_inputs_for_pages',False)
        payload['published_source_commit']=require_page_scope(
            root,target,allow_global_inputs,
        )
        payload['page_scope_global_inputs']=(changed_global_inputs(
            root,payload['published_source_commit'],
        ) if allow_global_inputs else [])
    with p.ExitStack() as stack:
        pdfs=[]
        if getattr(args,'with_pdfs',False):
            from zo_publish_pdfs import selected_pdfs
            pdfs=selected_pdfs(root,selected_sources(root,args.page))
        with clock.phase('source_setup'):
            source=root
            if args.committed_source:
                engine=['publish_public.yml','scripts/zo_publish.py','scripts/zo_publish_pages.py']
                if pdfs:engine.append('scripts/zo_publish_pdfs.py')
                for name in engine:
                    if p.git(root,'ls-files','--error-unmatch','--',name).returncode:
                        raise p.ConfigError('Publication engine/config must be tracked and committed: '+name)
                if p.git(root,'diff','--quiet','HEAD','--',*engine).returncode:
                    raise p.ConfigError('Commit publication engine/config before --committed-source prepare.')
                source=stack.enter_context(p.detached_source_tree(root,root/'.quarto/_zpp',source_state['commit'],root/'.quarto'))
                p.copy_ignored_render_support(root,source)
                payload['committed_source']=True
                payload['excluded_working_changes']=source_state['status']
        with clock.phase('preflight'):
            result=preflight(source,args.page,config,target)
            if pdfs:
                from zo_publish_pdfs import validate_pdfs
                result['issues'].extend(validate_pdfs(source,pdfs,config))
            if result['issues']:payload['issues'].extend(result['issues']);return finish(root,args,config,payload,clock)
        stage.mkdir(parents=True)
        with clock.phase('backup'):
            before=p.tree_manifest(target,True);p.copy_manifest(target,stage/'backup',before)
        retention={'keep':False}
        def cleanup_failed_stage():
            if not retention['keep'] and stage.exists() and p.tree_manifest(target,True)==before:
                p.safe_remove_tree(stage,root/'_audit')
        stack.callback(cleanup_failed_stage)
        d0_pdf=getattr(args,'d0_pdf',False)
        made=artifact(source,args.page,config,stage/'render',root/'.quarto/zo_publish_cache',clock,source,d0_pdf,pdfs)
        with clock.phase('candidate_validation'):
            result=candidate(target,stage/'render',stage/'public',args.page,config,d0_pdf,source,pdfs)
        payload.update(result)
        payload['page_release']={'version':VERSION,'pages':sorted(set(args.page)),'d0_pdf':d0_pdf,'pdfs':pdfs,**made}
        payload['prepare_paths']={key:f'{config["prepare"]["staging_dir"]}/{folder}' for key,folder in [('render_dir','render'),('public_dir','public'),('backup_dir','backup')]}
        payload['prepare_paths'].update(staging_dir=config['prepare']['staging_dir'],report_file=config['prepare']['report_file'])
        if not result['issues']:
            with clock.phase('sync'):
                if p.tree_manifest(target,True)!=before:raise p.ConfigError('Public worktree changed during prepare.')
                p.sync_exact(stage/'public',target,result['manifest'],result['diff'])
                if p.tree_manifest(target,True)!=result['manifest']:
                    p.restore_from_backup(target,stage/'backup',before)
                    raise p.RestoreError('Prepared public sync mismatch; restored backup.')
                if p.git_text(target,'diff','--cached','--name-only',safe=target):raise p.ConfigError('Public Git index changed.')
                retention['keep']=True
    return finish(root,args,config,payload,clock)


def finish(root,args,config,payload,clock):
    payload['timings']=clock.report();payload['exit_code']=1 if payload['issues'] else 0
    save(p.report_target(root,args.report or config['prepare']['report_file']),payload)
    p.print_summary(payload,payload['exit_code'])
    print('TIMINGS:',json.dumps(payload['timings']))
    return payload['exit_code']
