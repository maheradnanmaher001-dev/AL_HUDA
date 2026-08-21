from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.metrics import dp
from app.utils.responsive import fs
from app.screens.base import ScreenBase
from app.screens.common import header
from app.theme import GOLD,TEXT,MUTED,CARD
class CalendarScreen(ScreenBase):
    def on_enter(self):
        if self.children:return
        root=BoxLayout(orientation="vertical",padding=dp(12),spacing=dp(8));root.add_widget(header("Calendar"))
        tabs=BoxLayout(size_hint_y=None,height=dp(48),spacing=dp(5))
        for x in ("Islamic","Gregorian"):
            tabs.add_widget(Button(text=x,background_normal="",background_color=CARD,color=GOLD))
        root.add_widget(tabs)
        root.add_widget(Label(text="August 2026\n\nMon  Tue  Wed  Thu  Fri  Sat  Sun\n 27   28   29   30   31    1    2\n  3    4    5    6    7    8    9\n 10   11   12   13   14   15   16\n 17   18   19   20   21   22   23\n 24   25   26   27   28   29   30\n 31",color=TEXT,font_size=fs(17),halign="center"))
        root.add_widget(Label(text="Selected date → Hijri conversion • Prayer times • Islamic events • Notes",color=MUTED,font_size=fs(12)))
        self.add_widget(root)
