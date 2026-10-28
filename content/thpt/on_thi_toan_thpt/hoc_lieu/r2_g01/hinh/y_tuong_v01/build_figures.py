"""Data-owned statistical diagrams using ZO Math 0.4 colours and STIX Two."""
from pathlib import Path
import collections, json, statistics
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager

HERE = Path(__file__).resolve().parent
REPO = next(p for p in HERE.parents if (p/'assets/fonts/STIXTwoText-Regular.otf').is_file())

def style():
    palette = json.loads((REPO/'_design/ngon_ngu_thiet_ke_zo_math_0_4/03_du_lieu/color_system.json').read_text('utf-8'))['palette']
    for name in ['Regular', 'Bold']:
        font_manager.fontManager.addfont(REPO/f'_design/ngon_ngu_thiet_ke_zo_math_0_4/07_mau_thi_giac/assets/STIXTwoText_{name}.ttf')
    plt.rcParams.update({'font.family':'STIX Two Text','font.size':13,
        'text.color':palette['gray-8'],'axes.labelcolor':palette['gray-8'],
        'xtick.color':palette['gray-7'],'ytick.color':palette['gray-7'],
        'svg.fonttype':'path','axes.titleweight':'semibold'})
    return palette

def axis(ax, palette):
    ax.set_yticks([])
    ax.spines[['left','right','top']].set_visible(False)
    ax.spines['bottom'].set_color(palette['gray-5'])
    ax.spines['bottom'].set_linewidth(.8)
    ax.tick_params(axis='x',labelsize=12,length=3,pad=5)

def dots(ax, values, palette):
    seen=collections.Counter()
    for value in values:
        ax.plot(value,.22+seen[value]*.24,'o',color=palette['gray-8'],markersize=7,zorder=4)
        seen[value]+=1

def save(fig, path, title, description):
    fig.savefig(path,bbox_inches='tight',metadata={'Date':None,'Title':title,'Description':description})
    plt.close(fig)

def draw():
    p=style(); data=json.loads((HERE/'data.json').read_text('utf-8'))
    fig,axes=plt.subplots(2,1,figsize=(9,5.5))
    for ax,row in zip(axes,data['mean_median']):
        values=row['values'];mean=statistics.mean(values);median=statistics.median(values)
        axis(ax,p); ax.set_xlim(0,30);ax.set_ylim(0,1.35)
        ax.set_title(row['name']+'  ·  '+ '; '.join(map(str,values))+' phút',loc='left',pad=14,fontsize=15)
        ax.vlines(median,0,1.12,color=p['gray-7'],linewidth=1)
        ax.vlines(mean,0,.74,color=p['red-5'],linewidth=1.6,linestyle=(0,(4,3)))
        ax.annotate(f'Trung vị = {median:g}',(median,1.12),(median+1,1.12),ha='left',va='center',
            arrowprops={'arrowstyle':'-','color':p['gray-7'],'lw':.8},fontsize=13)
        ax.annotate(f'Trung bình = {mean:g}',(mean,.74),(mean+1,.74),ha='left',va='center',
            arrowprops={'arrowstyle':'-','color':p['red-5'],'lw':.8},color=p['red-5'],fontsize=13)
        dots(ax,values,p);ax.set_xticks([0,4,8,12,16,20,24,28]);ax.set_xlabel('Thời gian chờ (phút)',labelpad=8)
    fig.tight_layout(h_pad=2.5)
    save(fig,HERE/'trung_binh_trung_vi.svg','Trung bình thay đổi, trung vị giữ nguyên',
         'Hai mẫu 2; 3; 3; 4; 8 và 2; 3; 3; 4; 28 phút. Mỗi chấm là một người. Trung bình từ 4 thành 8 phút, trung vị vẫn 3 phút.')
    fig,axes=plt.subplots(2,1,figsize=(9,5.6))
    for ax,row in zip(axes,data['same_groups']):
        values=row['values'];axis(ax,p);ax.set_xlim(-.5,20.5);ax.set_ylim(0,1.18)
        for a,b in zip(data['group_edges'],data['group_edges'][1:]):
            ax.axvspan(a,b,color=p['yellow-1'],ec=p['gray-3'],linewidth=.8,zorder=0)
            ax.text((a+b)/2,.96,f'[{a}; {b}) · 2 quan sát',ha='center',va='center',fontsize=13)
        dots(ax,values,p)
        ax.set_title(f"{row['name']}: "+'; '.join(map(str,values))+f"  ·  Trung bình = trung vị = {statistics.mean(values):g}",
                     loc='left',pad=14,fontsize=15)
        ax.set_xticks([0,1,5,9,10,11,15,19,20]);ax.tick_params(axis='x',labelsize=11)
        ax.set_xlabel('Giá trị quan sát',labelpad=8)
    fig.tight_layout(h_pad=2.5)
    save(fig,HERE/'cung_bang_khac_mau.svg','Cùng bảng nhóm, khác trung bình và trung vị',
         'Mẫu A: 1; 1; 11; 11. Mẫu B: 9; 9; 19; 19. Mỗi mẫu đều có hai quan sát trong mỗi nhóm [0; 10) và [10; 20).')

if __name__=='__main__':draw()
