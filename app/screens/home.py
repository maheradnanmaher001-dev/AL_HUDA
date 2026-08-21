from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.metrics import dp
from app.utils.responsive import fs
from app.screens.base import BottomNavScreen
from app.screens.common import header
from app.theme import GOLD,TEXT,MUTED,CARD

class HomeScreen(BottomNavScreen):
    def on_enter(self):
        if self.children:return
        root=BoxLayout(orientation="vertical",padding=dp(14),spacing=dp(10))
        root.add_widget(header("AL-HUDA"))
        root.add_widget(Label(text="السلام علیکم",color=GOLD,font_size=fs(24),size_hint_y=None,height=dp(48)))
        root.add_widget(Label(text="16 August 2026  •  3 Safar 1448",color=MUTED,font_size=fs(13),size_hint_y=None,height=dp(30)))
        root.add_widget(Label(text="NEXT PRAYER\n\nAsr   01:24:35\n\nFajr  04:15 AM    Zuhr  12:20 PM\nAsr   05:05 PM    Maghrib 06:50 PM\nIsha  08:20 PM",
                              color=TEXT,font_size=fs(16),halign="center",size_hint_y=None,height=dp(170)))
        for txt, dest in [("📖 Continue Quran","quran"),("📚 Daily Hadith","hadith"),("🧭 Qibla","qibla"),("📅 Calendar","calendar")]:
            b=Button(text=txt,background_normal="",background_color=CARD,color=TEXT,size_hint_y=None,height=dp(46))
            b.bind(on_release=lambda _,d=dest:self.go(d)); root.add_widget(b)
        root.add_widget(Label(text="Daily Ayah • Daily Hadith • Daily Dua",color=MUTED,font_size=fs(13)))
        self.add_widget(root)
