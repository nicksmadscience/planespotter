# Some helpful utility functions...
import math, datetime

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




def generateHumanReadableStatus(aircraft, userLat, userLon):
    '''Provide the aircraft info in the adsbexchange API format, and it gives you a quick
    summary suitable for, say, an SMS alert.'''
    global ps_config

    degrees = coordsToDegrees(userLat, userLon, float(aircraft['lat']), float(aircraft['lon']))
    cardinal = degreesToCardinal(degrees)
    planeHeading = float(aircraft['trak'])
    invertedPlaneHeading = (planeHeading - 180.0) % 360.0
    deviance = round((invertedPlaneHeading - degrees) % 180, 1)
    estArrival_mins = round((float(aircraft['dst']) / float(aircraft['spd']) * 60))

    return ("{datetime} Cool aircraft nearby! {type}, tail {tail}, {dist} mi {card}, {dev}deg deviance, {arr}m est arrival".format(type = aircraft['type'], tail=aircraft['reg'], dist = aircraft['dst'], card = cardinal, dev = deviance, arr=estArrival_mins, datetime=datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")))
