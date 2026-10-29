"""Project approved contextual bitmaps only inside the isolated PDF build."""
from pathlib import Path
import re,hashlib
from bs4 import BeautifulSoup
from PIL import Image

def prepare(root,mirror,source,shell):
    specs=shell.get('raster_illustrations',{})
    if not specs:return
    text=source.read_text('utf-8');seen=set()
    def project(match):
        fig=BeautifulSoup(match.group(),'html.parser').figure
        ident=fig.get('id')
        if ident not in specs:
            img=fig.img
            assert img and fig.figcaption and img.get('alt') and Path(img['src']).suffix.lower()=='.svg', 'Unconfigured raster illustration'
            caption=fig.figcaption.get_text(' ',strip=True)
            import subprocess, shutil
            original=(source.parent/img['src']).resolve()
            assert original.is_relative_to((source.parent/'hinh').resolve())
            target=mirror/'assets/tex/course-runtime'/(ident+'.pdf')
            converter=shutil.which('inkscape') or shutil.which('inkscape.com')
            assert converter, 'Inkscape is required for vector PDF illustrations'
            subprocess.run([converter,str(original),'--export-type=pdf','--export-filename='+str(target)],check=True,capture_output=True)
            # Match the existing cover/scene conversion: LuaTeX supplies its own Group.
            from pypdf import PdfReader, PdfWriter
            from pypdf.generic import NameObject
            import io
            reader=PdfReader(target); assert len(reader.pages)==1
            page=reader.pages[0]; page.pop(NameObject('/Group'),None)
            writer=PdfWriter(); writer.add_page(page)
            stream=io.BytesIO(); writer.write(stream); target.write_bytes(stream.getvalue())
            rel=Path(__import__('os').path.relpath(target,mirror/source.parent.relative_to(root))).as_posix()
            return '::: {#'+ident+' .r1-figure}\n\n!['+img['alt']+']('+rel+'){width="150mm"}\n\n::: {.r1-figcaption}\n'+caption+'\n:::\n\n:::'
        img=fig.img;assert img and fig.figcaption and img.get('alt')
        original=(source.parent/img['src']).resolve()
        assert original.is_relative_to((source.parent/'hinh').resolve())
        target=mirror/'assets/tex/course-runtime'/(ident+'.png')
        with Image.open(original) as image:
            image.convert('RGB').save(target)
        seen.add(ident)
        rel=Path(__import__('os').path.relpath(target,mirror/source.parent.relative_to(root))).as_posix()
        caption=fig.figcaption.get_text(' ',strip=True)
        return '::: {#'+ident+' .r1-figure}\n\n!['+img['alt']+']('+rel+'){width="'+str(specs[ident])+'mm"}\n\n::: {.r1-figcaption}\n'+caption+'\n:::\n\n:::'
    projected=re.sub(r'<figure[^>]*data-zo-role="context-illustration".*?</figure>',project,text,flags=re.S)
    assert seen==set(specs),'Missing configured raster illustrations'
    projected=projected.replace('assets/lua/zo_course_learning.lua','assets/lua/zo_course_package_pdf.lua')
    (mirror/source.relative_to(root)).write_text(projected,encoding='utf-8')


def check(pdf,source,root,variant="full"):
    """Verify actual embedded pixels, scale, placement and same-page captions."""
    from pypdf import PdfReader
    from zo_qmd_config import discover_project_config
    cfg=discover_project_config(root,source.relative_to(root))
    specs=cfg.raw.get('extensions',{}).get('course_pdf_shell',{}).get('raster_illustrations',{})
    if not specs:return {}
    from zo_course_pdf_layout import selected_source
    selected=selected_source(source.read_text("utf-8"),variant)
    reader=PdfReader(pdf);checks={}
    for raw in re.findall(r'<figure[^>]*data-zo-role="context-illustration".*?</figure>',selected,re.S):
        fig=BeautifulSoup(raw,'html.parser').figure;ident=fig['id']
        if ident not in specs:continue
        with Image.open(source.parent/fig.img['src']) as im:
            expected=hashlib.sha256(im.convert('RGB').tobytes()).hexdigest();size=im.size
        found=[]
        for page in reader.pages:
            matches=set()
            for key in page.images.keys():
                image=page.images[key].image
                if image.size==size and hashlib.sha256(image.convert('RGB').tobytes()).hexdigest()==expected:
                    if isinstance(key,str):matches.add(key)
            if not matches:continue
            def before(op,args,cm,tm):
                if op==b'Do' and str(args[0]) in matches:found.append((page,list(cm)))
            page.extract_text(visitor_operand_before=before)
        checks[ident+'/original pixels embedded once']=len(found)==1
        if len(found)==1:
            page,cm=found[0];w,h=abs(cm[0]),abs(cm[3]);pw,ph=float(page.mediabox.width),float(page.mediabox.height)
            checks[ident+'/size centered inside page']=abs(w-specs[ident]*72/25.4)<1 and abs(w/h-size[0]/size[1])<.002 and abs(cm[4]+w/2-pw/2)<2 and cm[4]>=0 and cm[5]>=0 and cm[4]+w<=pw+1 and cm[5]+h<=ph+1
            caption=' '.join(fig.figcaption.get_text(' ',strip=True).split())
            checks[ident+'/caption on same page']=caption in ' '.join(page.extract_text().split())
    return checks
