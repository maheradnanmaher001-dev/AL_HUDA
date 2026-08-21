from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.metrics import dp
from app.utils.responsive import fs
from app.screens.base import ScreenBase
from app.screens.common import header
from app.theme import GOLD,TEXT,MUTED,CARD
class RamadanScreen(ScreenBase):
    def on_enter(self):
        if self.children:return
        root=BoxLayout(orientation="vertical",padding=dp(14),spacing=dp(9));root.add_widget(header("🌙 Ramadan"))
        root.add_widget(Label(text="Sehri  04:15 AM\nIftar  06:50 PM\n\nNext: Iftar in 01:24:35",color=TEXT,font_size=fs(21),halign="center"))
        for x in ("Roza Tracker","Ramadan Calendar","Sehri Notification","Iftar Notification","Daily Ramadan Dua"):
            root.add_widget(Button(text=x,background_normal="",background_color=CARD,color=TEXT,size_hint_y=None,height=dp(48)))
        root.add_widget(Label(text="Ramadan dates are calculated from the selected location/calendar source.",color=MUTED,font_size=fs(11)))
        self.add_widget(root)
