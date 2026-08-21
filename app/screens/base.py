from kivy.uix.screen import Screen
from kivy.properties import ListProperty
from kivy.app import App
from app.animations import fade_in, slide_in

class ScreenBase(Screen):
    def on_pre_enter(self, *args):
        for child in self.walk():
            if child is not self:
                try: child.opacity = 0
                except Exception: pass
        return super().on_pre_enter(*args)

    def on_enter(self, *args):
        for child in self.children:
            try: fade_in(child, .3)
            except Exception: pass
        return super().on_enter(*args)

    def go(self, name):
        self.manager.transition.direction = "left" if name != self.manager.current else "right"
        self.manager.current = name

class BottomNavScreen(ScreenBase):
    pass

class HeaderMixin:
    pass
