"""G04 editorial variants from the exact parameterization v=t+1/t.

Here t=x-1 and v=u(x)-2 for u(x)=x²/(x-1). All geometry, including
the two asymptotes, uses ONE affine map in each composition.
"""
from pathlib import Path
import base64,hashlib,json,math
from PIL import Image,ImageDraw,ImageFont

ROOT=Path(__file__).resolve().parents[1]
FOLDER=Path('content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g04/hinh/minh_hoa_chuyen_de_v1')
FORMATS={'1x1':(1200,1200),'3x4':(960,1280),'4x3':(1280,960),'9x16':(864,1536)}
RED='#EF5350'; YELLOW='#FFCA28'; INK='#3E3A35'


def geometry(width,height):
    margin_x=width*.075; margin_y=height*.075
    cx,cy=width/2,height/2
    sx=(width/2-margin_x)/4
    sy=(height/2-margin_y)/4.25
    def point(t,v):return (cx+sx*t,cy-sy*v)
    positive=[math.exp(math.log(.25)+i/1000*math.log(16)) for i in range(1001)]
    negative=[-t for t in reversed(positive)]
    branches=[]
    for ts in (negative,positive):
        curve=[]
        for t in ts:
            v=t+1/t
            p=point(t,v)
            guide=point(t,t)
            # The signed vertical difference is -sy/t in image coordinates.
            assert (p[1]-guide[1])*t<0
            assert abs((v-t)-1/t)<1e-12
            assert 0<p[0]<width and 0<p[1]<height
            curve.append(p)
        branches.append(curve)
    extrema=[point(-1,-2),point(1,2)]
    assert extrema[0][1]>extrema[1][1]
    return branches,extrema,[(cx,margin_y),(cx,height-margin_y)],[point(-4,-4),point(4,4)]


def render(root,ratio,size):
    width,height=size
    curves,points,vertical,oblique=geometry(width,height)
    unit=min(width,height)/1200
    stroke=8*unit; guide_width=4.5*unit; radius=20*unit; rim=6*unit
    dash=19*unit; gap=15*unit; text_size=29*unit
    font_path=root/'_design/ngon_ngu_thiet_ke_zo_math_0_4/07_mau_thi_giac/assets/BeVietnamPro_Regular.ttf'
    supersample=3
    canvas=Image.new('RGBA',(width*supersample,height*supersample))
    draw=ImageDraw.Draw(canvas)
    def xy(p):return tuple(v*supersample for v in p)
    def line(vertices,color,thickness):
        draw.line([xy(p) for p in vertices],fill=color,width=round(thickness*supersample),joint='curve')
        rr=thickness*supersample/2
        for p in (vertices[0],vertices[-1]):
            x,y=xy(p);draw.ellipse((x-rr,y-rr,x+rr,y+rr),fill=color)
    def dashed(vertices):
        (x0,y0),(x1,y1)=vertices
        length=math.hypot(x1-x0,y1-y0)
        for offset in range(math.ceil(length/(dash+gap))):
            lo=offset*(dash+gap); hi=min(lo+dash,length)
            if lo>=length:break
            line([(x0+(x1-x0)*lo/length,y0+(y1-y0)*lo/length),
                  (x0+(x1-x0)*hi/length,y0+(y1-y0)*hi/length)],INK,guide_width)
    dashed(vertical);dashed(oblique)
    for curve in curves:line(curve,RED,stroke)
    font=ImageFont.truetype(str(font_path),round(text_size*supersample))
    labels=[]
    for index,(x,y) in enumerate(points):
        xx,yy=x*supersample,y*supersample;rr=radius*supersample
        draw.ellipse((xx-rr,yy-rr,xx+rr,yy+rr),fill=YELLOW,outline=RED,width=round(rim*supersample))
        text='Cực đại' if index==0 else 'Cực tiểu'
        tx=x+10*unit if index==0 else x-10*unit
        ty=y-38*unit if index==0 else y+55*unit
        anchor='ms'
        draw.text((tx*supersample,ty*supersample),text,font=font,fill=INK,anchor=anchor)
        labels.append((tx,ty,text,'middle'))
    dest=root/FOLDER/'candidates'
    dest.mkdir(exist_ok=True)
    png=dest/f'r1_g04-{ratio}-formula.png'
    svg=png.with_suffix('.svg')
    canvas.resize(size,Image.Resampling.LANCZOS).save(png,optimize=True)
    encoded_font=base64.b64encode(font_path.read_bytes()).decode('ascii')
    def pts(vertices):return ' '.join(f'{x:.6f},{y:.6f}' for x,y in vertices)
    guides=''.join(f'<polyline points="{pts(v)}"/>' for v in [vertical,oblique])
    paths=''.join(f'<polyline points="{pts(v)}"/>' for v in curves)
    circles=''.join(f'<circle cx="{x:.6f}" cy="{y:.6f}" r="{radius:.6f}"/>' for x,y in points)
    texts=''.join(f'<text x="{x:.6f}" y="{y:.6f}" text-anchor="{anchor}">{text}</text>' for x,y,text,anchor in labels)
    svg.write_text(f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">Khảo sát hàm số: cực đại thấp hơn cực tiểu</title>
<desc id="desc">u(x)=x²/(x−1). Tọa độ dùng t=x−1, v=u−2=t+1/t. Cùng phép đổi tọa độ được áp lên đường cong và hai tiệm cận. Nhánh phải luôn trên đường xiên; nhánh trái luôn dưới.</desc>
<style>@font-face{{font-family:Be;src:url(data:font/ttf;base64,{encoded_font})}}text{{font-family:Be,sans-serif;font-size:{text_size:.6f}px;fill:{INK}}}</style>
<g fill="none" stroke="{INK}" stroke-width="{guide_width:.6f}" stroke-dasharray="{dash:.6f} {gap:.6f}" stroke-linecap="round">{guides}</g>
<g fill="none" stroke="{RED}" stroke-width="{stroke:.6f}" stroke-linecap="round" stroke-linejoin="round">{paths}</g>
<g fill="{YELLOW}" stroke="{RED}" stroke-width="{rim:.6f}">{circles}</g>{texts}</svg>''','utf-8')
    return png,svg


def main():
    root=ROOT
    manifest_path=root/FOLDER/'manifest.json'
    manifest=json.loads(manifest_path.read_text('utf-8'))
    master=root/FOLDER/manifest['master']['file']
    assert hashlib.sha256(master.read_bytes()).hexdigest()==manifest['master']['sha256']
    sources={}
    for ratio,size in FORMATS.items():
        png,svg=render(root,ratio,size)
        with Image.open(png) as im:
            assert im.mode=='RGBA' and im.getpixel((0,0))[3]==0
        sources[ratio]=dict(file=png.relative_to(root/FOLDER).as_posix(),
            sha256=hashlib.sha256(png.read_bytes()).hexdigest(),dimensions=list(size),approval='pending_owner_review',
            mechanism='formula_based_native_geometry',recipe='scripts/zo_topic_art_g04.py',
            vector_source=svg.relative_to(root/FOLDER).as_posix(),vector_sha256=hashlib.sha256(svg.read_bytes()).hexdigest(),
            reference_master_sha256=manifest['master']['sha256'],
            math_checks=dict(formula='v=t+1/t',right_above_oblique=True,left_below_oblique=True,
                sample_count=2002,extrema_t=[-1,1],extrema_v=[-2,2],same_affine_map_for_curve_and_asymptotes=True))
    manifest.update(variant_sources=sources,requested_formats=['1x1','3x4','4x3','9x16','16x9'],export_margin_px=2)
    manifest['approval']={'status':'approved','date':'2026-11-04','scope':'artwork_master',
        'evidence':{'kind':'direct_user_message','quote':'Mình duyệt ảnh này. Hãy tạo các phiên bản kích thước khác và tổ chức lưu bộ ảnh.'}}
    manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n','utf-8')
    print(json.dumps({'rendered':list(sources),'master_unchanged':True,'math_checked':True}))


if __name__=='__main__':main()
