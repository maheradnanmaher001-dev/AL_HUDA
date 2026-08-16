import json, threading
from pathlib import Path
from urllib.request import Request, urlopen

BASE="https://cdn.jsdelivr.net/gh/fawazahmed0/hadith-api@1"
CACHE=Path("data/hadith_cache"); CACHE.mkdir(parents=True,exist_ok=True)

def _get(url):
    req=Request(url,headers={"User-Agent":"AL-HUDA/0.3"})
    with urlopen(req,timeout=25) as r: return json.loads(r.read().decode())

def _cached(key,url):
    p=CACHE/(key+".json")
    if p.exists():
        try: return json.loads(p.read_text(encoding="utf-8"))
        except Exception: pass
    x=_get(url)
    try: p.write_text(json.dumps(x,ensure_ascii=False),encoding="utf-8")
    except Exception: pass
    return x

def book(book_id,lang="eng"):
    return _cached(f"{lang}-{book_id}",f"{BASE}/editions/{lang}-{book_id}.json")

def hadith(book_id,num,lang="eng"):
    return _cached(f"{lang}-{book_id}-{num}",f"{BASE}/editions/{lang}-{book_id}/{num}.json")

def text(x):
    if isinstance(x,dict):
        for k in ("text","hadith","body","contents"):
            if isinstance(x.get(k),str): return x[k]
        for v in x.values():
            t=text(v)
            if t:return t
    return ""

def normalize(x):
    if not isinstance(x,dict): return {"number":"","text":str(x),"grade":"","reference":"","narrator":""}
    return {"number":x.get("hadithnumber",x.get("number",x.get("id",""))),
            "text":text(x),"grade":x.get("grade",""),
            "reference":x.get("reference",""),"narrator":x.get("narrator","")}

def async_call(fn,ok,err=None,*args):
    def run():
        try: ok(fn(*args))
        except Exception as e:
            if err: err(str(e))
    threading.Thread(target=run,daemon=True).start()
