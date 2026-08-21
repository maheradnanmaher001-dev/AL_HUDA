from kivy.animation import Animation
from kivy.properties import NumericProperty
from kivy.uix.widget import Widget

def fade_in(widget, duration=0.35):
    widget.opacity = 0
    Animation(opacity=1, duration=duration, t="out_quad").start(widget)

def slide_in(widget, x_offset=80, duration=0.35):
    target_x = widget.x
    widget.x = target_x + x_offset
    Animation(x=target_x, opacity=1, duration=duration, t="out_cubic").start(widget)

def pop_in(widget, duration=0.28):
    widget.opacity = 0
    old = widget.scale if hasattr(widget, "scale") else 1
    Animation(opacity=1, duration=duration, t="out_quad").start(widget)
