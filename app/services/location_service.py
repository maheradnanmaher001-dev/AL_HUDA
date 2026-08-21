"""AL-HUDA GPS/location foundation."""
from typing import Callable, Optional

class LocationService:
    def __init__(self): self._gps=None; self._running=False; self.last_location=None
    @property
    def running(self): return self._running
    def request_permissions(self):
        try:
            from android.permissions import Permission, request_permissions
            request_permissions([Permission.ACCESS_COARSE_LOCATION, Permission.ACCESS_FINE_LOCATION]); return True
        except Exception: return False
    def start(self, on_location: Optional[Callable]=None):
        try: from plyer import gps
        except Exception: return False
        self._gps=gps; self.request_permissions()
        try:
            gps.configure(on_location=on_location or self._on_location, on_status=self._on_status)
            gps.start(minTime=1000,minDistance=1); self._running=True; return True
        except Exception: self._running=False; return False
    def stop(self):
        if self._gps:
            try: self._gps.stop()
            except Exception: pass
        self._running=False
    def _on_location(self, **kwargs): self.last_location=kwargs
    @staticmethod
    def _on_status(status,*args): return None
