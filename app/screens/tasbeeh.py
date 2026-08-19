from kivy.properties import NumericProperty,StringProperty,BooleanProperty
from kivy.animation import Animation
from kivy.uix.screenmanager import Screen
from app.services.tasbeeh_service import load_state,increment,reset,set_target,set_dhikr

class TasbeehScreen(Screen):
    count=NumericProperty(0); target=NumericProperty(33); progress=NumericProperty(0)
    dhikr=StringProperty("SubhanAllah"); status=StringProperty("Tap to count")
    vibration_enabled=BooleanProperty(True)

    def on_enter(self):
        self.state=load_state()
        self.count=int(self.state.get("count",0)); self.target=int(self.state.get("target",33))
        self.dhikr=self.state.get("dhikr","SubhanAllah"); self.update_progress()

    def tap(self):
        self.count=increment(self.state); self.update_progress()
        self.status="Target reached — MashaAllah!" if self.count>=self.target else "Keep going"
        if "tap_button" in self.ids:
            Animation.cancel_all(self.ids.tap_button)
            (Animation(scale=0.96,duration=.06)+Animation(scale=1,duration=.10)).start(self.ids.tap_button)
        if self.vibration_enabled: self.vibrate()

    def reset_count(self):
        self.count=reset(self.state); self.update_progress(); self.status="Counter reset"

    def choose_target(self,n):
        try: self.target=set_target(self.state,n); self.update_progress()
        except Exception: self.status="Invalid target"

    def choose_dhikr(self,n):
        self.dhikr=set_dhikr(self.state,n); self.status=n+" selected"

    def update_progress(self): self.progress=min(1,self.count/float(self.target or 1))

    def toggle_vibration(self): self.vibration_enabled=not self.vibration_enabled

    def vibrate(self):
        try:
            from kivy.utils import platform
            if platform!="android": return
            from jnius import autoclass
            A=autoclass("org.kivy.android.PythonActivity")
            C=autoclass("android.content.Context")
            A.mActivity.getSystemService(C.VIBRATOR_SERVICE).vibrate(20)
        except Exception: pass
