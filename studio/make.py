"""Build the media for scheduled RIWAQ posts.
usage: python3 make.py 2026-11-07 [2026-11-08 ...]     (specs in posts/<date>.json)
Output: social/<yyyy-mm>/<date>-<slug>/ (ig-NN.jpg + tt-NN.jpg for carousels, clip.mp4 + cover.jpg for clips) and post.json
with the public raw URLs that Metricool needs."""
import os, sys, json, shutil, time
from common import REPO, RAW, HERE
import slides, clip, capture

def build(date, _shots={}):
    spec = json.load(open(os.path.join(HERE, "posts", f"{date}.json"), encoding="utf-8"))
    rel = os.path.join("social", date[:7], f"{date}-{spec['slug']}")
    out = os.path.join(REPO, rel)
    if os.path.isdir(out): shutil.rmtree(out)
    os.makedirs(out)
    url = lambda p: RAW + rel + "/" + os.path.basename(p)
    tag = "-" + time.strftime("%d%H%M")                 # new file names on every build, so caches never serve an old file
    post = dict(date=date, slug=spec["slug"], kind=spec["kind"], caption=spec["caption"],
                tiktok_title=spec.get("tiktok_title", ""), time=spec.get("time"))
    if spec["kind"] == "carousel":
        ss = spec["slides"]
        if any(s.get("shot") for s in ss):
            if not _shots:
                _shots.update(capture.stills("admin", os.path.join(REPO, ".cache", "admin")))
            for s in ss:
                if s.get("shot"): s["phone_img"] = _shots[s["shot"]]
        files = slides.render_carousel(ss, out, tag=tag)
        post["ig"] = [url(f) for f in files["ig"]]
        post["tt"] = [url(f) for f in files["tt"]]
    else:
        r = clip.make_clip(spec["clip"], out, tag=tag)
        post["video"], post["cover"] = url(r["video"]), url(r["cover"])
    shutil.rmtree(os.path.join(out, ".src"), ignore_errors=True)
    json.dump(post, open(os.path.join(out, "post.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("built", rel)
    return post

if __name__ == "__main__":
    for d in sys.argv[1:]:
        build(d)
