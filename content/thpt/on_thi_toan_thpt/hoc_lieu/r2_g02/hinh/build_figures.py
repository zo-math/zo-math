"""R2-G02 statistical figures: canonical data, explicit ZO Math 0.4 typography."""
from pathlib import Path
import argparse, collections, hashlib, json, statistics
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.patches import Rectangle

HERE=Path(__file__).resolve().parent
REPO=next(p for p in HERE.parents if (p/'scripts/zo_python.py').is_file())
ASSETS=REPO/'_design/ngon_ngu_thiet_ke_zo_math_0_4/07_mau_thi_giac/assets'
STYLE=REPO/'_design/ngon_ngu_thiet_ke_zo_math_0_4/03_du_lieu/color_system.json'
P=json.loads(STYLE.read_text('utf-8'))['palette']
REG=FontProperties(fname=str(ASSETS/'BeVietnamPro_Regular.ttf'),size=12)
HEAD=FontProperties(fname=str(ASSETS/'BeVietnamPro_SemiBold.ttf'),size=14)
plt.rcParams.update({'svg.fonttype':'path','svg.hashsalt':'zo-r2g02-figures-v2',
                     'text.color':P['gray-8'],'axes.labelcolor':P['gray-8'],
                     'axes.titleweight':'normal','font.weight':'normal'})

def text(ax,x,y,label,**kw):
    return ax.text(x,y,label,fontproperties=REG,**kw)

def canvas(height,title,subtitle):
    fig,ax=plt.subplots(figsize=(6.6,height))
    fig.subplots_adjust(left=.10,right=.96,bottom=.30 if height<4 else .24,top=.71)
    fig.text(.10,.94,title,fontproperties=HEAD,va='top')
    fig.text(.10,.82,subtitle,fontproperties=REG,va='top')
    fig.text(.10,.025,'Mỗi chấm tròn biểu diễn một quan sát.',fontproperties=REG,va='bottom')
    ax.set_yticks([]);ax.spines[['left','right','top']].set_visible(False)
    ax.spines['bottom'].set_color(P['gray-7']);ax.spines['bottom'].set_linewidth(.8)
    ax.tick_params(axis='x',colors=P['gray-7'],length=3,pad=6)
    ax.set_xlabel('Giá trị quan sát',fontproperties=REG,labelpad=9)
    return fig,ax

def dots(ax,values):
    counts=collections.Counter()
    for value in values:
        ax.plot(value,.18+counts[value]*.20,'o',color=P['gray-8'],markersize=6,zorder=5)
        counts[value]+=1

def draw(preview_dir=None):
    data=json.loads((HERE/'data.json').read_text('utf-8'));outputs={}
    def save(fig,ax,name,title):
        for label in ax.get_xticklabels():label.set_fontproperties(REG)
        # Text is exported as glyph paths from these exact font files, with no fallback.
        fig.canvas.draw()
        fig.savefig(HERE/(name+'.svg'),metadata={'Date':None,'Title':title},facecolor='white')
        if preview_dir:
            preview_dir.mkdir(parents=True,exist_ok=True)
            fig.savefig(preview_dir/(name+'.png'),dpi=150,facecolor='white')
        outputs[name+'.svg']=hashlib.sha256((HERE/(name+'.svg')).read_bytes()).hexdigest()
        plt.close(fig)
    for name,values in data['cung_trung_tam'].items():
        fig,ax=canvas(3.5,'Mẫu '+name,'Gồm 5 quan sát: '+'; '.join(map(str,values))+'.')
        ax.set_xlim(0,20);ax.set_ylim(0,.95);ax.set_xticks([0,5,10,15,20])
        dots(ax,values);mean=statistics.mean(values)
        ax.vlines(mean,0,.65,color=P['red-5'],lw=1.1,linestyles='dashed')
        text(ax,mean,.78,f'Trung bình của mẫu: {mean:g}',ha='center',color=P['red-5'])
        save(fig,ax,'cung_trung_tam_'+name.lower(),'Mẫu '+name+' có trung bình bằng 10')
    for name in ['A','B']:
        values=data['cung_bang_nhom'][name]['values'] if isinstance(data['cung_bang_nhom'][name],dict) else data['cung_bang_nhom'][name]
        variance=statistics.pvariance(values)
        fig,ax=canvas(4.3,'Mẫu '+name+': '+'; '.join(map(str,values)),f'Phương sai của mẫu gốc: {variance:g}.')
        ax.set_xlim(-1,21);ax.set_ylim(0,1.65);ax.set_xticks([0,5,10,15,20])
        for lo,hi in zip(data['cung_bang_nhom']['edges'],data['cung_bang_nhom']['edges'][1:]):
            count=sum(lo<=v<hi for v in values);middle=(lo+hi)/2
            ax.axvspan(lo,hi,facecolor=P['yellow-1'],edgecolor=P['gray-3'],lw=.7,zorder=0)
            text(ax,middle,1.48,f'Lớp [{lo}; {hi})\nCó {count} quan sát.',ha='center',va='top',linespacing=1.5)
            ax.plot(middle,.86,'D',color=P['red-5'],ms=5,zorder=3)
            text(ax,middle,.68,f'Trung điểm của lớp: {middle:g}',ha='center',va='top',color=P['red-5'],fontsize=11)
        dots(ax,values)
        save(fig,ax,'cung_bang_nhom_'+name.lower(),'Cùng bảng nhóm; phương sai mẫu '+name+' bằng '+str(variance))
    d=data['gia_tri_bat_thuong']
    fig,ax=canvas(5.1,'Nhận diện giá trị bất thường','Mẫu: '+'; '.join(map(str,d['values']))+'.')
    ax.set_xlim(-3,17);ax.set_ylim(0,2.2);ax.set_xticks([0,2,4,6,8,10,12,14])
    dots(ax,d['values'])
    ax.add_patch(Rectangle((d['Q1'],1.35),d['Q3']-d['Q1'],.30,facecolor=P['yellow-1'],edgecolor=P['gray-7'],lw=.9))
    ax.vlines(d['median'],1.35,1.65,color=P['red-5'],lw=1.3)
    text(ax,3.8,1.72,'Q₁ = 4',ha='right');text(ax,7.2,1.72,'Q₃ = 7',ha='left')
    text(ax,5,2.0,'Trung vị: 5',ha='center',color=P['red-5'])
    for x,label in [(d['lower'],'Ngưỡng dưới: −0,5'),(d['upper'],'Ngưỡng trên: 11,5')]:
        ax.vlines(x,0,1.0,color=P['gray-6'],lw=.9,linestyles='dashed')
        text(ax,x,1.07,label,ha='center',fontsize=11)
    ax.annotate('Giá trị 14 vượt\nngưỡng trên.',(14,.23),(15.5,.56),ha='center',fontproperties=REG,color=P['red-5'],fontsize=11,
                arrowprops={'arrowstyle':'-','lw':.8,'color':P['red-5']})
    save(fig,ax,'gia_tri_bat_thuong','Giá trị 14 vượt ngưỡng trên 11,5')
    manifest={'style':'ZO Math 0.4','data_sha256':hashlib.sha256((HERE/'data.json').read_bytes()).hexdigest(),
              'font_regular':'BeVietnamPro_Regular.ttf','font_heading':'BeVietnamPro_SemiBold.ttf','outputs':outputs}
    if preview_dir:(preview_dir/'figures.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),'utf-8')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--preview-dir',type=Path)
    parser.add_argument('--repo',type=Path);parser.add_argument('--independent-only',action='store_true')
    args=parser.parse_args();draw(args.preview_dir)
