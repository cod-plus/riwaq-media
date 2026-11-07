"""Metricool createScheduledPost payloads for built posts.
usage: python3 payloads.py 2026-11-14=10:00 2026-11-15=18:00 ...   -> JSON list [{date, network, info}] to pass to
createScheduledPost(blogId="7776769", date=<date>, info=json.dumps(info)). Times are Asia/Dubai."""
import os, sys, json, glob
from common import REPO

TZ = "Asia/Dubai"

def payloads(day, hhmm):
    f = glob.glob(os.path.join(REPO, "social", day[:7], f"{day}-*", "post.json"))
    if len(f) != 1: raise SystemExit(f"no unique built post for {day}: {f}")
    p = json.load(open(f[0], encoding="utf-8"))
    dt = f"{day}T{hhmm}:00"
    base = dict(autoPublish=True, draft=False, descendants=[], firstCommentText="", hasNotReadNotes=False, mediaAltText=[],
                publicationDate={"dateTime": dt, "timezone": TZ}, shortener=False, smartLinkData={"ids": []}, text=p["caption"])
    tk = dict(disableComment=False, disableDuet=False, disableStitch=False, privacyOption="PUBLIC_TO_EVERYONE",
              commercialContentThirdParty=False, commercialContentOwnBrand=True,      # own-brand promotion disclosure
              title=p["tiktok_title"][:90], isAigc=False)                            # TikTok requires a title (photo and video)
    if p["kind"] == "carousel":
        tt = dict(base, media=p["tt"], providers=[{"network": "tiktok"}], tiktokData=dict(tk, autoAddMusic=True, photoCoverIndex=0))
        ig = dict(base, media=p["ig"], providers=[{"network": "instagram"}], instagramData=dict(type="POST", collaborators=[], isAiGenerated=False))
    else:
        tt = dict(base, media=[p["video"]], videoThumbnailUrl=p["cover"], providers=[{"network": "tiktok"}], tiktokData=tk)
        ig = dict(base, media=[p["video"]], videoThumbnailUrl=p["cover"], providers=[{"network": "instagram"}],
                  instagramData=dict(type="REEL", collaborators=[], showReelOnFeed=True, isAiGenerated=False))
    d = dt + "+04:00"
    return [dict(date=d, network="tiktok", info=tt), dict(date=d, network="instagram", info=ig)]

if __name__ == "__main__":
    out = []
    for a in sys.argv[1:]:
        day, hhmm = a.split("=")
        out += payloads(day, hhmm)
    print(json.dumps(out, ensure_ascii=False, indent=1))
