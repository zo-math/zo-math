from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,math,subprocess,wave,numpy as np
R=Path(__file__).resolve().parents[1];A=R/'assets';M=R/'media';S=R/'social';PAPER='#FBFAF8';INK='#3E3A35';DARK='#25221F';RED='#EF5350';YELLOW='#FFCA28'
def f(n,b=False):return ImageFont.truetype(str(A/('BeVietnamPro_SemiBold.ttf' if b else 'BeVietnamPro_Regular.ttf')),int(n))
def wrap(s,font,width):
 d=ImageDraw.Draw(Image.new('RGB',(1,1)));out=[];line=''
 for word in s.split():
  a=(line+' '+word).strip()
  if d.textlength(a,font=font)>width and line:out.append(line);line=word
  else:line=a
 if line:out.append(line)
 return out
def text(im,s,x,y,width,n=40,c=INK,b=False,leading=1.3):
 d=ImageDraw.Draw(im)
 for para in s.split('\n'):
  for line in wrap(para,f(n,b),width):d.text((int(x),int(y)),line,font=f(n,b),fill=c);y+=n*leading
 return y
def pic(im,p,box):
 a=Image.open(R/p).convert('RGBA');k=min(box[2]/a.width,box[3]/a.height);a=a.resize((max(1,round(a.width*k)),max(1,round(a.height*k))),Image.Resampling.LANCZOS);im.paste(a,(round(box[0]+(box[2]-a.width)/2),round(box[1]+(box[3]-a.height)/2)),a)
def logo(im,w,h,dark=False):pic(im,'logos/horizontal_color'+('_dark' if dark else '')+'.png',(w*.66,h*.04,w*.25,h*.08))
def motif(im,w,h,y=.91):pic(im,'logos/motif.png',(w*.07,h*y,w*.26,h*.035))
def cover(kind,w,h):
 v=h>w;dark=kind=='back';bg=DARK if dark else ('#FFE9A9' if kind=='thumbnail' else PAPER);im=Image.new('RGB',(w,h),bg);d=ImageDraw.Draw(im);m=w*.075;logo(im,w,h,dark);ink=PAPER if dark else INK
 text(im,'HÀM SỐ / 01',m,h*.055,w*.52,w*.017,ink)
 if kind=='back':
  text(im,'Tiếp tuyến ngang.\nHàm vẫn tăng.',m,h*.28,w*.82,w*(.082 if v else .055),ink,True,1.32)
  text(im,'Đạo hàm bằng không chưa đủ\nđể kết luận cực trị.',m,h*.63,w*.76,w*(.032 if v else .027),'#DFD7CA')
  text(im,'Biên soạn và biên tập: ZO Math',m,h*.84,w*.8,w*.018,'#C7BEB2');motif(im,w,h);return im
 if v:
  y=text(im,'Tiếp tuyến ngang.\nHàm vẫn tăng.' if kind=='thumbnail' else 'Một tiếp tuyến ngang\nnói được điều gì?',m,h*.20,w*.84,w*.073,INK,True,1.28)
  pic(im,'graphics/cubic.png',(m,y+h*.06,w*.85,min(h*.33,h*.77-y-h*.06)))
  text(im,'Quan sát hình, rồi kiểm bằng lập luận.',m,h*.83,w*.78,w*.027);motif(im,w,h)
 else:
  text(im,'Tiếp tuyến\nngang.\nHàm vẫn tăng.' if kind=='thumbnail' else 'Tiếp tuyến ngang\ncó đủ để kết luận\ncực trị?',m,h*.24,w*.43,w*.042,INK,True,1.3)
  pic(im,'graphics/cubic.png',(w*.53,h*.22,w*.42,h*.55))
  text(im,'Quan sát hình, rồi kiểm bằng lập luận.',m,h*.82,w*.74,w*.021);motif(im,w,h)
 return im
records=[]
for orient,w,h in [('doc',1080,1920),('ngang',1920,1080)]:
 for k,label in [('thumbnail','Ảnh thu nhỏ'),('front','Bìa trước'),('back','Bìa sau')]:
  id=f'video_{orient}_{k}';cover(k,w,h).save(S/(id+'.png'));records.append({'id':id,'size':[w,h],'title':label+' · '+orient,'why':{'thumbnail':'yellow-2 tạo một trường nhận diện lớn; tiêu đề và đường cong cùng dẫn vào một ý. Logo giữ vị trí góc trên, dấu nhấn giữ chân bố cục.','front':'Đặt câu hỏi trước, dùng nền giấy cho mạch học. Khoảng trống chia vùng tiêu đề và biểu diễn, không đóng thêm hộp quanh mọi thành phần.','back':'Nền gray-9 đánh dấu kết thúc; chữ sáng trả lời câu hỏi, hai màu thương hiệu tập trung ở logo và dấu nhấn. Giảm chữ phụ để không cạnh tranh kết luận.'}[k]})
for id,w,h,title,desc in [('the_hoc_truoc',1080,1080,'Đạo hàm bằng 0.\nEm kết luận gì?','Thử nghĩ trước khi mở thẻ sau.'),('the_hoc_sau',1080,1080,'Một điều kiện.\nChưa đủ kết luận.','Hàm x³ tăng qua gốc dù đạo hàm ở đó bằng 0.'),('chia_se',1200,630,'Tiếp tuyến ngang.\nHàm vẫn tăng.','ZO Math · Đọc đúng biểu diễn.'),('bia_bai_hoc',1600,900,'Đơn điệu\nvà cực trị','Đọc đúng biểu diễn. Giữ đủ điều kiện.')]:
 im=Image.new('RGB',(w,h),'#FFF9E9' if id.endswith('sau') else PAPER);logo(im,w,h);text(im,'ZO MATH / HÀM SỐ',w*.07,h*.055,w*.5,w*.018);n=w*.052 if w==h else w*.043;text(im,title,w*.07,h*.24,w*.84 if w==h else w*.48,n,INK,True)
 pic(im,'graphics/cubic.png',(w*.38,h*.49 if w==h else h*.26,w*.54,h*.28 if w==h else h*.48));text(im,desc,w*.07,h*.83,w*.84,w*.021);motif(im,w,h);im.save(S/(id+'.png'));records.append({'id':id,'size':[w,h],'title':id.replace('_',' '),'why':'Cùng hệ lề, vị trí logo, vai trò tiêu đề và dấu nhấn. Thẻ trước hỏi, thẻ sau giải thích; bìa bài đặt tên chủ đề. Các phần không cùng tăng kích thước chỉ để lấp chỗ trống.'})
(R/'design/distribution.json').write_text(json.dumps(records,ensure_ascii=False,indent=2))
# Reuse the offline narration to compare visual design without changing the spoken experiment.
items=json.loads((M/'timing.json').read_text());caps=json.loads((M/'captions.json').read_text());total=items[-1]['end'];keys=['graphics/cubic.png','tables/bbt03.png','graphics/cubic.png','graphics/disconnected.png','graphics/inverse.png','graphics/geometry_3d.png','graphics/cubic.png']
def frame(t,w,h):
 if t<3:return cover('front',w,h)
 if t>=total+3:return cover('back',w,h)
 t-=3;im=Image.new('RGB',(w,h),PAPER);logo(im,w,h);i=next((j for j,it in enumerate(items) if it['start']<=t<it['end']),6);m=w*.07;v=h>w
 text(im,f'HÀM SỐ / {i+1:02}',m,h*.055,w*.48,w*.017)
 y=text(im,items[i]['title'],m,h*.18,w*.85,w*(.057 if v else .035),INK,True)
 pic(im,keys[i],(m,y+h*.04,w*.86,max(100,h*.72-y-h*.04)));motif(im,w,h,.745)
 cap=next((c['text'].upper() for c in caps if c['start']<=t<c['end']),'')
 if cap:
  sz=int(w*(.034 if v else .023));lines=wrap(cap,f(sz,True),w*.81)
  while len(lines)>2:sz-=1;lines=wrap(cap,f(sz,True),w*.81)
  yy=h*.825;hh=len(lines)*sz*1.4+36;ImageDraw.Draw(im).rounded_rectangle((m,yy,w*.93,yy+hh),radius=9,fill=DARK);text(im,'\n'.join(lines),m+22,yy+14,w*.81,sz,YELLOW,True,1.4)
 return im
with wave.open(str(M/'narration.wav')) as z:a=np.frombuffer(z.readframes(z.getnframes()),dtype='<i2')
with wave.open(str(M/'sonic_candidate.wav')) as z:sonic=np.frombuffer(z.readframes(z.getnframes()),dtype='<i2')
audio=np.r_[np.zeros(144000,dtype=np.int16),a,np.zeros(144000,dtype=np.int16)];pos=144000+len(a)+12000;audio[pos:pos+len(sonic)]=sonic
with wave.open(str(M/'video_audio.wav'),'wb') as z:z.setparams((1,2,48000,0,'NONE','not compressed'));z.writeframes(audio.astype('<i2').tobytes())
for orient,w,h in [('ngang',1920,1080),('doc',1080,1920)]:
 out=M/f'video_{orient}.mp4';p=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{w}x{h}','-r','12','-i','pipe:0','-i',str(M/'video_audio.wav'),'-c:v','libx264','-preset','veryfast','-crf','22','-pix_fmt','yuv420p','-c:a','aac','-shortest','-movflags','+faststart',str(out)],stdin=subprocess.PIPE)
 for j in range(math.ceil((total+6)*12)):
  if j%3==0:buf=frame(j/12,w,h).tobytes()
  p.stdin.write(buf)
 p.stdin.close();assert p.wait()==0
 for k,t in enumerate([1]+[3+(i['start']+i['end'])/2 for i in items]+[total+4]):frame(t,w,h).resize((480,270) if w>h else (270,480)).save(R/'qa'/f'video_{orient}_{k:02}.png')
 print('video',orient,flush=True)
