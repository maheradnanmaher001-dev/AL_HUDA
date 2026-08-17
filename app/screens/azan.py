from kivy.clock import Clock
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.screenmanager import Screen
from app.services import prayer_service
from app.services.azan_service import next_prayer, schedule_azan, cancel_azan

class AzanScreen(Screen):
    enabled=BooleanProperty(True)
    status=StringProperty("Azan notifications are enabled")
    selected_prayer=StringProperty("Next Prayer")

    def on_enter(self):
        self.refresh()

    def refresh(self):
        # Uses prayer times already cached by the Prayer screen/service.
        self.status="Prayer reminders are ready. Background Android receiver will use the selected prayer time."

    def toggle(self):
        self.enabled=not self.enabled
        self.status="Azan notifications enabled" if self.enabled else "Azan notifications disabled"

    def stop_azan(self):
        cancel_azan()
        self.status="Azan stopped"
