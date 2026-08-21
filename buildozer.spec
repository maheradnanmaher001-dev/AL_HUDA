[app]
title = AL-HUDA
package.name = alhuda
package.domain = org.alhuda
source.dir = .
source.include_exts = py,kv,png,jpg,jpeg,json,db,txt,md
version = 1.0.0
requirements = python3,kivy,requests
orientation = portrait
fullscreen = 0
icon.filename = %(source.dir)s/assets/icon.png
presplash.filename = %(source.dir)s/assets/splash.png
android.api = 35
android.minapi = 23
android.archs = arm64-v8a,armeabi-v7a
android.permissions = INTERNET,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,POST_NOTIFICATIONS,WAKE_LOCK,FOREGROUND_SERVICE
android.enable_androidx = 1

[buildozer]
log_level = 2
warn_on_root = 1
