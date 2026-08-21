from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.metrics import dp
from app.utils.responsive import fs
from app.screens.base import ScreenBase
from app.screens.common import header
from app.theme import GOLD,TEXT,MUTED,CARD

BOOKS=["Sahih al-Bukhari","Sahih Muslim","Sunan Abu Dawud","Jami' at-Tirmidhi","Sunan an-Nasa'i","Sunan Ibn Majah","Muwatta Malik","Musnad Ahmad","Sunan ad-Darimi"]
class HadithScreen(ScreenBase):
    def on_enter(self):
        if self.children:return
        root=BoxLayout(orientation="vertical",padding=dp(12),spacing=dp(7))
        root.add_widget(header("الحديث الشريف"))
        root.add_widget(Button(text="⌕ Search Hadith / Rawi / Reference",background_normal="",background_color=CARD,color=TEXT,size_hint_y=None,height=dp(46)))
        for bname in BOOKS:
            b=Button(text=f"▣  {bname}   ›",background_normal="",background_color=CARD,color=TEXT,size_hint_y=None,height=dp(50))
            b.bind(on_release=lambda *_:self.go("hadith_detail"));root.add_widget(b)
        root.add_widget(Label(text="Arabic • Urdu • English • Number • Chapter • Reference • Rawi • Grade",color=MUTED,font_size=fs(11)))
        self.add_widget(root)

class HadithDetailScreen(ScreenBase):
    def on_enter(self):
        if self.children:return
        root=BoxLayout(orientation="vertical",padding=dp(14),spacing=dp(9))
        root.add_widget(header("Sahih al-Bukhari • Hadith 1",lambda:self.go("hadith")))
        root.add_widget(Label(text="[Verified Arabic Hadith]\n\n[Verified Urdu translation]\n\n[Verified English translation]",color=TEXT,font_size=fs(17),halign="center"))
        root.add_widget(Label(text="Narrator: [source metadata]\nReference: Sahih al-Bukhari, Book / Chapter\nGrade: [source metadata]",color=MUTED,font_size=fs(13),halign="center"))
        row=BoxLayout(size_hint_y=None,height=dp(48),spacing=dp(6))
        for x in ("🔖 Bookmark","📝 Note","↗ Share"):
            row.add_widget(Button(text=x,background_normal="",background_color=CARD,color=GOLD))
        root.add_widget(row);self.add_widget(root)
