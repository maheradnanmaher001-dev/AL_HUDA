from kivy.clock import Clock
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from app.services import quran_service

class QuranScreen(Screen):
    status = StringProperty("114 Surahs")

    def on_enter(self):
        self.show_surah_list()

    def _metadata(self):
        return __import__("json").loads(open("data/quran_metadata.json",encoding="utf-8").read())

    def _tile(self,title,subtitle,callback):
        b=Button(text=f"{title}\n{subtitle}",size_hint_y=None,height=76,
                 background_normal="",background_color=(.04,.16,.12,1),
                 color=(.96,.95,.90,1),halign="left",valign="middle")
        b.bind(on_release=lambda *_: callback())
        return b

    def show_surah_list(self):
        self.status="114 Surahs"
        self.ids.content.clear_widgets()
        for x in self._metadata()["surahs"]:
            self.ids.content.add_widget(self._tile(
                f'{x["number"]}. {x["english"]}  |  {x["arabic"]}',
                f'{x["ayahs"]} Ayahs • {x["revelation"]}',
                lambda n=x["number"]: self.open_surah(n)))

    def show_juz_list(self):
        self.status="30 Paras / Juz"
        self.ids.content.clear_widgets()
        for x in self._metadata()["juz"]:
            self.ids.content.add_widget(self._tile(
                f'Juz {x["number"]}',f'{x["start"]} → {x["end"]}',
                lambda n=x["number"]: self.open_juz(n)))

    def search(self):
        q=self.ids.search.text.strip()
        if not q:
            self.show_surah_list(); return
        self.status=f"Searching: {q}"
        self.ids.content.clear_widgets()
        quran_service.async_call(quran_service.search_quran,self._search_done,self._error,q)

    def _search_done(self,data):
        matches=data.get("data",{}).get("matches",[])
        def ui(_):
            self.ids.content.clear_widgets()
            self.status=f"{len(matches)} result(s)"
            for m in matches[:100]:
                s=m.get("surah",{})
                self.ids.content.add_widget(self._tile(
                    f'{s.get("number","?")}:{m.get("numberInSurah","?")} • {s.get("englishName","")}',
                    m.get("text",""),lambda n=s.get("number",1): self.open_surah(n)))
        Clock.schedule_once(ui)

    def open_surah(self,n):
        self.status="Loading Quran…"
        self.ids.content.clear_widgets()
        quran_service.async_call(quran_service.get_surah,self._reader_done,self._error,n)

    def open_juz(self,n):
        self.status=f"Loading Juz {n}…"
        self.ids.content.clear_widgets()
        quran_service.async_call(quran_service.get_juz,self._juz_done,self._error,n)

    def _reader_done(self,data):
        def ui(_):
            ed=data.get("data",[])
            if len(ed)<3:
                self._error("Quran editions were not returned."); return
            self.ids.content.clear_widgets()
            self.status=f'{ed[0].get("englishName","Quran")} • {len(ed[0].get("ayahs",[]))} Ayahs'
            for i,a in enumerate(ed[0].get("ayahs",[])):
                u=ed[1].get("ayahs",[])[i].get("text","")
                e=ed[2].get("ayahs",[])[i].get("text","")
                box=BoxLayout(orientation="vertical",size_hint_y=None,height=245,spacing=5,padding=10)
                box.add_widget(Label(text=f'﴿ {a.get("numberInSurah",i+1)} ﴾',size_hint_y=None,height=28,color=(.98,.86,.55,1)))
                box.add_widget(Label(text=a.get("text",""),font_size="23sp",halign="right",valign="middle",text_size=(None,None),size_hint_y=None,height=85,color=(.98,.95,.88,1)))
                box.add_widget(Label(text=f"اردو: {u}",halign="right",valign="middle",text_size=(None,None),size_hint_y=None,height=58,color=(.88,.91,.87,1)))
                box.add_widget(Label(text=f"English: {e}",valign="middle",text_size=(None,None),size_hint_y=None,height=58,color=(.76,.82,.78,1)))
                self.ids.content.add_widget(box)
        Clock.schedule_once(ui)

    def _juz_done(self,data):
        def ui(_):
            ayahs=data.get("data",{}).get("ayahs",[])
            self.ids.content.clear_widgets()
            self.status=f'Juz {data.get("data",{}).get("number","")} • {len(ayahs)} Ayahs'
            for a in ayahs:
                self.ids.content.add_widget(self._tile(
                    f'Ayah {a.get("numberInSurah","")}',a.get("text",""),lambda: None))
        Clock.schedule_once(ui)

    def _error(self,msg):
        Clock.schedule_once(lambda _: self._show_error(msg))

    def _show_error(self,msg):
        self.ids.content.clear_widgets()
        self.status="Unable to load Quran data"
        self.ids.content.add_widget(self._tile("Network/API error",msg,self.show_surah_list))
