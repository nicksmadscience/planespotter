# Some helpful utility functions...
import math, datetime, traceback
from geopy.distance import geodesic

def coordsToDegrees(home_x, home_y, target_x, target_y):
    '''Give it a pair of locations and it turns the angle between them in degrees.'''
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
        print ("aircraft position: ", aircraftPosition)
    except KeyError:
        try:
            aircraftPosition = (float(aircraft['lastPosition']['lat']), float(aircraft['lastPosition']['lon']))
            print ("aircraft last position: ", aircraftPosition)
        except:
            return -1

    feederPosition = (config['location']['latitude'], config['location']['longitude'])
    return geodesic(aircraftPosition, feederPosition).nm


def calculateDeviance(heading, degrees):
    invertedPlaneHeading = (heading - 180.0) % 360.0
    return round((invertedPlaneHeading - degrees) % 180, 1)



def generateHumanReadableStatus(aircraft, config):
    '''Provide the aircraft info in the adsbexchange API format, and it gives you a quick
    summary suitable for, say, an SMS alert.'''
    global ps_config

    # due to the nature of ADS-B sending one variable per packet and uncertainty about whether
    # all information will be present at any given time, we have to be VERY forgiving of
    # missing information
    
    # so as to eliminate reference-before-assignment errors in case my fancy try-excepts don't work
    cardinal        = "(unknown)"
    dist            = "(unknown distance)"
    deviance        = "(unknown)"
    estArrival_mins = "(unknown)"
    type            = "(unknown type)"
    tail            = "(unknown tail)"
    

    try:
        degrees = coordsToDegrees(config['location']['latitude'], config['location']['longitude'], float(aircraft['lat']), float(aircraft['lon']))
        cardinal = degreesToCardinal(degrees)
    except KeyError:
        degrees = -1
        cardinal = "(unknown)"

    try:
        dist_nm = calculateDistance(aircraft, config)
        if dist_nm == -1:
            print ("dist_nm is -1")
            dist = "(unknown distance)"
        else:
            dist = str(round(float(dist_nm), 2))
    except:
        traceback.print_exc()
        dist = "(unknown distance)"

    try:
        if degrees != -1:
            deviance = calculateDeviance(float(aircraft['track']), degrees)
    except (KeyError, UnboundLocalError):
        traceback.print_exc()
        deviance = "(unknown)"

    try:
        estArrival_mins = round((dist_nm / float(aircraft['gs']) * 60))
    except:
        traceback.print_exc()
        estArrival_mins = "(unknown)"

    try:
        type = aircraft['type']
    except KeyError:
        traceback.print_exc()
        type = "(unknown type)"

    try:
        tail = aircraft['flight']
    except KeyError:
        traceback.print_exc()
        tail = "(unknown tail)"

    

    return ("{datetime} Cool aircraft nearby! {type}, tail {tail}, {dist}nm {card}, {dev}deg deviance, {arr}m est arrival".format(type = type, tail=tail, dist = dist, card = cardinal, dev = deviance, arr=estArrival_mins, datetime=datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")))
