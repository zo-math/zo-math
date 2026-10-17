"""Canonical icon-only contents trigger; independent of downloads and package adapters."""
from pathlib import Path
import argparse,copy,json,re
from bs4 import BeautifulSoup

ROOT=Path(__file__).resolve().parents[1]
KIT=ROOT/'_design/web_2027_mau_dung_chung'

def checks(doc):
    nodes=doc.select('button.mobile-trigger')
    values={'one contents trigger':len(nodes)==1}
    if len(nodes)!=1:return values
    trigger=nodes[0];icon=trigger.select('svg');state=trigger.select_one('.mobile-view')
    visible=[]
    for text in trigger.find_all(string=True):
        if not text.strip():continue
        if any(n.has_attr('hidden') or n.get('aria-hidden')=='true' for n in [text.parent,*text.parents] if getattr(n,'attrs',None) is not None):continue
        visible.append(str(text).strip())
    values.update({
        'icon contract selected':'mobile-trigger--icon' in trigger.get('class',[]),
        'accessible name':bool(trigger.get('aria-label','').strip()),
        'native button':trigger.get('type')=='button',
        'dialog target':bool(trigger.get('aria-controls') and doc.find('dialog',id=trigger['aria-controls'])),
        'dialog semantics':trigger.get('aria-haspopup')=='dialog' and trigger.get('aria-expanded') in ['true','false'],
        'one decorative icon':len(icon)==1 and icon[0].get('aria-hidden')=='true' and icon[0].get('focusable')=='false',
        'list icon shape':len(icon)==1 and len(icon[0].select('path'))==1 and icon[0].path.get('d')=='M5 6h14M5 12h14M5 18h14',
        'no visible caption':not visible,
        'legacy label hook hidden':state is None or state.has_attr('hidden'),
    })
    return values

def css_checks(css):
    matches=re.findall(r'\.prototype-js \.mobile-trigger\{([^}]+)\}',css)
    declarations=dict(re.findall(r'([\w-]+)\s*:\s*([^;]+)',matches[0])) if len(matches)==1 else {}
    return {
        'single shared trigger rule':len(matches)==1,
        'shared 52px trigger':all(declarations.get(k)=='52px' for k in ['width','height','min-height']),
        'shared circle':declarations.get('border-radius')=='50%' and declarations.get('padding')=='0',
        'fixed viewport anchor':declarations.get('position')=='fixed' and declarations.get('bottom')=='16px',
        'legacy caption hidden':bool(re.search(r'\.mobile-trigger \.mobile-view\s*\{\s*display:none\s*\}',css)),
        'decorative icon size':bool(re.search(r'\.mobile-trigger svg\s*\{\s*display:block;width:20px;height:20px\s*\}',css)),
    }

def require(doc,page=None):
    values=checks(doc)
    css=(KIT/'web-shell.css').read_text(encoding='utf-8')
    values.update(css_checks(css))
    if page is not None:
        from urllib.parse import urlsplit,unquote
        links=[n for n in doc.select('link[href]') if Path(urlsplit(n['href']).path).name=='web-shell.css']
        values['shared runtime stylesheet']=len(links)==1
        if len(links)==1:
            runtime=(Path(page).parent/unquote(urlsplit(links[0]['href']).path)).resolve()
            values['runtime CSS matches source']=runtime.is_file() and runtime.read_bytes()==(KIT/'web-shell.css').read_bytes()
    bad=[k for k,v in values.items() if not v]
    if bad:raise ValueError('Shared contents trigger: '+'; '.join(bad))
    return values

BROWSER=r"""(()=>{const n=document.querySelector('button.mobile-trigger'),s=getComputedStyle(n),r=n.getBoundingClientRect(),icon=n.querySelector('svg'),svg=icon?.getBoundingClientRect(),label=n.querySelector('.mobile-view');return {visible:s.display!=='none'&&!!r.width,width:r.width,height:r.height,icon:!!svg&&Math.abs(svg.width-20)<.1&&Math.abs(svg.height-20)<.1,captionHidden:!label||getComputedStyle(label).display==='none',visibleText:n.innerText.trim(),name:n.getAttribute('aria-label'),expanded:n.getAttribute('aria-expanded'),fixed:s.position==='fixed',bottom:innerHeight-r.bottom}})()"""

def self_test():
    doc=BeautifulSoup((KIT/'templates/page.html.tpl').read_text(encoding='utf-8'),'html.parser')
    values={'canonical template valid':all(checks(doc).values()),
            'canonical CSS valid':all(css_checks((KIT/'web-shell.css').read_text(encoding='utf-8')).values())}
    def negative(name,change):
        candidate=copy.deepcopy(doc);change(candidate)
        values[name]=not all(checks(candidate).values())
    negative('reject missing component mode',lambda d:d.select_one('.mobile-trigger').__setitem__('class',['mobile-trigger']))
    negative('reject missing accessible name',lambda d:d.select_one('.mobile-trigger').attrs.pop('aria-label'))
    negative('reject missing icon',lambda d:d.select_one('.mobile-trigger svg').decompose())
    negative('reject different icon',lambda d:d.select_one('.mobile-trigger svg path').__setitem__('d','M1 1h2'))
    negative('reject visible view caption',lambda d:d.select_one('.mobile-trigger').append('Bài học · Mục lục'))
    negative('reject unhidden state hook',lambda d:d.select_one('.mobile-view').attrs.pop('hidden'))
    negative('reject wrong dialog target',lambda d:d.select_one('.mobile-trigger').__setitem__('aria-controls','missing'))
    css=(KIT/'web-shell.css').read_text(encoding='utf-8')
    values['reject capsule width']=not all(css_checks(css.replace('width:52px;height:52px','width:220px;height:52px')).values())
    return values

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--self-test',action='store_true');ap.add_argument('--html',type=Path);ap.add_argument('--report',type=Path);args=ap.parse_args()
    values=self_test() if args.self_test else {}
    if args.html:values.update(require(BeautifulSoup(args.html.read_text(encoding='utf-8'),'html.parser'),args.html))
    result={'checks':values,'passed':sum(values.values()),'total':len(values),'failures':[k for k,v in values.items() if not v]}
    if args.report:args.report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k!='checks'},ensure_ascii=False))
    return int(bool(result['failures']))
if __name__=='__main__':raise SystemExit(main())
