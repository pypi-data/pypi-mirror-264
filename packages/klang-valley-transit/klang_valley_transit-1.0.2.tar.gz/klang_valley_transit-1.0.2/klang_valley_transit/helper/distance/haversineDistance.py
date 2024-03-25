from ..model.baseModel import Coordinates
import numpy as np

def HaversineDist(_from:Coordinates,_to:Coordinates):
    try:
        _from = Coordinates(**_from)
        _to = Coordinates(**_to)
        lat1 = _from.lat
        lon1 = _from.lon
        lat2 = _to.lat
        lon2 = _to.lon

        EarthRadius = 6371*1000 # meter
        PI = 22/7
        lat1Radians = lat1 * PI/180
        lat2Radians = lat2 * PI/180
        latDist = (lat2-lat1) * PI/180
        lonDist = (lon2-lon1) * PI/180

        a = np.sin(latDist/2) * np.sin(latDist/2) + np.cos(lat1Radians) * np.cos(lat2Radians) * np.sin(lonDist/2) * np.sin(lonDist/2)
        c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))

        dist = EarthRadius * c #in metres
        return {"res":dist}

    except Exception as error:
        return {"err": str(error)}