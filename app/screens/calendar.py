from datetime import date
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.screenmanager import Screen
from app.services.calendar_service import hijri_label, month_grid

class CalendarScreen(Screen):
    title=StringProperty("")
    hijri=StringProperty("")
    selected=StringProperty("")
    year=NumericProperty(date.today().year)
    month=NumericProperty(date.today().month)

    def on_enter(self):
        self.refresh()

    def refresh(self):
        d=date(int(self.year),int(self.month),1)
        self.title=d.strftime("%B %Y")
        self.hijri=hijri_label(date.today())
        if "days" in self.ids:
            self.ids.days.text="\n".join(
                d.strftime("%d") if d.month==self.month else f"({d.day})"
                for d in month_grid(int(self.year),int(self.month))
            )

    def previous(self):
        self.month-=1
        if self.month<1: self.month=12; self.year-=1
        self.refresh()

    def next(self):
        self.month+=1
        if self.month>12: self.month=1; self.year+=1
        self.refresh()

    def today(self):
        d=date.today(); self.year=d.year; self.month=d.month
        self.refresh()
