from kivy.properties import ColorProperty
from kivy.app import App
from app.utils.responsive import get_text_scale, set_text_scale, MIN_TEXT_SCALE, MAX_TEXT_SCALE, STEP, install_responsive_window

BG=(0.012,0.055,0.043,1)
NAV_BG=(0.018,0.085,0.065,1)
CARD=(0.028,0.12,0.092,1)
CARD2=(0.05,0.18,0.135,1)
GOLD=(0.95,0.76,0.22,1)
TEXT=(0.95,0.95,0.91,1)
MUTED=(0.62,0.70,0.66,1)

class ThemeMixin:
    @property
    def colors(self):
        return BG,CARD,CARD2,GOLD,TEXT,MUTED

def install_theme_properties(app):
    app.bg=BG; app.nav_bg=NAV_BG; app.card=CARD; app.card2=CARD2
    app.gold=GOLD; app.text=TEXT; app.muted=MUTED
    app.text_scale = get_text_scale()
    app.min_text_scale = MIN_TEXT_SCALE
    app.max_text_scale = MAX_TEXT_SCALE
    install_responsive_window()
