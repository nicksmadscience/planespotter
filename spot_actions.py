# Customize this script to your heart's content!  This is where you can specify what happens
# when a new aircraft is spotted.
import json, pprint, requests
from termcolor import colored
from planespotter_helpers import *
from matrix import *


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
    
hex_on = bytearray.fromhex('a00101a2')
hex_off = bytearray.fromhex('a00100a1')

import serial, time
# ser = serial.Serial('/dev/ttyUSB0', 9600)  # open serial port

# while True:
#     ser.write(hex_on)
#     time.sleep(1.0)
#     ser.write(hex_off)
#     time.sleep(1.0)

def planeSpotted(aircraft, config):
    '''Called by main script when an aircraft is spotted nearby.  This is where all your custom functionality goes.'''
    # exampleAlertFunction(aircraft)
    
    degreesPan, degreesTilt, distance, cardinal, dist, deviance, estArrival_mins, type, tail = generateStats(aircraft, config)
    status = generateHumanReadableStatus(degreesPan, degreesTilt, distance, cardinal, dist, deviance, estArrival_mins, type, tail)
    
    
    # ser = serial.Serial('/dev/ttyUSB0', 9600)
    # print ("activating strobe light")
    # ser.write(hex_on)
    # time.sleep(5.0)
    # print ("strobe light off")
    # ser.write(hex_off)
    # ser.close()

    
    whitelist = ["EC35",
                 "EC20",
                 "AS65",
                 "EC45",
                 "B06",
                 "R22",
                 "R44",
                 "R66",
                 "B412",
                 "B407",
                 "B429",
                 "EC55",
                 "BK17",
                 "AS50",
                 "UH1",
                 "H60",
                 "A139",
                 "A109",
                 "A119"
                 ]
    
    

    try:
        if aircraft["t"] in whitelist:
            # sendTwilioTextMessage (client, status)   # Remove if not using Twilio SMS
            print (colored(status, "yellow"))
            matrixAlert(4)
            
            matrixDrawFromString(aircraft['t'])
                
            time.sleep(3)
            try:
                matrixDrawFromString(aircraft["flight"])
                time.sleep(3)
            except KeyError:
                pass
        else:
            print (colored(status, "blue"))
            # matrixAlert()
            
            matrixDrawFromString(aircraft['t'])
                
            time.sleep(3)
            try:
                matrixDrawFromString(aircraft["flight"])
                time.sleep(3)
            except KeyError:
                pass
    except KeyError:
        print (colored(status, "red"))
        matrixAlert(3)
        matrixDrawFromString("bogey")
        time.sleep(3)
        
    # print ("e")
    # if aircraft["t"] not in whitelist:
    
        