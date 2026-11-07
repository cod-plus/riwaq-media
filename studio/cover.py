"""Cover / hook composition shared by carousels (slide 1) and clips (opening scene).
A full-bleed store photo, the RIWAQ logo, a gold kicker and a big headline — all kept inside the centre 3:4 and 4:5 crops that
TikTok and Instagram use for grid thumbnails, so the cover reads in the feed, in the profile grid and as a video poster."""
from common import INK, GOLD, SAND, NIGHT, svg, esc

# geometry per canvas (1080 wide): logo top, text top, kicker/headline/sub sizes, foot bottom
GEO = {
    (1080, 1920): dict(ltop=300, ttop=470, kfs=48, hfs=116, sfs=42, fbot=330, gap=30),
    (1080, 1350): dict(ltop=84, ttop=215, kfs=42, hfs=100, sfs=38, fbot=84, gap=24),
}

CSS = """
.cv{position:relative;width:%(W)dpx;height:%(H)dpx;overflow:hidden;background:%(NIGHT)s;color:%(SAND)s;font-family:"IBM Plex Sans Arabic",sans-serif;direction:rtl}
.cv-bg{position:absolute;inset:0}
.cv-bg img{width:100%%;height:100%%;object-fit:cover;object-position:%(focus)s;transform:scale(1.05);transform-origin:50%% 60%%}
.cv-shade{position:absolute;inset:0;background:linear-gradient(180deg,rgba(15,34,40,.94) 0%%,rgba(15,34,40,.88) 34%%,rgba(15,34,40,.46) 54%%,rgba(15,34,40,.10) 74%%,rgba(15,34,40,.66) 100%%)}
.cv-logo{position:absolute;top:%(ltop)dpx;right:64px;height:96px}.cv-logo svg{height:96px;width:auto}
.cv-pg{position:absolute;top:%(pgtop)dpx;left:90px;font-size:28px;font-weight:500;opacity:.6}
.cv-txt{position:absolute;top:%(ttop)dpx;right:90px;left:90px;display:flex;flex-direction:column;gap:%(gap)dpx;align-items:flex-start}
.cv-k{display:inline-flex;align-items:center;gap:14px;color:%(GOLD)s;font-size:%(kfs)dpx;font-weight:600}
.cv-k:before{content:"";width:16px;height:16px;border-radius:50%%;background:%(GOLD)s}
.cv-h{font-size:%(hfs)dpx;font-weight:700;line-height:1.16;letter-spacing:0}
.cv-h .ln{display:block;white-space:nowrap}
.cv-h em{font-style:normal;color:%(GOLD)s}
.cv-s{font-size:%(sfs)dpx;font-weight:500;line-height:1.5;opacity:.9;max-width:880px}
.cv-foot{position:absolute;bottom:%(fbot)dpx;right:90px;left:90px;display:flex;justify-content:space-between;align-items:center}
.cv-pill{display:inline-flex;align-items:center;gap:12px;background:rgba(244,238,227,.14);border:1.5px solid rgba(244,238,227,.4);border-radius:999px;padding:12px 30px;font-size:32px;font-weight:600;-webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px)}
.cv-pill.gold{background:%(GOLD)s;border-color:%(GOLD)s;color:%(NIGHT)s}
.cv-handle{font-size:28px;font-weight:500;opacity:.8;direction:ltr}
.u{will-change:transform,opacity}
"""
FIT_JS = """() => { document.querySelectorAll('.cv-h').forEach(h => { const box = h.getBoundingClientRect().width;
  h.querySelectorAll('.ln').forEach(l => { let fs = parseFloat(getComputedStyle(h).fontSize); l.style.fontSize = '';
    while (l.scrollWidth > box && fs > 72) { fs -= 4; l.style.fontSize = fs + 'px'; } }); }); return 1; }"""

def css(W, H, focus="50% 62%"):
    g = GEO[(W, H)]
    return CSS % dict(W=W, H=H, NIGHT=NIGHT, SAND=SAND, GOLD=GOLD, focus=focus, pgtop=g["ltop"] + 34, **g)

def body(c, pg=None, foot=None):
    """c: photo (url), kicker, lines (list of html), sub (optional). pg: '1/6' label. foot: ('swipe'|'try', text)."""
    lines = "".join(f'<span class="ln u">{l}</span>' for l in c["lines"])
    sub = f'<div class="cv-s u">{c["sub"]}</div>' if c.get("sub") else ""
    pgl = f'<div class="cv-pg">{esc(pg)}</div>' if pg else ""
    if foot == "swipe":
        ft = '<div class="cv-pill">اسحب <span style="font-size:36px;line-height:1">&larr;</span></div>'
    elif foot:
        ft = f'<div class="cv-pill gold u" id="cvpill">{esc(foot)}</div>'
    else:
        ft = "<span></span>"
    return (f'<div class="cv-bg"><img id="cvimg" src="{c["photo"]}"></div><div class="cv-shade"></div>'
            f'<div class="cv-logo">{svg("riwaq-horizontal-dark-transparent.svg")}</div>{pgl}'
            f'<div class="cv-txt"><div class="cv-k u">{esc(c["kicker"])}</div><div class="cv-h">{lines}</div>{sub}</div>'
            f'<div class="cv-foot">{ft}<span class="cv-handle">@riwaquae</span></div>')
