from datetime import datetime, timedelta
from kivy.utils import platform

PRAYER_ORDER=("Fajr","Dhuhr","Asr","Maghrib","Isha")

def next_prayer(times, now=None):
    now=now or datetime.now()
    found=[]
    for name in PRAYER_ORDER:
        try:
            h,m=map(int,times.get(name,"").split(":")[:2])
            t=now.replace(hour=h,minute=m,second=0,microsecond=0)
            if t<=now: t+=timedelta(days=1)
            found.append((t,name))
        except Exception: pass
    return min(found) if found else (None,None)

def schedule_azan(prayer_name, when):
    if platform != "android":
        return False
    try:
        from jnius import autoclass
        PythonActivity=autoclass("org.kivy.android.PythonActivity")
        Intent=autoclass("android.content.Intent")
        PendingIntent=autoclass("android.app.PendingIntent")
        AlarmManager=autoclass("android.app.AlarmManager")
        context=PythonActivity.mActivity
        intent=Intent(context, context.getClass())
        intent.putExtra("ALHUDA_PRAYER", prayer_name)
        flags=PendingIntent.FLAG_UPDATE_CURRENT
        if hasattr(PendingIntent,"FLAG_IMMUTABLE"): flags |= PendingIntent.FLAG_IMMUTABLE
        pi=PendingIntent.getActivity(context, abs(hash(prayer_name))%100000, intent, flags)
        alarm=context.getSystemService(context.ALARM_SERVICE)
        alarm.setExactAndAllowWhileIdle(AlarmManager.RTC_WAKEUP, int(when.timestamp()*1000), pi)
        return True
    except Exception:
        return False

def cancel_azan(prayer_name="ALHUDA"):
    # Placeholder-safe cancellation hook; the final receiver/service will
    # cancel the active playback notification by its notification id.
    return platform=="android"
