"""G05 draft scene renderer, SVG/PNG only. Not a production geometry engine.
Source: minh_hoa.json. All outputs are generated; edit data/code, never SVG/PNG.
Uses existing ZO geometry palette, stroke widths and STIX Two Text font.
"""
from pathlib import Path
import hashlib,json,re,sys,copy,xml.etree.ElementTree as ET
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'scripts/zo_python.py').is_file())
sys.path.insert(0,str(ROOT/'scripts'))
from zo_graphics import graphics_root
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt, font_manager as fm
from matplotlib.patches import Polygon,Rectangle,Circle,Ellipse,PathPatch
from matplotlib.path import Path as MPath
from matplotlib.transforms import Affine2D,ScaledTranslation
from fontTools.ttLib import TTFont
from fontTools.pens.basePen import BasePen
import numpy as np
HERE=Path(__file__).resolve().parent
TOOL=graphics_root(ROOT)
STYLE=TOOL/'assets/tex/zo-geometry-styles.tex'
FONT=TOOL/'assets/fonts/STIXTwoText-Regular.otf'
fm.fontManager.addfont(str(FONT))
FP=fm.FontProperties(fname=str(FONT))
style=STYLE.read_text(encoding='utf-8')
colors=dict(re.findall(r'\\definecolor\{(\w+)\}\{HTML\}\{([A-Fa-f0-9]+)\}',style))
C={k:'#'+colors['zoGeometry'+v] for k,v in {'text':'Text','strong':'Strong','line':'Line','hidden':'Hidden','main':'Main','surface':'Surface'}.items()}
widths={k:float(re.search(r'\\newcommand\{\\zoGeometry'+v+r'Width\}\{([0-9.]+)pt\}',style).group(1)) for k,v in {'line':'Visible','hidden':'Hidden','main':'Main'}.items()}
plt.rcParams.update({'font.family':FP.get_name(),'svg.fonttype':'path','svg.hashsalt':'zo-g05-scenes-v1','axes.unicode_minus':False})

FT=TTFont(FONT)
GLYPHS=FT.getGlyphSet(); CMAP=FT.getBestCmap(); UPM=FT['head'].unitsPerEm
MATHFONT=TOOL/'assets/fonts/STIXTwoMath.otf'
MFT=TTFont(MATHFONT)
class OutlinePen(BasePen):
 def __init__(self,glyphs):super().__init__(glyphs);self.vertices=[];self.codes=[]
 def _moveTo(self,p):self.vertices.append(p);self.codes.append(MPath.MOVETO)
 def _lineTo(self,p):self.vertices.append(p);self.codes.append(MPath.LINETO)
 def _curveToOne(self,a,b,c):self.vertices.extend([a,b,c]);self.codes.extend([MPath.CURVE4]*3)
 def _qCurveToOne(self,a,b):self.vertices.extend([a,b]);self.codes.extend([MPath.CURVE3]*2)
 def _closePath(self):self.vertices.append((0,0));self.codes.append(MPath.CLOSEPOLY)
 def _endPath(self):pass

def txt(ax,x,y,s,size=11,align='center',color=None,coordinates='data'):
 if not s:return
 # Direct font outlines avoid the observed CFF/FreeType raster glyph corruption.
 # No font substitution; same STIX font bytes and vector paths in SVG and PNG.
 math_label=bool(re.fullmatch(r'[xyhp]|[0-9.]+ − 2x',s))
 font=MFT if math_label else FT
 if math_label:s=s.translate(str.maketrans({'x':'𝑥','y':'𝑦','h':'ℎ','p':'𝑝'}))
 glyphs=font.getGlyphSet();cmap=font.getBestCmap();upm=font['head'].unitsPerEm
 verts=[];codes=[];advance=0
 for ch in s:
  assert ord(ch) in cmap, 'missing glyph '+ch
  name=cmap[ord(ch)];pen=OutlinePen(glyphs);glyphs[name].draw(pen)
  verts.extend([(a+advance,b) for a,b in pen.vertices]);codes.extend(pen.codes)
  advance+=font['hmtx'][name][0]
 if not verts:return
 path=MPath(verts,codes);box=path.get_extents()
 xshift={'left':0,'center':-advance/2,'right':-advance}[align]
 yshift=-(box.ymin+box.ymax)/2
 base=ax.transData if coordinates=='data' else ax.transAxes
 transform=Affine2D().translate(xshift,yshift).scale(size/upm/72)+ax.figure.dpi_scale_trans+ScaledTranslation(x,y,base)
 patch=PathPatch(path,facecolor=color or C['text'],edgecolor='none',transform=transform,clip_on=False)
 ax.add_patch(patch)
 if not hasattr(ax.figure,'zo_labels'):ax.figure.zo_labels=[]
 ax.figure.zo_labels.append((s,patch))
 return patch

def poly(ax,points,fill=None,lw=None,color=None,alpha=1):
 patch=Polygon(points,closed=True,facecolor=fill or 'none',edgecolor=color or C['line'],linewidth=lw or widths['line'],joinstyle='round',alpha=alpha)
 ax.add_patch(patch);return patch

def line(ax,a,b,color=None,dash=False,lw=None):
 ax.plot([a[0],b[0]],[a[1],b[1]],color=color or C['line'],lw=lw or widths['line'],ls=(0,(3,2.2)) if dash else '-',solid_capstyle='round')

def dim(ax,a,b,label,distance,label_gap=.32):
 # Anchor to physical vertices. Offset perpendicular to the projected edge;
 # the dimension line keeps the complete edge vector, with no arrow shrink.
 a,b=np.asarray(a,dtype=float),np.asarray(b,dtype=float)
 v=b-a;length=np.linalg.norm(v)
 assert length>1e-9 and abs(distance)>.12, 'degenerate dimension'
 n=np.array([v[1],-v[0]])/length*np.sign(distance)
 ends=np.array([a,b])+abs(distance)*n
 def stroke(points):
  artist,=ax.plot(*np.asarray(points).T,color=C['hidden'],lw=widths['hidden'],solid_capstyle='butt')
  return artist
 bar=stroke(ends)
 caps=[stroke([e-.10*n,e+.10*n]) for e in ends]
 witnesses=[stroke([p+.06*n,e+.14*n]) for p,e in zip([a,b],ends)]
 txt(ax,*((ends[0]+ends[1])/2+label_gap*n),label,size=10)
 record={'edge':np.array([a,b]),'distance':abs(distance),'normal':n,
         'bar':bar,'caps':caps,'witnesses':witnesses,'label':label}
 if not hasattr(ax.figure,'zo_dimensions'):ax.figure.zo_dimensions=[]
 ax.figure.zo_dimensions.append(record)
 return record

def check_dimension(d):
 # Check actual artists, not only the helper's calculated coordinates.
 edge=d['edge'];v=edge[1]-edge[0];bar=d['bar'].get_xydata()
 assert np.linalg.norm(v)>1e-9, 'zero edge'
 assert np.allclose(bar[1]-bar[0],v,atol=1e-9,rtol=0), 'shortened or rotated bar'
 offsets=bar-edge
 assert np.allclose(offsets[0],offsets[1],atol=1e-9,rtol=0), 'unequal offsets'
 assert abs(np.dot(offsets[0],v))<1e-9, 'bar shifted along edge'
 assert abs(np.linalg.norm(offsets[0])-d['distance'])<1e-9, 'incorrect distance'
 for p,e,cap,witness in zip(edge,bar,d['caps'],d['witnesses']):
  c=cap.get_xydata();w=witness.get_xydata();n=e-p
  assert np.allclose(c.mean(axis=0),e,atol=1e-9,rtol=0), 'cap misses endpoint'
  assert abs(np.dot(c[1]-c[0],v))<1e-9, 'cap not perpendicular'
  assert np.linalg.norm(c[1]-c[0])>0, 'missing cap'
  assert len(w)==2 and witness.get_visible(), 'missing witness'
  assert all(abs(np.dot(t-p,v))<1e-9 for t in w), 'witness not aligned to vertex'
  assert 0<np.dot(w[0]-p,n)<np.dot(n,n)<np.dot(w[1]-p,n), 'witness does not reach bar'
 # Equal aspect is a precondition of this projected scene helper.
 assert d['bar'].axes.get_aspect()==1, 'dimension requires equal aspect'

def dimension_regressions():
 rejected=[]
 for defect in ['shortened','axial_shift','cap_shift','witness_shift','missing_witness']:
  fig,ax=plt.subplots();ax.set_aspect('equal')
  d=dim(ax,(0,0),(4,1),'x',.6);check_dimension(d)
  if defect=='shortened':
   p=d['bar'].get_xydata().copy();v=(p[1]-p[0])/np.linalg.norm(p[1]-p[0]);p[0]+=.1*v;p[1]-=.1*v;d['bar'].set_data(p.T)
  elif defect=='axial_shift':d['bar'].set_data((d['bar'].get_xydata()+[.4,.1]).T)
  elif defect=='cap_shift':d['caps'][0].set_data((d['caps'][0].get_xydata()+[.1,0]).T)
  elif defect=='witness_shift':d['witnesses'][0].set_data((d['witnesses'][0].get_xydata()+[.1,0]).T)
  else:d['witnesses'][0].set_visible(False)
  try:check_dimension(d)
  except AssertionError:rejected.append(defect)
  else:raise AssertionError('dimension defect accepted: '+defect)
  finally:plt.close(fig)
 return rejected

def project(x,y,z=0): return np.array([x-.65*y,.35*x+.35*y+z])

def open_box(ax,a,b,h,labels=('x','x','h'),glass=False):
 P=[project(0,0),project(a,0),project(a,b),project(0,b)]
 Q=[p+np.array([0,h]) for p in P]
 # Far walls, floor, then near walls. Top is never filled: this is an open object.
 for ids in [(3,2),(1,2)]:
  i,j=ids;poly(ax,[P[i],P[j],Q[j],Q[i]],C['surface'],alpha=.55 if glass else 1)
 poly(ax,P,'white')
 for i,j in [(0,3),(0,1)]:poly(ax,[P[i],P[j],Q[j],Q[i]],C['surface'],alpha=.35 if glass else 1)
 for i in range(4):line(ax,Q[i],Q[(i+1)%4],color=C['main'] if not glass else C['line'])
 if labels[0]:dim(ax,P[0],P[1],labels[0],.65)
 if labels[1]:dim(ax,P[3],P[0],labels[1],.55,label_gap=.43)
 if labels[2]:dim(ax,P[1],Q[1],labels[2],.6)
 allp=np.array(P+Q);ax.set_xlim(allp[:,0].min()-1.8,allp[:,0].max()+1.8);ax.set_ylim(-1.8,allp[:,1].max()+.8)
 ax.set_aspect('equal');ax.axis('off')

def validate(s):
 assert re.fullmatch(r'[a-z_]+',s['id']), 'unsafe id'
 if s['kind']=='cut_fold':
  L,W,x=s['L'],s['W'],s['cut'];assert 0<x<min(L,W)/2,'degenerate cut'
  if not s.get('cover'):assert s['labels']==[f'{L:g} cm',f'{W:g} cm',f'{L:g} − 2x',f'{W:g} − 2x','x'],'labels disagree with dimensions'
  # Kept cross area equals base plus four walls.
  assert abs(L*W-4*x*x-((L-2*x)*(W-2*x)+2*x*(L-2*x)+2*x*(W-2*x)))<1e-9
 elif s['kind']=='garden':
  assert s['length']>0 and s['depth']>0 and s['partitions'] in (0,1)
 elif s['kind']=='tank':assert s['side']>0 and s['height']>0
 else:assert s['kind']=='kiosk'

def cut_fold(s):
 fig,axes=plt.subplots(1,2,figsize=(22/2.54,8/2.54),gridspec_kw={'width_ratios':[1,1.2]})
 ax=axes[0];L,W,x=s['L'],s['W'],s['cut'];scale=6/max(L,W);L*=scale;W*=scale;x*=scale
 poly(ax,[(0,0),(L,0),(L,W),(0,W)],C['surface'])
 for a,b in [(0,0),(L-x,0),(0,W-x),(L-x,W-x)]:
  poly(ax,[(a,b),(a+x,b),(a+x,b+x),(a,b+x)],'white',color=C['main'])
  line(ax,(a+.12,b+.12),(a+x-.12,b+x-.12),color=C['main'],lw=.6)
  line(ax,(a+.12,b+x-.12),(a+x-.12,b+.12),color=C['main'],lw=.6)
 for y in [x,W-x]:line(ax,(x,y),(L-x,y),dash=True)
 for z in [x,L-x]:line(ax,(z,x),(z,W-x),dash=True)
 labels=s['labels']
 if not s.get('cover'):
  dim(ax,(0,0),(L,0),labels[0],.55);dim(ax,(0,0),(0,W),labels[1],-.5,label_gap=.62)
 if not s.get('cover'):
  dim(ax,(L-x,W),(L,W),'x',-.35)
  txt(ax,L/2,W/2,'Đáy',12);txt(ax,L/2,W+1.05,'Cắt bốn góc',12)
  txt(ax,L/2,-1.35,'Nét đứt: đường gấp',9)
 ax.set_xlim(-1.6,L+.5);ax.set_ylim(-1.7,W+1.5);ax.set_aspect('equal');ax.axis('off')
 open_box(axes[1],L-2*x,W-2*x,x,(labels[2],labels[3],labels[4]))
 if not s.get('cover'):txt(axes[1],.5,1.02,'Gấp thành hộp không nắp',12,coordinates='axes')
 fig.subplots_adjust(left=.02,right=.98,bottom=.05,top=.90,wspace=.10)
 return fig

def garden(s):
 fig,ax=plt.subplots(figsize=(16/2.54,9/2.54));L,D=s['length'],s['depth']
 p=lambda x,y,z=0:project(x,y,z)
 poly(ax,[p(0,0),p(L,0),p(L,D),p(0,D)],C['surface'])
 # Wall and masonry pattern are context; fence geometry is separate.
 poly(ax,[p(0,D),p(L,D),p(L,D,1),p(0,D,1)],C['surface'])
 for z in [.33,.66]:line(ax,p(0,D,z),p(L,D,z),color=C['hidden'],lw=.35)
 for z0,z1,shift in [(0,.33,0),(.33,.66,.5),(.66,1,0)]:
  for u in np.arange(.7+shift,L,.9):line(ax,p(u,D,z0),p(u,D,z1),color=C['hidden'],lw=.35)
 def fence(a,b):
  line(ax,a,b,C['main'],lw=widths['main'])
  for t in np.linspace(0,1,9):
   q=(1-t)*a+t*b;line(ax,q,q+[0,.25],C['main'],lw=.7)
 fence(p(0,0),p(L,0));fence(p(0,0),p(0,D));fence(p(L,0),p(L,D))
 if s['partitions']:fence(p(L/2,0),p(L/2,D))
 for u in np.linspace(.9,L-.9,5):
  for v in [1,2.6]:
   if s['partitions'] and abs(u-L/2)<.4:continue
   q=p(u,v);line(ax,q,q+[0,.24],C['hidden'],lw=.45)
   line(ax,q+[0,.1],q+[-.13,.22],C['hidden'],lw=.45);line(ax,q+[0,.12],q+[.13,.26],C['hidden'],lw=.45)
 dim(ax,p(0,0),p(L,0),'y',.65)
 dim(ax,p(0,0),p(0,D),'x',-.5)
 dim(ax,p(L,0),p(L,D),'x',.5)
 if s['partitions']:txt(ax,*p(L/2,D/2,.45),'x',11,color=C['main'])
 txt(ax,.5,.94,'Tường — không rào cạnh này',12,coordinates='axes')
 ax.set_xlim(-D*.65-1.5,L+1.5);ax.set_ylim(-1.6,.35*(L+D)+2);ax.set_aspect('equal');ax.axis('off')
 fig.subplots_adjust(left=.02,right=.98,bottom=.03,top=.98);return fig

def kiosk(s):
 fig,ax=plt.subplots(figsize=(16/2.54,9/2.54));ax.set_xlim(0,12);ax.set_ylim(0,7);ax.axis('off');ax.set_aspect('equal')
 # One oblique projection for counter, posts and the complete roof slab.
 p=lambda x,y,z:np.array([2+x+y,1+z+.65*y])
 width,depth,table_z,roof_z,thickness=7.5,1.,2.1,4.25,.25
 corners=[(0,0),(width,0),(width,depth),(0,depth)]
 table=np.array([p(x,y,table_z) for x,y in corners])
 floor=np.array([p(x,y,0) for x,y in corners])
 def face(points,fill,zorder):
  obj=poly(ax,points,fill);obj.set_zorder(zorder);return obj
 face([floor[0],floor[1],table[1],table[0]],C['surface'],1)
 face([floor[1],floor[2],table[2],table[1]],'white',1)
 face(table,'white',1)
 for u in np.arange(2.7,9.4,.9):line(ax,(u,1.15),(u,2.9),C['hidden'],lw=.3)
 roof_xy=[(-.3,-.15),(width+.3,-.15),(width+.3,depth+.15),(-.3,depth+.15)]
 lower=np.array([p(x,y,roof_z) for x,y in roof_xy])
 upper=np.array([p(x,y,roof_z+thickness) for x,y in roof_xy])
 posts=[]
 for x in [.28,width-.28]:
  y=depth/2;foot=p(x,y,table_z);head=p(x,y,roof_z)
  post,=ax.plot(*np.array([foot,head]).T,color=C['line'],lw=2.2,solid_capstyle='butt',zorder=3)
  posts.append({'artist':post,'xy':(x,y)})
  # Small mounting plates lie in the same table plane as the post feet.
  face([p(x+dx,y+dy,table_z) for dx,dy in [(-.08,-.08),(.08,-.08),(.08,.08),(-.08,.08)]],C['line'],3.1)
 # Explicit depth order hides post tips behind the roof; default line zorder
 # would otherwise put columns above filled roof faces regardless of draw order.
 roof=[face(upper,C['surface'],4),
       face([lower[0],lower[1],upper[1],upper[0]],'white',4),
       face([lower[1],lower[2],upper[2],upper[1]],'white',4)]
 for x in np.arange(.5,width,.9):
  ax.plot(*np.array([p(x,roof_xy[0][1],roof_z+thickness),p(x,roof_xy[2][1],roof_z+thickness)]).T,color=C['hidden'],lw=.5,zorder=4.1)
 fig.zo_kiosk={'project':p,'table_z':table_z,'roof_z':roof_z,'thickness':thickness,
               'width':width,'depth':depth,'table':table,'lower':lower,'upper':upper,
               'roof':roof,'posts':posts}
 # Paper cartons are objects, not a count of demand.
 for u in [3.2,4.1,5.0]:
  poly(ax,[(u,3.4),(u+.55,3.4),(u+.55,4.3),(u,4.3)],C['surface'])
  poly(ax,[(u,4.3),(u+.55,4.3),(u+.38,4.55),(u+.16,4.55)],'white')
  line(ax,(u+.15,3.8),(u+.4,3.8),C['hidden'],lw=.6)
 poly(ax,[(7.3,3.45),(9.05,3.45),(9.05,4.65),(7.3,4.65)],'white',color=C['main'])
 txt(ax,8.18,4.25,'Giá bán',12,color=C['main']);txt(ax,8.18,3.85,'p',15,color=C['main'])
 txt(ax,5.6,.35,'Số lượng vẽ chỉ minh họa bối cảnh',10)
 fig.subplots_adjust(left=.01,right=.99,bottom=.01,top=.99);return fig

def check_kiosk(fig):
 d=fig.zo_kiosk;p=d['project'];t=d['table'];u=d['roof'][0].get_xy()[:4]
 f=d['roof'][1].get_xy()[:4];side=d['roof'][2].get_xy()[:4]
 assert len(d['posts'])==2 and len(d['roof'])==3, 'missing structure'
 assert np.allclose(u,d['upper']), 'roof top detached from model'
 assert np.allclose(f,[d['lower'][0],d['lower'][1],u[1],u[0]]), 'front fascia detached'
 assert np.allclose(side,[d['lower'][1],d['lower'][2],u[2],u[1]]), 'side fascia detached'
 assert np.allclose(u-d['lower'],[0,d['thickness']]), 'inconsistent roof thickness'
 # Depth edges of the roof and counter must be parallel in the projection.
 v=t[2]-t[1];w=u[2]-u[1]
 assert abs(v[0]*w[1]-v[1]*w[0])<1e-9, 'inconsistent perspective'
 for post in d['posts']:
  x,y=post['xy'];artist=post['artist'];ends=artist.get_xydata()
  assert 0<x<d['width'] and 0<y<d['depth'], 'post outside tabletop'
  assert np.allclose(ends,[p(x,y,d['table_z']),p(x,y,d['roof_z'])],atol=1e-9,rtol=0), 'post disconnected'
  assert all(face.get_zorder()>artist.get_zorder() for face in d['roof']), 'post drawn through roof'

def kiosk_regressions():
 rejected=[]
 for defect in ['floating_foot','floating_head','roof_perspective','open_side_fascia','post_above_roof']:
  fig=kiosk({});check_kiosk(fig);d=fig.zo_kiosk
  if defect in ['floating_foot','floating_head']:
   artist=d['posts'][0]['artist'];v=artist.get_xydata().copy();v[0 if defect=='floating_foot' else 1,1]+=.12;artist.set_data(v.T)
  elif defect=='roof_perspective':
   v=d['roof'][0].get_xy().copy();v[2:4,1]+=.12;d['roof'][0].set_xy(v)
  elif defect=='open_side_fascia':
   v=d['roof'][2].get_xy().copy();v[1,0]+=.12;d['roof'][2].set_xy(v)
  else:d['posts'][0]['artist'].set_zorder(5)
  try:check_kiosk(fig)
  except AssertionError:rejected.append(defect)
  else:raise AssertionError('kiosk defect accepted: '+defect)
  finally:plt.close(fig)
 return rejected

def tank(s):
 fig,ax=plt.subplots(figsize=(12/2.54,9/2.54));open_box(ax,s['side'],s['side'],s['height'],('x','x','h'),True)
 txt(ax,.5,1.04,'Không có nắp',12,coordinates='axes');fig.subplots_adjust(left=.05,right=.95,bottom=.05,top=.88);return fig

BUILD={'cut_fold':cut_fold,'garden':garden,'kiosk':kiosk,'tank':tank}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 data=json.loads((HERE/'minh_hoa.json').read_text(encoding='utf-8'))
 for s in data['scenes']:validate(s)
 # Meaningful negative fixtures: invalid cuts and unsupported partition arrangements.
 for source,patch in [(data['scenes'][0],{'cut':15}),(data['scenes'][1],{'partitions':2}),(data['scenes'][3],{'height':0})]:
  invalid={**source,**patch}
  try:validate(invalid)
  except AssertionError:pass
  else:raise AssertionError('invalid scene accepted')
 outputs={};dimension_checks={};dimension_negative=dimension_regressions();kiosk_negative=kiosk_regressions()
 for s in data['scenes']:
  fig=BUILD[s['kind']](s)
  fig.canvas.draw()
  if s["kind"]=="kiosk":check_kiosk(fig)
  dimensions=getattr(fig,"zo_dimensions",[])
  for d in dimensions:check_dimension(d)
  dimension_checks[s["id"]]=len(dimensions)
  for label,patch in getattr(fig,'zo_labels',[]):
   box=patch.get_window_extent();frame=fig.bbox
   assert box.x0>=frame.x0 and box.x1<=frame.x1 and box.y0>=frame.y0 and box.y1<=frame.y1, 'label outside canvas: '+label
   assert box.height<frame.height*.12, 'oversized glyph: '+label
  for ext in ['svg','png']:
   out=HERE/(s['id']+'.'+ext)
   kw={'metadata':{'Date':None,'Creator':'ZO Math G05 parametric scenes v1'}} if ext=='svg' else {'metadata':{'Software':'ZO Math G05 parametric scenes v1'}}
   fig.savefig(out,dpi=data['dpi'],transparent=bool(s.get('cover')),**kw)
   if ext=='svg':
    r=ET.parse(out).getroot();assert r.tag.endswith('svg')
    assert not any(e.tag.endswith('image') for e in r.iter()),'raster embedded in vector'
   outputs[out.name]=sha(out)
  plt.close(fig)
 receipt={'generator':Path(__file__).name,'generator_sha256':sha(Path(__file__)),'data_sha256':sha(HERE/'minh_hoa.json'),'style_source':str(STYLE),'style_sha256':sha(STYLE),'font_source':str(FONT),'font_sha256':sha(FONT),'math_font_source':str(MATHFONT),'math_font_sha256':sha(MATHFONT),'matplotlib':matplotlib.__version__,'outputs':outputs,'negative_cases':3,'dimension_checks':dimension_checks,'dimension_negative_cases':dimension_negative,'kiosk_negative_cases':kiosk_negative,'kiosk_geometry_check':'passed','status':'generated_pending_visual_and_owner_review','limits':['context illustrations, not mathematical plots','no production geometry certification','perspective drawings must not be measured','no HTML/PDF generated']}
 (HERE/'manifest.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print('Generated',len(outputs),'SVG/PNG files; 3 invalid-scene cases rejected; dimensions:',dimension_checks,'; negative dimension cases:',len(dimension_negative),'; negative kiosk cases:',len(kiosk_negative))
if __name__=='__main__':main()
