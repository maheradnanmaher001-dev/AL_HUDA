from kivy.properties import StringProperty, ListProperty, BooleanProperty
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from app.services.search_service import search_all

class SearchScreen(Screen):
    query=StringProperty("")
    section=StringProperty("All")
    results=ListProperty([])
    searching=BooleanProperty(False)

    def on_enter(self):
        if "search_input" in self.ids:
            self.ids.search_input.focus=False

    def run_search(self):
        self.query=self.ids.search_input.text.strip()
        self.searching=True
        Clock.schedule_once(lambda dt:self._do_search(),0)

    def _do_search(self):
        try:
            rows=search_all(self.query)
            if self.section!="All":
                rows=[r for r in rows if r.section==self.section]
            self.results=rows
            self._render()
        finally:
            self.searching=False

    def set_section(self, section):
        self.section=section
        self.run_search()

    def clear(self):
        self.ids.search_input.text=""
        self.query=""
        self.results=[]
        self._render()

    def _render(self):
        if "result_label" not in self.ids: return
        if not self.query:
            self.ids.result_label.text="Search Quran, Hadith or Duas"
            return
        if not self.results:
            self.ids.result_label.text="No results found."
            return
        chunks=[]
        for r in self.results[:100]:
            ref=f"\\nReference: {r.reference}" if r.reference else ""
            chunks.append(f"[{r.section}] {r.title}\\n{r.text}\\n{r.subtitle}{ref}")
        self.ids.result_label.text="\\n\\n".join(chunks)
