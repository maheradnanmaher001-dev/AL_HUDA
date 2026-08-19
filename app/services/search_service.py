from dataclasses import dataclass
from pathlib import Path
import json

@dataclass
class SearchResult:
    section: str
    title: str
    subtitle: str
    text: str
    reference: str = ""

def _read_json_candidates(folder):
    folder=Path(folder)
    if not folder.exists():
        return []
    items=[]
    for p in sorted(folder.rglob("*.json")):
        try:
            data=json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        if isinstance(data,list):
            items.extend(data)
        elif isinstance(data,dict):
            for key in ("data","items","results","surahs","hadith"):
                value=data.get(key)
                if isinstance(value,list):
                    items.extend(value)
    return items

def _stringify(value):
    if value is None: return ""
    if isinstance(value,(str,int,float,bool)): return str(value)
    if isinstance(value,list): return " ".join(_stringify(x) for x in value)
    if isinstance(value,dict): return " ".join(_stringify(v) for v in value.values())
    return str(value)

def _search_items(items, section, query):
    q=query.casefold().strip()
    out=[]
    for item in items:
        blob=_stringify(item)
        if q not in blob.casefold():
            continue
        title=(item.get("name") or item.get("title") or item.get("surah")
               or item.get("book") or item.get("collection") or section)
        subtitle=(item.get("translation") or item.get("urdu")
                  or item.get("english") or item.get("reference") or "")
        text=(item.get("text") or item.get("arabic") or item.get("hadith")
              or item.get("ayah") or item.get("content") or blob)
        ref=(item.get("reference") or item.get("number") or item.get("hadith_number") or "")
        out.append(SearchResult(section,str(title),str(subtitle),str(text),str(ref)))
    return out

def search_all(query, data_root="data"):
    if not query or not query.strip():
        return []
    root=Path(data_root)
    results=[]
    results += _search_items(_read_json_candidates(root/"quran"),"Quran",query)
    results += _search_items(_read_json_candidates(root/"hadith"),"Hadith",query)
    results += _search_items(_read_json_candidates(root/"duas"),"Duas",query)
    # Current Step 8/9 service data fallbacks.
    try:
        from app.services.dua_service import search as dua_search
        for d in dua_search(query):
            results.append(SearchResult("Duas",d.title,d.urdu,d.arabic,d.reference))
    except Exception:
        pass
    return results

def search_section(query, section, data_root="data"):
    section=section.casefold()
    all_results=search_all(query,data_root)
    return [r for r in all_results if r.section.casefold()==section]
