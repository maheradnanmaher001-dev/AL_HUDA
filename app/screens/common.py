from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.metrics import dp
from app.theme import GOLD,TEXT,MUTED,CARD,CARD2
from app.utils.responsive import fs
from app.screens.base import ScreenBase,BottomNavScreen

def header(title, back=None):
    row=BoxLayout(size_hint_y=None,height=dp(58),spacing=dp(8))
    if back:
        b=Button(text="‹",background_normal="",background_color=(0,0,0,0),color=GOLD,font_size=fs(30),size_hint_x=None,width=dp(45))
        b.bind(on_release=lambda *_: back())
        row.add_widget(b)
    row.add_widget(Label(text=title,color=GOLD,font_size=fs(22),bold=True,halign="center"))
    return row

def card_label(text,size=15):
    return Label(text=text,color=TEXT,font_size=fs(size),halign="center",valign="middle")
