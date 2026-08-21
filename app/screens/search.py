from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.metrics import dp
from app.utils.responsive import fs
from app.screens.base import ScreenBase
from app.screens.common import header
from app.theme import GOLD,TEXT,MUTED,CARD
class SearchScreen(ScreenBase):
    def on_enter(self):
        if self.children:return
        root=BoxLayout(orientation="vertical",padding=dp(14),spacing=dp(8))
        root.add_widget(header("Universal Search"))
        root.add_widget(TextInput(hint_text="Search Quran, Hadith, Surah, Para, Book, Rawi...",multiline=False,size_hint_y=None,height=dp(52)))
        tabs=BoxLayout(size_hint_y=None,height=dp(45),spacing=dp(4))
        for t in ("Quran","Hadith","Surah","Para","Books"):
            tabs.add_widget(Button(text=t,background_normal="",background_color=CARD,color=GOLD))
        root.add_widget(tabs)
        root.add_widget(Label(text="Search Arabic • Urdu • English • Hadith number • narrator • reference",color=MUTED,font_size=fs(13)))
        self.add_widget(root)
