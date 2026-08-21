"""AL-HUDA complete Quran integration.

Keeps the existing public API while adding explicit 114-Surah/30-Juz,
translation, search and source metadata helpers. Data is retrieved from
Al Quran Cloud at runtime and cached locally; no Quran text is fabricated.
"""

import json
import threading
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen

API = "https://api.alquran.cloud/v1"
ARABIC = "quran-uthmani"
URDU = "ur.jalandhry"
ENGLISH = "en.sahih"
CACHE = Path("data/quran_cache")
CACHE.mkdir(parents=True, exist_ok=True)

SURAH_COUNT = 114
JUZ_COUNT = 30
AYAH_COUNT = 6236

def _get_json(url, timeout=30):
    req = Request(url, headers={"User-Agent": "AL-HUDA/1.0"})
    with urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))

def _cached_get(key, url):
    p = CACHE / (key + ".json")
    if p.exists():
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            pass
    data = _get_json(url)
    try:
        p.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    except Exception:
        pass
    return data

def get_surah(surah_number):
    n = int(surah_number)
    if not 1 <= n <= SURAH_COUNT:
        raise ValueError("Surah number must be between 1 and 114.")
    editions = ",".join([ARABIC, URDU, ENGLISH])
    return _cached_get(
        f"surah_{n}",
        f"{API}/surah/{n}/editions/{editions}"
    )

def get_juz(juz_number, edition=ARABIC):
    n = int(juz_number)
    if not 1 <= n <= JUZ_COUNT:
        raise ValueError("Juz number must be between 1 and 30.")
    return _cached_get(f"juz_{n}_{edition}", f"{API}/juz/{n}/{edition}")

def get_juz_with_translations(juz_number):
    n = int(juz_number)
    if not 1 <= n <= JUZ_COUNT:
        raise ValueError("Juz number must be between 1 and 30.")
    editions = ",".join([ARABIC, URDU, ENGLISH])
    return _cached_get(
        f"juz_{n}_all",
        f"{API}/juz/{n}/{editions}"
    )

def get_surah_list():
    return _cached_get("surah_list", f"{API}/surah")

def search_quran(keyword, edition=ENGLISH):
    return _get_json(f"{API}/search/{quote(str(keyword))}/all/{edition}")

def source_metadata():
    return {
        "provider": "Al Quran Cloud",
        "api": API,
        "arabic": ARABIC,
        "urdu": URDU,
        "english": ENGLISH,
        "surahs": SURAH_COUNT,
        "juz": JUZ_COUNT,
        "ayahs": AYAH_COUNT,
    }

def async_call(fn, callback, error_callback=None, *args):
    def worker():
        try:
            callback(fn(*args))
        except Exception as exc:
            if error_callback:
                error_callback(str(exc))
    threading.Thread(target=worker, daemon=True).start()
