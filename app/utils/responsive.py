"""Responsive sizing and user-controlled text scale for AL-HUDA."""
from __future__ import annotations
from kivy.metrics import dp, sp
from kivy.core.window import Window
from kivy.storage.jsonstore import JsonStore
from kivy.clock import Clock

_STORE = JsonStore(".al_huda_settings.json")
DEFAULT_TEXT_SCALE = 1.0
MIN_TEXT_SCALE = 0.80
MAX_TEXT_SCALE = 1.60
STEP = 0.10


def _read_scale() -> float:
    try:
        value = float(_STORE.get("display").get("text_scale", DEFAULT_TEXT_SCALE))
    except Exception:
        value = DEFAULT_TEXT_SCALE
    return max(MIN_TEXT_SCALE, min(MAX_TEXT_SCALE, value))


def get_text_scale() -> float:
    return _read_scale()


def set_text_scale(value: float) -> float:
    old = get_text_scale()
    value = max(MIN_TEXT_SCALE, min(MAX_TEXT_SCALE, round(float(value), 2)))
    _STORE.put("display", text_scale=value)
    _refresh_app_text(old, value)
    return value


def fs(size: float) -> float:
    """Return a Kivy font size adjusted for the user's text-scale setting."""
    return sp(float(size) * get_text_scale())


def adaptive_dp(value: float, reference_width: float = 360.0) -> float:
    """Scale spacing gently with screen width while keeping safe bounds."""
    width = max(240.0, min(1200.0, float(Window.width or reference_width)))
    factor = width / reference_width
    factor = max(0.90, min(1.18, factor))
    return dp(float(value) * factor)


def _refresh_app_text(old_scale=1.0, new_scale=1.0):
    """Update already-created widgets immediately after a text-size change."""
    app = __import__("kivy.app", fromlist=["App"]).App.get_running_app()
    if not app or not getattr(app, "root", None):
        return
    ratio = float(new_scale) / max(float(old_scale), 0.01)
    for widget in app.root.walk():
        if hasattr(widget, "font_size"):
            try:
                widget.font_size = max(sp(8), min(sp(72), widget.font_size * ratio))
            except Exception:
                pass
    setattr(app, "text_scale", new_scale)


def install_responsive_window():
    """Keep a stable UI on very narrow/wide screens; Kivy dp handles density."""
    def _on_resize(_window, width, height):
        app = __import__("kivy.app", fromlist=["App"]).App.get_running_app()
        if app is not None:
            setattr(app, "is_landscape", width > height)
            setattr(app, "screen_width_dp", dp(width))
            setattr(app, "screen_height_dp", dp(height))
            # Keep large headings readable on narrow screens without overriding
            # the user's chosen text scale.
            width_factor = max(0.90, min(1.0, float(width) / 360.0))
            for widget in app.root.walk() if getattr(app, "root", None) else []:
                if hasattr(widget, "font_size") and not hasattr(widget, "_alhuda_base_font"):
                    try:
                        widget._alhuda_base_font = float(widget.font_size)
                    except Exception:
                        pass
                if hasattr(widget, "font_size") and hasattr(widget, "_alhuda_base_font"):
                    try:
                        widget.font_size = widget._alhuda_base_font * width_factor
                    except Exception:
                        pass
    Window.bind(on_resize=_on_resize)
