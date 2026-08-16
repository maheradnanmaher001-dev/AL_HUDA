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
