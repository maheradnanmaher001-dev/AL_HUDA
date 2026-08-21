from kivy.uix.screen import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.metrics import dp
from app.screens.base import ScreenBase
from app.screens.common import header
from app.theme import GOLD,TEXT,MUTED,CARD
from app.utils.responsive import get_text_scale, set_text_scale, MIN_TEXT_SCALE, MAX_TEXT_SCALE, STEP, fs

class SettingsScreen(ScreenBase):
    def on_enter(self):
        if self.children:return
        root=BoxLayout(orientation="vertical",padding=dp(12),spacing=dp(7));root.add_widget(header("Settings & More"))
        self._add_font_control(root)
        opts=["👤 Account / Login","🌐 Language • اردو | English | العربية","🎨 Theme • Dark / Light","🔔 Prayer Notifications","🕌 Short Adhan • ON/OFF","⏱ Prayer Time Method & Adjustments","🔖 Bookmarks","📜 History & Notes","📥 Offline Data","☁ Cloud Sync","🌙 Ramadan","🤲 Dua & Azkar","📿 Tasbeeh","📅 Islamic & Gregorian Calendar","ℹ About AL-HUDA","🔐 Privacy & Security"]
        for x in opts:
            root.add_widget(Button(text=x,background_normal="",background_color=CARD,color=TEXT,size_hint_y=None,height=dp(45),font_size=fs(14)))
        self.add_widget(root)

    def _add_font_control(self, root):
        box=BoxLayout(orientation="vertical",size_hint_y=None,height=dp(118),spacing=dp(4))
        title=Label(text="🔤 Text Size",color=GOLD,font_size=fs(17),bold=True,size_hint_y=None,height=dp(28))
        value=Label(color=TEXT,font_size=fs(14),size_hint_y=None,height=dp(25))
        row=BoxLayout(size_hint_y=None,height=dp(48),spacing=dp(6))
        minus=Button(text="A−",background_normal="",background_color=CARD,color=TEXT,font_size=fs(16))
        plus=Button(text="A+",background_normal="",background_color=CARD,color=TEXT,font_size=fs(16))
        reset=Button(text="Reset",background_normal="",background_color=CARD,color=TEXT,font_size=fs(14))
        def refresh(*_):
            value.text=f"{int(round(get_text_scale()*100))}%"
            for widget, base in ((title,17),(value,14),(minus,16),(plus,16),(reset,14)):
                widget.font_size=fs(base)
        def change(delta):
            set_text_scale(get_text_scale()+delta); refresh()
        minus.bind(on_release=lambda *_: change(-STEP))
        plus.bind(on_release=lambda *_: change(STEP))
        reset.bind(on_release=lambda *_: (set_text_scale(1.0), refresh()))
        row.add_widget(minus);row.add_widget(value);row.add_widget(plus);row.add_widget(reset)
        box.add_widget(title);box.add_widget(value);box.add_widget(row)
        root.add_widget(box)
