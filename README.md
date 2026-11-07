# riwaq-media

Public media files for RIWAQ social posts (TikTok @riwaquae, Instagram @riwaqae). Files are served from this repo's raw URLs
(`https://raw.githubusercontent.com/cod-plus/riwaq-media/main/<path>`) for scheduling in Metricool.

## Daily posts — `social/<yyyy-mm>/<date>-<slug>/`

| Kind | Files |
|---|---|
| carousel | `ig-NN.jpg` (1080×1350, Instagram) and `tt-NN.jpg` (1080×1920, TikTok photo mode) |
| clip | `clip.mp4` (1080×1920, 14 s, original procedural music) and `cover.jpg` |

Each folder has a `post.json` with the caption, TikTok title and the public URLs.

## Studio — `studio/`

Builds the posts in the RIWAQ identity (ink #142B33, gold #C8963E, sand #F4EEE3, night #0F2228, IBM Plex Sans Arabic, the arch logo).
Needs a checkout of `cod-plus/riwaq-site-` next to this repo (`../riwaq-site-`, or set `RIWAQ_SITE`) for the demo stores.

```
cd studio
python3 make.py 2026-11-07 2026-11-08      # reads posts/<date>.json, writes social/...
```

- `posts/<date>.json` — the content: `kind` carousel (`slides`: hook / point / list / price / phone / cta) or clip (`clip`: store, kicker, lines).
- `slides.py` carousels · `clip.py` store clips (hook → live demo on a phone → call to action) · `capture.py` scripted screen
  captures of the demo stores and the dashboard · `sound.py` procedural soundtrack (no licensed music) · `fonts/` OFL fonts.

Facts used in posts come from riwaquae.com (packages, payment options, demos). Don't add claims that aren't there.

## October videos — `tiktok/2026-10/`

| File | Content | Length |
|---|---|---|
| tiktok/2026-10/01_eclore_store.mp4 | متجر إكلور من رواق | 27s |
| tiktok/2026-10/02_dashboard.mp4 | لوحة تحكم متجرك من رواق | 27s |
| tiktok/2026-10/03_teaser_alheen.mp4 | تيزر رواق — «الحين» | 40s |
| tiktok/2026-10/04_english_online.mp4 | Your customers are already online (no audio) | 39s |
| tiktok/2026-10/05_eight_stores.mp4 | ٨ متاجر، كل واحد بهويته | 33s |
