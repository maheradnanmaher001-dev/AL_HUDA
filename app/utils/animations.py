from kivy.animation import Animation

def fade_in(widget,duration=.28):
    widget.opacity=0
    Animation(opacity=1,duration=duration,t='out_quad').start(widget)

def slide_in(widget,duration=.30):
    x=widget.x
    widget.x=x+28
    Animation(x=x,opacity=1,duration=duration,t='out_cubic').start(widget)
