"""AL-HUDA complete Hadith integration.

Uses the public fawazahmed0 hadith-api editions with fallback URLs.
The service preserves the old book()/hadith()/normalize() API and adds
collection/book/section helpers. No Hadith text is generated.
"""

import json
import threading
from pathlib import Path
from urllib.request import Request, urlopen

CDN = "https://cdn.jsdelivr.net/gh/fawazahmed0/hadith-api@1"
RAW = "https://raw.githubusercontent.com/fawazahmed0/hadith-api/1"
CACHE = Path("data/hadith_cache")
CACHE.mkdir(parents=True, exist_ok=True)

# 17 catalog entries documented by the source; two are non-hadith types.
COLLECTIONS = (
    "bukhari", "muslim", "abudawud", "tirmidhi", "nasai", "ibnmajah",
    "malik", "ahmad", "darimi", "riyadussalihin", "adab", "shamail",
    "mishkat", "bulugh", "forty", "hisn", "virtues"
)
HADITH_COLLECTIONS = COLLECTIONS[:15]

def _get(url, timeout=40):
    req = Request(url, headers={"User-Agent": "AL-HUDA/1.0"})
    with urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))

def _cached(key, urls):
    p = CACHE / (key + ".json")
    if p.exists():
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            pass
    last = None
    for url in urls:
        try:
            data = _get(url)
            p.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
            return data
        except Exception as exc:
            last = exc
    raise RuntimeError(f"Hadith source unavailable: {last}")

def editions():
    return _cached("editions", [
        f"{CDN}/editions.json",
        f"{RAW}/editions.json",
    ])

def book(book_id, lang="eng"):
    slug = f"{lang}-{book_id}"
    return _cached(slug, [
        f"{CDN}/editions/{slug}.json",
        f"{RAW}/editions/{slug}.json",
    ])

def hadith(book_id, num, lang="eng"):
    slug = f"{lang}-{book_id}"
    return _cached(f"{slug}-{num}", [
        f"{CDN}/editions/{slug}/{num}.json",
        f"{RAW}/editions/{slug}/{num}.json",
    ])

def section(book_id, section_no, lang="eng"):
    slug = f"{lang}-{book_id}"
    return _cached(f"{slug}-section-{section_no}", [
        f"{CDN}/editions/{slug}/sections/{section_no}.json",
        f"{RAW}/editions/{slug}/sections/{section_no}.json",
    ])

def collection_languages(book_id):
    info = editions()
    found = []
    needle = str(book_id).lower()
    for item in info.get("books", info if isinstance(info, list) else []):
        if not isinstance(item, dict):
            continue
        for edition in item.get("collection", []):
            if str(edition.get("book", "")).lower() == needle:
                found.append(edition.get("name", ""))
    return sorted(set(found))

def text(x):
    if isinstance(x, dict):
        for key in ("text", "hadith", "body", "contents"):
            if isinstance(x.get(key), str):
                return x[key]
        for value in x.values():
            found = text(value)
            if found:
                return found
    elif isinstance(x, list):
        for value in x:
            found = text(value)
            if found:
                return found
    return ""

def normalize(x):
    if not isinstance(x, dict):
        return {"number": "", "text": str(x), "grade": "", "reference": "", "narrator": ""}
    return {
        "number": x.get("hadithnumber", x.get("number", x.get("id", ""))),
        "text": text(x),
        "grade": x.get("grade", ""),
        "reference": x.get("reference", ""),
        "narrator": x.get("narrator", ""),
    }

def async_call(fn, ok, err=None, *args):
    def run():
        try:
            ok(fn(*args))
        except Exception as exc:
            if err:
                err(str(exc))
    threading.Thread(target=run, daemon=True).start()
