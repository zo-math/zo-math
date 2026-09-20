"""Bộ dựng hình R1-G01 v1.1. Chạy từ bất kì thư mục nào: python zo_bieu_dien.py.
Đồ thị dùng công thức chính xác; bảng dùng dữ liệu tường minh, không suy đoán ô thiếu.
"""
from pathlib import Path
import json, re
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import fontManager
from matplotlib.patches import FancyBboxPatch

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'hinh'; OUT.mkdir(exist_ok=True)
PALETTE=dict(background='#fff9e9',border='#dfd7ca',axis='#554f48',text='#3e3a35',main='#ef5350',second='#bf4240',ref='#997918',highlight='#ffca28')
for f in (ROOT/'hinh'/'fonts').glob('*.ttf'):fontManager.addfont(str(f))
plt.rcParams.update({'font.family':'STIX Two Text','font.size':12,'mathtext.fontset':'stix','svg.fonttype':'path','axes.unicode_minus':True,'text.color':PALETTE['text']})

def canvas(n=1):
 fig,axs=plt.subplots(1,n,figsize=(8.8,4.5) if n==1 else (11.5,4.9),squeeze=False)
 fig.subplots_adjust(left=.07,right=.98,bottom=.12,top=.83,wspace=.20)
 return fig,list(axs[0])

def axis(ax,xlim,ylim,title,xticks=None,yticks=None):
 ax.set(xlim=xlim,ylim=ylim)
 ax.set_facecolor(PALETTE['background'])
 for spine in ax.spines.values():spine.set_visible(False)
 # A rounded field; axes cross at the origin and have two arrowheads.
 ax.add_patch(FancyBboxPatch((0,0),1,1,boxstyle='round,pad=0.008,rounding_size=0.025',transform=ax.transAxes,fill=False,ec=PALETTE['border'],lw=.8,clip_on=False))
 for which in ['left','bottom']:
  ax.spines[which].set_position('zero');ax.spines[which].set_visible(True);ax.spines[which].set_color(PALETTE['axis']);ax.spines[which].set_linewidth(.7)
 ax.annotate('',xy=(xlim[1],0),xytext=(xlim[0],0),arrowprops=dict(arrowstyle='<->',color=PALETTE['axis'],lw=.8),annotation_clip=False)
 ax.annotate('',xy=(0,ylim[1]),xytext=(0,ylim[0]),arrowprops=dict(arrowstyle='<->',color=PALETTE['axis'],lw=.8),annotation_clip=False)
 ax.text(.99,(0-ylim[0])/(ylim[1]-ylim[0])+.04,'$x$',transform=ax.transAxes,ha='right')
 ax.text((0-xlim[0])/(xlim[1]-xlim[0])+.03,.99,'$y$',transform=ax.transAxes,va='top')
 ax.tick_params(colors=PALETTE['axis'],width=.6,length=3,labelsize=10,pad=3)
 if xticks is not None:ax.set_xticks([v for v in xticks if v!=0])
 if yticks is not None:ax.set_yticks([v for v in yticks if v!=0])
 ax.annotate('O',(0,0),xytext=(-12,-13),textcoords='offset points',fontsize=10)
 ax.set_title(title,loc='left',pad=16,fontsize=13)

def curve(ax,fn,xlim,label,color='main',ls='-'):
 x=np.linspace(*xlim,1601); ax.plot(x,fn(x),color=PALETTE[color],lw=1.4 if color=='main' else 1.1,label=label,ls=ls)
def point(ax,x,y,label='',offset=(8,10),opened=False):
 ax.plot(x,y,'o',ms=5,mec=PALETTE['second'],mfc=PALETTE['background'] if opened else PALETTE['second'],mew=1.2,zorder=6)
 if label:ax.annotate(label,(x,y),xytext=offset,textcoords='offset points',fontsize=11,color=PALETTE['text'],bbox=dict(fc=PALETTE['background'],ec='none',pad=1,alpha=.95))
def legend(ax):
 ax.legend(loc='upper right',fontsize=10,framealpha=1,facecolor='white',edgecolor=PALETTE['border'],handlelength=1.9)
def save(fig,name):
 for ext in ['svg','png']:fig.savefig(OUT/f'{name}.{ext}',dpi=150,facecolor='white',bbox_inches='tight')
 svg_path=OUT/f'{name}.svg'
 svg='\n'.join(line.rstrip() for line in svg_path.read_text(encoding='utf-8').splitlines())+'\n'
 with svg_path.open('w',encoding='utf-8',newline='\n') as stream:stream.write(svg)
 plt.close(fig)

def graphs():
 fig,(ax,)=canvas();axis(ax,(-1.4,3.4),(-3,8),'Tiếp tuyến ngang và hàm số đồng biến',range(-1,4),[-2,2,4,6])
 curve(ax,lambda x:(x-1)**3+2,(-1.4,3.4),'$y=(x-1)^3+2$');ax.plot([-.2,2.5],[2,2],ls='--',color=PALETTE['ref'],lw=.9,label='Tiếp tuyến $y=2$');point(ax,1,2,'(1; 2)',(10,-25));legend(ax);save(fig,'do_thi_01')
 fig,(ax,)=canvas();axis(ax,(-2.5,2.5),(-7,9),'Từ bảng biến thiên đến đồ thị',range(-2,3),[-6,-3,3,6])
 curve(ax,lambda x:x**3-3*x+1,(-2.5,2.5),'$y=p(x)=x^3-3x+1$')
 for x,y,l,o in [(-1,3,'A(−1; 3)',(-72,13)),(1,-1,'B(1; −1)',(10,-25)),(0,1,'C(0; 1)',(12,12))]:point(ax,x,y,l,o)
 legend(ax);save(fig,'do_thi_02')
 for name,shift,base in [('do_thi_03',0,0),('do_thi_09',-1,-2)]:
  fig,axs=canvas(2)
  for i,ax in enumerate(axs):
   axis(ax,(-3.5,2.5),(-3,4),'Giữ điểm tại mốc' if i==0 else 'Loại điểm tại mốc',[-3,-2,-1,1,2],[-2,-1,1,2,3])
   curve(ax,lambda x:np.abs(x-shift)+base,(-3.5,2.5),'$y=u(x)$' if i==0 else '$y=v(x)$')
   point(ax,shift,base,f'({shift}; {base})',(12,-20),opened=i==1);legend(ax)
  save(fig,name)
 fig,axs=canvas(2)
 for i,ax in enumerate(axs):
  axis(ax,(-.6,2.6),(-3,4),'Đồ thị hàm số' if i==0 else 'Đồ thị đạo hàm',[1,2],[-2,-1,1,2,3]);ax.axvspan(0,1,color=PALETTE['highlight'],alpha=.2)
  curve(ax,(lambda x:x*x-2*x) if i==0 else (lambda x:2*x-2),(-.6,2.6),'$y=s(x)=x^2-2x$' if i==0 else r"$y=s^{\prime}(x)=2x-2$");legend(ax)
 save(fig,'do_thi_04')
 fig,(ax,)=canvas();axis(ax,(-1.5,1.5),(-4,4),'Hai hàm số có cùng bảng biến thiên tóm tắt',[-1,1],[-3,-2,-1,1,2,3])
 curve(ax,lambda x:x**3,(-1.5,1.5),'$y=x^3$');curve(ax,lambda x:2*x**3,(-1.5,1.5),'$y=2x^3$','second','--');point(ax,1,1,'(1; 1)',(12,-17));point(ax,1,2,'(1; 2)',(-62,12));legend(ax);save(fig,'do_thi_05')
 fig,axs=canvas(2)
 for i,ax in enumerate(axs):
  axis(ax,(-.5,4.5),(-5,7),'Hình A' if i==0 else 'Hình B',[1,2,3,4],[-4,-2,2,4,6])
  curve(ax,lambda x:(1 if i==0 else -1)*(x**3-6*x*x+9*x-1),(-.5,4.5),'Đường biểu diễn')
  for x,y in [(1,3*(1 if i==0 else -1)),(3,-1*(1 if i==0 else -1))]:point(ax,x,y,f'({x}; {y})',(6,12) if y>0 else (6,-24))
  legend(ax)
 save(fig,'do_thi_06')
 fig,(ax,)=canvas();axis(ax,(-3,2.8),(-12,13),'Đọc dấu từ đồ thị đạo hàm',[-2,-1,1,2],[-10,-5,5,10]);curve(ax,lambda x:(x+2)*(x-1)**2,(-3,2.8),r"$y=h^{\prime}(x)$")
 point(ax,-2,0,'(−2; 0)',(-55,-30));point(ax,1,0,'(1; 0)',(7,13));legend(ax);save(fig,'do_thi_07')
 fig,(ax,)=canvas();axis(ax,(-4.25,3.25),(-2.5,7),'Đồ thị đạo hàm trên khoảng (−4; 3)',[-4,-3,-2,-1,1,2,3],[-2,2,4,6]);curve(ax,lambda x:.05*(x+3)*(x+1)*(x-2)**2,(-3.9999,2.9999),r"$y=k^{\prime}(x)$")
 for x,o in [(-3,(-49,-30)),(-1,(5,-30)),(2,(-16,15))]:point(ax,x,0,f'({x}; 0)',o)
 legend(ax);save(fig,'do_thi_08')
 fig,(ax,)=canvas();axis(ax,(-3,5.5),(-23,33),'Đồ thị để đối chiếu bài kiểm tra 01',[-2,-1,1,2,3,4,5],[-20,-10,10,20,30]);curve(ax,lambda x:-x**3+3*x*x+9*x-4,(-3,5.5),'$y=-x^3+3x^2+9x-4$');point(ax,-1,-9,'(−1; −9)',(10,-23));point(ax,3,23,'(3; 23)',(-71,13));legend(ax);save(fig,'do_thi_10')

if __name__=='__main__':graphs();print('Đã dựng 10 đồ thị theo bảng màu ZO Math.')
