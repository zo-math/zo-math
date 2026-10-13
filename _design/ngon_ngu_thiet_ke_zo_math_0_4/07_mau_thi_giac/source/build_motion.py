from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np,math,wave,json,subprocess,fitz
R=Path(__file__).resolve().parents[1];M=R/'media';A=R/'assets';SR=48000
# Locally synthesized, original cue candidates. They are never automatically played by the page.
def tone(freq,duration,gain):
 t=np.arange(int(duration*SR))/SR;env=(1-np.exp(-t/.014))*np.exp(-t/1.2)*np.minimum(1,np.maximum(0,(duration-t)/.13));return gain*env*(np.sin(2*np.pi*freq*t)+.13*np.sin(2*np.pi*freq*2*t))
def wav(name,a):
 a=np.asarray(a);pcm=np.int16(np.clip(a,-.98,.98)*32767)
 with wave.open(str(M/name),'wb') as w:w.setparams((1,2,SR,0,'NONE','not compressed'));w.writeframes(pcm.tobytes())
 return {'file':name,'duration':len(a)/SR,'sample_peak_dbfs':round(20*np.log10(max(abs(a))),2),'rms_dbfs':round(20*np.log10(np.sqrt(np.mean(a*a))),2)}
focus=tone(523.251,.65,.18);close=np.zeros(int(SR*1.1));x=tone(523.251,.60,.16);close[:len(x)]+=x;x=tone(659.255,.42,.13);j=int(.55*SR);close[j:j+len(x)]+=x
stats=[wav('cue_focus.wav',focus),wav('cue_close.wav',close)];audio=np.zeros(24*SR);audio[SR:SR+len(focus)]=focus;audio[22*SR:22*SR+len(close)]=close;wav('motion_audio.wav',audio)
# Render a real formula with LaTeX for video, not text that pretends to be math.
tex=r'''\documentclass[border=3pt]{standalone}\usepackage{fontspec,unicode-math,xcolor}\setmathfont{STIXTwoMath.ttf}[Path=../assets/]\definecolor{ink}{HTML}{3E3A35}\begin{document}\color{ink}$f(x)=x^3\quad f^{\prime}(x)=3x^2$\end{document}'''
(R/'pdf/motion_formula.tex').write_text(tex);subprocess.run(['xelatex','-interaction=nonstopmode','-halt-on-error','motion_formula.tex'],cwd=R/'pdf',stdout=subprocess.DEVNULL,check=True);d=fitz.open(R/'pdf/motion_formula.pdf');d[0].get_pixmap(matrix=fitz.Matrix(4,4),alpha=True).save(M/'motion_formula.png')
def font(n,b=False):return ImageFont.truetype(str(A/('BeVietnamPro_SemiBold.ttf' if b else 'BeVietnamPro_Regular.ttf')),int(n))
def paste(im,p,box):
 a=Image.open(R/p).convert('RGBA');a.thumbnail((int(box[2]),int(box[3])),Image.Resampling.LANCZOS);im.paste(a,(int(box[0]+(box[2]-a.width)/2),int(box[1]+(box[3]-a.height)/2)),a)
def a_value(t):
 if t<4:return -1.2
 if t<10:return -1.2+1.2*(t-4)/6
 if t<14:return 0
 if t<20:return 1.2*(t-14)/6
 return 1.2
cues=[(0,4,'Một tiếp tuyến ngang nói được điều gì?'),(4,10,'Tiến gần gốc. Hàm đang tăng.'),(10,14,'Tiếp tuyến ngang tại gốc.'),(14,20,'Đi qua gốc. Hàm vẫn tăng.'),(20,24,'Đạo hàm bằng không chưa đủ kết luận cực trị.')]
def scene(t,w,h):
 v=h>w;im=Image.new('RGB',(w,h),'#DFD7CA');d=ImageDraw.Draw(im);m=int(w*.055);d.rounded_rectangle((m,h*.04,w-m,h*.95),radius=18,fill='white');paste(im,'logos/horizontal_color.png',(w*.63,h*.065,w*.27,h*.08));d.text((w*.09,h*.09),'ZO MATH / QUAN SÁT',font=font(w*.015),fill='#766F66')
 title='Tiếp tuyến ngang.\nHàm vẫn tăng.';n=w*(.064 if v else .043)
 d.multiline_text((w*.09,h*.205 if v else h*.19),title,font=font(n,True),spacing=int(n*.18),fill='#3E3A35')
 if v:box=(w*.12,h*.40,w*.76,h*.31);fb=(w*.17,h*.345,w*.66,h*.042)
 else:box=(w*.48,h*.25,w*.43,h*.47);fb=(w*.51,h*.17,w*.36,h*.065)
 paste(im,'media/motion_formula.png',fb)
 x0,y0,bw,bh=box;cx=x0+bw/2;cy=y0+bh/2;sx=bw/3.3;sy=bh/5.3
 point=lambda x,y:(cx+x*sx,cy-y*sy)
 d.line((x0,cy,x0+bw,cy),fill='#554F48',width=2);d.line((cx,y0,cx,y0+bh),fill='#554F48',width=2)
 d.text((x0+bw-12,cy+12),'𝑥',font=ImageFont.truetype(str(A/'STIXTwoMath.ttf'),int(w*.018)),fill='#554F48');d.text((cx+12,y0),'𝑦',font=ImageFont.truetype(str(A/'STIXTwoMath.ttf'),int(w*.018)),fill='#554F48')
 # Both axes use open arrowheads and short ticks.
 for xx,yy,dx,dy in [(x0+bw,cy,-7,-5),(x0,cy,7,-5),(cx,y0,-5,7),(cx,y0+bh,-5,-7)]:
  if xx==cx:d.line((xx+dx,yy+dy,xx,yy,xx-dx,yy+dy),fill='#554F48',width=2)
  else:d.line((xx+dx,yy+dy,xx,yy,xx+dx,yy-dy),fill='#554F48',width=2)
 for val in [-1,1]:
  x,y=point(val,0);d.line((x,y-4,x,y+4),fill='#554F48',width=1);d.text((x-10,y+10),str(val),font=font(w*.013),fill='#554F48')
 for val in [-2,2]:
  x,y=point(0,val);d.line((x-4,y,x+4,y),fill='#554F48',width=1);d.text((x+10,y-8),str(val),font=font(w*.013),fill='#554F48')
 limit=-1.36+2.72*min(1,t/3)
 pts=[point(x,x**3) for x in np.linspace(-1.36,limit,200)];d.line(pts,fill='#EF5350',width=max(3,int(w*.0025)),joint='curve')
 if t>=3:
  a=a_value(t);slope=3*a*a
  for j in range(0,24,2):
   xx=a-.48+j*.04;xx2=xx+.04;pa=point(xx,a**3+slope*(xx-a));pb=point(xx2,a**3+slope*(xx2-a));d.line((*pa,*pb),fill='#554F48',width=2)
  xx,yy=point(a,a**3);rad=max(5,int(w*.004));d.ellipse((xx-rad,yy-rad,xx+rad,yy+rad),fill='#EF5350')
 cap=next(c for a,b,c in cues if a<=t<b).upper();sz=int(w*(.03 if v else .024));words=cap.split();lines=[];cur=''
 for wd in words:
  new=(cur+' '+wd).strip()
  if d.textlength(new,font=font(sz,True))>w*.74 and cur:lines.append(cur);cur=wd
  else:cur=new
 lines.append(cur);yy=h*.79;hh=len(lines)*sz*1.35+32;d.rounded_rectangle((w*.09,yy,w*.91,yy+hh),radius=9,fill='#3E3A35');d.multiline_text((w*.115,yy+13),'\n'.join(lines),font=font(sz,True),spacing=int(sz*.3),fill='#FFCA28')
 paste(im,'logos/motif.png',(w*.075,h*.90,w*.24,h*.02));return im
for orient,w,h in [('ngang',1920,1080),('doc',1080,1920)]:
 p=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{w}x{h}','-r','24','-i','pipe:0','-i',str(M/'motion_audio.wav'),'-c:v','libx264','-preset','veryfast','-crf','22','-pix_fmt','yuv420p','-c:a','aac','-t','24','-movflags','+faststart',str(M/f'motion_{orient}.mp4')],stdin=subprocess.PIPE)
 for j in range(24*24):p.stdin.write(scene(j/24,w,h).tobytes())
 p.stdin.close();assert p.wait()==0
 scene(12,w,h).save(M/f'motion_{orient}_poster.png')
 for i,t in enumerate([3,7,12,17,22]):scene(t,w,h).resize((480,270) if w>h else (270,480)).save(R/'qa'/f'motion_{orient}_{i}.png')
 print('Motion',orient,flush=True)
(M/'motion.srt').write_text('\n\n'.join(f'{i+1}\n00:00:{a:02},000 --> 00:00:{b:02},000\n{c}' for i,(a,b,c) in enumerate(cues)))
(R/'design/audio_motion.json').write_text(json.dumps({'status':'Ứng viên nghe/xem thử, chưa phải sonic identity đã duyệt','sample_rate':SR,'cues':stats,'motion_duration_seconds':24,'default':'No autoplay; no sound on hover; controls always visible','sound_semantics':'Open/close a listening segment; never label correct/incorrect answers','animation_semantics':'Point (a,a³) and tangent slope 3a²; 4 second hold at origin','timing':cues,'web_reduced_motion':'Discrete steps at -1.1, 0, 1.1'},ensure_ascii=False,indent=2))
