"""AL-HUDA Step 15 - reusable UI animation helpers.

Designed to be additive: existing screens can import these helpers without
changing the project's existing navigation/data services.
"""

from kivy.animation import Animation


class UIAnimationService:
    """Central animation presets for AL-HUDA screens/widgets."""

    @staticmethod
    def fade_in(widget, duration=0.25):
        widget.opacity = 0
        Animation(opacity=1, duration=duration, t="out_quad").start(widget)

    @staticmethod
    def fade_out(widget, duration=0.20):
        Animation(opacity=0, duration=duration, t="in_quad").start(widget)

    @staticmethod
    def slide_in(widget, x=None, y=None, duration=0.28):
        """Slide a widget from its current position offset by x/y pixels."""
        if x is None:
            x = 0
        if y is None:
            y = 0
        target_x, target_y = widget.x, widget.y
        widget.pos = (target_x + x, target_y + y)
        Animation(x=target_x, y=target_y, duration=duration,
                  t="out_cubic").start(widget)

    @staticmethod
    def scale_in(widget, start_scale=0.92, duration=0.25):
        """Scale a widget into view when it exposes scale_x/scale_y."""
        if hasattr(widget, "scale_x") and hasattr(widget, "scale_y"):
            widget.scale_x = start_scale
            widget.scale_y = start_scale
            Animation(scale_x=1, scale_y=1, duration=duration,
                      t="out_back").start(widget)

    @staticmethod
    def press(widget, duration=0.10):
        """Small press feedback for widgets that expose scale_x/scale_y."""
        if hasattr(widget, "scale_x") and hasattr(widget, "scale_y"):
            Animation(scale_x=0.96, scale_y=0.96, duration=duration).start(widget)
            Animation(scale_x=1, scale_y=1, duration=duration).start(widget)

    @staticmethod
    def stop(widget):
        """Stop animations started by this helper."""
        Animation.cancel_all(widget)
