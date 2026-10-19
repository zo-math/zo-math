"""Shared R1 print contract. Canonical source in; measurable candidate checks out."""
import collections, hashlib, json, math, re, subprocess
import xml.etree.ElementTree as ET
from pathlib import Path
from pypdf import PdfReader
from zo_course_table_roles import contract, function_profile, table_rows
from zo_graphics import lesson_layout,load_graph

PROFILE=Path('assets/tex/zo-course-print-profile.json')
INPUTS=(Path('assets/lua/zo_course_package_pdf.lua'),Path('assets/lua/zo_course_print.lua'),PROFILE,Path('assets/tex/zo-course-print-layout.tex'),Path('scripts/zo_course_pdf_layout.py'),
        Path('scripts/zo_pdf_course_check.py'),Path('scripts/zo_course_table_roles.py'),Path('scripts/zo_graphics.py'),Path('quy_trinh_xay_dung/cong_cu_do_thi_ham_so_zo_math/axis_ticks.py'))

def pdf_id(value):
    return ''.join(chr(c) if chr(c).isascii() and (chr(c).isalnum() or chr(c) in '-_.:') else '_%02X'%c for c in value.encode('utf-8'))

def enabled(config):
    return config.raw.get('extensions',{}).get('course_pdf_shell',{}).get('layout')=='course-print-v2'

def model(root,source,variant="full"):
    root=Path(root);source=Path(source);profile=json.loads((root/PROFILE).read_text('utf-8'))
    if profile['id']!='course-print-v2' or profile['body_font']!='STIX Two Text' or profile['heading_font']!='Be Vietnam Pro':
        raise ValueError('Unknown print typography contract')
    if lesson_layout(root)['id']!=profile['graph_layout']:raise ValueError('Current G03 graph layout required')
    import yaml
    data=contract(root);full=source.read_text('utf-8');text=full;tables={}
    metadata=yaml.safe_load(full.split('---',2)[1])
    if variant!='full':
        part=next((v for v in metadata.get('r1-section-download-files',[]) if v['variant']==variant),None)
        chunks=re.split(r'(?m)(?=^## )',full)
        kept=[]
        for chunk in chunks:
            header=re.match(r'^## [^\n]*\{#([^\s}]+)',chunk)
            section=header[1] if header else ''
            keep=(section!='loi-giai') if variant=='student' else (section in {'bat-dau','nguon',(part or {}).get('start')})
            if keep and section!='tai-tai-lieu':kept.append(chunk)
        text=''.join(kept)
    selected_ids=set(re.findall(r'\{#([^\s}]+)',text))|set(re.findall(r'<a\s+id=["\']([^"\']+)',text))

    for entry in data['pages'][source.parent.name]:
        ident=entry['selector'][1:].split()[0];rows=table_rows(text,ident)
        # Shared journal include belongs to the source closure, not the main QMD.
        if not rows:
            for inc in re.findall(r'{{<\s*include\s+([^\s>]+)',text):
                rows=table_rows((source.parent/inc).resolve().read_text('utf-8'),ident)
                if rows:break
        if not rows:continue
        fp=function_profile(entry,data)
        widths=fp['widths'] if fp else entry.get('widths')
        if widths is None:continue
        if len(widths)!=len(rows[0]) or any(len(r)!=len(widths) for r in rows):
            raise ValueError('Table profile/column mismatch: '+ident)
        tables[ident]={'widths':widths,'center_columns':list(range(len(widths))) if entry.get('kind') in {'sign','values'} else [],'right_columns':(fp or entry).get('right_columns',[]),'rows':len(rows)-1}
    graphs={};graph_engine=None
    for ref in re.findall(r'\]\(([^)\s]+\.svg)\)',text):
        if 'figures_0_4/' not in ref:continue
        if graph_engine is None:graph_engine=load_graph("print_graph_axis_gate",root)
        pdf=(source.parent/ref).with_suffix('.pdf');reader=PdfReader(pdf)
        box=reader.pages[0].mediabox;w=float(box.width);h=float(box.height)
        sizes=[]
        reader.pages[0].extract_text(visitor_text=lambda t,cm,tm,f,size:sizes.append(size) if t.strip() and size>2 else None)
        nominal=profile['graph_source_label_pt']*72/72.27
        if not sizes or abs(max(sizes)-nominal)>.1:raise ValueError('Unexpected graph label size: '+ref)
        ratio=profile['graph_label_pt']/profile['graph_source_label_pt']
        graphs[ref]={'pdf':ref[:-4]+'.pdf','width_pt':w*72.27/72*ratio,'height_pt':h*72.27/72*ratio,'scale':ratio,
          'rotate':w*72.27/72*ratio>476,'stream_sha256':hashlib.sha256(reader.pages[0].get_contents().get_data().strip()).hexdigest(),'axis_ticks':graph_engine.graph_axis_check(pdf)}
    variation=json.loads((source.parent/'du_lieu/bang_bien_thien.json').read_text('utf-8'))
    native_ids=re.findall(r'\{#([^\s}]+)\s+\.zo-native-bbt',text)+re.findall(r'\.r1-bbt\s+bbt="([^"]+)"',text)
    if not set(native_ids)<=set(v['id'] for v in variation):raise ValueError('Missing canonical variation data')
    links=[v for v in re.findall(r'\[Xem lời giải\]\(#([^)]*)\)',text) if v in selected_ids]
    backs=[v for v in re.findall(r'\[Xem đề bài\]\(#([^)]*)\)',text) if v in selected_ids]
    task_numbers={ident:int(number) for number,ident in re.findall(r'(?m)^#{2,6}\s+[^\n]*?Nhiệm vụ\s+(\d+)[^\n]*\{#([^\s}]+)',text)}
    return dict(profile,explicit_figure_captions=text.count('r1-figcaption')+text.count('<figcaption>'),task_numbers={pdf_id(k):v for k,v in task_numbers.items()},tables=tables,graphs=graphs,variation_ids=native_ids,variations={v['id']:v for v in variation if v['id'] in native_ids},solution_targets=[pdf_id(v) for v in links],problem_targets=[pdf_id(v) for v in backs])

def validate_tex(text,data):
    checks={}
    emitted={k:[float(w) for w in widths.split(',')] for k,widths in re.findall(r'% zo-table ([^\s]+) widths=([0-9.,]+)',text)}
    checks['all bound table profiles projected']=all(emitted.get(k)==v['widths'] for k,v in data['tables'].items())
    checks['all native variation tables projected']=all('% zo-variation '+k in text for k in data['variation_ids'])
    for ident,item in data.get('variations',{}).items():
        match=re.search(r'% zo-variation '+re.escape(ident)+r'\n(.*?)\\end\{tabular\}',text,re.S)
        rows=[]
        if match:
            rawrows=re.findall(r'^([^\n]+) \\\\ \\hline$',match[1],re.M)
            def cell(value):
                value=value.strip().strip('$')
                if value.startswith('\\shortstack{'):value=value[len('\\shortstack{'):-1].replace('\\\\',' ')
                for a,b in [('\\infty','∞'),('\\nearrow','↗'),('\\searrow','↘'),('\\parallel','∥')]:value=value.replace(a,b)
                return re.sub(r'\s+','',value).replace('−','-').replace('′',"'")
            rows=[[cell(c) for c in row.split(' & ')] for row in rawrows]
            expected=[[cell('∥' if r>0 and c in item.get('excluded_columns',[]) else v) for c,v in enumerate(row)] for r,row in enumerate(item['rows'])]
        else:expected=item['rows']
        checks['variation cells preserved/'+ident]=rows==expected
        checks['variation text labels use text/'+ident]=bool(match) and all(
            rawrows[i].lstrip().startswith('\\shortstack{') for i,row in enumerate(item['rows']) if ' ' in row[0])
    checks['header hierarchy is promoted']='\\section{' in text and '\\subsection{' in text
    placements=re.findall(r'\\begin\{figure\}(?:\[([^]]*)\])?',text)
    default_here=data.get('figure_placement')=='H' and r'\input{zo-course-print-layout.tex}' in text
    checks['figures remain in source order']=all(v=='H' or v=='' and default_here for v in placements)
    marked=re.findall(r'% zo-explicit-figure-caption\s*(.*?)\\end\{figure\}',text,re.S)
    checks['explicit figure captions emitted once']=len(marked)==data.get('explicit_figure_captions',0) and all(v.count(r'\caption')==2 and r'\captionsetup{labelformat=empty}\caption' in v for v in marked)
    return checks

def centered_graphs(records):
    return all(r.get('center_offset_pt',float('inf'))<2 for r in records)

def embedded_graphs(reader,data):
    expected={v['stream_sha256']:(k,v) for k,v in data['graphs'].items()};seen=[]
    for n,page in enumerate(reader.pages,1):
        objects=page['/Resources'].get('/XObject',{})
        def before(op,args,cm,tm):
            if op!=b'Do' or args[0] not in objects:return
            obj=objects[args[0]].get_object()
            if obj.get('/Subtype')!='/Form':return
            match=expected.get(hashlib.sha256(obj.get_data().strip()).hexdigest())
            if not match:return
            key,item=match;sx=math.hypot(cm[0],cm[1]);sy=math.hypot(cm[2],cm[3])
            box=[float(v) for v in obj['/BBox']]
            corners=[(cm[0]*x+cm[2]*y+cm[4],cm[1]*x+cm[3]*y+cm[5]) for x in [box[0],box[2]] for y in [box[1],box[3]]]
            left=min(p[0] for p in corners);right=max(p[0] for p in corners);bottom=min(p[1] for p in corners);top=max(p[1] for p in corners)
            seen.append({'source':key,'page':n,'scale_x':sx,'scale_y':sy,'expected_scale':item['scale'],
                         'center_offset_pt':abs((left+right)/2-float(page.mediabox.width)/2),
                         'inside_page':left>=0 and right<=float(page.mediabox.width)+1 and bottom>=0 and top<=float(page.mediabox.height)+1})
        page.extract_text(visitor_operand_before=before)
    return seen

def print_reference_checks(pdf,reader):
    result=subprocess.run(['pdftotext','-bbox-layout',str(pdf),'-'],check=True,capture_output=True)
    xml=ET.fromstring(result.stdout);pages=[];footers={};outside=[]
    for number,node in enumerate(xml.findall('.//{*}page')):
        width=float(node.attrib['width']);height=float(node.attrib['height']);words=[]
        for word in node.findall('.//{*}word'):
            a=word.attrib;item=(float(a['xMin']),float(a['yMin']),float(a['xMax']),float(a['yMax']),word.text or '')
            words.append(item)
            if item[0]<-1 or item[2]>width+1:outside.append({'page':number+1,'text':item[4]})
        pages.append((width,height,words))
        digits=[w for w in words if w[4].isdigit() and w[0]>width*.8 and w[1]>height*.9]
        if digits:footers[number]=int(digits[-1][4])
    samples=[];errors=[];names=reader.named_destinations
    first_body=reader.get_destination_page_number(names['bat-dau']) if 'bat-dau' in names else 0
    for number,page in enumerate(reader.pages):
        width,height,words=pages[number]
        for ref in page.get('/Annots',[]):
            ann=ref.get_object();action=ann.get('/A',{});dest=action.get('/D')
            if not isinstance(dest,str) or dest not in names:continue
            rect=[float(v) for v in ann['/Rect']];x1,y1,x2,y2=rect[0],height-rect[3],rect[2],height-rect[1]
            text=' '.join(w[4] for w in words if x1-1<=(w[0]+w[2])/2<=x2+1 and y1-1<=(w[1]+w[3])/2<=y2+1)
            match=re.search(r'trang\s+(\d+)',text)
            number_text=match[1] if match else (text if text.isdigit() and x1>width*.75 and number<first_body else None)
            if number_text is None:continue
            target=reader.get_destination_page_number(names[dest]);expected=footers.get(target)
            sample={'from_physical_page':number+1,'target':dest,'printed':int(number_text),'expected_footer':expected,'text':text}
            samples.append(sample)
            if expected is None or int(number_text)!=expected:errors.append(sample)
    return {'samples':samples,'errors':errors,'outside':outside}

def orphan_print_headers(reader):
    failures=[]
    for number,page in enumerate(reader.pages[1:-1],2):
        height=float(page.mediabox.height);chunks=[];depth=0
        def before(op,args,cm,tm):
            nonlocal depth
            if op==b'Do':depth+=1
        def after(op,args,cm,tm):
            nonlocal depth
            if op==b'Do':depth-=1
        def visitor(text,cm,tm,font,size):
            y=tm[4]*cm[1]+tm[5]*cm[3]+cm[5]
            if depth or not text.strip() or not 70<y<height-65:return
            chunks.append((y,text.strip(),str((font or {}).get('/BaseFont','')),size))
        page.extract_text(visitor_text=visitor,visitor_operand_before=before,visitor_operand_after=after)
        if chunks:
            last=min(chunks,key=lambda x:x[0])
            if 'BeVietnamPro-SemiBold' in last[2] and last[3]>11.5:failures.append({'page':number,'text':last[1]})
    return failures

def check(pdf,source,root,tex_path=None,variant="full"):
    data=model(root,source,variant);reader=PdfReader(pdf);texts=[p.extract_text() for p in reader.pages];alltext='\n'.join(texts)
    records=embedded_graphs(reader,data);named=reader.named_destinations
    actual_names=set(named)
    def position(dest):
        return (reader.get_destination_page_number(dest),str(dest.top),str(dest.left))
    target_ids=data['solution_targets']+data['problem_targets']
    dest_positions=[position(named[k]) for k in set(data['solution_targets']) if k in named]
    counts=collections.Counter()
    for page in reader.pages[1:-1]:
        def visitor(text,cm,tm,font,size):
            if text.strip() and font:counts[re.sub(r'^/?[A-Z]{6}\+','',str(font.get('/BaseFont','')))]+=len(text.strip())
        page.extract_text(visitor_text=visitor)
    checks={'all graph sources have no endpoint tick strokes':all(v['axis_ticks']['passed'] for v in data['graphs'].values()),'all current graph streams embedded':set(r['source'] for r in records)==set(data['graphs']),
      'all graphs use shared print scale':(not data['graphs'] or bool(records)) and all(abs(r['scale_x']-r['expected_scale'])<.002 and abs(r['scale_y']-r['expected_scale'])<.002 for r in records),
      'all graph bounds inside page':all(r['inside_page'] for r in records),
      'all graphs centered on paper':centered_graphs(records),
      'STIX body and Be headings by role':counts['STIXTwoText-Regular']>counts['BeVietnamPro-Regular'] and counts['BeVietnamPro-SemiBold']>0,
      'no replacement glyphs': '\ufffd' not in alltext,
      'printed contents present':any('Mục lục' in s for s in texts[1:4]),
      'all problem and solution destinations exist':set(target_ids)<=actual_names,
      'task anchors land on their heading page':all(k in named and re.search(r'Nhiệm\s+vụ\s+0*'+str(n)+r'\b',texts[reader.get_destination_page_number(named[k])]) for k,n in data['task_numbers'].items()),
      'solutions have distinct destinations':len(dest_positions)==len(set(data['solution_targets'])) and len(set(dest_positions))==len(dest_positions)}
    orphan_headers=orphan_print_headers(reader)
    checks['no heading stranded before a page break']=not orphan_headers
    references=print_reference_checks(pdf,reader)
    checks['printed page references match actual destinations']=len(references['samples'])>=len(set(data['solution_targets'])) and not references['errors']
    checks['no text extends horizontally beyond paper']=not references['outside']
    if tex_path:checks.update(validate_tex(Path(tex_path).read_text('utf-8'),data))
    return {'checks':checks,'failures':[k for k,v in checks.items() if not v],'orphan_headers':orphan_headers,'graphs':records,'print_references':references,'font_text_counts':dict(counts),'solution_count':len(data['solution_targets']),
            'task_anchor_errors':[{'id':k,'number':n,'page':reader.get_destination_page_number(named[k])+1 if k in named else None} for k,n in data['task_numbers'].items() if k not in named or not re.search(r'Nhiệm\s+vụ\s+0*'+str(n)+r'\b',texts[reader.get_destination_page_number(named[k])])], 'missing_destinations':sorted(set(target_ids)-actual_names),'pages':len(reader.pages),'owner_acceptance':'pending','published':False}
