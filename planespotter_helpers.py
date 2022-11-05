# Some helpful utility functions...
import math, datetime, traceback
from geopy.distance import geodesic
from AltAzRange import AltAzimuthRange


import math


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
    hex             = "(unknown hex)"
    
    
    try:
        alt = aircraft['alt_geom']
    except KeyError:
        try:
            alt = aircraft['alt_baro']
        except KeyError:
            alt = 0
    

    
    try:
        satellite = AltAzimuthRange()
        satellite.observer(config['location']['latitude'], config['location']['longitude'], config['location']['altitude-ft'] * .308)
        satellite.target(float(aircraft['lat']), float(aircraft['lon']), float(alt) * .308)

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
        
    try:
        hex = aircraft['hex']
    except KeyError:
        traceback.print_exc()
        
    return degreesPan, degreesTilt, distance, cardinal, dist, deviance, estArrival_mins, type, tail, hex


def generateHumanReadableStatus(degreesPan, degreesTilt, distance, cardinal, dist, deviance, estArrival_mins, type, tail, hex):
    return ("{datetime} Cool aircraft nearby! {type}, tail {tail}, {dist}nm {card}, {dev}deg deviance, {arr}m est arrival (pan: {degreesPan}, tilt: {degreesTilt}, distance: {distance}) {hex}".format(type = type, tail=tail, dist = dist, card = cardinal, dev = deviance, arr=estArrival_mins, degreesPan=degreesPan, degreesTilt=degreesTilt, distance=distance, hex=hex, datetime=datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")))



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