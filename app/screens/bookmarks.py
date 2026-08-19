from kivy.properties import StringProperty, ListProperty
from kivy.uix.screenmanager import Screen
from app.services.bookmark_service import get_bookmarks, get_history, clear_history, remove_bookmark

class BookmarkScreen(Screen):
    mode=StringProperty("Bookmarks")
    items=ListProperty([])

    def on_enter(self):
        self.refresh()

    def set_mode(self, mode):
        self.mode=mode
        self.refresh()

    def refresh(self):
        self.items=get_bookmarks() if self.mode=="Bookmarks" else get_history()
        self.render()

    def delete_bookmark(self, item_id):
        remove_bookmark(item_id)
        self.refresh()

    def clear_history_items(self):
        clear_history()
        self.refresh()

    def render(self):
        if "result_label" not in self.ids: return
        if not self.items:
            self.ids.result_label.text="No saved items yet."
            return
        rows=[]
        for x in self.items:
            ref=f"\nReference: {x.get('reference','')}" if x.get("reference") else ""
            trans=x.get("translation","")
            rows.append(f"[{x.get('section','')}] {x.get('title','')}\n{x.get('text','')}\n{trans}{ref}")
        self.ids.result_label.text="\n\n".join(rows)
