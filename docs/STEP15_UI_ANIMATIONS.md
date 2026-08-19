# AL-HUDA — Step 15: Complete UI & Animations

Step 15 adds a central, reusable animation layer for the AL-HUDA Kivy UI.

Included:
- Fade-in / fade-out
- Slide-in
- Scale-in
- Button press feedback
- Central motion-duration constants
- A single service that screens can import

Important:
- This step is intentionally additive.
- It does not replace `main.py`, existing screens, navigation, data, prayer,
  Quran, Hadith, account, calendar, or other services.
- Existing screen logic remains intact.
- Screen-by-screen animation calls can be wired into the existing UI without
  changing backend/data behavior.

Example:

    from app.services.ui_animation_service import UIAnimationService

    UIAnimationService.fade_in(widget)
    UIAnimationService.slide_in(widget, x=32)
