# AL-HUDA Step 19 — Responsive Design & User Text Size

## Scope
This step audits responsive behavior and adds a persistent user-controlled text-size setting.

### Included
- Responsive window tracking for portrait/landscape and small/large screens.
- Bounded adaptive spacing helper.
- User text scale from 80% to 160%, in 10% steps, with Reset to 100%.
- Text-size setting persists in Kivy JSON storage.
- Existing widgets update when the user changes text size.
- Screen font sizes use the shared responsive `fs()` helper.
- Navigation and common headers use responsive font sizing.
- No Quran/Hadith text is changed; local Step 18 data remains untouched.

## GitHub extraction
The Step 19 workflow overlays the supplied files on the existing project. It does not delete Step 18 data.
