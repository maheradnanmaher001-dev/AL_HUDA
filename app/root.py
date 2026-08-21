from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.metrics import dp
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from app.theme import NAV_BG,GOLD

class AppRoot(BoxLayout):
    def __init__(self, manager, **kwargs):
        super().__init__(orientation="vertical", **kwargs)
        self.manager_ref=manager
        self.add_widget(manager)
        bar=BoxLayout(size_hint_y=None,height=dp(62),padding=dp(4),spacing=dp(3))
        for text,name in [("Home","home"),("Quran","quran"),("Hadith","hadith"),("Prayer","prayer"),("Qibla","qibla"),("More","settings")]:
            b=Button(text=text,background_normal="",background_color=NAV_BG,color=GOLD,font_size="10sp",bold=True)
            b.bind(on_release=lambda _,n=name:self.go(n))
            bar.add_widget(b)
        self.add_widget(bar)
    def go(self,name):
        self.manager_ref.transition.direction="left" if name != self.manager_ref.current else "right"
        self.manager_ref.current=name
