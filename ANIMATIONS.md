# AL-HUDA Animation System

Animations are intentionally reusable rather than copied screen-by-screen.

- Screen changes: Kivy `FadeTransition` plus directional navigation.
- Screen contents: fade-in on enter.
- Cards/buttons: designed for slide/fade expansion as features are connected.
- Splash: dedicated branded entry screen.
- Reader/search/detail screens use the same transition hooks.

When adding a new screen, inherit `ScreenBase` so the standard fade animation is applied automatically.
