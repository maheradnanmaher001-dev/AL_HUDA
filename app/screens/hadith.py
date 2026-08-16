import json
from kivy.clock import Clock
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from app.services import hadith_service

class HadithScreen(Screen):
    status=StringProperty("Hadith Collections")

    def on_enter(self): self.show_books()

    def _books(self):
        return json.loads(open("data/hadith_books.json",encoding="utf-8").read())["books"]

    def tile(self,title,sub,cb,h=82):
        b=Button(text=f"{title}\n{sub}",size_hint_y=None,height=h,
                 background_normal="",background_color=(.04,.16,.12,1),
                 color=(.96,.95,.90,1),halign="left",valign="middle")
        b.bind(on_release=lambda *_:cb()); return b

    def show_books(self):
        self.status="Hadith Collections"; self.ids.content.clear_widgets()
        for x in self._books():
            self.ids.content.add_widget(self.tile(
                f'{x["name"]}  •  {x["arabic"]}',x["urdu"],
                lambda bid=x["id"],name=x["name"]:self.open_book(bid,name)))

    def open_book(self,bid,name):
        self.current_book=bid; self.status=f"Loading {name}…"; self.ids.content.clear_widgets()
        hadith_service.async_call(hadith_service.book,self.book_done,self.error,bid,"eng")

    def book_done(self,data):
        def ui(_):
            items=data.get("hadiths",data.get("data",[])) if isinstance(data,dict) else []
            if isinstance(items,dict): items=items.get("hadiths",[])
            self.ids.content.clear_widgets(); self.status=f"{len(items)} Hadiths"
            for raw in items[:300]:
                x=hadith_service.normalize(raw)
                self.ids.content.add_widget(self.tile(
                    f'Hadith {x["number"]}',x["text"][:180] or "Open Hadith",
                    lambda n=x["number"]:self.open_hadith(n),96))
        Clock.schedule_once(ui)

    def search(self):
        q=self.ids.search.text.strip().lower()
        if not q:self.show_books();return
        bid=getattr(self,"current_book","bukhari")
        self.status=f"Searching: {q}"; self.ids.content.clear_widgets()
        hadith_service.async_call(hadith_service.book,self.search_done,self.error,bid,"eng")

    def search_done(self,data):
        q=self.ids.search.text.strip().lower()
        items=data.get("hadiths",data.get("data",[])) if isinstance(data,dict) else []
        if isinstance(items,dict):items=items.get("hadiths",[])
        hits=[hadith_service.normalize(x) for x in items if q in hadith_service.text(x).lower() or q in str(x.get("hadithnumber",x.get("number",""))).lower()]
        self.ids.content.clear_widgets(); self.status=f"{len(hits)} result(s)"
        for x in hits[:100]:
            self.ids.content.add_widget(self.tile(f'Hadith {x["number"]}',x["text"][:180],
                lambda n=x["number"]:self.open_hadith(n),96))

    def open_hadith(self,num):
        bid=getattr(self,"current_book","bukhari"); self.status=f"Hadith {num}"; self.ids.content.clear_widgets()
        hadith_service.async_call(hadith_service.hadith,self.english_done,self.error,bid,num,"eng")

    def english_done(self,eng):
        bid=getattr(self,"current_book","bukhari"); num=hadith_service.normalize(eng)["number"]
        hadith_service.async_call(hadith_service.hadith,
            lambda ara:self.render(eng,ara,bid,num),self.error,bid,num,"ara")
        hadith_service.async_call(hadith_service.hadith,
            lambda urdu:self.add_urdu(urdu),self.error,bid,num,"urd")

    def render(self,eng,ara,bid,num):
        self.ids.content.clear_widgets()
        self.card("العربية",hadith_service.normalize(ara)["text"],True)
        self.card("English",hadith_service.normalize(eng)["text"],False)
        self.ids.content.add_widget(self.tile("Reference",f"{bid} • Hadith {num}",lambda:None,70))
        grade=hadith_service.normalize(eng)["grade"]
        if grade:self.ids.content.add_widget(self.tile("Grade",grade,lambda:None,65))

    def add_urdu(self,urdu): self.card("اردو",hadith_service.normalize(urdu)["text"],True)

    def card(self,title,text,rtl=False):
        box=BoxLayout(orientation="vertical",size_hint_y=None,height=220,padding=10,spacing=4)
        box.add_widget(Label(text=title,size_hint_y=None,height=30,color=(.98,.86,.55,1),font_size="18sp"))
        box.add_widget(Label(text=text or "Text not available.",halign="right" if rtl else "left",
                             valign="middle",text_size=(None,None),color=(.96,.95,.90,1)))
        self.ids.content.add_widget(box)

    def error(self,msg):
        Clock.schedule_once(lambda _:self.show_error(msg))

    def show_error(self,msg):
        self.ids.content.clear_widgets(); self.status="Hadith data error"
        self.ids.content.add_widget(self.tile("Unable to load",msg,self.show_books,100))
