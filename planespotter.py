import requests, json, pprint, time, yaml, datetime, csv



with open("secrets-adsbx.json", "r") as secrets_file:
    secrets = json.load(secrets_file)
    key = secrets["x-rapidapi-key"]

with open(r'planespotter-conf.yaml') as file:
    ps_config = yaml.load(file, Loader=yaml.FullLoader)
    

from planespotter_helpers import *
from spot_actions import *

# url = 'https://adsbexchange-com1.p.rapidapi.com/v2/lat/{lat}/lon/{lon}/dist/{dist}/'.format(lat = ps_config['location']['latitude'], lon = ps_config['location']['longitude'], dist = ps_config['filters']['max-distance-nm'])

# headers = {
#     "X-RapidAPI-Host": "adsbexchange-com1.p.rapidapi.com",
#     "X-RapidAPI-Key": key
#     }


url = 'http://10.0.0.222/tar1090/data/aircraft.json'

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
    # response = requests.request("GET", url, headers=headers)
    response = requests.request("GET", url)
    # print (response.text)

    try:
        currentAircraftList = json.loads(response.text)['aircraft']
        # pprint.pprint (currentAircraftList)
    except KeyError:
        currentAircraftList = None
    except:
        traceback.print_exc()

    if currentAircraftList != None:

        # pprint.pprint (currentAircraftList)

        numberOfAircraft = 0
        for aircraft in currentAircraftList:
            aircraft["timestamp"] = datetime.datetime.now()
            # pprint.pprint(aircraft)
            numberOfAircraft += 1
            # print ("now processing aircraft {noa} of {total}".format(noa = numberOfAircraft, total = len(currentAircraftList)))

            # this is cool; thanks Odorlemon for the assist!
            aircraft_hash = { aircraft['hex']: aircraft for aircraft in masterAircraft }
            # pprint.pprint (aircraft_hash)

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
    #     if aircraft not in currentAircraftList:
    #         try:
    #             tail = aircraft["flight"]
    #         except KeyError:
    #                 tail = "(bogey)"
    #         print ("{tail} no longer nearby and will be removed".format(tail=tail))
    #         # print (aircraft)
    #         masterAircraft.remove(aircraft)
    
    
    # Expiration handling
    for aircraft in masterAircraft:
        try:
            tail = aircraft["flight"]
        except KeyError:
            tail = "(bogey)"
            
        time_now = datetime.datetime.now()
        aircraft_timestamp = aircraft["timestamp"]
        aircraft_timestamp_plus_delta = aircraft["timestamp"] + datetime.timedelta(minutes = 1)
        
        # print ("time_now: ", time_now)
        # print ("aircraft_timestamp: ", aircraft_timestamp)
        # print ("aircraft_timestamp_plus_delta: ", aircraft_timestamp_plus_delta)
                
        if datetime.datetime.now() > aircraft["timestamp"] + datetime.timedelta(minutes = 1):
            if aircraft not in currentAircraftList:
                print ("{tail} has expired and is no longer in currentAircraftList; removing".format(tail=tail))
                masterAircraft.remove(aircraft)
            else: 
                print ("{tail} has expired but is still in currentAircraftList; not removing yet".format(tail=tail))
                
            print ()
            
    for aircraft in masterAircraft:
        print ("{tail} is still in masterAircraft".format(tail=tail))
    
    
    time.sleep(int(ps_config['api-query-interval-seconds']))