# AL-HUDA — Step 14 Settings

This step is intentionally **non-destructive**.

It adds:
- persistent language preference
- Urdu + English translation preference
- Islamic theme preference
- notification / Azan / sound / vibration toggles
- Qibla and automatic-location preferences
- font-scale preference
- reset-to-default settings

## Important

Do **not** replace `main.py` or the existing `app/screens/settings.py` with this update.
The repository already contains those files. This update only adds the reusable
`app/services/settings_service.py` module.

The existing Settings screen should import:

```python
from app.services.settings_service import (
    load_settings,
    save_settings,
    set_setting,
    get_setting,
    reset_settings,
)
```

Then connect its existing controls to these functions.

This separation prevents Step 14 from overwriting working AL-HUDA screens.
