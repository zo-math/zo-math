"""Browser QA of the video-only candidate or live page in an isolated Edge profile."""
from pathlib import Path
import argparse,functools,json,socket,subprocess,tempfile,threading,time
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
import requests
from zo_web_2027_check import Browser,edge_executable
from zo_publish_videos import PAGE,PACKAGE

ROOT=Path(__file__).resolve().parents[1]
def main():
    parser=argparse.ArgumentParser(description=__doc__)
    target=parser.add_mutually_exclusive_group(required=True)
    target.add_argument('--root',type=Path);target.add_argument('--url')
    parser.add_argument('--report',type=Path,required=True);parser.add_argument('--playback',action='store_true')
    args=parser.parse_args();out=args.report.resolve().parent
    if not out.is_relative_to(ROOT/'_audit'):parser.error('Report must be in this repository audit directory')
    out.mkdir(parents=True,exist_ok=True)
    mapping=json.loads((ROOT/PACKAGE/'_quy_trinh/ho_so/videos_20261104_mapping.json').read_text('utf-8'))
    server=None;checks={};playback=[];scheduled=[];error=None
    class Quiet(SimpleHTTPRequestHandler):
        def log_message(self,*args):pass
    if args.root:
        server=ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(args.root.resolve())))
        threading.Thread(target=server.serve_forever,daemon=True).start()
        url=f'http://127.0.0.1:{server.server_port}/'+PAGE
    else:url=args.url
    def test(name,value):
        checks[name]=bool(value);print(('PASS ' if value else 'FAIL ')+name,flush=True)
    with socket.socket() as sock:sock.bind(('127.0.0.1',0));port=sock.getsockname()[1]
    with tempfile.TemporaryDirectory(prefix='video-check-',dir=out,ignore_cleanup_errors=True) as profile:
        proc=subprocess.Popen([edge_executable(),'--headless=new','--disable-gpu','--no-first-run','--no-default-browser-check',f'--remote-debugging-port={port}','--remote-debugging-address=127.0.0.1','--remote-allow-origins=http://localhost','--user-data-dir='+profile,'about:blank'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
        b=None
        try:
            endpoint=f'http://127.0.0.1:{port}'
            for _ in range(100):
                try:
                    if requests.get(endpoint+'/json/version',timeout=.3).ok:break
                except requests.RequestException:time.sleep(.1)
            target=requests.put(endpoint+'/json/new?about:blank',timeout=10).json();b=Browser(target['webSocketDebuggerUrl']);b.call('Page.enable');b.call('Runtime.enable')
            for width in [1440,390,430]:
                b.viewport(width,1080 if width>500 else 844);b.navigate(url+'#bai-hoc')
                test(f'{width}: all videos initially closed',b.evaluate('document.querySelectorAll(".zo-learning-video").length==='+str(len(mapping))+'&&!document.querySelector(".zo-learning-video[open],.zo-learning-video iframe")'))
                test(f'{width}: page fits',b.evaluate('document.documentElement.scrollWidth<=innerWidth+1'))
                b.evaluate('document.querySelector("#video-h01 summary").focus()');b.key('Enter',13,'\r')
                test(f'{width}: keyboard opens player',b.evaluate('!!document.querySelector("#video-h01 iframe[title]")'))
                test(f'{width}: portrait fits',b.evaluate('(()=>{const r=document.querySelector("#video-h01 iframe").getBoundingClientRect();return r.width>100&&r.right<=innerWidth&&Math.abs(r.height/r.width-16/9)<.02})()'))
                b.evaluate('document.querySelector("#video-h01").scrollIntoView({block:"start"})');time.sleep(3)
                b.screenshot(out/f'video-{width}.png');b.key('Enter',13,'\r')
                test(f'{width}: close stops player',b.evaluate('!document.querySelector("#video-h01 iframe")'))
            b.viewport(1440,1080)
            for item in mapping:
                ident='video-'+item['code'].lower();b.navigate(url+'#'+ident);time.sleep(.2)
                test(ident+': iframe and fallback',b.evaluate('(()=>{const n=document.getElementById('+json.dumps(ident)+'),f=n.querySelector("iframe");return !!f&&f.src.includes('+json.dumps(item['video_id'])+')&&!!n.querySelector("a[target=_blank]")})()'))
                if item.get('availability',{}).get('status')=='scheduled_at_review':
                    notice=b.evaluate('document.querySelector('+json.dumps('#'+ident+' .zo-video-status')+').textContent')
                    test(ident+': schedule and YouTube authority disclosed','YouTube' in notice and ('Lịch công khai dự kiến' in notice or 'chưa cho phát' in notice))
                    if args.playback:
                        for _ in range(20):
                            time.sleep(1)
                            notice=b.evaluate('document.querySelector('+json.dumps('#'+ident+' .zo-video-status')+').textContent')
                            if 'YouTube chưa cho phát' in notice:break
                        unavailable='YouTube chưa cho phát' in notice
                        scheduled.append(dict(code=item['code'],video_id=item['video_id'],unavailable_reported=unavailable,notice=notice))
                        test(ident+': actual unavailable response explained',unavailable)
                    b.screenshot(out/(ident+'.png'))
                elif args.playback:
                    time.sleep(3);frame=next((t for t in b.call('Target.getTargets')['targetInfos'] if t['type']=='iframe' and item['video_id'] in t['url']),None)
                    record=dict(code=item['code'],video_id=item['video_id'],played=False)
                    if frame:
                        session=b.call('Target.attachToTarget',{'targetId':frame['targetId'],'flatten':True})['sessionId']
                        def evaluate(code):
                            b.counter+=1;request_id=b.counter;b.ws.send(json.dumps(dict(id=request_id,sessionId=session,method='Runtime.evaluate',params=dict(expression=code,returnByValue=True))))
                            while True:
                                msg=json.loads(b.ws.recv())
                                if msg.get('id')==request_id:return msg.get('result',{}).get('result',{}).get('value')
                        point=b.evaluate('(()=>{const r=document.querySelector('+json.dumps('#'+ident+' iframe')+').getBoundingClientRect();return {x:r.x+r.width/2,y:r.y+r.height/2}})()')
                        for kind in ['mousePressed','mouseReleased']:b.call('Input.dispatchMouseEvent',dict(type=kind,button='left',clickCount=1,**point))
                        state=None
                        for _ in range(6):
                            time.sleep(2);state=evaluate('(()=>{const v=document.querySelector("video");return {title:document.title,paused:v?.paused,time:v?.currentTime,ready:v?.readyState,error:v?.error?.message}})()')
                            if state and state.get('time',0)>.1 and not state.get('paused'):break
                        record.update(state or {});record['played']=bool(state and state.get('time',0)>.1 and not state.get('paused'))
                    playback.append(record);test(ident+': actual playback',record['played'])
                if item['code'] in ['H01','L04','n-dt-01']:b.screenshot(out/(ident+'.png'))
                b.evaluate('document.querySelectorAll(".zo-learning-video").forEach(n=>n.open=false)');time.sleep(.1)
            b.navigate(url+'#video-h01');b.click('a[data-view="phieu-luyen"]')
            test('view change stops hidden video',b.evaluate('!document.querySelector(".zo-learning-video iframe")'))
            b.navigate(url+'#tu-kiem-tra');test('no video in test',b.evaluate('!document.querySelector("#tu-kiem-tra .zo-learning-video")'))
            b.click('a[data-view="bai-hoc"]');test('test support gate retained',b.evaluate('document.querySelector("#support-gate").open'))
            b.call('Emulation.setScriptExecutionDisabled',{'value':True});b.call('Page.navigate',{'url':url});time.sleep(1)
            test('no JS: all fallback links retained',b.evaluate('document.querySelectorAll(".zo-learning-video a[href^=\\"https://www.youtube.com/shorts/\\"]").length==='+str(len(mapping))))
        except Exception as exc:error=str(exc);print(error,flush=True)
        finally:
            if b:
                try:b.call('Browser.close')
                except Exception:pass
                b.ws.close()
            try:proc.wait(timeout=10)
            except subprocess.TimeoutExpired:proc.terminate();proc.wait(timeout=10)
            if server:server.shutdown()
    args.report.write_text(json.dumps(dict(url=url,checks=checks,passed=sum(checks.values()),total=len(checks),playback=playback,scheduled=scheduled,error=error),ensure_ascii=False,indent=2),encoding='utf-8')
    return int(bool(error) or not checks or not all(checks.values()))
if __name__=='__main__':raise SystemExit(main())
