import requests, json, pprint, time, yaml, datetime



with open("secrets-adsbx.json", "r") as secrets_file:
    secrets = json.load(secrets_file)
    key = secrets["x-rapidapi-key"]

with open(r'planespotter-conf.yaml') as file:
    ps_config = yaml.load(file, Loader=yaml.FullLoader)

from planespotter_helpers import *
from spot_actions import *

url = 'https://adsbexchange-com1.p.rapidapi.com/v2/lat/{lat}/lon/{lon}/dist/{dist}/'.format(lat = ps_config['location']['latitude'], lon = ps_config['location']['longitude'], dist = ps_config['filters']['max-distance-nm'])

headers = {
    "X-RapidAPI-Host": "adsbexchange-com1.p.rapidapi.com",
    "X-RapidAPI-Key": key
    }

# headers = {
# 	"X-RapidAPI-Key": "06a3d0bb77msh2a63f5b2b65f764p173e43jsn885b3b6380f3",
# 	"X-RapidAPI-Host": "adsbexchange-com1.p.rapidapi.com"
# }

# url = 'http://localhost:80/tar1090/data/aircraft.json'

# All aircraft are added to this list when they're first spotted and
# are ignored if their ICAO number appears in the adsbx API call
# subsequent times

# TODO: very important to remove aircraft that are no longer
# being picked up by API calls
masterAircraft = []


def findAltitude(aircraft):
    try:
        return int(aircraft['alt_geom'])
    except KeyError:
        try:
            return int(aircraft['alt_baro'])
        except:
            return 999999999


# begin the infinite loop!
while True:
    response = requests.request("GET", url, headers=headers)
    # print (response.text)

    try:
        newAircraft = json.loads(response.text)['ac']
    except KeyError:
        newAircraft = None

    if newAircraft != None:

        # pprint.pprint (newAircraft)

        numberOfAircraft = 0
        for aircraft in newAircraft:
            aircraft["timestamp"] = datetime.datetime.now()
            # pprint.pprint(aircraft)
            numberOfAircraft += 1
            # print ("now processing aircraft {noa} of {total}".format(noa = numberOfAircraft, total = len(newAircraft)))

            # this is cool; thanks Odorlemon for the assist!
            aircraft_hash = { aircraft['hex']: aircraft for aircraft in masterAircraft }

            distance_nm = calculateDistance(aircraft, ps_config)
            # print ("distance: ", distance_nm)
            
            if distance_nm <= ps_config['filters']['max-distance-nm']:
                # TODO: This needs a more elegant filtering system,  not one
                # based on a series of if statements
                if aircraft['hex'] not in aircraft_hash:
                    if int(findAltitude(aircraft)) <= int(ps_config['filters']['max-altitude-ft']):
                        
                        try:
                            if aircraft['flight'] == '':
                                reg = "(no tail)"
                            else:
                                reg = aircraft['flight']
                        except KeyError:
                            reg = "(no tail)"

                        # print ("New aircraft! {flight}".format(flight = reg))
                        masterAircraft.append(aircraft)

                        planeSpotted(aircraft, ps_config)
                        # requests.get("http://10.0.0.220:8081/yellowlight")
            #         else:
            #             print ("aircraft too high {reg}, {galt}".format(reg = aircraft["reg"], galt = aircraft["galt"]))
                # else:   # for debugging
                #     print ("Dupe aircraft {reg}".format(reg = aircraft['reg']))

                # TODO: if an aircraft in masterAircraft is *no longer* in the radius, remove it from the list
                # (can you remove it from the list?  yes)

    # for aircraft in masterAircraft:
    #     if aircraft not in newAircraft:
    #         try:
    #             tail = aircraft["flight"]
    #         except KeyError:
    #                 tail = "(bogey)"
    #         print ("{tail} no longer nearby and will be removed".format(tail=tail))
    #         # print (aircraft)
    #         masterAircraft.remove(aircraft)
    
    
    
    for aircraft in masterAircraft:
        if datetime.datetime.now() > aircraft["timestamp"] + datetime.timedelta(minutes = 1):
            try:
                tail = aircraft["flight"]
            except KeyError:
                tail = "(bogey)"
            # print ("{tail} has expired; removing".format(tail=tail))
            masterAircraft.remove(aircraft)
            
    for aircraft in masterAircraft:
        try:
            tail = aircraft["flight"]
        except KeyError:
                tail = "(bogey)"
        # print ("{tail} is still in masterAircraft".format(tail=tail))
    
    
    time.sleep(int(ps_config['api-query-interval-seconds']))