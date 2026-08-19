import json
from pathlib import Path
from dataclasses import dataclass

@dataclass(frozen=True)
class Dhikr:
    name: str
    arabic: str
    urdu: str
    english: str

DHIKR_PRESETS=(
    Dhikr("SubhanAllah","سُبْحَانَ اللَّهِ","اللہ پاک ہے۔","Glory be to Allah."),
    Dhikr("Alhamdulillah","الْحَمْدُ لِلَّهِ","تمام تعریفیں اللہ کے لیے ہیں۔","All praise is for Allah."),
    Dhikr("Allahu Akbar","اللَّهُ أَكْبَرُ","اللہ سب سے بڑا ہے۔","Allah is the Greatest."),
    Dhikr("La ilaha illallah","لَا إِلٰهَ إِلَّا اللَّهُ","اللہ کے سوا کوئی معبود نہیں۔","There is no deity except Allah."),
)

def _file():
    try:
        from kivy.app import App
        return Path(App.get_running_app().user_data_dir)/"tasbeeh_state.json"
    except Exception:
        return Path.home()/".al_huda_tasbeeh_state.json"

def load_state():
    try: return json.loads(_file().read_text(encoding="utf-8"))
    except Exception: return {"count":0,"target":33,"dhikr":"SubhanAllah"}

def save(s):
    p=_file(); p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(s,ensure_ascii=False),encoding="utf-8")

def increment(s):
    s["count"]=int(s.get("count",0))+1; save(s); return s["count"]

def reset(s):
    s["count"]=0; save(s); return 0

def set_target(s,n):
    n=int(n)
    if n<1: raise ValueError("Target must be positive")
    s["target"]=n; save(s); return n

def set_dhikr(s,n):
    s["dhikr"]=n; save(s); return n
