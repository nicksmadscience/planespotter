import requests, json, pprint, time, math
from twilio.rest import Client

# TODO: move to config file
SETTING_INTERVAL_SECONDS  = 15
SETTING_DISTANCE_NM       = 15
SETTING_LATITUDE          = 39.113938
SETTING_LONGITUDE         = -76.984350
SETTING_PHONE_NUMBER_TO   = "+12404013264"
SETTING_PHONE_NUMBER_FROM = "+12317296969"
SETTING_MAX_ALTITUDE      = 4000
# SETTING_FILTER_BY_CRAFT_TYPE = ["B738","AS65","EC35","B429"] # maybe future
# TODO: min airspeed filter to skip taxiing / parked aircraft

with open("secrets.json", "r") as secrets_file:
    secrets = json.load(secrets_file)


client = Client(secrets["twilio-sid"], secrets["twilio-token"])


url = 'https://adsbexchange-com1.p.rapidapi.com/json/lat/{lat}/lon/{lon}/dist/{dist}/'.format(lat = SETTING_LATITUDE, lon = SETTING_LONGITUDE, dist = SETTING_DISTANCE_NM)

headers = {
    'x-rapidapi-host': "adsbexchange-com1.p.rapidapi.com",
    'x-rapidapi-key': secrets["x-rapidapi-key"]  # TODO: also in config file
    }




def coordsToDegrees(home_x, home_y, target_x, target_y):
    # stolen from https://stackoverflow.com/questions/42258637/how-to-know-the-angle-between-two-vectors
    myradians = math.atan2(target_y - home_y, target_x - home_x)
    return math.degrees(myradians) % 360.0



def degreesToCardinal(degrees):
    # stolen from https://gist.github.com/RobertSudwarts/acf8df23a16afdb5837f
    dirs = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
    ix = round(degrees / (360. / len(dirs)))
    return dirs[ix % len(dirs)]



# TODO: move to custom action .py file
def textMeAboutAircraft(aircraft):
    global SETTING_PHONE_NUMBER_FROM, SETTING_PHONE_NUMBER_TO, SETTING_LATITUDE, SETTING_LONGITUDE

    degrees = coordsToDegrees(SETTING_LATITUDE, SETTING_LONGITUDE, float(aircraft['lat']), float(aircraft['lon']))
    cardinal = degreesToCardinal(degrees)

    planeHeading = float(aircraft['trak'])


    invertedPlaneHeading = (planeHeading - 180.0) % 360.0

    deviance = round((invertedPlaneHeading - degrees) % 180, 1)


    estArrival_mins = round((float(aircraft['dst']) / float(aircraft['spd']) * 60))

    bodyText = "Cool aircraft nearby! {type}, tail {tail}, {dist} mi {card}, {dev}deg deviance, {arr}m est arrival".format(type = aircraft['type'], tail=aircraft['reg'], dist = aircraft['dst'], card = cardinal, dev = deviance, arr=estArrival_mins)

    print (bodyText)

    # message = client.messages \
    #     .create(
    #             body=bodyText,
    #             from_= SETTING_PHONE_NUMBER_FROM,
    #             to= SETTING_PHONE_NUMBER_TO
    #         )




masterAircraft = []

# begin the infinite loop!
while True:
    response = requests.request("GET", url, headers=headers)

    newAircraft = json.loads(response.text)['ac']

    if newAircraft != None:

        # pprint.pprint (newAircraft)

        numberOfAircraft = 0
        for aircraft in newAircraft:
            # pprint.pprint(aircraft)
            numberOfAircraft += 1
            # print ("now processing aircraft {noa} of {total}".format(noa = numberOfAircraft, total = len(newAircraft)))

            # this is cool; thanks Odorlemon for the assist!
            aircraft_hash = { aircraft['icao']: aircraft for aircraft in masterAircraft }

            if aircraft['icao'] not in aircraft_hash:
                if aircraft['galt'] != '':
                    if int(aircraft['galt']) <= int(SETTING_MAX_ALTITUDE):
                        
                        if aircraft['reg'] == '':
                            reg = "(no tail)"
                        else:
                            reg = aircraft['reg']

                        print ("New aircraft! {reg}".format(reg = reg))
                        masterAircraft.append(aircraft)

                        textMeAboutAircraft(aircraft)
                        # requests.get("http://10.0.0.220:8081/yellowlight")
            #         else:
            #             print ("aircraft too high {reg}, {galt}".format(reg = aircraft["reg"], galt = aircraft["galt"]))
            # else:   # for debugging
            #     print ("Dupe aircraft {reg}".format(reg = aircraft['reg']))

            # TODO: if an aircraft in masterAircraft is *no longer* in the radius, remove it from the list
            # (can you remove it from the list?  yes)

    time.sleep(SETTING_INTERVAL_SECONDS)