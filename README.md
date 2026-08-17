# AL-HUDA

## Step 2 — Quran Pak module

Added:
- 114 Surah browsing
- 30 Juz browsing
- Arabic Uthmani text
- Urdu translation (Fateh Muhammad Jalandhry, `ur.jalandhry`)
- English translation (Saheeh International, `en.sahih`)
- Quran search
- Local caching of fetched Surahs/Juz
- Metadata for all 114 Surahs and 30 Juz

Quran data is fetched through the Al Quran Cloud REST API and cached locally.
The API documents Surah, Juz, Ayah, Search and multi-edition endpoints.
Arabic corpus attribution is retained through the provider/source metadata.

Next Quran work:
- persistent bookmarks and last-read position
- audio playback
- Mushaf/page mode
- font-size and translation controls
- stronger offline packaging and verification

Sources:
- Tanzil Project
- Al Quran Cloud API


## Step 3 — Hadith

Book-wise Hadith foundation with Arabic, Urdu and English editions, search, Hadith number, reference and grade fields when supplied by the source. Initial catalog includes Bukhari, Muslim, Abu Dawud, Tirmidhi, Nasa'i, Ibn Majah, Muwatta Malik, Musnad Ahmad and Nawawi 40. Data is fetched/cached through the open hadith-api dataset; upstream edition availability and licensing/attribution will be verified before production release.


## Step 4 — Prayer Times
- Fajr, Sunrise, Dhuhr, Asr, Maghrib and Isha
- City/country lookup
- Local JSON cache
- Live next-prayer countdown
- Integrated Prayer Times screen

Uses AlAdhan's timingsByCity endpoint. GPS, calculation-method selection, Azan/background notifications and stop controls will be implemented in the next prayer sub-step.


## Step 5 — Live Qibla Compass
- Accurate great-circle bearing to the Kaaba
- Latitude/longitude input
- 8-direction label
- Android rotation-vector sensor bridge
- Live heading and relative Qibla turn
- Islamic-themed Qibla screen


## Step 6 — Azan & Notifications Foundation

Added:
- Azan/notification settings screen
- Enable/disable notification control
- Stop-active-Azan control hook
- Next-prayer scheduling foundation
- Android AlarmManager integration hook
- Safe non-Android fallback

The complete production background-audio receiver, Android notification channel, boot rescheduling and audio stop action require final Android packaging/manifest integration.


## Step 7 — Islamic + Gregorian Calendar

Added:
- Islamic/Hijri date label
- Gregorian month calendar
- January and every Gregorian month through the same calendar
- Previous/next month navigation
- Today button
- 42-cell month grid foundation
- AL-HUDA calendar screen

Note: the arithmetic Hijri conversion is a foundation. For publication-grade dates and moon-sighting-sensitive observances, a selectable official/local calendar source should be used.


## Step 8 — Duas & Azkar
Added a Dua/Azkar screen with Arabic, Urdu, English, references, categories foundation and search. `PROJECT_ROADMAP.md` and `CHANGELOG.md` are now included to preserve project continuity between chats.
