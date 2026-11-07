# RIWAQ daily posts — playbook

One post a day on TikTok (@riwaquae) and Instagram (@riwaqae), scheduled in Metricool (brand id `7776769`, timezone Asia/Dubai).
Weeks run Saturday → Friday. The weekly run prepares next week's 7 posts on Thursday.

## Weekly run

1. Clone `cod-plus/riwaq-media` (push) to `/home/claude/riwaq-media` and `cod-plus/riwaq-site-` (read) to `/home/claude/riwaq-site-`.
2. Look back: Metricool `getAnalyticsDataByMetrics` for the last 14 days — TikTok `TKPO02,TKPO05,TKPO07,TKPO08,TKPO09,TKPO10`,
   Instagram reels `IGRE02,IGRE03,IGRE11,IGRE23,IGRE24`, Instagram posts `IGPO02,IGPO03,IGPO14,IGPO15`. Note which formats and
   topics got the most views / watch time / saves and lean the new week toward them.
3. Check nothing is already scheduled for the target dates (`getScheduledPosts`), so no day gets two posts.
4. Write `studio/posts/<date>.json` for each day (copy the shape of an existing file). Alternate carousel and clip days unless
   the numbers say otherwise. Rotate stores and topics (see backlog); don't repeat a store clip within 3 weeks.
5. `cd studio && python3 make.py <dates…>`; then LOOK at every output (contact sheet of the slides, a few frames of each clip)
   before publishing anything: text cut off, wrong numbers, empty screens and overlapping elements are blockers.
6. Commit and push to `main` (the raw URLs are what Metricool downloads).
7. `python3 payloads.py <date>=<HH:MM> …` → call `createScheduledPost` once per item (blogId `7776769`). Defaults: carousels 10:00,
   clips 18:00 (check `getBestTimeToPostByNetwork`). Verify with `getScheduledPosts`: exactly 2 posts per day.
8. Tell the owner in a few lines of Emirati Arabic what is scheduled and what last week's numbers say.

## Voice and rules

- Emirati dialect, short sentences, one idea per slide. Every post ends with the call to action:
  «أرسل كلمة «متجر» على الواتساب» + «الرابط في البايو 👆».
- Hashtags: `#رواق #متجر_إلكتروني #الإمارات #مشاريع_صغيرة` + 1–3 topical ones.
- Only these facts (all from riwaquae.com). Do NOT invent others: no client counts, testimonials, reviews, results, discounts,
  sample turnaround times, or guarantees.
  - Free sample (نموذج مجاني) of the owner's store before paying anything; we reply on WhatsApp within an hour.
  - «متجر جاهز» 2,500 د.إ in two payments (1,250 at start, 1,250 at delivery): custom design in the shop's identity (not a template),
    up to ٣٠ products in Arabic and English, card / Tabby / Tamara / cash on delivery, own domain, Instagram + TikTok linking,
    delivery in ٥ working days + one hour of training. After delivery: platform subscription only (~145 د.إ/month); optional monthly
    follow-up 450 د.إ/month.
  - «متجر وتشغيل» 4,500 د.إ in two payments (2,250 + 2,250): everything above + up to ١٠٠ products, product photography and
    descriptions, shipping / tax / invoice setup, ٣ TikTok launch videos, one month of follow-up and edits free. Optional
    «إدارة ونمو» 1,200 د.إ/month.
  - Second payment only after the owner receives and tries the store.
  - Dashboard (riwaquae.com/demos/admin): orders arrive the moment the customer pays; status updates in one tap and the customer
    gets a WhatsApp message; add a product with three fields (name, price, quantity); payments and delivery from the phone.
- Demo stores (riwaquae.com/<slug>) are examples, never real clients — except إكلور, our first client (real photos only:
  hero, c5, c9, art, paper, story).

## Backlog

Store clips (`kind: clip`, `clip.store`): hail «تعبّي علبة التمر بنفسك حبة حبة» · yaqoot «تحفر الاسم وتشوفه على الذهب» ·
nabd «يعرض لك اللي يناسب جوالك بس» · abaq «يختار لك عطرك بثلاث أسئلة» · taas «دليل ضغط التواير قبل الطعس» · batla · qand · lujain.

Carousel topics: الفرق بين متجر وحساب إنستقرام · تابي وتمارا في متجرك · ليش الدومين باسمك مهم · قبل/بعد: طلبات الواتساب
مقابل متجر · ٣ أخطاء تخلي الزبون يطلع بدون ما يشتري · كيف تصوّر منتجك بالجوال (عام) · جولة في متجر تجريبي (صور الشاشة) ·
كيف تشتغل خطوات رواق (نموذج ← موافقة ← تسليم) · الأسعار (كل شهر مرة).

## Metricool gotchas

- TikTok needs `tiktokData.title` (≤ 90 chars) for photo AND video posts; photo posts use `autoAddMusic: true`.
- `commercialContentOwnBrand: true` (we promote our own business).
- Instagram: carousel = `type: POST` with several images; clip = `type: REEL` + `videoThumbnailUrl` (cover.jpg).
- TikTok photos are the `tt-NN.jpg` (1080×1920); Instagram uses `ig-NN.jpg` (1080×1350).
