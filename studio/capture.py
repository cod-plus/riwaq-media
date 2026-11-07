"""Scripted phone-screen capture of a RIWAQ demo store (riwaq-site-/public/demos/<slug>/), deterministic, frame by frame.
capture(slug, outdir, seconds) -> list of jpg frames (390x844 CSS px @2x)."""
import os, math, threading, functools
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from playwright.sync_api import sync_playwright
from common import DEMOS, SITE, font_css, launch

_SRV = {}
def site_url(path):
    """Serve riwaq-site-/public over localhost (the demos use root-relative /demos/... image paths)."""
    if "port" not in _SRV:
        class Quiet(SimpleHTTPRequestHandler):
            def log_message(self, *a, **k): pass
        h = functools.partial(Quiet, directory=os.path.join(SITE, "public"))
        srv = ThreadingHTTPServer(("127.0.0.1", 0), h)
        threading.Thread(target=srv.serve_forever, daemon=True).start()
        _SRV.update(port=srv.server_address[1], srv=srv)
    return f"http://127.0.0.1:{_SRV['port']}{path}"

FPS = 30
BASE_CSS = ("*,*::before,*::after{transition:none!important;animation:none!important;scroll-behavior:auto!important}"
            "html{scroll-behavior:auto!important}.rq-fab{display:none!important}.rq-toast{display:none!important}")

# (kind, t0, ...) — scroll: t0,t1,target | jump: t0,target | click: t0,selector | type: t0,t1,selector,text | range: t0,t1,selector,v0,v1
# targets: CSS selector, absolute y (number) or "+N" (relative to the current position)
_INTRO = [("scroll", 0.5, 2.3, "#shop"), ("scroll", 2.6, 3.6, "+420")]
ACTS = {
    "batla": _INTRO + [("jump", 3.9, "#build"), ("click", 4.3, '[data-btf="1"]'), ("type", 4.8, 6.6, "#btMsg", "كل عام وأنتِ بخير يا أمي")],
    "qand": _INTRO + [("jump", 3.9, "#design"), ("click", 4.3, '[data-qdf="1"]'), ("click", 4.9, '[data-qdd="1"]'),
                      ("click", 5.5, '[data-qds="3"]'), ("click", 6.1, '[data-qdf="3"]'), ("click", 6.7, '[data-qdd="0"]')],
    "lujain": _INTRO + [("jump", 3.9, "#size"), ("range", 4.3, 7.0, "#ljH", 150, 174)],
    "hail": _INTRO + [("jump", 3.9, "#box"), ("click", 4.0, "[data-hlclear]")] +
            [("click", 4.25 + i * 0.22, f'[data-hlp="{v}"]') for i, v in enumerate(
                ["medjool", "almond", "pista", "orange", "sukkari", "medjool", "almond", "pista", "orange", "sukkari", "medjool", "almond"])],
    "yaqoot": _INTRO + [("jump", 3.9, "#engrave"), ("type", 4.2, 5.4, "#yqName", "مريم"), ("click", 5.8, '[data-yqm="1"]'), ("click", 6.4, '[data-yqf="1"]')],
    "nabd": [("scroll", 0.3, 1.3, 260), ("click", 1.6, '[data-nbdev="ip16p"]'), ("scroll", 2.0, 3.4, "#shop"),
             ("jump", 3.9, "#bundle"), ("click", 4.4, '[data-nbpick="p8"]'), ("click", 5.0, '[data-nbpick="p6"]')],
    "abaq": _INTRO + [("jump", 3.9, "#finder"), ("click", 4.4, '[data-abq="who"][data-v="gift"]'),
                      ("click", 5.1, '[data-abq="when"][data-v="night"]'), ("click", 5.8, '[data-abq="fam"][data-v="amber"]')],
    "taas": _INTRO + [("jump", 3.9, "#pressure"), ("click", 4.4, 'label[for="t-road"]'), ("click", 5.2, 'label[for="t-gravel"]'),
                      ("click", 6.0, 'label[for="t-sand"]')],
    "eclore": [("scroll", 0.5, 2.6, 900), ("scroll", 3.0, 5.0, 1900), ("scroll", 5.4, 7.4, 3000)],
    "admin": [("scroll", 1.0, 2.6, 520), ("scroll", 3.4, 5.0, 1150), ("scroll", 5.8, 7.4, 1800)],
}

def ease(x):
    x = max(0.0, min(1.0, x)); return 4 * x ** 3 if x < 0.5 else 1 - (-2 * x + 2) ** 3 / 2

def _target(pg, tgt, cur):
    if isinstance(tgt, (int, float)): return float(tgt)
    if isinstance(tgt, str) and tgt.startswith("+"): return cur + float(tgt[1:])
    return pg.evaluate("""s => { const e = document.querySelector(s); if (!e) return 0;
        const top = document.querySelector('.rq-top, .hdr, header'); const off = top ? Math.min(top.getBoundingClientRect().height, 90) : 60;
        return Math.max(0, e.getBoundingClientRect().top + scrollY - off + 4); }""", tgt)

def capture(slug, outdir, seconds=8.2, page=None, acts=None, quality=88):
    url = ("file://" + page) if page else site_url(f"/demos/{slug}/")
    acts = sorted(acts if acts is not None else ACTS.get(slug, _INTRO), key=lambda a: a[1])
    os.makedirs(outdir, exist_ok=True)
    n = int(round(seconds * FPS)); files = []
    pos = [a for a in acts if a[0] in ("scroll", "jump")]
    other = [a for a in acts if a[0] not in ("scroll", "jump")]
    with sync_playwright() as p:
        b = launch(p)
        ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True, has_touch=True)
        pg = ctx.new_page()
        pg.route("**/fonts.g*.com/**", lambda r: r.abort())
        pg.goto(url, wait_until="load"); pg.wait_for_timeout(400)
        pg.add_style_tag(content=font_css() + BASE_CSS)
        pg.evaluate("document.querySelectorAll('img[loading=lazy]').forEach(i => i.loading = 'eager')")
        pg.evaluate("document.fonts.ready.then(()=>1)")
        pg.evaluate("async () => { const H = document.body.scrollHeight; for (let y = 0; y < H; y += 700) { scrollTo(0, y); await new Promise(r => setTimeout(r, 30)); } }")
        pg.evaluate("Promise.all([...document.images].map(i => i.complete ? 1 : i.decode().catch(() => 0)))")
        pg.wait_for_timeout(300)
        pg.evaluate("scrollTo(0,0)"); pg.wait_for_timeout(150)
        done, resolved, y = set(), {}, 0.0
        for f in range(n):
            t = f / FPS
            for i, a in enumerate(other):
                kind, t0 = a[0], a[1]
                if t < t0: continue
                if kind == "click" and i not in done:
                    pg.evaluate("s => { const e = document.querySelector(s); if (e) e.click(); }", a[2]); done.add(i)
                elif kind == "type":
                    t1, sel, text = a[2], a[3], a[4]
                    k = len(text) if t >= t1 else int(math.ceil(len(text) * (t - t0) / (t1 - t0)))
                    pg.evaluate("a => { const e = document.querySelector(a[0]); if (!e) return; if (e.value !== a[1]) { e.value = a[1]; e.dispatchEvent(new Event('input', {bubbles:true})); } }", [sel, text[:k]])
                elif kind == "range":
                    t1, sel, v0, v1 = a[2], a[3], a[4], a[5]
                    v = round(v0 + (v1 - v0) * ease((t - t0) / (t1 - t0)))
                    pg.evaluate("a => { const e = document.querySelector(a[0]); if (!e) return; if (String(e.value) !== String(a[1])) { e.value = a[1]; e.dispatchEvent(new Event('input', {bubbles:true})); } }", [sel, v])
            last = None
            for j, a in enumerate(pos):
                if t >= a[1]: last = j
            if last is not None:
                a = pos[last]
                if last not in resolved:
                    resolved[last] = (y, _target(pg, a[2] if a[0] == "jump" else a[3], y))
                frm, to = resolved[last]
                y = to if a[0] == "jump" else frm + (to - frm) * ease((t - a[1]) / (a[2] - a[1]))
            pg.evaluate("y => scrollTo(0, y)", y)
            fp = os.path.join(outdir, "f%04d.jpg" % f)
            pg.screenshot(path=fp, type="jpeg", quality=quality); files.append(fp)
        b.close()
    return files

ADMIN_SHOTS = {   # dashboard demo (/demos/admin/) still screens: name -> JS run before the screenshot
    "home": "",
    "orders": "document.querySelector('[data-tab=\"orders\"]').click()",
    "order": "document.querySelector('[data-tab=\"orders\"]').click(); setTimeout(() => document.querySelector('#orders .order').click(), 60)",
    "add": ("document.querySelector('[data-tab=\"products\"]').click(); setTimeout(() => { document.querySelector('#fab').click();"
            " setTimeout(() => { const v = {aName: 'باقة الفاونيا الوردية', aPrice: '450', aStock: '8'};"
            " for (const k in v) { const e = document.getElementById(k); if (e) { e.value = v[k]; e.dispatchEvent(new Event('input', {bubbles: true})); } } }, 80) }, 60)"),
    "store": "document.querySelector('[data-tab=\"store\"]').click()",
}

def stills(slug, outdir, shots=None, path=None):
    """Still phone screenshots of a demo page (390x844 @2x). shots: name -> JS. Returns name -> jpg."""
    shots = shots or (ADMIN_SHOTS if slug == "admin" else {"top": ""})
    url = site_url(path or f"/demos/{slug}/")
    os.makedirs(outdir, exist_ok=True); out = {}
    with sync_playwright() as p:
        b = launch(p)
        for name, js in shots.items():
            ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True, has_touch=True)
            pg = ctx.new_page(); pg.route("**/fonts.g*.com/**", lambda r: r.abort())
            pg.goto(url, wait_until="load"); pg.wait_for_timeout(400)
            pg.add_style_tag(content=font_css() + BASE_CSS)
            pg.evaluate("document.fonts.ready.then(()=>1)")
            if js: pg.evaluate(js); pg.wait_for_timeout(500)
            pg.evaluate("Promise.all([...document.images].map(i => i.complete ? 1 : i.decode().catch(() => 0)))")
            f = os.path.join(outdir, f"{name}.jpg"); pg.screenshot(path=f, type="jpeg", quality=92); out[name] = f
            ctx.close()
        b.close()
    return out

if __name__ == "__main__":
    import sys
    fs = capture(sys.argv[1], sys.argv[2], float(sys.argv[3]) if len(sys.argv) > 3 else 8.2)
    print(len(fs), "frames")
