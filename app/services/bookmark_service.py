import json
from pathlib import Path
from dataclasses import dataclass, asdict

@dataclass
class SavedItem:
    item_id: str
    section: str
    title: str
    text: str
    translation: str = ""
    reference: str = ""

def _file():
    try:
        from kivy.app import App
        return Path(App.get_running_app().user_data_dir)/"bookmarks_history.json"
    except Exception:
        return Path.home()/".al_huda_bookmarks_history.json"

def _load():
    try:
        data=json.loads(_file().read_text(encoding="utf-8"))
        return {
            "bookmarks": data.get("bookmarks", []),
            "history": data.get("history", [])
        }
    except Exception:
        return {"bookmarks": [], "history": []}

def _save(data):
    p=_file(); p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding="utf-8")

def add_bookmark(item):
    data=_load()
    if not any(x.get("item_id")==item.item_id for x in data["bookmarks"]):
        data["bookmarks"].insert(0,asdict(item))
        _save(data)
        return True
    return False

def remove_bookmark(item_id):
    data=_load()
    old=len(data["bookmarks"])
    data["bookmarks"]=[x for x in data["bookmarks"] if x.get("item_id")!=item_id]
    _save(data)
    return len(data["bookmarks"])<old

def is_bookmarked(item_id):
    return any(x.get("item_id")==item_id for x in _load()["bookmarks"])

def get_bookmarks():
    return _load()["bookmarks"]

def add_history(item, limit=100):
    data=_load()
    data["history"]=[x for x in data["history"] if x.get("item_id")!=item.item_id]
    data["history"].insert(0,asdict(item))
    data["history"]=data["history"][:limit]
    _save(data)

def get_history():
    return _load()["history"]

def clear_history():
    data=_load()
    data["history"]=[]
    _save(data)
