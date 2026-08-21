import math
KAABA_LAT, KAABA_LON = 21.4225, 39.8262
def bearing(lat, lon):
    p1,p2=math.radians(lat),math.radians(KAABA_LAT)
    dl=math.radians(KAABA_LON-lon)
    y=math.sin(dl)*math.cos(p2)
    x=math.cos(p1)*math.sin(p2)-math.sin(p1)*math.cos(p2)*math.cos(dl)
    return (math.degrees(math.atan2(y,x))+360)%360
