"""
Notification/short-Adhan architecture.
On Android, connect this service to a native notification channel with
MediaSession/MediaPlayer controls so Stop is available from the notification
shade and lock screen. Do not play a full recording unless the user enables it.
"""
PRAYER_CHANNEL = "alhuda_prayer"
SHORT_ADHAN_SECONDS = 12
