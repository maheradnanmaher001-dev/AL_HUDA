from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.metrics import dp
from app.utils.responsive import fs
from app.screens.base import ScreenBase
from app.screens.common import header
from app.theme import GOLD,TEXT,MUTED,CARD

S=[("1","Al-Fatihah","الفاتحة","7"),("2","Al-Baqarah","البقرة","286"),("3","Aal-Imran","آل عمران","200"),("4","An-Nisa","النساء","176"),("5","Al-Ma'idah","المائدة","120"),("6","Al-An'am","الأنعام","165"),("7","Al-A'raf","الأعراف","206"),("8","Al-Anfal","الأنفال","75"),("9","At-Tawbah","التوبة","129"),("10","Yunus","يونس","109")]
class QuranScreen(ScreenBase):
    def on_enter(self):
        if self.children:return
        root=BoxLayout(orientation="vertical",padding=dp(12),spacing=dp(7))
        root.add_widget(header("القرآن الكريم"))
        tabs=BoxLayout(size_hint_y=None,height=dp(46),spacing=dp(6))
        for t in ("Surah","Para (Juz)"):
            tabs.add_widget(Button(text=t,background_normal="",background_color=CARD,color=GOLD))
        root.add_widget(tabs)
        root.add_widget(Button(text="⌕ Search Surah / Ayah",background_normal="",background_color=CARD,color=TEXT,size_hint_y=None,height=dp(46)))
        for n,en,ar,c in S:
            b=Button(text=f"{n}. {en}   |   {ar}   |   {c} Ayat",background_normal="",background_color=CARD,color=TEXT,size_hint_y=None,height=dp(48))
            b.bind(on_release=lambda *_: self.go("quran_reader"));root.add_widget(b)
        root.add_widget(Label(text="Full dataset loader: 114 Surahs + 30 Paras/Juz.",color=MUTED,font_size=fs(12)))
        self.add_widget(root)

class QuranReaderScreen(ScreenBase):
    def on_enter(self):
        if self.children:return
        root=BoxLayout(orientation="vertical",padding=dp(14),spacing=dp(10))
        root.add_widget(header("Al-Baqarah • Ayah 255",lambda:self.go("quran")))
        root.add_widget(Label(text="اللَّهُ لَا إِلَٰهَ إِلَّا هُوَ الْحَيُّ الْقَيُّومُ\n\n[Verified Arabic Quran dataset loads here]",color=TEXT,font_size=fs(22),halign="center",valign="middle"))
        root.add_widget(Label(text="Urdu translation\n[Verified translation loads here]\n\nEnglish translation\n[Verified translation loads here]",color=TEXT,font_size=fs(15),halign="center"))
        row=BoxLayout(size_hint_y=None,height=dp(48),spacing=dp(6))
        for x in ("‹ Previous","🔖 Bookmark","▶ Play","Next ›"):
            row.add_widget(Button(text=x,background_normal="",background_color=CARD,color=GOLD))
        root.add_widget(row); self.add_widget(root)
