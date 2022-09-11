# Some helpful utility functions...
import math, datetime, traceback
from geopy.distance import geodesic
from AltAzRange import AltAzimuthRange


import math

def threeDAzimuth(x1, y1, z1, x2, y2, z2):
    # print ("x1: ", x1)
    # print ("y1: ", y1)
    # print ("z1: ", z1)
    # print ("x2: ", x2)
    # print ("y2: ", y2)
    # print ("z2: ", z2)
    distance = math.sqrt((x2-x1)**2+(y2-y1)**2+(z2 -z1)**2)
    # print("distance: ", distance)
    # 5.5910642993977451
    plunge = math.degrees(math.asin((z2-z1)/distance))
    # print("plunge: ", plunge)
    # 1.0248287567800018 # the resulting dip_plunge is positive downward if z2 > z1
    azimuth = math.degrees(math.atan2((x2-x1),(y2-y1)))
    # print("azimuth: ", azimuth)
    return azimuth
    # -169.69515353123398 # = 360 + azimuth = 190.30484646876602 or  180+ azimuth = 10.304846468766016 over the range of 0 to 360°


def asRadians(degrees):
    return degrees * math.pi / 180

def getXYpos(cam_lat, cam_lon, ac_lat, ac_lon):
    """ Calculates X and Y distances in meters.
    """
    deltaLatitude = ac_lat - cam_lat
    deltaLongitude = ac_lon - cam_lon
    latitudeCircumference = 40075160 * math.cos(asRadians(cam_lat))
    resultX = deltaLongitude * latitudeCircumference / 360
    resultY = deltaLatitude * 40008000 / 360
    return resultX, resultY

def latToMeters(lat):
    return lat * 111320.0

def lonToMeters(lat, lon):
    return lon * (40075000.0 * math.cos(lat) / 360.0)


def elevation(cam_lat, cam_lon, cam_alt_ft, ac_lat, ac_lon, ac_alt_ft):
    
    # # convert lat and lon to meters
    # x_meters, y_meters = getXYpos(cam_lat, cam_lon, ac_lat, ac_lon)
    
    cam_lat_m = latToMeters(cam_lat)
    cam_lon_m = lonToMeters(cam_lat, cam_lon)
    
    ac_lat_m = latToMeters(ac_lat)
    ac_lon_m = lonToMeters(ac_lat, ac_lon)
    
    cam_alt_m = cam_alt_ft * 0.3048
    ac_alt_m = ac_alt_ft * 0.3048
    
    elev = math.atan((ac_alt_m - cam_alt_m) / math.sqrt((ac_lat_m - cam_lat_m)**2 + (ac_lon_m - cam_lon_m)**2))
    
    return elev
    
    # convert alt to meters
    


def coordsToDegrees(home_x, home_y, target_x, target_y):
    '''Give it a pair of locations and it returns the angle between them in degrees.'''
    # stolen from https://stackoverflow.com/questions/42258637/how-to-know-the-angle-between-two-vectors
    myradians = math.atan2(target_y - home_y, target_x - home_x)
    return math.degrees(myradians) % 360.0


def degreesToCardinal(degrees):
    '''Provide a degrees value and it returns the nearest cardinal direction in string form.'''
    # stolen from https://gist.github.com/RobertSudwarts/acf8df23a16afdb5837f
    dirs = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
    ix = round(degrees / (360. / len(dirs)))
    return dirs[ix % len(dirs)]


def calculateDistance(aircraft, config):
    try:
        aircraftPosition = (float(aircraft['lat']), float(aircraft['lon']))
        # print ("aircraft position: ", aircraftPosition)
    except KeyError:
        try:
            aircraftPosition = (float(aircraft['lastPosition']['lat']), float(aircraft['lastPosition']['lon']))
            # print ("aircraft last position: ", aircraftPosition)
        except:
            return -1

    feederPosition = (config['location']['latitude'], config['location']['longitude'])
    return geodesic(aircraftPosition, feederPosition).nm


def calculateDeviance(heading, degrees):
    invertedPlaneHeading = (heading - 180.0) % 360.0
    return round((invertedPlaneHeading - degrees) % 180, 1)



def generateStats(aircraft, config):
    # due to the nature of ADS-B sending one variable per packet and uncertainty about whether
    # all information will be present at any given time, we have to be VERY forgiving of
    # missing information
    
    # so as to eliminate reference-before-assignment errors in case my fancy try-excepts don't work
    degreesPan      = -1
    degreesTilt     = -1
    distance        = -1
    cardinal        = "(unknown)"
    dist            = "(unknown distance)"
    deviance        = "(unknown)"
    estArrival_mins = "(unknown)"
    type            = "(unknown type)"
    tail            = "(unknown tail)"
    

    # try:
    #     degreesPan = coordsToDegrees(config['location']['latitude'], config['location']['longitude'], float(aircraft['lat']), float(aircraft['lon']))
    #     cardinal = degreesToCardinal(degreesPan)
    # except KeyError:
    #     degreesPan = -1
    #     cardinal = "(unknown)"
        
    # try:
    #     # myradians = math.atan2(float(aircraft['alt_geom']), config['location']['altitude-ft'])
    #     # degreesTilt = math.degrees(myradians) % 360.0
    #     degreesTilt = threeDAzimuth(config['location']['latitude'],
    #                                 config['location']['longitude'],
    #                                 config['location']['altitude-ft'],
    #                                 float(aircraft['lat']),
    #                                 float(aircraft['lon']),
    #                                 float(aircraft['alt_geom']))
    # except KeyError:
    #     degreesTilt = -1
    
    try:
        satellite = AltAzimuthRange()
        satellite.observer(config['location']['latitude'], config['location']['longitude'], config['location']['altitude-ft'] * .308)
        satellite.target(float(aircraft['lat']), float(aircraft['lon']), float(aircraft['alt_geom']) * .308)

        altazar = satellite.calculate()
        degreesPan = altazar['azimuth']
        degreesTilt = altazar['elevation']
        distance = altazar['distance']
        cardinal = degreesToCardinal(degreesPan)
    except:
        traceback.print_exc()
        
        
    
    

    try:
        dist_nm = calculateDistance(aircraft, config)
        if dist_nm == -1:
            # print ("dist_nm is -1")
            dist = "(unknown distance)"
        else:
            dist = str(round(float(dist_nm), 2))
    except:
        traceback.print_exc()
        dist = "(unknown distance)"

    try:
        if degreesPan != -1:
            deviance = calculateDeviance(float(aircraft['track']), degreesPan)
    except (KeyError, UnboundLocalError):
        traceback.print_exc()
        deviance = "(unknown)"

    try:
        estArrival_mins = round((dist_nm / float(aircraft['gs']) * 60))
    except:
        traceback.print_exc()
        estArrival_mins = "(unknown)"

    try:
        type = aircraft['t']
    except KeyError:
        traceback.print_exc()
        type = "(unknown type)"

    try:
        tail = aircraft['flight']
    except KeyError:
        traceback.print_exc()
        tail = "(unknown tail)"
        
    return degreesPan, degreesTilt, distance, cardinal, dist, deviance, estArrival_mins, type, tail


def generateHumanReadableStatus(degreesPan, degreesTilt, distance, cardinal, dist, deviance, estArrival_mins, type, tail):
    return ("{datetime} Cool aircraft nearby! {type}, tail {tail}, {dist}nm {card}, {dev}deg deviance, {arr}m est arrival (pan: {degreesPan}, tilt: {degreesTilt}, distance: {distance})".format(type = type, tail=tail, dist = dist, card = cardinal, dev = deviance, arr=estArrival_mins, degreesPan=degreesPan, degreesTilt=degreesTilt, distance=distance, datetime=datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")))



if __name__ == "__main__":
    # for i in range(1, 9):
    #     print (threeDAzimuth(30, -70, 400, 30, -71, 400 + (i * 100)))
    
    # myradians = math.atan2(400, 1000)
    # degreesTilt = math.degrees(myradians) % 360.0
    
    # print (degreesTilt)
    
    # print (latToMeters(1))
    # print (lonToMeters(0, 1))
    
    # print (elevation(30, -70, 400, 30, -71, 1000))
    
    
    satellite = AltAzimuthRange()
    satellite.observer(39.113938, -76.984350, 135)
    satellite.target(39.031128, -76.950989, 3357)

    print(satellite.calculate())