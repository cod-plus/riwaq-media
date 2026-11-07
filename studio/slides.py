"""Carousel slides in the RIWAQ identity, rendered with Playwright.
render_carousel(slides, outdir) -> {"ig": [...jpg 1080x1350], "tt": [...jpg 1080x1920]}"""
import os
from playwright.sync_api import sync_playwright
from common import (INK, GOLD, SAND, NIGHT, font_css, svg, arch_path, esc, demo_img, file_url, launch, WA_TEXT, SITE_URL, BRAND)
import cover

SIZES = {"ig": (1080, 1350), "tt": (1080, 1920)}
CHECK = f'<svg class="chk" viewBox="0 0 24 24"><path d="M4 12.5l5 5L20 6.5" fill="none" stroke="{GOLD}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>'

def arch_img(src, w, h, stroke=None, pad=10):
    """An image cut in the RIWAQ door shape, with an optional thin outline arch around it."""
    W, H = w + 2 * pad, h + 2 * pad
    clip = arch_path(w, h, pad, pad)
    outline = f'<path d="{arch_path(W - 2, H - 2, 1, 1)}" fill="none" stroke="{stroke}" stroke-width="2.5"/>' if stroke else ""
    cid = "c%x" % (abs(hash((src, w, h))) % 0xFFFFFF)
    body = (f'<image href="{src}" x="{pad}" y="{pad}" width="{w}" height="{h}" preserveAspectRatio="xMidYMid slice" clip-path="url(#{cid})"/>'
            if src else f'<path d="{clip}" fill="{GOLD}"/>')
    return (f'<svg class="arch" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><defs><clipPath id="{cid}"><path d="{clip}"/></clipPath></defs>'
            f'{body}{outline}</svg>')

def door_num(n, w=128, h=168):
    return (f'<div class="num"><svg width="{w}" height="{h}" viewBox="0 0 {w} {h}"><path d="{arch_path(w, h)}" fill="{GOLD}"/></svg>'
            f'<b>{esc(n)}</b></div>')

def _imgs(srcs, W, kind):
    srcs = [s for s in srcs if s]
    if not srcs: return ""
    n = len(srcs)
    if kind == "tt":
        w = {1: 560, 2: 380, 3: 270}[min(n, 3)]
    else:
        w = {1: 470, 2: 330, 3: 250}[min(n, 3)]
    h = int(w * 1.32)
    return '<div class="imgs">' + "".join(arch_img(s, w, h, stroke=GOLD) for s in srcs[:3]) + "</div>"

def _src(ref):
    """'batla/hero.webp' -> demo store image; absolute paths pass through."""
    if not ref: return ""
    if os.path.isabs(ref): return file_url(ref)
    slug, name = ref.split("/", 1)
    return demo_img(slug, name)

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:%(W)dpx;height:%(H)dpx;overflow:hidden}
body{font-family:"IBM Plex Sans Arabic",sans-serif;direction:rtl;-webkit-font-smoothing:antialiased;text-rendering:geometricPrecision}
.s{position:relative;width:%(W)dpx;height:%(H)dpx;overflow:hidden;display:flex;flex-direction:column;
   padding:%(pt)dpx %(pr)dpx %(pb)dpx %(pl)dpx}
.dark{background:radial-gradient(120%% 80%% at 80%% 0%%,#173640 0%%,%(NIGHT)s 55%%) ;color:%(SAND)s}
.sand{background:%(SAND)s;color:%(INK)s}
.deco{position:absolute;left:50%%;transform:translateX(-50%%);bottom:-%(decoOff)dpx;opacity:.07;pointer-events:none;z-index:0}
.top,.mid,.imgs,.phwrap,.foot{position:relative;z-index:1}
.top{display:flex;justify-content:space-between;align-items:center;height:92px;flex:none}
.logo{height:92px}.logo svg{height:92px;width:auto;margin-right:-22px}
.cta-h{font-size:%(ctah)dpx}
.pg{font-size:28px;font-weight:500;opacity:.55;letter-spacing:.5px}
.mid{flex:1;display:flex;flex-direction:column;justify-content:center;gap:%(gap)dpx}
.kicker{font-size:%(kfs)dpx;font-weight:600;color:%(GOLD)s}
.sand .kicker{color:%(INK)s;display:inline-flex;align-items:center;gap:14px}
.sand .kicker:before{content:"";width:42px;height:6px;border-radius:3px;background:%(GOLD)s}
h1{font-size:%(h1)dpx;font-weight:700;line-height:1.24;letter-spacing:0}
h1 em{font-style:normal;color:%(GOLD)s}
.sand h1 em{color:%(INK)s;background:linear-gradient(transparent 62%%,rgba(200,150,62,.45) 62%%)}
.body{font-size:%(bfs)dpx;font-weight:400;line-height:1.62;opacity:.86}
.body b{font-weight:600;opacity:1}
.imgs{display:flex;justify-content:center;align-items:flex-end;gap:26px;flex:none}
.num{position:relative;width:128px;height:168px;flex:none}
.num b{position:absolute;inset:auto 0 18px 0;text-align:center;font-size:72px;font-weight:700;color:%(NIGHT)s;line-height:1}
.foot{display:flex;justify-content:space-between;align-items:center;height:64px;flex:none;font-size:28px;font-weight:500;opacity:.7}
.foot .em svg{height:44px;width:auto}
.swipe{display:flex;align-items:center;gap:10px;font-weight:600;opacity:.85}
ul{list-style:none;display:flex;flex-direction:column;gap:%(lig)dpx}
li{display:flex;align-items:flex-start;gap:18px;font-size:%(lfs)dpx;line-height:1.45;font-weight:500}
.chk{width:%(lfs)dpx;height:%(lfs)dpx;flex:none;margin-top:6px}
.price{display:flex;align-items:baseline;gap:18px}
.price b{font-size:%(pfs)dpx;font-weight:700;line-height:1;font-family:"IBM Plex Sans Arabic";direction:ltr}
.price span{font-size:%(ufs)dpx;font-weight:600;opacity:.8}
.note{font-size:%(nfs)dpx;font-weight:500;opacity:.75;line-height:1.5}
.pill{align-self:flex-start;background:%(GOLD)s;color:%(NIGHT)s;font-weight:700;font-size:%(pillfs)dpx;padding:22px 44px;border-radius:999px}
.url{font-size:%(urlfs)dpx;font-weight:600;direction:ltr;letter-spacing:1px;opacity:.9}
.cta .mid{align-items:center;text-align:center}
.cta .pill{align-self:center}
.emblem svg{width:%(emw)dpx;height:auto}
.tag{align-self:flex-start;border:2px solid currentColor;border-radius:999px;padding:8px 26px;font-size:28px;font-weight:600;opacity:.8}
.phonely .mid{flex:none;justify-content:flex-start;padding-top:%(phtop)dpx}
.phwrap{flex:1;min-height:0;display:flex;justify-content:center;align-items:flex-start;overflow:hidden;margin:0 -%(pl)dpx -%(pb)dpx -%(pr)dpx;padding-top:44px}
.ph{width:%(phw)dpx;padding:15px;border-radius:76px;background:#0A0A0A;box-shadow:0 0 0 3px rgba(0,0,0,.12),0 40px 90px rgba(0,0,0,.35);flex:none}
.dark .ph{box-shadow:0 0 0 3px #2b3a3f,0 40px 90px rgba(0,0,0,.5)}
.ph-scr{border-radius:62px;overflow:hidden;background:#fff}
.ph-scr img{display:block;width:100%%}
.phonely .num{width:100px;height:131px}.phonely .num svg{width:100px;height:131px}.phonely .num b{font-size:56px;bottom:14px}
"""

def _css(W, H, kind):
    tt = kind == "tt"
    p = dict(W=W, H=H, INK=INK, GOLD=GOLD, SAND=SAND, NIGHT=NIGHT,
             pt=280 if tt else 70, pb=400 if tt else 64, pr=170 if tt else 90, pl=90,
             gap=40 if tt else 30, kfs=38 if tt else 34, h1=92 if tt else 84, bfs=44 if tt else 40,
             lig=26 if tt else 20, lfs=40 if tt else 36, pfs=150 if tt else 136, ufs=50 if tt else 46,
             nfs=36 if tt else 32, pillfs=42 if tt else 38, urlfs=40 if tt else 36, emw=230 if tt else 200, ctah=76 if tt else 70,
             phw=600 if tt else 500, phtop=40 if tt else 24,
             decoOff=260 if tt else 330)
    return CSS % p

def _logo(theme):
    return svg("riwaq-horizontal-dark-transparent.svg" if theme == "dark" else "riwaq-horizontal-transparent.svg")

def photo_hook_html(s, i, n, kind):
    """Slide 1 as a cover: full-bleed store photo + headline (see cover.py)."""
    W, H = SIZES[kind]
    c = dict(photo=_src(s["photo"]), kicker=s.get("kicker", ""), lines=s["lines"], sub=s.get("body", ""))
    return (f'<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><style>{font_css()}'
            f'*{{box-sizing:border-box;margin:0;padding:0}}html,body{{width:{W}px;height:{H}px;overflow:hidden}}'
            f'body{{-webkit-font-smoothing:antialiased}}{cover.css(W, H, s.get("focus", "50% 62%"))}</style></head>'
            f'<body><div class="cv">{cover.body(c, pg=f"{i}/{n}", foot="swipe")}</div></body></html>')

def slide_html(s, i, n, kind):
    if s["t"] == "hook" and s.get("photo"):
        return photo_hook_html(s, i, n, kind)
    W, H = SIZES[kind]
    theme = s.get("theme", "dark" if s["t"] in ("hook", "cta") else "sand")
    deco_w = 900 if kind == "tt" else 820
    deco = (f'<svg class="deco" width="{deco_w}" height="{int(deco_w*1.25)}" viewBox="0 0 {deco_w} {int(deco_w*1.25)}">'
            f'<path d="{arch_path(deco_w - 8, int(deco_w*1.25) - 8, 4, 4)}" fill="none" stroke="{SAND if theme == "dark" else INK}" stroke-width="7"/></svg>')
    top = f'<div class="top"><div class="logo">{_logo(theme)}</div><div class="pg">{i}/{n}</div></div>'
    swipe = '<div class="swipe">اسحب <span style="font-size:34px">&larr;</span></div>' if s["t"] == "hook" else ""
    foot = f'<div class="foot"><span dir="ltr">@riwaquae</span>{swipe}</div>'
    k = f'<div class="kicker">{esc(s["kicker"])}</div>' if s.get("kicker") else ""
    title = s.get("title", "")
    h1 = f"<h1>{title}</h1>" if title else ""                      # title may carry <em> / <br>
    body = f'<div class="body">{s["body"]}</div>' if s.get("body") else ""
    imgs = _imgs([_src(r) for r in s.get("imgs", [])], W, kind)
    t = s["t"]
    phone = (f'<div class="phwrap"><div class="ph"><div class="ph-scr"><img src="{file_url(s["phone_img"])}"></div></div></div>'
             if s.get("phone_img") else "")
    if phone:
        foot = ""
    if t == "hook":
        mid = f'<div class="mid">{k}{h1}{body}</div>{phone or imgs}'
    elif t == "phone":
        num = door_num(s["num"]) if s.get("num") else ""
        mid = f'<div class="mid">{num}{k}{h1}{body}</div>{phone}'
    elif t == "point":
        num = door_num(s["num"]) if s.get("num") else ""
        mid = f'<div class="mid">{num}{k}{h1}{body}</div>{imgs}'
    elif t == "list":
        lis = "".join(f"<li>{CHECK}<span>{b}</span></li>" for b in s.get("bullets", []))
        mid = f'<div class="mid">{k}{h1}<ul>{lis}</ul>{body}</div>{imgs}'
    elif t == "price":
        lis = "".join(f"<li>{CHECK}<span>{b}</span></li>" for b in s.get("bullets", []))
        price = f'<div class="price"><b>{esc(s["price"])}</b><span>{esc(s.get("unit", "د.إ"))}</span></div>'
        note = f'<div class="note">{s["note"]}</div>' if s.get("note") else ""
        mid = f'<div class="mid">{k}{h1}{price}{note}<ul>{lis}</ul></div>'
    elif t == "cta":
        em = f'<div class="emblem">{svg("riwaq-emblem-white.svg") if theme == "dark" else svg("riwaq-emblem.svg")}</div>'
        ttl = s.get("title") or "أرسل كلمة «متجر»<br>على الواتساب"
        sub = s.get("body") or "ونسوي لك نموذج مجاني لمتجرك قبل ما تدفع شي"
        mid = (f'<div class="mid">{em}<h1 class="cta-h">{ttl}</h1><div class="body">{sub}</div>'
               f'<div class="pill">{esc(s.get("pill", "الرابط في البايو"))}</div><div class="url">{SITE_URL}</div></div>')
    else:
        raise ValueError(t)
    cls = f"s {theme}" + (" cta" if t == "cta" else "") + (" phonely" if phone else "")
    return (f'<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><style>{font_css()}{_css(W, H, kind)}</style></head>'
            f'<body><div class="{cls}">{deco}{top}{mid}{foot}</div></body></html>')

def render_carousel(slides, outdir, kinds=("ig", "tt"), tag=""):
    os.makedirs(outdir, exist_ok=True)
    src = os.path.join(outdir, ".src"); os.makedirs(src, exist_ok=True)
    out = {k: [] for k in kinds}
    with sync_playwright() as p:
        b = launch(p)
        for kind in kinds:
            W, H = SIZES[kind]
            pg = b.new_context(viewport={"width": W, "height": H}, device_scale_factor=1).new_page()
            for i, s in enumerate(slides, 1):
                f = os.path.join(src, f"{kind}-{i:02d}.html")
                open(f, "w", encoding="utf-8").write(slide_html(s, i, len(slides), kind))
                pg.goto(file_url(f)); pg.evaluate("document.fonts.ready.then(()=>1)"); pg.wait_for_timeout(150)
                pg.evaluate(cover.FIT_JS); pg.wait_for_timeout(40)
                img = os.path.join(outdir, f"{kind}-{i:02d}{tag}.jpg")
                pg.screenshot(path=img, type="jpeg", quality=92); out[kind].append(img)
            pg.context.close()
        b.close()
    return out

if __name__ == "__main__":
    import json, sys
    spec = json.load(open(sys.argv[1], encoding="utf-8"))
    print(render_carousel(spec["slides"], sys.argv[2]))
