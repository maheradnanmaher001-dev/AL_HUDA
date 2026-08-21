"""Android runtime location permissions."""
def request_location_permissions():
    try:
        from android.permissions import Permission, request_permissions
        request_permissions([Permission.ACCESS_COARSE_LOCATION, Permission.ACCESS_FINE_LOCATION]); return True
    except Exception: return False
