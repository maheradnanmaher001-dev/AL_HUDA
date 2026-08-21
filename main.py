from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from kivy.clock import Clock
from app.database import initialize
from app.theme import install_theme_properties
from app.root import AppRoot
from app.screens.splash import SplashScreen
from app.screens.auth import LoginScreen, RegisterScreen, VerifyScreen, ForgotPasswordScreen, ResetPasswordScreen
from app.screens.home import HomeScreen
from app.screens.quran import QuranScreen, QuranReaderScreen
from app.screens.hadith import HadithScreen, HadithDetailScreen
from app.screens.prayer import PrayerScreen
from app.screens.qibla import QiblaScreen
from app.screens.search import SearchScreen
from app.screens.dua import DuaScreen
from app.screens.tasbeeh import TasbeehScreen
from app.screens.calendar import CalendarScreen
from app.screens.ramadan import RamadanScreen
from app.screens.bookmarks import BookmarksScreen
from app.screens.settings import SettingsScreen

class AlHudaApp(App):
    title="AL-HUDA"
    def build(self):
        install_theme_properties(self)
        initialize()
        sm=ScreenManager(transition=FadeTransition(duration=.18))
        classes=[
            (SplashScreen,"splash"),(LoginScreen,"login"),(RegisterScreen,"register"),
            (VerifyScreen,"verify"),(ForgotPasswordScreen,"forgot"),(ResetPasswordScreen,"reset"),
            (HomeScreen,"home"),(QuranScreen,"quran"),(QuranReaderScreen,"quran_reader"),
            (HadithScreen,"hadith"),(HadithDetailScreen,"hadith_detail"),(PrayerScreen,"prayer"),
            (QiblaScreen,"qibla"),(SearchScreen,"search"),(DuaScreen,"dua"),(TasbeehScreen,"tasbeeh"),
            (CalendarScreen,"calendar"),(RamadanScreen,"ramadan"),(BookmarksScreen,"bookmarks"),
            (SettingsScreen,"settings")]
        for cls,name in classes: sm.add_widget(cls(name=name))
        sm.current="splash"
        root=AppRoot(sm)
        Clock.schedule_once(lambda *_: self._show_home(sm),2.2)
        return root
    def _show_home(self,sm):
        sm.transition=FadeTransition(duration=.35)
        sm.current="home"

if __name__=="__main__":
    AlHudaApp().run()
