from kivy.clock import Clock
from kivy.properties import NumericProperty, StringProperty
from kivy.uix.screenmanager import Screen
from app.services.qibla_service import qibla_bearing, direction_name, QiblaSensor

class QiblaScreen(Screen):
    bearing=NumericProperty(0)
    heading=NumericProperty(0)
    relative=NumericProperty(0)
    status=StringProperty("Set your location")
    sensor_status=StringProperty("Starting compass…")

    def on_enter(self):
        self.calculate()
        self.sensor=QiblaSensor()
        ok=self.sensor.start(self._heading)
        self.sensor_status="Live compass active" if ok else "Compass sensor unavailable"

    def on_leave(self):
        if hasattr(self,"sensor"): self.sensor.stop()

    def calculate(self):
        try:
            lat=float(self.ids.latitude.text)
            lon=float(self.ids.longitude.text)
            self.bearing=qibla_bearing(lat,lon)
            self.status=f"Qibla: {self.bearing:.1f}° • {direction_name(self.bearing)}"
            self.update_relative()
        except Exception:
            self.status="Enter valid latitude and longitude."

    def _heading(self,value):
        Clock.schedule_once(lambda _: self._set_heading(value))
    def _set_heading(self,value):
        self.heading=value
        self.update_relative()

    def update_relative(self):
        self.relative=(self.bearing-self.heading+360)%360
        if "needle" in self.ids:
            self.ids.needle.rotation=self.relative
