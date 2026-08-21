# AL-HUDA — Islamic Companion

A Python/Kivy Android Islamic companion app foundation with a premium green/gold theme and reusable slide/fade animations.

## Included

- AL-HUDA branding + supplied icon
- Animated splash screen
- Animated screen transitions
- Home dashboard
- Quran Surah + Para/Juz navigation
- Quran reader data model for Arabic/Urdu/English
- Hadith book-wise architecture and metadata fields
- Prayer-times architecture
- Prayer notifications/short Adhan service architecture
- Qibla bearing calculation + sensor-ready service
- Universal search architecture
- Bookmarks/history/notes database
- Dua & Azkar
- Tasbeeh
- Islamic + Gregorian calendar
- Ramadan screen
- Account UI
- Secure authentication backend starter (FastAPI + Argon2 + verification/reset codes)
- Buildozer configuration
- Data schemas/import guidance

## Important

This repository deliberately does not invent Quran/Hadith text. Put verified, licensed/source-traceable datasets into `data/` or connect an approved source/API. Preserve collection, book, chapter, number, narrator and grade metadata for Hadith.

The backend must be deployed behind HTTPS and configured with real SMTP credentials before production authentication/email is used.

## Android build

On Linux/WSL:

```bash
python -m pip install -r requirements.txt
buildozer android debug
```

APK output appears under `bin/`.

## Backend

```bash
cd backend
python -m pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

For production use HTTPS, a production database, strong secret keys and a real transactional email provider.

## Structure

```text
AL-HUDA/
├── main.py
├── al_huda.kv
├── buildozer.spec
├── requirements.txt
├── .env.example
├── app/
│   ├── database.py
│   ├── theme.py
│   ├── animations.py
│   ├── screens/
│   ├── services/
│   └── utils/
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   └── .env.example
├── assets/
│   ├── icon.png
│   └── splash.png
└── data/
    ├── quran/README.md
    └── hadith/README.md
```
