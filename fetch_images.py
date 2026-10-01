#!/usr/bin/env python3
"""Free-licence photos from Wikimedia Commons, credited properly.

  python3 fetch_images.py candidates SLOT [SLOT...]   # contact sheet of options per slot
  python3 fetch_images.py pick SLOT "File:Title.jpg"   # download, crop, record credit
  python3 fetch_images.py pick-all                    # re-download everything in images.json

Only licences that allow commercial use and modification are accepted. Every
picked image is recorded in content/images.json with author, licence and
source URL; the Image credits page and each caption are built from that file.
"""
import html
import io
import json
import pathlib
import re
import sys
import urllib.parse
import urllib.request

from PIL import Image, ImageDraw, ImageFont

HERE = pathlib.Path(__file__).parent
SLOTS = json.loads((HERE / "content/image_slots.json").read_text())
RECORD = HERE / "content/images.json"
OUT = HERE / "assets/photos"
SHEETS = pathlib.Path("/tmp/cbs-image-sheets")
UA = {"User-Agent": "CraftBeerSchoolSite/1.0 (https://craftbeerschool.in; napaankur@gmail.com)"}
API = "https://commons.wikimedia.org/w/api.php"
OK = re.compile(r"^(CC0|Public domain|PD|CC BY(-SA)? [1-4]\.0)", re.I)
SIZE = (1200, 750)  # 16:10, cropped from the centre


def get(url, raw=False):
    b = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read()
    return b if raw else json.loads(b)


def plain(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s or "")).strip()


def search(query, n=12):
    q = urllib.parse.urlencode({
        "action": "query", "format": "json", "generator": "search", "gsrnamespace": 6,
        "gsrsearch": f"{query} filetype:bitmap", "gsrlimit": 40, "prop": "imageinfo",
        "iiprop": "url|extmetadata|size", "iiurlwidth": 1600})
    pages = get(f"{API}?{q}").get("query", {}).get("pages", {}).values()
    out = []
    for p in sorted(pages, key=lambda p: p.get("index", 0)):
        i = p["imageinfo"][0]
        m = i["extmetadata"]
        lic = plain(m.get("LicenseShortName", {}).get("value"))
        if not OK.match(lic) or i["width"] < 1200 or i["width"] < i["height"]:
            continue
        out.append(dict(title=p["title"], thumb=i["thumburl"], page=i["descriptionurl"], licence=lic,
                        licence_url=m.get("LicenseUrl", {}).get("value", ""),
                        author=plain(m.get("Artist", {}).get("value")) or "Unknown",
                        width=i["width"], height=i["height"]))
        if len(out) == n:
            break
    return out


def candidates(slots):
    SHEETS.mkdir(exist_ok=True)
    font = ImageFont.load_default()
    for slot in slots:
        found = search(SLOTS[slot])
        cells = []
        for k, c in enumerate(found):
            try:
                im = Image.open(io.BytesIO(get(c["thumb"].replace("1600px", "400px"), raw=True))).convert("RGB")
            except Exception:
                continue
            im.thumbnail((400, 260))
            cells.append((k, im, c))
        sheet = Image.new("RGB", (1220, 290 * ((len(cells) + 2) // 3) + 10), "white")
        for n, (k, im, c) in enumerate(cells):
            x, y = 10 + (n % 3) * 405, 10 + (n // 3) * 290
            sheet.paste(im, (x, y))
            ImageDraw.Draw(sheet).text((x, y + 264), f"{k}: {c['licence']} {c['width']}px", fill="black", font=font)
        path = SHEETS / f"{slot.replace(':', '_')}.png"
        sheet.save(path)
        (SHEETS / f"{slot.replace(':', '_')}.json").write_text(json.dumps(found, indent=1))
        print(slot, len(cells), "candidates ->", path)


def pick(slot, index):
    found = json.loads((SHEETS / f"{slot.replace(':', '_')}.json").read_text())
    c = found[int(index)]
    OUT.mkdir(parents=True, exist_ok=True)
    im = Image.open(io.BytesIO(get(c["thumb"], raw=True))).convert("RGB")
    w, h = im.size
    tw = min(w, int(h * SIZE[0] / SIZE[1]))
    th = int(tw * SIZE[1] / SIZE[0])
    im = im.crop(((w - tw) // 2, (h - th) // 2, (w - tw) // 2 + tw, (h - th) // 2 + th)).resize(SIZE, Image.LANCZOS)
    name = slot.replace(":", "-") + ".jpg"
    im.save(OUT / name, quality=80, optimize=True, progressive=True)
    im.resize((600, 375), Image.LANCZOS).save(OUT / name.replace(".jpg", "-sm.jpg"), quality=78, optimize=True)
    rec = json.loads(RECORD.read_text()) if RECORD.exists() else {}
    rec[slot] = {k: c[k] for k in ("title", "page", "licence", "licence_url", "author")} | {"file": f"assets/photos/{name}"}
    RECORD.write_text(json.dumps(dict(sorted(rec.items())), indent=1, ensure_ascii=False))
    print(slot, "->", name, "|", c["licence"], "|", c["author"][:60])


if __name__ == "__main__":
    cmd, *rest = sys.argv[1:]
    if cmd == "candidates":
        candidates(rest or list(SLOTS))
    elif cmd == "pick":
        pick(*rest)
