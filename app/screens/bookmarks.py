from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.metrics import dp
from app.utils.responsive import fs
from app.screens.base import ScreenBase
from app.screens.common import header
from app.theme import GOLD,TEXT,CARD
class BookmarksScreen(ScreenBase):
    def on_enter(self):
        if self.children:return
        root=BoxLayout(orientation="vertical",padding=dp(14),spacing=dp(8));root.add_widget(header("My Bookmarks"))
        for x in ["Quran • Al-Baqarah 255","Hadith • Bukhari 1","Dua • Morning","Notes"]:
            root.add_widget(Button(text=x,background_normal="",background_color=CARD,color=TEXT,size_hint_y=None,height=dp(50)))
        root.add_widget(Label(text="Cloud sync when the user is signed in.",color=GOLD,font_size=fs(12)))
        self.add_widget(root)
