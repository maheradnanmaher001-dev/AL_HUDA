from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp
from app.utils.responsive import fs
from app.theme import GOLD,TEXT

class SplashScreen(Screen):
    def on_enter(self):
        box=BoxLayout(orientation="vertical",padding=dp(28),spacing=dp(10))
        box.add_widget(Image(source="assets/icon.png",allow_stretch=True,keep_ratio=True))
        box.add_widget(Label(text="AL-HUDA",font_size=fs(32),bold=True,color=GOLD,size_hint_y=None,height=dp(60)))
        box.add_widget(Label(text="Quran • Hadith • Prayer • Qibla",font_size=fs(13),color=TEXT,size_hint_y=None,height=dp(35)))
        self.add_widget(box)
