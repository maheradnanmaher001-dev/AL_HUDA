from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.metrics import dp
from app.utils.responsive import fs
from app.screens.base import ScreenBase
from app.screens.common import header
from app.theme import GOLD,TEXT,MUTED,CARD
class QiblaScreen(ScreenBase):
    def on_enter(self):
        if self.children:return
        root=BoxLayout(orientation="vertical",padding=dp(14),spacing=dp(9))
        root.add_widget(header("🕋 Qibla Compass"))
        root.add_widget(Label(text="             N\n             ↑\n      W  ←  🕋  →  E\n             ↓\n             S",color=GOLD,font_size=fs(27),halign="center"))
        root.add_widget(Label(text="Bearing: --°\nDistance to Kaaba: -- km",color=TEXT,font_size=fs(18),halign="center"))
        root.add_widget(Button(text="⌖ Calibrate Compass",background_normal="",background_color=CARD,color=GOLD,size_hint_y=None,height=dp(50)))
        root.add_widget(Label(text="Live phone sensor + GPS service is ready for implementation.",color=MUTED,font_size=fs(12)))
        self.add_widget(root)
