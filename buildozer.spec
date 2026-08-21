[app]
title = AL-HUDA
package.name = alhuda
package.domain = org.alhuda
source.dir = .
source.include_exts = py,kv,png,jpg,jpeg,json,txt,md
version = 0.1.0
requirements = python3,kivy,pillow
orientation = portrait
fullscreen = 0
android.api = 35
android.minapi = 23
android.archs = arm64-v8a, armeabi-v7a
android.permissions = INTERNET,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,POST_NOTIFICATIONS,VIBRATE,WAKE_LOCK,FOREGROUND_SERVICE,FOREGROUND_SERVICE_MEDIA_PLAYBACK

[buildozer]
log_level = 2
warn_on_root = 1

# Step 17 service assets are kept in the existing Android source layer.
