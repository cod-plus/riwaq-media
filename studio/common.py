"""Shared bits for the RIWAQ social studio: brand, fonts, paths, the arch shape, and Playwright helpers."""
import os, math, html

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)                                   # riwaq-media checkout
SITE = os.environ.get("RIWAQ_SITE", os.path.join(os.path.dirname(REPO), "riwaq-site-"))  # riwaq-site- checkout
DEMOS = os.path.join(SITE, "public", "demos")
FONTS = os.path.join(HERE, "fonts")
BRAND = os.path.join(HERE, "brand")
RAW = "https://raw.githubusercontent.com/cod-plus/riwaq-media/main/"

# brand (src/brand/kit/README-ar.txt in riwaq-site-)
INK, GOLD, SAND, NIGHT = "#142B33", "#C8963E", "#F4EEE3", "#0F2228"
WA_TEXT = "أرسل كلمة «متجر» على الواتساب"
SITE_URL = "riwaquae.com"

# family -> [(file, weight-range, style)]
_FACES = {
    "IBM Plex Sans Arabic": [("IBMPlexSansArabic-Light.ttf", "300", "normal"), ("IBMPlexSansArabic-Regular.ttf", "400", "normal"),
                             ("IBMPlexSansArabic-Medium.ttf", "500", "normal"), ("IBMPlexSansArabic-SemiBold.ttf", "600", "normal"),
                             ("IBMPlexSansArabic-Bold.ttf", "700", "normal")],
    "Amiri": [("Amiri-Regular.ttf", "400", "normal"), ("Amiri-Bold.ttf", "700", "normal")],
    "Aref Ruqaa": [("ArefRuqaa-Regular.ttf", "400", "normal"), ("ArefRuqaa-Bold.ttf", "700", "normal")],
    "Cormorant Garamond": [("CormorantGaramond.ttf", "300 700", "normal"), ("CormorantGaramond-Italic.ttf", "300 700", "italic")],
    "Markazi Text": [("MarkaziText.ttf", "400 700", "normal")],
    "Almarai": [("Almarai-Light.ttf", "300", "normal"), ("Almarai-Regular.ttf", "400", "normal"),
                ("Almarai-Bold.ttf", "700", "normal"), ("Almarai-ExtraBold.ttf", "800", "normal")],
    "Alexandria": [("Alexandria-VF.ttf", "100 900", "normal")],
    "Baloo Bhaijaan 2": [("BalooBhaijaan2-VF.ttf", "400 800", "normal")],
    "Bodoni Moda": [("BodoniModa-VF.ttf", "400 900", "normal"), ("BodoniModa-Italic-VF.ttf", "400 900", "italic")],
    "Changa": [("Changa-VF.ttf", "200 800", "normal")],
    "Cinzel": [("Cinzel-VF.ttf", "400 900", "normal")],
    "El Messiri": [("ElMessiri-VF.ttf", "400 700", "normal")],
    "Fraunces": [("Fraunces-VF.ttf", "100 900", "normal"), ("Fraunces-Italic-VF.ttf", "100 900", "italic")],
    "Italiana": [("Italiana-Regular.ttf", "400", "normal")],
    "Lalezar": [("Lalezar-Regular.ttf", "400", "normal")],
    "Marhey": [("Marhey-VF.ttf", "300 700", "normal")],
    "Noto Kufi Arabic": [("NotoKufiArabic-VF.ttf", "100 900", "normal")],
    "Prata": [("Prata-Regular.ttf", "400", "normal")],
    "Readex Pro": [("ReadexPro-VF.ttf", "160 700", "normal")],
    "Reem Kufi": [("ReemKufi-VF.ttf", "400 700", "normal")],
    "Rubik": [("Rubik-VF.ttf", "300 900", "normal"), ("Rubik-Italic-VF.ttf", "300 900", "italic")],
    "Unbounded": [("Unbounded-VF.ttf", "200 900", "normal")],
}

def font_css():
    """@font-face rules with absolute file:// URLs (works for brand pages and for the demo stores)."""
    out = []
    for fam, faces in _FACES.items():
        for f, w, st in faces:
            out.append(f'@font-face{{font-family:"{fam}";src:url("file://{os.path.join(FONTS, f)}");font-weight:{w};font-style:{st};font-display:block}}')
    return "\n".join(out)

def svg(name):
    return open(os.path.join(BRAND, name), encoding="utf-8").read()

def arch_path(w, h, x=0.0, y=0.0):
    """The RIWAQ door: a pointed arch (same proportions as the logo's gold door) filling a w x h box."""
    r = w * 68.5 / 81.0
    a = math.sqrt(r * r - (r - w / 2) ** 2)          # apex height above the spring line
    a = min(a, h)
    return (f"M{x:.1f},{y + h:.1f} L{x:.1f},{y + a:.1f} A{r:.1f},{r:.1f} 0 0 1 {x + w / 2:.1f},{y:.1f} "
            f"A{r:.1f},{r:.1f} 0 0 1 {x + w:.1f},{y + a:.1f} L{x + w:.1f},{y + h:.1f} Z")

esc = lambda s: html.escape(str(s), quote=True)

def file_url(p): return "file://" + os.path.abspath(p)

def demo_img(slug, name):
    """Product/hero image of a demo store (public/demos/<slug>/img/<name>)."""
    p = os.path.join(DEMOS, slug, "img", name)
    return file_url(p) if os.path.exists(p) else ""

# the nine demo stores (names/features as used in earlier RIWAQ posts)
STORES = {
    "batla":  dict(name="بتلة", cat="محل ورد", feat="تصمّم باقتك وتكتب البطاقة بنفسك", hero="hero.webp", bg="#FBF6F4", ink="#2E1823", acc="#5C1A36"),
    "abaq":   dict(name="عبق", cat="عطور وعود", feat="يختار لك عطرك بثلاث أسئلة", hero="hero.webp", bg="#100C09", ink="#F1E6D3", acc="#E3C68E"),
    "lujain": dict(name="لُجين", cat="عبايات", feat="طول العباية على مقاسك بالإنش", hero="hero.webp", bg="#FBFAF8", ink="#111111", acc="#000000"),
    "hail":   dict(name="هَيْل", cat="قهوة وتمور", feat="تعبّي علبة التمر بنفسك حبة حبة", hero="hero.webp", bg="#EEDFCB", ink="#3A2316", acc="#3A2316"),
    "qand":   dict(name="قَنْد", cat="حلويات وكيك", feat="تشوف كيكتك قبل لا تطلبها", hero="p1.webp", bg="#EEF3E5", ink="#4A2A22", acc="#4A2A22"),
    "yaqoot": dict(name="ياقوت", cat="مجوهرات", feat="تحفر الاسم وتشوفه على الذهب", hero="hero.webp", bg="#5E0E1C", ink="#F6E7D6", acc="#E8D3A6"),
    "nabd":   dict(name="نبض", cat="إكسسوارات جوالات", feat="يعرض لك اللي يناسب جوالك بس", hero="p1.webp", bg="#EDEFF3", ink="#0F1426", acc="#2347D8"),
    "taas":   dict(name="طعس", cat="إكسسوارات سيارات", feat="دليل ضغط التواير قبل الطعس", hero="", bg="#120B08", ink="#F6E7CF", acc="#FF6A26"),
    "eclore": dict(name="إكلور", cat="حلويات وورد وخياطة", feat="ثلاث أقسام في متجر واحد", hero="hero.webp", bg="#F4ECE2", ink="#45432A", acc="#B8945C"),
}

def launch(p):
    return p.chromium.launch(args=["--font-render-hinting=none", "--disable-lcd-text"])
