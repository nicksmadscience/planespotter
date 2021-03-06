# Customize this script to your heart's content!  This is where you can specify what happens
# when a new aircraft is spotted.
import json, pprint, requests
from planespotter_helpers import *


#### TWILIO SMS STUFF - REMOVE IF NOT USED #####

from twilio.rest import Client

# Secrets file needs to include "twilio-sid" and "twilio-token"; you can grab these
# from your Twilio console.  From and To numbers are also specified here so you're
# not hard-coding your private numbers
with open("secrets-twilio.json", "r") as secrets_file:
    secrets = json.load(secrets_file)

client = Client(secrets["twilio-sid"], secrets["twilio-token"])

def sendTwilioTextMessage(twilioClient, message):
    '''Allows you to send an SMS message from / to the number you specify,
    using the power of Twilio SMS.'''
    message = twilioClient.messages \
        .create(
                body = message,
                from_ = secrets["from"],
                to = secrets["to"]
            )

##### END TWILIO STUFF #####

    




##### HERE'S WHERE YOU PUT THE STUFF YOU WANT TO HAPPEN #####

def exampleAlertFunction(aircraft):
    pprint.pprint(aircraft)

def planeSpotted(aircraft, config):
    '''Called by main script when an aircraft is spotted nearby.  This is where all your custom functionality goes.'''
    # exampleAlertFunction(aircraft)

    status = generateHumanReadableStatus(aircraft, config['location']['latitude'], config['location']['longitude'])
    print (status)
    

    if aircraft["type"] == "EC35" or aircraft["type"] == "AS65" or aircraft["type"] == "EC45" or aircraft["type"] == "B06" or aircraft["type"] == "R66" or aircraft["type"] == "BK17":
        requests.get("http://10.0.0.220:8081/raidlight")
        sendTwilioTextMessage (client, status)   # Remove if not using Twilio SMS
    # else:
    #     requests.get("http://10.0.0.220:8081/yellowlight")


