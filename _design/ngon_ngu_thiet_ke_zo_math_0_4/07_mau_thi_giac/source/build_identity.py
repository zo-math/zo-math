from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
import json
R=Path(__file__).resolve().parents[1];font=TTFont(R/'assets/BeVietnamPro_SemiBold.ttf');gs=font.getGlyphSet();cm=font.getBestCmap();reg=[]
def word(text,x,y,size,spacing,fill):
 scale=size/font['head'].unitsPerEm;s=''
 for c in text:
  g=gs[cm[ord(c)]];p=SVGPathPen(gs);g.draw(TransformPen(p,(scale,0,0,-scale,x,y)));s+=f'<path d="{p.getCommands()}" fill="{fill}"/>';x+=g.width*scale+spacing
 return s
Z='M2 0H84V13L20 86H84V100H0V87L64 14H2Z';O='M47 -2C76 -2 94 18 94 50C94 82 76 102 47 102C18 102 0 82 0 50C0 18 18 -2 47 -2Z M47 13C27 13 16 27 16 50C16 73 27 87 47 87C67 87 78 73 78 50C78 27 67 13 47 13Z'
def mark(mode):
 z='#EF5350' if mode=='color' else '#FFFFFF';o='#FFCA28' if mode=='color' else '#FFFFFF'
 return '<rect width="128" height="128" rx="3" fill="#3E3A35"/><rect x="140" width="128" height="128" rx="3" fill="#3E3A35"/>'+f'<path d="{Z}" transform="translate(27 20) scale(.88)" fill="{z}"/><path d="{O}" transform="translate(163 20) scale(.88)" fill="{o}" fill-rule="evenodd"/>'
def save(id,w,h,body,why):
 (R/'logos'/f'{id}.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img"><title>ZO Math — {id}</title><desc>{why}</desc>{body}</svg>');reg.append({'id':id,'file':'logos/'+id+'.svg','why':why})
for mode in ['color','mono']:
 for dark in [False,True]:
  suffix=mode+('_dark' if dark else '');ink='#FFFFFF' if dark else '#3E3A35';bg='<rect width="600" height="260" fill="#25221F"/>' if dark else ''
  why='Hai ô độc lập cùng màu Xám ZO #3E3A35; Z đỏ, O vàng không viền. Khe 12/128 bề rộng ô giữ tách biệt mà cùng nhịp. Góc bo 3/128 chỉ làm mềm biên, không biến thành viên thuốc.'
  save('stack_'+suffix,316,230,bg+'<g transform="translate(24 20)">'+mark(mode)+'</g>'+word('MATH',158-(sum(gs[cm[ord(c)]].width for c in 'MATH')*38/font['head'].unitsPerEm+21)/2,206,38,7,ink),why)
  save('horizontal_'+suffix,490,168,bg+'<g transform="translate(20 20)">'+mark(mode)+'</g>'+word('MATH',319,98,37,2.2,ink),why+' Bản ngang dành cho đầu trang.')
  save('symbol_'+suffix,300,160,bg+'<g transform="translate(16 16)">'+mark(mode)+'</g>',why)
 save('avatar_'+mode,300,300,'<rect width="300" height="300" rx="48" fill="#FFFFFF"/><g transform="translate(16 86)">'+mark(mode)+'</g>',why)
 save('favicon_'+mode,64,64,'<g transform="translate(1 17.2) scale(.231)">'+mark(mode)+'</g>',why)
save('motif',230,40,'<g transform="translate(16 16)"><rect width="120" height="8" rx="4" fill="#EF5350"/><rect x="134" width="64" height="8" rx="4" fill="#FFCA28"/></g>','Giữ tỉ lệ dấu nhấn nguồn 15 : 1,75 : 8; không phải đường gạch chân nội dung.')
(R/'design/logos.json').write_text(json.dumps(reg,ensure_ascii=False,indent=2))
print('17 logo/motif SVG; O has no stroke')
