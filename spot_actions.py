# Customize this script to your heart's content!  This is where you can specify what happens
# when a new aircraft is spotted.
import json, pprint, requests
from termcolor import colored
from planespotter_helpers import *
from matrix import *
import subprocess


##### TWILIO SMS STUFF - REMOVE IF NOT USED #####

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
    
    degreesPan, degreesTilt, distance, cardinal, dist, deviance, estArrival_mins, type, tail, hex = generateStats(aircraft, config)
    status = generateHumanReadableStatus(degreesPan, degreesTilt, distance, cardinal, dist, deviance, estArrival_mins, type, tail, hex)
    
    
    # ser = serial.Serial('/dev/ttyUSB0', 9600)
    # print ("activating strobe light")
    # ser.write(hex_on)
    # time.sleep(5.0)
    # print ("strobe light off")
    # ser.write(hex_off)
    # ser.close()

    
    whitelist = ["BK17", # mbb / kawasaki
                 
                 "EC20", # aerospatiale / eurocopter / airbus
                 "EC30",
                 "EC35", 
                 "EC45",
                 "EC55",
                 "AS50",
                 "AS55",
                 "AS65",
                 "H160",
                 "BK17",
                 
                 "R22", # robinson
                 "R44",
                 "R66",
                 
                 "B06", # bell
                 "UH1",
                 "UH1N",
                 "B212",
                 "B407",
                 "B412",
                 "B429",
                 "B505",
                 
                 "H64", # boeing
                 "H47",
                 
                 "V22", # bell boeing
                 
                 "H60", # sikorsky
                 "S76",

                 "A139", # agusta-westland / leonardo
                 "A109",
                 "A119",
                 "A169",
                 
                 "G2CA", # guimbal
                 
                 "H500", # hughes
                 
                 "EN28", # enstrom
                 ]
    
    
    

    
    str = "{type}, {tail}, {est}m {cardinal}".format(type=type, tail=tail, est=estArrival_mins, cardinal=cardinal)
    
    try:
        if aircraft["t"] in whitelist:
            pprint.pprint(aircraft)
            print (colored(status, "yellow"))
            subprocess.Popen(["afplay", "airplane-ding-dong.wav"])
            # requests.get("http://10.0.0.44:8081/preset/hypetrain1")
            matrixAlert(4)
            for i in range(0, 3):
                matrixDrawFromString(str)
        else:
            print (status)
            matrixDrawFromString(str)
            
        

    except KeyError:
        if tail == "(unknown tail)":
            print (colored(status, "red"))
            subprocess.Popen(["afplay", "airplane-ding.wav"])
            matrixAlert(3)
            for i in range(0, 3):
                matrixDrawFromString("bogey")
        
