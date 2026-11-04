"""Exercise scheduled-video errors, retries and public transition with a fake YouTube API.

The real page and video.js run in Edge; only YouTube is replaced. This is a
simulation of API events, not evidence that a scheduled video is public.
"""
from pathlib import Path
import argparse,functools,json,socket,subprocess,tempfile,threading,time
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
import requests
from zo_web_2027_check import Browser,edge_executable
from zo_publish_videos import PAGE

ROOT=Path(__file__).resolve().parents[1]
FAKE="""
window.testPlayers=[];
window.YT={PlayerState:{PLAYING:1},Player:function(frame,options){
  this.frame=frame;this.options=options;this.destroyed=false;
  this.destroy=()=>{this.destroyed=true;frame.remove()};
  window.testPlayers.push(this);
}};
"""
API_FAILURE="""
const append=Element.prototype.append;
Element.prototype.append=function(...nodes){
  for(const node of nodes){
    if(node.src==='https://www.youtube.com/iframe_api'){
      queueMicrotask(()=>node.dispatchEvent(new Event('error')));
    }else append.call(this,node);
  }
};
"""

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,required=True)
    parser.add_argument('--report',type=Path,required=True)
    args=parser.parse_args();out=args.report.resolve().parent
    if not out.is_relative_to(ROOT/'_audit'):parser.error('Report must be within audit')
    out.mkdir(parents=True,exist_ok=True);checks={};error=None
    class Quiet(SimpleHTTPRequestHandler):
        def log_message(self,*args):pass
    server=ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(args.root.resolve())))
    threading.Thread(target=server.serve_forever,daemon=True).start()
    url=f'http://127.0.0.1:{server.server_port}/'+PAGE
    def test(name,value):checks[name]=bool(value);print(('PASS ' if value else 'FAIL ')+name,flush=True)
    with socket.socket() as sock:sock.bind(('127.0.0.1',0));port=sock.getsockname()[1]
    with tempfile.TemporaryDirectory(prefix='state-check-',dir=out,ignore_cleanup_errors=True) as profile:
        proc=subprocess.Popen([edge_executable(),'--headless=new','--disable-gpu','--no-first-run','--no-default-browser-check',f'--remote-debugging-port={port}','--remote-debugging-address=127.0.0.1','--remote-allow-origins=http://localhost','--user-data-dir='+profile,'about:blank'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
        b=None
        try:
            endpoint=f'http://127.0.0.1:{port}'
            for _ in range(100):
                try:
                    if requests.get(endpoint+'/json/version',timeout=.3).ok:break
                except requests.RequestException:time.sleep(.1)
            target=requests.put(endpoint+'/json/new?about:blank',timeout=10).json();b=Browser(target['webSocketDebuggerUrl'])
            b.call('Page.enable');b.call('Runtime.enable');b.call('Network.enable')
            b.call('Network.setBlockedURLs',{'urls':['*youtube.com*','*youtube-nocookie.com*']})
            fake=b.call('Page.addScriptToEvaluateOnNewDocument',{'source':FAKE})['identifier']
            b.viewport(390,844);b.navigate(url+'#bai-hoc')
            test('closed scheduled blocks do not contact YouTube',b.evaluate('testPlayers.length===0&&!document.querySelector(".zo-learning-video iframe")'))
            b.navigate(url+'#video-l05');time.sleep(.2)
            test('scheduled disclosure opens a real YouTube iframe',b.evaluate('testPlayers.length===1&&document.querySelector("#video-l05 iframe").src.includes("Ec4Y_drZlv0")'))
            test('all scheduled videos are inside matching solutions',b.evaluate('document.querySelectorAll(".zo-learning-video[data-scheduled-at]").length===5&&[...document.querySelectorAll(".zo-learning-video[data-scheduled-at]")].every(n=>n.closest(".zo-learning-solution"))'))
            for code in [100,101,150,153]:
                b.evaluate(f'testPlayers.at(-1).options.events.onError({{data:{code}}})')
                test(f'YouTube error {code} explained with retry',b.evaluate('(()=>{const n=document.querySelector("#video-l05");return !n.querySelector(".zo-video-status").hidden&&n.querySelector(".zo-video-status").textContent.includes("chưa cho phát")&&!n.querySelector(".zo-video-retry").hidden})()'))
            test('mobile scheduled video fits',b.evaluate('document.documentElement.scrollWidth<=innerWidth+1'))
            b.screenshot(out/'unavailable-mobile.png')
            b.click('#video-l05 .zo-video-retry')
            test('retry replaces stale iframe with the same ID',b.evaluate('testPlayers.length===2&&testPlayers[0].destroyed&&testPlayers[0].frame!==testPlayers[1].frame&&testPlayers[1].frame.src.includes("Ec4Y_drZlv0")'))
            b.evaluate('testPlayers[1].options.events.onStateChange({data:1})')
            test('public playback hides unavailable notice and retry',b.evaluate('document.querySelector("#video-l05 .zo-video-status").hidden&&document.querySelector("#video-l05 .zo-video-retry").hidden'))
            b.evaluate('testPlayers[0].options.events.onError({data:100})')
            test('stale player error cannot overwrite public state',b.evaluate('document.querySelector("#video-l05 .zo-video-status").hidden'))
            b.evaluate('document.querySelector("#video-l05").open=false');time.sleep(.2)
            test('closing destroys player',b.evaluate('testPlayers[1].destroyed&&!document.querySelector("#video-l05 iframe")'))
            b.evaluate('document.querySelector("#video-l05").open=true');time.sleep(.2)
            test('reopening rechecks YouTube without a date gate',b.evaluate('testPlayers.length===3&&testPlayers[2].frame.src.includes("Ec4Y_drZlv0")'))
            b.click('a[data-view="bai-hoc"]')
            test('view change destroys scheduled player',b.evaluate('testPlayers[2].destroyed&&!document.querySelector(".zo-learning-video iframe")'))
            b.call('Page.removeScriptToEvaluateOnNewDocument',{'identifier':fake})
            b.call('Page.addScriptToEvaluateOnNewDocument',{'source':API_FAILURE})
            b.navigate(url+'?video-state-case=api-error#video-l05');time.sleep(.3)
            test('API failure retains iframe, fallback and truthful status',b.evaluate('(()=>{const n=document.querySelector("#video-l05");return !!n.querySelector("iframe")&&!!n.querySelector("a[href*=Ec4Y_drZlv0]")&&n.querySelector(".zo-video-status").textContent.includes("Chưa kiểm tra được")})()'))
        except Exception as exc:error=str(exc);print(error,flush=True)
        finally:
            if b:
                try:b.call('Browser.close')
                except Exception:pass
                b.ws.close()
            try:proc.wait(timeout=10)
            except subprocess.TimeoutExpired:proc.terminate();proc.wait(timeout=10)
            server.shutdown()
    args.report.write_bytes(json.dumps(dict(simulated_youtube_api=True,checks=checks,passed=sum(checks.values()),total=len(checks),error=error),ensure_ascii=False,indent=2).encode())
    return int(bool(error) or not checks or not all(checks.values()))
if __name__=='__main__':raise SystemExit(main())
