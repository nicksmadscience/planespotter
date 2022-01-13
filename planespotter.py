import requests, json, pprint, time
from twilio.rest import Client

# TODO: move to config file
SETTING_INTERVAL_SECONDS  = 5
SETTING_DISTANCE_NM       = 7
SETTING_LATITUDE          = 39.06
SETTING_LONGITUDE         = -76.98
SETTING_PHONE_NUMBER_TO   = "+12404013264"
SETTING_PHONE_NUMBER_FROM = "+12317296969"
SETTING_MAX_ALTITUDE      = 5000
# SETTING_FILTER_BY_CRAFT_TYPE = ["B738","AS65","EC35","B429"] # maybe future

with open("secrets.json", "r") as secrets_file:
    secrets = json.load(secrets_file)


client = Client(secrets["twilio-sid"], secrets["twilio-token"])


url = 'https://adsbexchange-com1.p.rapidapi.com/json/lat/{lat}/lon/{lon}/dist/{dist}/'.format(lat = SETTING_LATITUDE, lon = SETTING_LONGITUDE, dist = SETTING_DISTANCE_NM)

headers = {
    'x-rapidapi-host': "adsbexchange-com1.p.rapidapi.com",
    'x-rapidapi-key': secrets["x-rapidapi-key"]  # TODO: also in config file
    }


def textMeAboutAircraft(_tail, _type):
    global SETTING_PHONE_NUMBER_FROM, SETTING_PHONE_NUMBER_TO

    message = client.messages \
        .create(
                body="Cool aircraft nearby! {type}, tail {tail}".format(type = _type, tail=_tail),
                from_= SETTING_PHONE_NUMBER_FROM,
                to= SETTING_PHONE_NUMBER_TO
            )






masterAircraft = []

# begin the infinite loop!
while True:
    response = requests.request("GET", url, headers=headers)

    try:
        newAircraft = json.loads(response.text)['ac']

        for aircraft in newAircraft:

            # this is cool; thanks Odorlemon for the assist!
            aircraft_hash = { aircraft['icao']: aircraft for aircraft in masterAircraft }

            if aircraft['icao'] not in aircraft_hash:
                if aircraft['reg'] == '':
                    reg = "(no tail)"
                else:
                    reg = aircraft['reg']

                print ("New aircraft! {reg}".format(reg = reg))
                masterAircraft.append(aircraft)
                textMeAboutAircraft(aircraft['reg'], aircraft['type'])
            # else:   # for debugging
            #     print ("Dupe aircraft {reg}".format(reg = aircraft['reg']))

        # TODO: if an aircraft in masterAircraft is *no longer* in the radius, remove it from the list
        # (can you remove it from the list?  yes)
    except TypeError:  # no aircraft in the area right now
        pass

    time.sleep(SETTING_INTERVAL_SECONDS)