from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.metrics import dp
from app.utils.responsive import fs
from app.screens.base import ScreenBase
from app.screens.common import header
from app.theme import GOLD,TEXT,CARD
class TasbeehScreen(ScreenBase):
    count=0
    def on_enter(self):
        if self.children:return
        root=BoxLayout(orientation="vertical",padding=dp(20),spacing=dp(12));root.add_widget(header("Tasbeeh"))
        label=Label(text="0",color=GOLD,font_size=fs(70))
        def add(*_): self.count+=1;label.text=str(self.count)
        b=Button(text="TAP TO COUNT",background_normal="",background_color=CARD,color=GOLD,font_size=fs(22))
        b.bind(on_release=add);root.add_widget(label);root.add_widget(b)
        for x in ("33","100","Custom","Reset"):
            root.add_widget(Button(text=x,background_normal="",background_color=CARD,color=TEXT,size_hint_y=None,height=dp(45)))
        self.add_widget(root)
