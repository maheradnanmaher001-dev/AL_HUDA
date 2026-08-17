import math

KAABA_LAT = 21.422487
KAABA_LON = 39.826206

def qibla_bearing(latitude, longitude):
    lat1 = math.radians(float(latitude))
    lat2 = math.radians(KAABA_LAT)
    dlon = math.radians(KAABA_LON - float(longitude))
    x = math.sin(dlon) * math.cos(lat2)
    y = math.cos(lat1)*math.sin(lat2) - math.sin(lat1)*math.cos(lat2)*math.cos(dlon)
    return (math.degrees(math.atan2(x, y)) + 360) % 360

def direction_name(degrees):
    names = ("N","NE","E","SE","S","SW","W","NW")
    return names[int((float(degrees)+22.5)//45) % 8]

class QiblaSensor:
    def __init__(self):
        self.manager = None
        self.listener = None
    def start(self, callback):
        try:
            from jnius import autoclass, PythonJavaClass, java_method
            Context = autoclass("android.content.Context")
            Activity = autoclass("org.kivy.android.PythonActivity")
            Sensor = autoclass("android.hardware.Sensor")
            SensorManager = autoclass("android.hardware.SensorManager")
            self.manager = Activity.mActivity.getSystemService(Context.SENSOR_SERVICE)
            sensor = self.manager.getDefaultSensor(Sensor.TYPE_ROTATION_VECTOR)
            if sensor is None: return False
            outer = self
            class Listener(PythonJavaClass):
                __javainterfaces__ = ["android/hardware/SensorEventListener"]
                @java_method("(Landroid/hardware/SensorEvent;)V")
                def onSensorChanged(self,event):
                    rm=[0.0]*9; ori=[0.0]*3
                    SensorManager.getRotationMatrixFromVector(rm,event.values)
                    SensorManager.getOrientation(rm,ori)
                    callback((math.degrees(ori[0])+360)%360)
                @java_method("(Landroid/hardware/Sensor;I)V")
                def onAccuracyChanged(self,sensor,accuracy): pass
            self.listener=Listener()
            self.manager.registerListener(self.listener,sensor,SensorManager.SENSOR_DELAY_GAME)
            return True
        except Exception:
            return False
    def stop(self):
        try:
            if self.manager and self.listener: self.manager.unregisterListener(self.listener)
        except Exception: pass
