import json, threading
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import urlencode
from datetime import datetime, timedelta

BASE="https://api.aladhan.com/v1"
CACHE=Path("data/prayer_cache"); CACHE.mkdir(parents=True,exist_ok=True)
PRAYERS=("Fajr","Sunrise","Dhuhr","Asr","Maghrib","Isha")

def _get(url):
    req=Request(url,headers={"User-Agent":"AL-HUDA/0.4"})
    with urlopen(req,timeout=20) as r:
        return json.loads(r.read().decode())

def _cached(key,url):
    p=CACHE/(key+".json")
    if p.exists():
        try:return json.loads(p.read_text(encoding="utf-8"))
        except Exception:pass
    data=_get(url)
    try:p.write_text(json.dumps(data,ensure_ascii=False),encoding="utf-8")
    except Exception:pass
    return data

def timings_by_city(city,country,date=None,method=2):
    date=date or datetime.now().strftime("%d-%m-%Y")
    key=f"city-{city}-{country}-{date}-{method}".replace(" ","_")
    q=urlencode({"city":city,"country":country,"method":method})
    return _cached(key,f"{BASE}/timingsByCity/{date}?{q}")

def clean(data):
    try:
        t=data["data"]["timings"]
        return {p:t.get(p,"").split(" ")[0] for p in PRAYERS}
    except Exception:return {}

def next_prayer(times,now=None):
    now=now or datetime.now()
    found=[]
    for name in PRAYERS:
        try:
            h,m=map(int,times.get(name,"").split(":")[:2])
            target=now.replace(hour=h,minute=m,second=0,microsecond=0)
            if target<=now: target+=timedelta(days=1)
            found.append((target,name))
        except Exception: pass
    return min(found) if found else (None,"")

def countdown(target,now=None):
    if not target:return "--:--:--"
    sec=max(0,int((target-(now or datetime.now())).total_seconds()))
    h,r=divmod(sec,3600); m,s=divmod(r,60)
    return f"{h:02d}:{m:02d}:{s:02d}"

def async_call(fn,ok,err=None,*args):
    def run():
        try:ok(fn(*args))
        except Exception as e:
            if err:err(str(e))
    threading.Thread(target=run,daemon=True).start()
