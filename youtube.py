"""YouTube page: every Cheers Chatty video and Short, with a keyword filter.

`python3 youtube.py` refreshes content/youtube.json. It needs yt-dlp for the
channel listing (pip install --user yt-dlp) and reads each public watch page for
the description and date. build.py only reads the JSON, so CI never calls YouTube.
"""
import html
import json
import pathlib
import re
import shutil
import subprocess
import time
import unicodedata
import urllib.request
from concurrent.futures import ThreadPoolExecutor

import podcast

SLUG = "youtube.html"
DATA = pathlib.Path("content/youtube.json")
THUMBS = pathlib.Path("assets/youtube")
CHANNEL = "https://www.youtube.com/c/CheersChatty"
SUBSCRIBE = "https://www.youtube.com/c/CheersChatty?sub_confirmation=1"
# Ankur asked (2026-10-09) to leave these guests' episodes off the site.
EXCLUDE = ("ishan grover", "gautam gandhi")
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120 Safari/537.36",
      "Accept-Language": "en"}


def _clean(text):
    # NFKC turns the channel's fancy bold letters into plain ones; then straight quotes, no dashes.
    return unicodedata.normalize("NFKC", text or "").translate(podcast.STRAIGHT).strip()


def _listing(tab):
    ytdlp = shutil.which("yt-dlp") or str(pathlib.Path.home() / "Library/Python/3.9/bin/yt-dlp")
    out = subprocess.run([ytdlp, "--flat-playlist", "-J", f"{CHANNEL}/{tab}"],
                         capture_output=True, text=True, check=True).stdout
    return [e["id"] for e in json.loads(out)["entries"]]


def _get(url, tries=6):
    for n in range(tries):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30).read()
        except OSError:
            if n == tries - 1:
                raise
            time.sleep(15 * (n + 1))  # YouTube answers bursts with 429; back off hard


def _details(vid):
    page = _get(f"https://www.youtube.com/watch?v={vid}").decode("utf-8", "replace")
    title = re.search(r'<meta name="title" content="([^"]*)"', page)
    desc = re.search(r'"shortDescription":("(?:[^"\\]|\\.)*")', page)
    date = re.search(r'itemprop="(?:datePublished|uploadDate)" content="(\d{4}-\d{2}-\d{2})', page)
    secs = re.search(r'"lengthSeconds":"(\d+)"', page)
    thumb = THUMBS / f"{vid}.jpg"
    if not thumb.exists():
        thumb.write_bytes(_get(f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg"))
    return dict(id=vid, title=_clean(html.unescape(title.group(1)) if title else vid),
                summary=_clean(json.loads(desc.group(1)) if desc else ""),
                date=date.group(1) if date else "", seconds=int(secs.group(1)) if secs else 0,
                thumb=thumb.as_posix())


CACHE = pathlib.Path(".cache/youtube_details.json")


def _cached(cache):
    def one(vid):
        if vid not in cache:
            cache[vid] = _details(vid)
            CACHE.write_text(json.dumps(cache, ensure_ascii=False))
        return cache[vid]
    return one


def fetch():
    THUMBS.mkdir(exist_ok=True)
    CACHE.parent.mkdir(exist_ok=True)
    cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}
    found = {"videos": [], "shorts": []}
    for tab in found:
        with ThreadPoolExecutor(2) as pool:
            found[tab] = list(pool.map(_cached(cache), _listing(tab)))
    if not found["videos"]:
        raise SystemExit("channel returned no videos, keeping the old youtube.json")
    dropped = []
    for tab, items in found.items():
        keep = [v for v in items if not any(n in f"{v['title']} {v['summary']}".lower() for n in EXCLUDE)]
        dropped += [v["title"] for v in items if v not in keep]
        found[tab] = sorted(keep, key=lambda v: v["date"], reverse=True)
    DATA.write_text(json.dumps(found, indent=1, ensure_ascii=False))
    print(f"wrote {DATA}: {len(found['videos'])} videos, {len(found['shorts'])} shorts; left out: {dropped}")


def _length(secs):
    return f"{secs // 60} min" if secs >= 60 else f"{secs} sec"


def _card(v, short=False):
    esc = html.escape
    url = f"https://www.youtube.com/{'shorts/' if short else 'watch?v='}{v['id']}"
    meta = " · ".join(x for x in (v["date"], _length(v["seconds"]) if v["seconds"] else "") if x)
    blurb = "" if short else f"<p>{esc(podcast._short(v['summary'].split(chr(10))[0], 160))}</p>"
    return f"""<article class="card yt{' yt-short' if short else ''} reveal" data-q="{esc((v['title'] + ' ' + v['summary']).lower())}"><a class="yt-thumb" href="{url}" target="_blank" rel="noopener" aria-label="Watch {esc(v['title'])} on YouTube"><img src="{esc(v['thumb'])}" alt="" width="480" height="360" loading="lazy" /><span class="yt-play" aria-hidden="true"></span></a><div class="card-body">
  <span class="cat">{meta}</span>
  <h3><a href="{url}" target="_blank" rel="noopener">{esc(v['title'])}</a></h3>
  {blurb}
</div></article>"""


def page(banner):
    data = json.loads(DATA.read_text())
    videos, shorts = data["videos"], data["shorts"]
    latest = videos[0]
    body = banner("YouTube", "Cheers Chatty on YouTube", "Watch every episode.",
                  f"{len(videos)} videos and {len(shorts)} Shorts from Cheers Chatty and Craft Beer School: brewer interviews, brewing lessons, tastings and food pairings, hosted by Chatty Girija.") + f"""
<section>
  <div class="wrap">
    <div class="pod-follow">
      <a href="{SUBSCRIBE}" class="btn btn-amber" target="_blank" rel="noopener" data-cta="youtube-subscribe">Subscribe on YouTube</a>
      <a href="podcast.html" class="btn btn-ghost">Listen to the podcast</a>
    </div>
    <div class="yt-embed"><iframe title="{html.escape(latest['title'])}" src="https://www.youtube-nocookie.com/embed/{latest['id']}" loading="lazy" allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture; fullscreen" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe></div>
  </div>
</section>
<section class="tint">
  <div class="wrap">
    {podcast.filter_box("yt-list", "Filter videos by guest, beer or topic")}
    <div id="yt-list">
      <div class="sec-head"><span class="eyebrow">Videos</span><h2>Interviews, lessons and tastings.</h2></div>
      <div class="grid-3">
{chr(10).join(_card(v) for v in videos)}
      </div>
      <div class="sec-head yt-shorts-head"><span class="eyebrow">Shorts</span><h2>One minute of beer.</h2></div>
      <div class="grid-shorts">
{chr(10).join(_card(v, short=True) for v in shorts)}
      </div>
    </div>
  </div>
</section>
<section class="cta"><div class="wrap"><h2>Want to be on the channel?</h2><p>Suggest a guest, a brewery to visit or a topic for the next video.</p><a href="contact.html#enroll" class="btn btn-amber" data-cta="youtube-suggest">Suggest a guest</a></div></section>
"""
    return ("Cheers Chatty on YouTube, All Videos | Craft Beer School",
            f"Watch all {len(videos)} Cheers Chatty and Craft Beer School videos and {len(shorts)} Shorts: brewer interviews, brewing lessons, tastings and beer and food pairings.",
            "podcast", body)


if __name__ == "__main__":
    fetch()
