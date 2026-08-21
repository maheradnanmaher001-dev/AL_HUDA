#!/usr/bin/env python3
"""
AL-HUDA Step 18 data downloader.
Downloads complete local Quran + Hadith datasets and verifies them before success.
No third-party Python packages are required.
"""
from __future__ import annotations
import json, os, sys, time, hashlib
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

ROOT = Path(__file__).resolve().parents[1]
QURAN_DIR = ROOT / "data" / "quran"
HADITH_DIR = ROOT / "data" / "hadith"
QURAN_DIR.mkdir(parents=True, exist_ok=True)
HADITH_DIR.mkdir(parents=True, exist_ok=True)

UA = "AL-HUDA-Step18/1.0 (+GitHub Actions)"
TIMEOUT = 60
RETRIES = 4

def fetch(url: str) -> bytes:
    last = None
    for attempt in range(1, RETRIES + 1):
        try:
            req = Request(url, headers={"User-Agent": UA, "Accept": "application/json,*/*"})
            with urlopen(req, timeout=TIMEOUT) as r:
                data = r.read()
                if not data:
                    raise RuntimeError(f"Empty response: {url}")
                return data
        except (HTTPError, URLError, TimeoutError, RuntimeError) as e:
            last = e
            if attempt < RETRIES:
                time.sleep(2 * attempt)
    raise RuntimeError(f"Download failed after {RETRIES} attempts: {url}\n{last}")

def fetch_json(url: str):
    raw = fetch(url)
    try:
        return json.loads(raw.decode("utf-8-sig"))
    except Exception as e:
        raise RuntimeError(f"Invalid JSON from {url}: {e}")

def write_json(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(path)

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def normalize_ayah_count(quran_obj):
    # Supports mjmirza nested dataset and common Al Quran Cloud response shapes.
    if isinstance(quran_obj, dict) and isinstance(quran_obj.get("surahs"), list):
        return len(quran_obj["surahs"]), sum(
            len(s.get("ayahs", [])) for s in quran_obj["surahs"] if isinstance(s, dict)
        )
    if isinstance(quran_obj, dict) and isinstance(quran_obj.get("data"), dict):
        data = quran_obj["data"]
        if isinstance(data.get("surahs"), list):
            return len(data["surahs"]), sum(len(s.get("ayahs", [])) for s in data["surahs"])
    return 0, 0

def download_quran():
    # Independently validated Arabic corpus: 114 surahs / 6236 ayahs / 30 juz.
    arabic_url = "https://raw.githubusercontent.com/mjmirza/quran-dataset/main/data/quran.json"
    arabic = fetch_json(arabic_url)
    surahs, ayahs = normalize_ayah_count(arabic)
    if surahs != 114 or ayahs != 6236:
        raise RuntimeError(f"Quran Arabic validation failed: surahs={surahs}, ayahs={ayahs}")
    write_json(QURAN_DIR / "quran_arabic_uthmani.json", arabic)

    # Complete translations from Al Quran Cloud. These are downloaded locally;
    # the app will not need a network connection to read them after packaging.
    editions = {
        "english": "https://api.alquran.cloud/v1/quran/en.asad",
        "urdu": "https://api.alquran.cloud/v1/quran/ur.jalandhry",
    }
    for lang, url in editions.items():
        obj = fetch_json(url)
        s, a = normalize_ayah_count(obj)
        if s != 114 or a != 6236:
            raise RuntimeError(f"Quran {lang} validation failed: surahs={s}, ayahs={a}")
        write_json(QURAN_DIR / f"quran_{lang}.json", obj)

    # Local catalogue expected by the app.
    catalogue = {
        "dataset": "AL-HUDA local Quran",
        "surahs": 114,
        "ayahs": 6236,
        "juz": 30,
        "arabic": "quran_arabic_uthmani.json",
        "english": "quran_english.json",
        "urdu": "quran_urdu.json",
        "sources": [arabic_url, editions["english"], editions["urdu"]],
    }
    write_json(QURAN_DIR / "catalogue.json", catalogue)

def download_hadith():
    editions_url = "https://cdn.jsdelivr.net/gh/fawazahmed0/hadith-api@1/editions.json"
    editions = fetch_json(editions_url)
    write_json(HADITH_DIR / "editions_catalogue.json", editions)

    # Download every collection that has Arabic, English, or Urdu editions.
    # This avoids hard-coding only Bukhari/Muslim and keeps the catalogue complete.
    selected = []
    for book_key, book in editions.items():
        collections = book.get("collection", []) if isinstance(book, dict) else []
        for item in collections:
            name = item.get("name", "")
            lang = item.get("language", "")
            link = item.get("link")
            if lang in {"Arabic", "English", "Urdu"} and link and name:
                selected.append((book_key, book.get("name", book_key), lang, name, link))

    if not selected:
        raise RuntimeError("Hadith catalogue returned no Arabic/English/Urdu editions.")

    manifest = []
    failed = []
    for idx, (book_key, book_name, lang, edition_name, url) in enumerate(selected, 1):
        safe = re_safe(edition_name)
        out = HADITH_DIR / f"{safe}.json"
        try:
            obj = fetch_json(url)
            if not isinstance(obj, dict) or not isinstance(obj.get("hadiths"), list):
                raise RuntimeError("missing 'hadiths' list")
            if len(obj["hadiths"]) == 0:
                raise RuntimeError("empty hadith list")
            write_json(out, obj)
            manifest.append({
                "collection_key": book_key,
                "collection_name": book_name,
                "language": lang,
                "edition": edition_name,
                "hadith_count": len(obj["hadiths"]),
                "file": str(out.relative_to(ROOT)),
                "source": url,
            })
            print(f"[{idx}/{len(selected)}] OK {edition_name}: {len(obj['hadiths'])} hadiths")
        except Exception as e:
            failed.append({"edition": edition_name, "url": url, "error": str(e)})
            print(f"[{idx}/{len(selected)}] FAILED {edition_name}: {e}")

    if failed:
        raise RuntimeError("Hadith download failed for one or more editions:\n" + json.dumps(failed, ensure_ascii=False, indent=2))

    # Ensure the core collection set exists in all available requested languages.
    collections = sorted(set(x["collection_key"] for x in manifest))
    if len(collections) < 10:
        raise RuntimeError(f"Hadith collection verification too small: only {len(collections)} collections")
    write_json(HADITH_DIR / "manifest.json", {
        "collections": len(collections),
        "editions": len(manifest),
        "languages": sorted(set(x["language"] for x in manifest)),
        "items": manifest,
    })

def re_safe(s):
    import re
    s = re.sub(r"[^A-Za-z0-9._-]+", "_", s).strip("_")
    return s or "edition"

def verify():
    qcat = fetch_json_file(QURAN_DIR / "catalogue.json")
    if qcat.get("surahs") != 114 or qcat.get("ayahs") != 6236 or qcat.get("juz") != 30:
        raise RuntimeError("Final Quran catalogue verification failed.")
    for name in ["quran_arabic_uthmani.json", "quran_english.json", "quran_urdu.json"]:
        p = QURAN_DIR / name
        if not p.exists() or p.stat().st_size < 1000:
            raise RuntimeError(f"Missing/too-small Quran file: {p}")

    hm = fetch_json_file(HADITH_DIR / "manifest.json")
    if hm.get("collections", 0) < 10 or hm.get("editions", 0) < 10:
        raise RuntimeError("Final Hadith manifest verification failed.")
    for item in hm["items"]:
        p = ROOT / item["file"]
        if not p.exists() or p.stat().st_size < 100:
            raise RuntimeError(f"Missing/too-small Hadith file: {p}")

    manifest = {
        "step": 18,
        "status": "verified",
        "quran": qcat,
        "hadith": {
            "collections": hm["collections"],
            "editions": hm["editions"],
            "languages": hm["languages"],
        },
        "files_sha256": {},
    }
    for p in sorted(QURAN_DIR.glob("*.json")):
        manifest["files_sha256"][str(p.relative_to(ROOT))] = sha256(p)
    for p in sorted(HADITH_DIR.glob("*.json")):
        manifest["files_sha256"][str(p.relative_to(ROOT))] = sha256(p)
    write_json(ROOT / "data" / "STEP18_MANIFEST.json", manifest)
    print("STEP 18 VERIFIED: complete local Quran/Hadith data is present.")

def fetch_json_file(path):
    return json.loads(path.read_text(encoding="utf-8"))

if __name__ == "__main__":
    try:
        download_quran()
        download_hadith()
        verify()
    except Exception as exc:
        print(f"STEP 18 FAILED: {exc}", file=sys.stderr)
        sys.exit(1)
