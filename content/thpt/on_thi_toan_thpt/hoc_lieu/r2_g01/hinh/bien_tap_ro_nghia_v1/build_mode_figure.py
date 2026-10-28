"""Construct the grouped-mode estimate from the preserved three class counts."""
from pathlib import Path
import importlib.util, json
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('statistical_style',HERE.parent/'y_tuong_v01/build_figures.py')
style_module=importlib.util.module_from_spec(spec);spec.loader.exec_module(style_module)
plt=style_module.plt

def build(out=HERE):
    p=style_module.style();data=json.loads((HERE/'data.json').read_text('utf-8'))
    before,modal,after=data['classes'];a,b,f=modal
    left=f-before[2];right=f-after[2]
    mode=a+left/(left+right)*(b-a);height=before[2]+left*left/(left+right)
    fig,ax=plt.subplots(figsize=(9,5.1))
    ax.set_xlim(174.3,190.7);ax.set_ylim(0,17)
    for l,r,count in data['classes']:
        ax.bar(l,count,width=r-l,align='edge',color=p['yellow-1'] if count==f else p['gray-1'],
               edgecolor=p['gray-6'],linewidth=1,zorder=2)
        ax.text((l+r)/2,count+.35,str(count),ha='center',va='bottom',fontsize=14)
    ax.plot([a,b],[before[2],f],color=p['red-5'],lw=1.8,label='Đoạn đi lên: từ mức 3 đến mức 15',zorder=3)
    ax.plot([a,b],[f,after[2]],color=p['gray-7'],lw=1.6,ls=(0,(6,3)),label='Đoạn đi xuống: từ mức 15 đến mức 10',zorder=3)
    ax.vlines(mode,0,height,color=p['red-5'],ls=(0,(2,3)),lw=1.2,zorder=3)
    ax.plot(mode,height,'o',color=p['red-5'],ms=6,zorder=4)
    ax.annotate('Giao điểm',(mode,height),(187,13.8),fontsize=13,
                arrowprops={'arrowstyle':'-','color':p['gray-6'],'lw':.8})
    ax.annotate('Mốt ước lượng: khoảng 183,53 mm',xy=(mode,0),xycoords='data',xytext=(.25,-.21),textcoords='axes fraction',
                ha='center',va='top',fontsize=14,color=p['red-5'],
                arrowprops={'arrowstyle':'-','color':p['red-5'],'lw':.8})
    ax.set_xticks([175,180,185,190]);ax.set_yticks([0,5,10,15]);ax.tick_params(labelsize=12)
    ax.set_ylabel('Tần số',labelpad=12);ax.set_xlabel('Chiều dài cánh bơi (mm)',labelpad=8,loc='right')
    ax.spines[['top','right']].set_visible(False)
    for side in ['bottom','left']:ax.spines[side].set_color(p['gray-5'])
    ax.set_axisbelow(True);ax.grid(axis='y',color=p['gray-3'],linewidth=.5)
    ax.legend(loc='upper left',bbox_to_anchor=(0,-.33),frameon=False,fontsize=13,handlelength=2.5)
    fig.subplots_adjust(left=.1,right=.97,top=.97,bottom=.37)
    style_module.save(fig,out/'noi_suy_mot.svg','Dựng mốt ước lượng từ ba cột tần số',
        'Ba nhóm cùng độ rộng 5 mm, có tần số 3, 15, 10. Hai đoạn thẳng cắt nhau trong nhóm [180; 185); đường chiếu xuống trục cho mốt ước lượng khoảng 183,53 mm.')

if __name__=='__main__':build()
