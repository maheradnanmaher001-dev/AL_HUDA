from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.metrics import dp
from app.utils.responsive import fs
from app.screens.base import ScreenBase
from app.screens.common import header
from app.theme import GOLD,TEXT,CARD
class DuaScreen(ScreenBase):
    def on_enter(self):
        if self.children:return
        root=BoxLayout(orientation="vertical",padding=dp(14),spacing=dp(7));root.add_widget(header("Dua & Azkar"))
        for x in ["Morning Azkar","Evening Azkar","After Salah","Sleep","Travel","Protection","Forgiveness","Rizq","Difficulty","Quranic Duas"]:
            root.add_widget(Button(text=x,background_normal="",background_color=CARD,color=TEXT,size_hint_y=None,height=dp(47)))
        root.add_widget(Label(text="Arabic • Urdu • English • Verified reference",color=GOLD,font_size=fs(12)))
        self.add_widget(root)
