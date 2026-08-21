# AL-HUDA Step 17 — Production Background Azan

## Scope
Adds the production-oriented Azan service foundation without replacing existing prayer calculations or screens.

## Included
- Centralized Azan playback service.
- Safe play/stop/pause controls.
- Audio path can be supplied by the existing asset/configuration layer.
- Android foreground/background integration is handled by the workflow/build configuration foundation, while existing app logic is preserved.

## Important
This step does not invent prayer times and does not delete existing notification/Azan code. The final APK test must verify background behavior on the target Android version, notification permissions, battery restrictions, audio focus, and user stop controls.
