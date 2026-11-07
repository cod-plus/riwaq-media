"""Vertical 1080x1920 clip for TikTok / Instagram Reels: hook over the store photo -> live demo on a phone -> RIWAQ call to action.
make_clip(spec, outdir) -> {"video": ..., "cover": ...}"""
import os, json, shutil, subprocess
from playwright.sync_api import sync_playwright
from common import (INK, GOLD, SAND, NIGHT, STORES, font_css, svg, esc, demo_img, file_url, launch, SITE_URL, WA_TEXT)
import capture, sound

FPS = 30
T1, DEMO = 2.4, 8.2                      # hook length, demo length
T2 = T1 + DEMO                           # CTA starts
TOTAL = T2 + 3.4

SCENE = """<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><style>
%(fonts)s
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1920px;overflow:hidden;background:%(NIGHT)s}
body{font-family:"IBM Plex Sans Arabic",sans-serif;-webkit-font-smoothing:antialiased}
.layer{position:absolute;inset:0;overflow:hidden}
#hero{position:absolute;inset:-2%%;width:104%%;height:104%%;object-fit:cover;transform-origin:50%% 60%%}
.shade{position:absolute;inset:0;background:linear-gradient(180deg,rgba(15,34,40,.94) 0%%,rgba(15,34,40,.82) 34%%,rgba(15,34,40,.25) 64%%,rgba(15,34,40,.6) 100%%)}
.htext{position:absolute;top:210px;right:100px;left:90px;color:%(SAND)s;display:flex;flex-direction:column;gap:26px}
.tag{align-self:flex-start;display:flex;align-items:center;gap:14px;background:rgba(244,238,227,.12);border:2px solid rgba(200,150,62,.75);
     color:%(SAND)s;border-radius:999px;padding:10px 26px 10px 30px;font-size:32px;font-weight:600}
.tag svg{height:40px;width:auto}
.hk{font-size:64px;font-weight:600;color:%(GOLD)s;line-height:1.25}
.hl{font-size:106px;font-weight:700;line-height:1.2}
.hl .ln{display:block}
.hl em{font-style:normal;color:%(GOLD)s}
#demo{background:radial-gradient(90%% 60%% at 70%% 10%%,#1B3E49 0%%,%(NIGHT)s 60%%)}
.dtop{position:absolute;top:150px;right:110px;left:90px;color:%(SAND)s;display:flex;flex-direction:column;gap:14px}
.sname{font-size:56px;font-weight:700}
.sname small{font-size:38px;font-weight:500;opacity:.7}
.feat{font-size:44px;font-weight:600;color:%(GOLD)s;line-height:1.35}
.phone{position:absolute;left:284px;top:430px;width:512px;padding:16px;border-radius:84px;background:#0A0A0A;
       box-shadow:0 0 0 3px #2b3a3f,0 50px 120px rgba(0,0,0,.55)}
.screen{position:relative;border-radius:68px;overflow:hidden;background:%(sbg)s}
.status{height:42px;display:flex;justify-content:space-between;align-items:center;padding:0 40px;font:600 19px "IBM Plex Sans Arabic";color:%(sink)s;direction:ltr}
.island{position:absolute;top:10px;left:50%%;transform:translateX(-50%%);width:120px;height:32px;border-radius:20px;background:#000}
#scr{display:block;width:480px;height:1039px;object-fit:cover;object-position:top}
#cta{background:%(SAND)s;color:%(INK)s;display:flex;flex-direction:column;align-items:center;text-align:center;padding:0 150px;justify-content:center;gap:34px}
#cta .emb svg{width:300px;height:auto}
#cta h2{font-size:84px;font-weight:700;line-height:1.22}
#cta .wa{font-size:52px;font-weight:600;line-height:1.3}
#cta .sub{font-size:40px;font-weight:500;opacity:.78;line-height:1.45}
#cta .url{background:%(NIGHT)s;color:%(SAND)s;border-radius:999px;padding:20px 48px;font-size:42px;font-weight:600;direction:ltr;letter-spacing:.5px}
.u{display:block;will-change:transform,opacity}
</style></head><body>
<div id="hook" class="layer"><img id="hero" src="%(hero)s"><div class="shade"></div>
 <div class="htext"><div class="tag u" id="tag">%(emblem_small)s<span>%(tag)s</span></div>
  <div class="hk u" id="hk">%(kicker)s</div><div class="hl" id="hl">%(lines)s</div></div></div>
<div id="demo" class="layer" style="opacity:0">
 <div class="dtop"><div class="sname u" id="sname">%(sname)s <small>· %(scat)s</small></div><div class="feat u" id="feat">%(feat)s</div></div>
 <div class="phone u" id="phone"><div class="screen"><div class="island"></div><div class="status"><span>9:41</span><span>&#9679;&#9679;&#9679;</span></div><img id="scr"></div></div>
</div>
<div id="cta" class="layer" style="clip-path:circle(0px at 50%% 100%%)">
 <div class="emb u" id="emb">%(emblem)s</div><h2 class="u" id="c1">%(cta_title)s</h2>
 <div class="wa u" id="c2">%(wa)s</div><div class="sub u" id="c3">%(cta_sub)s</div><div class="url u" id="c4">%(url)s</div>
</div>
<script>
const T1=%(T1)s, T2=%(T2)s, FPS=%(FPS)s, FR=%(frames)s;
const $=id=>document.getElementById(id), C=(a,b,t)=>Math.max(0,Math.min(1,(t-a)/(b-a)));
const E=x=>{x=Math.max(0,Math.min(1,x));return x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2};
const O=x=>1-Math.pow(1-Math.max(0,Math.min(1,x)),3);
function show(el,p,dy){el.style.opacity=p;el.style.transform=`translateY(${(1-p)*dy}px)`}
let cur=-1;
function seek(t){
  const h=1-C(T1,T1+.3,t); $('hook').style.opacity=h;
  $('hero').style.transform=`scale(${1.13-0.1*E(t/T1)})`;
  show($('tag'),1,0); show($('hk'),1,0);
  [...document.querySelectorAll('#hl .ln')].forEach((l,i)=>{const p=O(C(i*.12,.32+i*.12,t));l.style.opacity=.55+.45*p;l.style.transform=`translateY(${(1-p)*26}px)`});
  const d=C(T1,T1+.3,t)*(1-C(T2+.45,T2+.5,t)); $('demo').style.opacity=d;
  $('phone').style.transform=`translateY(${(1-E(C(T1,T1+.6,t)))*300}px)`;
  show($('sname'),O(C(T1+.15,T1+.5,t)),30); show($('feat'),O(C(T1+.5,T1+.9,t)),30);
  const r=E(C(T2,T2+.5,t))*2300; $('cta').style.clipPath=`circle(${r}px at 50%% 100%%)`;
  const es=O(C(T2+.15,T2+.65,t)); $('emb').style.opacity=es; $('emb').style.transform=`scale(${.82+.18*es})`;
  ['c1','c2','c3','c4'].forEach((id,i)=>show($(id),O(C(T2+.35+i*.18,T2+.75+i*.18,t)),36));
  const k=Math.max(0,Math.min(FR.length-1,Math.floor((t-T1)*FPS)));
  if(k!==cur && FR.length){cur=k;const im=$('scr');im.src=FR[k];return im.decode().catch(()=>0)}
  return Promise.resolve(1);
}
</script></body></html>"""

def scene_html(spec, frames):
    st = STORES.get(spec["store"], {})
    hero = spec.get("hero") or (demo_img(spec["store"], st.get("hero", "hero.webp")) if st.get("hero") else "")
    lines = "".join(f'<span class="ln">{l}</span>' for l in spec["lines"])
    dark_store = st.get("bg", "#fff").lower() in ("#100c09", "#5e0e1c", "#120b08")
    return SCENE % dict(
        fonts=font_css(), NIGHT=NIGHT, SAND=SAND, INK=INK, GOLD=GOLD, hero=hero,
        tag=esc(spec.get("tag", "متجر من رواق")), kicker=esc(spec["kicker"]), lines=lines,
        emblem_small=svg("riwaq-emblem-white.svg"), emblem=svg("riwaq-emblem.svg"),
        sname=esc(spec.get("sname", st.get("name", ""))), scat=esc(spec.get("scat", st.get("cat", ""))),
        feat=esc(spec.get("feat", st.get("feat", ""))), sbg=st.get("bg", "#fff"), sink="#fff" if dark_store else "#111",
        cta_title=esc(spec.get("cta_title", "متجرك الجاي يكون بهويتك")), wa=esc(spec.get("wa", WA_TEXT)),
        cta_sub=esc(spec.get("cta_sub", "ونسوي لك نموذج مجاني قبل ما تدفع شي")),
        url=esc(spec.get("url", f"{SITE_URL}/{spec['store']}")),
        T1=T1, T2=T2, FPS=FPS, frames=json.dumps([file_url(f) for f in frames]))

def make_clip(spec, outdir, keep_frames=False):
    os.makedirs(outdir, exist_ok=True)
    work = os.path.join(outdir, ".work"); os.makedirs(work, exist_ok=True)
    shots = capture.capture(spec["store"], os.path.join(work, "screen"), DEMO,
                            page=spec.get("page"), acts=spec.get("acts"))
    html_p = os.path.join(work, "scene.html")
    open(html_p, "w", encoding="utf-8").write(scene_html(spec, shots))
    fdir = os.path.join(work, "frames"); os.makedirs(fdir, exist_ok=True)
    n = int(round(TOTAL * FPS)); cover = os.path.join(outdir, "cover.jpg")
    with sync_playwright() as p:
        b = launch(p)
        pg = b.new_context(viewport={"width": 1080, "height": 1920}, device_scale_factor=1).new_page()
        pg.goto(file_url(html_p)); pg.evaluate("document.fonts.ready.then(()=>1)"); pg.wait_for_timeout(300)
        for f in range(n):
            pg.evaluate("t => seek(t)", f / FPS)
            pg.screenshot(path=os.path.join(fdir, "f%05d.jpg" % f), type="jpeg", quality=90)
        pg.evaluate("t => seek(t)", 1.2); pg.screenshot(path=cover, type="jpeg", quality=92)
        b.close()
    wav = sound.make(os.path.join(work, "music.wav"), TOTAL, T1, T2, seed=spec.get("seed", 3))
    video = os.path.join(outdir, "clip.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(fdir, "f%05d.jpg"), "-i", wav,
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p", "-r", str(FPS),
                    "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", video], check=True)
    if not keep_frames: shutil.rmtree(work, ignore_errors=True)
    return {"video": video, "cover": cover}

if __name__ == "__main__":
    import sys
    spec = json.load(open(sys.argv[1], encoding="utf-8"))
    print(make_clip(spec["clip"], sys.argv[2], keep_frames="--keep" in sys.argv))
