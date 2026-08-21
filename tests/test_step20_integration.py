import unittest
from pathlib import Path
import ast
import re

ROOT = Path(__file__).resolve().parents[1]

class Step20IntegrationTest(unittest.TestCase):
    def test_all_python_sources_parse(self):
        for path in ROOT.rglob("*.py"):
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path))

    def test_main_registers_expected_screens(self):
        main = (ROOT / "main.py").read_text(encoding="utf-8")
        for name in [
            "SplashScreen", "LoginScreen", "RegisterScreen", "VerifyScreen",
            "ForgotPasswordScreen", "ResetPasswordScreen", "HomeScreen",
            "QuranScreen", "QuranReaderScreen", "HadithScreen",
            "HadithDetailScreen", "PrayerScreen", "QiblaScreen", "SearchScreen",
            "DuaScreen", "TasbeehScreen", "CalendarScreen", "RamadanScreen",
            "BookmarksScreen", "SettingsScreen",
        ]:
            self.assertRegex(main, rf"\b{re.escape(name)}\b")

    def test_android_config(self):
        spec = (ROOT / "buildozer.spec").read_text(encoding="utf-8")
        for value in ["android.api = 35", "android.minapi = 23", "ACCESS_FINE_LOCATION", "POST_NOTIFICATIONS"]:
            self.assertIn(value, spec)

if __name__ == "__main__":
    unittest.main()
