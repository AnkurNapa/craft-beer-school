"""Podcast page: every Cheers Chatty Beer Podcast episode, playable on site.

`python3 podcast.py` refreshes content/podcast.json from the public RSS feed
and Apple's episode lookup. build.py only reads the JSON, so a feed outage
never breaks the daily build.
"""
import html
import json
import pathlib
import urllib.request
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime

SLUG = "podcast.html"
DATA = pathlib.Path("content/podcast.json")
FEED = "https://feeds.megaphone.fm/ISP9530441028"
APPLE_ID = "1493541371"
SPOTIFY_URL = "https://open.spotify.com/show/1qPO5UgB1WHnp4qfx7MCMX"
APPLE_URL = f"https://podcasts.apple.com/us/podcast/cheers-chatty-beer-podcast/id{APPLE_ID}"
IT = "{http://www.itunes.com/dtds/podcast-1.0.dtd}"
STRAIGHT = str.maketrans({"\u201c": '"', "\u201d": '"', "\u2018": "'", "\u2019": "'",
                          "\u2013": "-", "\u2014": "-"})


def _get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def fetch():
    apple = json.loads(_get(f"https://itunes.apple.com/lookup?id={APPLE_ID}&entity=podcastEpisode&limit=200"))
    apple_by_guid = {a["episodeGuid"]: a["trackViewUrl"].split("?")[0]
                     for a in apple["results"] if a.get("kind") == "podcast-episode"}
    episodes = []
    for it in ET.fromstring(_get(FEED)).iter("item"):
        guid = it.findtext("guid")
        summary = (it.findtext(f"{IT}summary") or it.findtext("description") or "").strip()
        episodes.append(dict(
            title=it.findtext("title").strip().translate(STRAIGHT),
            date=parsedate_to_datetime(it.findtext("pubDate")).date().isoformat(),
            season=it.findtext(f"{IT}season"), episode=it.findtext(f"{IT}episode"),
            minutes=round(int(it.findtext(f"{IT}duration") or 0) / 60),
            summary=summary.translate(STRAIGHT),
            audio=it.find("enclosure").get("url"),
            apple=apple_by_guid.get(guid, APPLE_URL)))
    if not episodes:
        raise SystemExit("feed returned no episodes, keeping the old podcast.json")
    DATA.write_text(json.dumps(episodes, indent=1, ensure_ascii=False))
    print(f"wrote {DATA}: {len(episodes)} episodes")


def _short(text, limit=240):
    return text if len(text) <= limit else text[:limit].rsplit(" ", 1)[0] + "..."


def _card(e):
    esc = html.escape
    tag = f"S{e['season']} E{e['episode']} · " if e["season"] and e["episode"] else ""
    return f"""<article class="card ep reveal"><div class="card-body">
  <span class="cat">{tag}{e['date']} · {e['minutes']} min</span>
  <h3>{esc(e['title'])}</h3>
  <p>{esc(_short(e['summary']))}</p>
  <audio controls preload="none" src="{esc(e['audio'])}" aria-label="Play {esc(e['title'])}"></audio>
  <div class="foot"><a href="{esc(e['apple'])}" class="link-arrow" target="_blank" rel="noopener">Apple Podcasts</a><a href="{SPOTIFY_URL}" class="link-arrow" target="_blank" rel="noopener">Spotify</a></div>
</div></article>"""


def page(banner):
    episodes = json.loads(DATA.read_text())
    body = banner("Podcast", "Cheers Chatty Beer Podcast", "Listen to every episode.",
                  f"{len(episodes)} conversations with brewers, founders and sensory pros, hosted by Chatty Girija. Play them right here, or follow on Spotify or Apple Podcasts.") + f"""
<section>
  <div class="wrap">
    <div class="pod-follow">
      <a href="{SPOTIFY_URL}" class="btn btn-amber" target="_blank" rel="noopener" data-cta="podcast-spotify">Follow on Spotify</a>
      <a href="{APPLE_URL}" class="btn btn-ghost" target="_blank" rel="noopener" data-cta="podcast-apple">Follow on Apple Podcasts</a>
    </div>
    <iframe class="pod-embed" title="Cheers Chatty Beer Podcast on Spotify" src="https://open.spotify.com/embed/show/1qPO5UgB1WHnp4qfx7MCMX" height="352" loading="lazy" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"></iframe>
  </div>
</section>
<section class="tint">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">All episodes</span><h2>Press play.</h2></div>
    <div class="grid-3">
{chr(10).join(_card(e) for e in episodes)}
    </div>
  </div>
</section>
<section class="cta"><div class="wrap"><h2>Got a story worth pouring?</h2><p>Suggest a guest or a topic for the next season.</p><a href="contact.html#enroll" class="btn btn-amber" data-cta="suggest-a-guest-or-topic">Suggest a guest</a></div></section>
"""
    return ("Cheers Chatty Beer Podcast, All Episodes | Craft Beer School",
            f"Listen to all {len(episodes)} episodes of the Cheers Chatty Beer Podcast with Chatty Girija. Brewers, founders and sensory pros, on Spotify and Apple Podcasts.",
            "blog", body)


if __name__ == "__main__":
    fetch()
