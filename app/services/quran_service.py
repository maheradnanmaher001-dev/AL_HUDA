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

def _get_json(url, timeout=20):
    req = Request(url, headers={"User-Agent": "AL-HUDA/0.2"})
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
    editions = ",".join([ARABIC, URDU, ENGLISH])
    return _cached_get(f"surah_{surah_number}", f"{API}/surah/{surah_number}/editions/{editions}")

def search_quran(keyword, edition=ENGLISH):
    return _get_json(f"{API}/search/{quote(keyword)}/all/{edition}")

def get_juz(juz_number, edition=ARABIC):
    return _cached_get(f"juz_{juz_number}_{edition}", f"{API}/juz/{juz_number}/{edition}")

def async_call(fn, callback, error_callback=None, *args):
    def worker():
        try:
            callback(fn(*args))
        except Exception as exc:
            if error_callback:
                error_callback(str(exc))
    threading.Thread(target=worker, daemon=True).start()
