# AL-HUDA — Step 20: Full Integration + Android Testing

## Scope

Step 20 is the integration and release-readiness audit after Step 18 (Quran/Hadith integration) and Step 19 (responsive design + user text-size control).

### Checks included
- All registered screens/classes referenced by `main.py` exist.
- All Python source files parse successfully without requiring a Kivy runtime in CI.
- Quran service contract covers 114 Surahs, 30 Juz, Arabic/Urdu/English translation paths and search helpers.
- Hadith service contract exposes collection, book, hadith, section and normalized metadata helpers.
- Step 19 responsive/text-size functions remain present and connected.
- SQLite persistence files and existing `data/quran` / `data/hadith` directories are preserved.
- Buildozer configuration is audited for Kivy, Android API/min API, location, notification, wake-lock and foreground-service permissions.
- No APK is built in Step 20; the final APK build remains Step 21.

## Important data rule

The Step 20 package does **not** delete or replace the repository's existing Quran/Hadith data. The extraction workflow only updates application/configuration/test files. Existing `data/` contents remain under the repository's control.

## Android testing boundary

CI performs source/configuration and integration checks. A real physical-device/emulator test and final APK compilation are intentionally left for Step 21, where the Android build environment is available.
