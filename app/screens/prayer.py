from datetime import datetime
from kivy.clock import Clock
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from app.services import prayer_service

class PrayerScreen(Screen):
    status=StringProperty("Prayer Times")
    next_prayer=StringProperty("Next Prayer: --")
    countdown=StringProperty("--:--:--")
    city=StringProperty("Lahore")
    country=StringProperty("Pakistan")
    method=2

    def on_enter(self):
        self.ids.city.text=self.city
        self.ids.country.text=self.country
        self.load()

    def load(self):
        self.city=self.ids.city.text.strip() or "Lahore"
        self.country=self.ids.country.text.strip() or "Pakistan"
        self.status=f"Loading prayer times for {self.city}…"
        prayer_service.async_call(prayer_service.timings_by_city,self.loaded,self.error,
                                  self.city,self.country,None,self.method)

    def loaded(self,data):
        def ui(_):
            self.times=prayer_service.clean(data)
            for name in prayer_service.PRAYERS:
                self.ids[name.lower()].text=self.times.get(name,"--")
            self.status=f"{self.city}, {self.country} • {datetime.now():%d %b %Y}"
            self.update_countdown()
            if not hasattr(self,"timer"):
                self.timer=Clock.schedule_interval(lambda dt:self.update_countdown(),1)
        Clock.schedule_once(ui)

    def update_countdown(self):
        target,name=prayer_service.next_prayer(getattr(self,"times",{}))
        self.next_prayer=f"Next Prayer: {name or '--'}"
        self.countdown=prayer_service.countdown(target)

    def error(self,msg):
        Clock.schedule_once(lambda _:self.show_error(msg))

    def show_error(self,msg):
        self.status="Unable to load prayer times"
        self.next_prayer="Check internet connection"
        self.countdown="--:--:--"
