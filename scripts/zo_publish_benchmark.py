"""Opt-in, local-only full/page/cache benchmark on an identical temporary edit."""
from __future__ import annotations
import argparse
from contextlib import ExitStack
import json
from pathlib import Path
import tempfile
import time
import zo_publish as p
import zo_publish_pages as pages


def benchmark(root,target,config,page,old,new,reference):
    source=p.git_text(root,'rev-parse',reference+'^{commit}')
    qmd=pages.selected_sources(root,[page])[0]
    protected_public=p.tree_manifest(target,True)
    report={'source_commit':source,'page':page,'scenario':{'old':old,'new':new},'passed':False}
    (root/'.quarto').mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='publish-benchmark-',dir=root/'.quarto') as temporary:
        work=Path(temporary)
        with ExitStack() as stack:
            def snapshot(name,edit):
                tree=stack.enter_context(p.detached_source_tree(root,root/'.quarto'/name,source,root/'.quarto'))
                p.copy_ignored_render_support(root,tree)
                if edit:
                    file=tree/qmd;text=file.read_text(encoding='utf-8')
                    if old not in text:raise p.ConfigError('Benchmark replacement is absent from committed page.')
                    file.write_text(text.replace(old,new),encoding='utf-8')
                return tree
            before_start=time.perf_counter();timing={}
            t=time.perf_counter();base=snapshot('_zmb',False);head=snapshot('_zmh',True)
            timing['source_setup']=time.perf_counter()-t
            for key,tree in [('baseline',base),('head',head)]:
                t=time.perf_counter();result=p.render_to_staging(tree,work/key,tool_root=root)
                if result['exit_code']:raise RuntimeError(result['stderr'][-5000:])
                timing[key+'_render']=time.perf_counter()-t
                report[key+'_source_count']=result['source_count']
            t=time.perf_counter()
            baseline=p.build_public_candidate(work/'baseline',work/'baseline-public',target,config,historical_comparison_only=True)
            rendered=p.build_public_candidate(work/'head',work/'head-public',target,config,source_root=head)
            for item in [baseline,rendered]:
                if item['issues']:raise p.ConfigError(str(item['issues']))
            allowed={x for x in rendered['public_manifest']['files'] if not x.endswith('.html')}|{page}
            full=p.build_scoped_candidate(work/'baseline-public',work/'head-public',work/'full-public',target,config,allowed_outputs=allowed,source_root=head)
            if full['issues']:raise p.ConfigError(str(full['issues']))
            timing['candidate_validation']=time.perf_counter()-t;timing['total_seconds']=time.perf_counter()-before_start
            report['before']={'timings':timing,'rendered_pages':report['baseline_source_count']+report['head_source_count']}
            results=[];fingerprint=None;fast_source=None
            for mode,name in [('cold','_zmc'),('warm','_zmw')]:
                clock=pages.Timings()
                with clock.phase('source_setup'):tree=snapshot(name,True)
                with clock.phase('preflight'):
                    early=pages.preflight(tree,[page],config,target)
                    if early['issues']:raise p.ConfigError(str(early['issues']))
                built=pages.artifact(tree,[page],config,work/(mode+'-render'),work/'cache',clock,root)
                with clock.phase('candidate_validation'):
                    candidate=pages.candidate(target,work/(mode+'-render'),work/(mode+'-public'),[page],config)
                    if candidate['issues']:raise p.ConfigError(str(candidate['issues']))
                report[mode]={'timings':clock.report(),'cache_hit':built['cache_hit'],'cache_eligible':built['cache_eligible'],'rendered_pages':built['render']['source_count']}
                results.append(candidate);fingerprint=built['fingerprint'];fast_source=tree
            if not report['warm']['cache_hit']:
                report['cache_note']='This source has execution/opaque inputs; reuse correctly disabled.'
            if p.sha256(work/'full-public'/page)!=p.sha256(work/'cold-public'/page):
                raise p.ConfigError('Selected HTML differs from full build.')
            if results[0]['manifest']!=results[1]['manifest']:
                raise p.ConfigError('Repeated page output differs.')
            expected=json.loads((work/'full-public/search.json').read_text(encoding='utf-8'))
            actual=json.loads((work/'cold-public/search.json').read_text(encoding='utf-8'))
            if [x for x in expected if pages.page_for_record(x,config)==page]!=[x for x in actual if pages.page_for_record(x,config)==page]:
                raise p.ConfigError('Selected search records differ.')
            unchanged=[name for name in protected_public['files'] if name.endswith('.pdf') or name.endswith('.html') and name!=page]
            if any(protected_public['files'][name]!=results[0]['manifest']['files'][name] for name in unchanged):
                raise p.ConfigError('Unselected HTML or PDF changed.')
            p.copy_manifest(target,work/'backup',protected_public)
            payload={'manifest':results[1]['manifest'],'target_before_manifest':protected_public,
                     'page_release':{'version':pages.VERSION,'fingerprint':fingerprint},
                     'prepare_paths':{'public_dir':str(work/'warm-public'),'backup_dir':str(work/'backup')}}
            t=time.perf_counter();pages.validate_receipt(fast_source,work/'warm-public',config,payload)
            report['validate_only_seconds']=time.perf_counter()-t
            report['checks']={'selected_html_byte_identical':True,'selected_search_identical':True,
                              'cache_output_byte_identical':True,'unchanged_other_html_and_pdfs':len(unchanged)}
            report['speedup_cold']=timing['total_seconds']/report['cold']['timings']['total_seconds']
            report['speedup_warm']=timing['total_seconds']/report['warm']['timings']['total_seconds']
            report['engine_sha256']=fingerprint['tools'];report['passed']=True
    if p.tree_manifest(target,True)!=protected_public:raise p.ConfigError('Public tree changed during benchmark.')
    return report


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--page',required=True)
    parser.add_argument('--old-text',required=True);parser.add_argument('--new-text',required=True)
    parser.add_argument('--source-ref',default='HEAD');parser.add_argument('--report',required=True)
    args=parser.parse_args(argv)
    if not args.old_text or args.old_text==args.new_text:parser.error('Provide a nonempty, real text change.')
    root=p.repo_root();_,config=p.load_config(root,'publish_public.yml')
    output=p.report_target(root,args.report);target=p.find_publish_worktree(root,config['target_branch'])
    try:report=benchmark(root,target,config,args.page,args.old_text,args.new_text,args.source_ref)
    except (p.ConfigError,RuntimeError) as exc:
        pages.save(output,{'passed':False,'error':str(exc)})
        print('ERROR:',exc);return 1
    pages.save(output,report)
    print(json.dumps(report,ensure_ascii=False,indent=2));return 0


if __name__=='__main__':raise SystemExit(main())
