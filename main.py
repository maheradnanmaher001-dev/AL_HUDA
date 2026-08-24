import os
import traceback


def _write_crash_log(text):
    candidates = []
    try:
        from android.storage import app_storage_path
        candidates.append(os.path.join(app_storage_path(), "alhuda_crash.txt"))
    except Exception:
        pass
    candidates.append(os.path.join(os.getcwd(), "alhuda_crash.txt"))
    candidates.append("/sdcard/alhuda_crash.txt")
    for path in candidates:
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(text)
            return path
        except Exception:
            continue
    return None


def _show_crash_screen(text):
    from kivy.app import App
    from kivy.uix.scrollview import ScrollView
    from kivy.uix.label import Label
    from kivy.metrics import dp

    class CrashApp(App):
        def build(self):
            lbl = Label(
                text=text,
                size_hint_y=None,
                text_size=(dp(360), None),
                halign="left",
                valign="top",
                padding=(dp(12), dp(12)),
            )
            lbl.bind(texture_size=lambda *_: setattr(lbl, "height", lbl.texture_size[1]))
            sv = ScrollView()
            sv.add_widget(lbl)
            return sv

    CrashApp().run()


try:
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
        title = "AL-HUDA"

        def build(self):
            install_theme_properties(self)
            initialize()
            sm = ScreenManager(transition=FadeTransition(duration=.18))
            classes = [
                (SplashScreen, "splash"), (LoginScreen, "login"), (RegisterScreen, "register"),
                (VerifyScreen, "verify"), (ForgotPasswordScreen, "forgot"), (ResetPasswordScreen, "reset"),
                (HomeScreen, "home"), (QuranScreen, "quran"), (QuranReaderScreen, "quran_reader"),
                (HadithScreen, "hadith"), (HadithDetailScreen, "hadith_detail"), (PrayerScreen, "prayer"),
                (QiblaScreen, "qibla"), (SearchScreen, "search"), (DuaScreen, "dua"), (TasbeehScreen, "tasbeeh"),
                (CalendarScreen, "calendar"), (RamadanScreen, "ramadan"), (BookmarksScreen, "bookmarks"),
                (SettingsScreen, "settings")]
            for cls, name in classes:
                sm.add_widget(cls(name=name))
            sm.current = "splash"
            root = AppRoot(sm)
            Clock.schedule_once(lambda *_: self._show_home(sm), 2.2)
            return root

        def _show_home(self, sm):
            sm.transition = FadeTransition(duration=.35)
            sm.current = "home"

    if __name__ == "__main__":
        AlHudaApp().run()

except Exception:
    _err = traceback.format_exc()
    _saved_path = _write_crash_log(_err)
    _header = f"AL-HUDA CRASH REPORT\nSaved to: {_saved_path}\n\n" if _saved_path else "AL-HUDA CRASH REPORT\n(could not save to file)\n\n"
    print(_header + _err)
    try:
        _show_crash_screen(_header + _err)
    except Exception:
        pass
