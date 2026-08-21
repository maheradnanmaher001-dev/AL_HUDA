from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.metrics import dp
from app.utils.responsive import fs
from app.screens.base import ScreenBase
from app.screens.common import header
from app.theme import GOLD,TEXT,MUTED,CARD

class PrayerScreen(ScreenBase):
    def on_enter(self):
        if self.children:return
        root=BoxLayout(orientation="vertical",padding=dp(14),spacing=dp(7))
        root.add_widget(header("Prayer Times"))
        root.add_widget(Button(text="📍 GPS Location • Islamabad, Pakistan",background_normal="",background_color=CARD,color=TEXT,size_hint_y=None,height=dp(48)))
        for n,t in [("Fajr","04:15 AM"),("Sunrise","05:40 AM"),("Zuhr","12:20 PM"),("Asr","05:05 PM"),("Maghrib","06:50 PM"),("Isha","08:20 PM")]:
            root.add_widget(Label(text=f"{n}     {t}",color=TEXT,font_size=fs(17),size_hint_y=None,height=dp(42)))
        root.add_widget(Label(text="Notifications: ON\nShort Adhan: ON • Stop from notification/lock screen\nAdjustments & calculation method available in Settings",color=MUTED,font_size=fs(13),halign="center"))
        self.add_widget(root)
