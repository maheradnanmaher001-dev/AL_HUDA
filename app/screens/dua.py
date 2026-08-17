from kivy.properties import StringProperty, NumericProperty
from kivy.uix.screenmanager import Screen
from app.services.dua_service import all_duas, search, CATEGORIES

class DuaScreen(Screen):
    selected_category=StringProperty("All")
    count=NumericProperty(0)

    def on_enter(self):
        self.refresh()

    def refresh(self):
        q=self.ids.search.text if "search" in self.ids else ""
        items=search(q)
        if self.selected_category!="All":
            items=[d for d in items if d.category==self.selected_category]
        self.count=len(items)
        if "results" in self.ids:
            self.ids.results.text="\n\n".join(
                f"{d.title}\n{d.arabic}\n{d.urdu}\n{d.english}\nReference: {d.reference}"
                for d in items
            ) or "No duas found."

    def clear_search(self):
        self.ids.search.text=""
        self.refresh()
