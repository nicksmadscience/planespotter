# Planespotter

A Python script to alert you of awesome aircraft in your area!  Uses the adsbexchange API to pull aircraft data.



## How to install

You'll need access to the [ADS-B Exchange AP](https://rapidapi.com/adsbx/api/adsbexchange-com1).  This is normally available for US$10 per month, but I've heard if you are feeding ADS-B data to ADS-B Exchange, this fee is waived.  (I don't have any further info on this at the moment.)

You'll need to add your ADS-B Exchange RapidAPI key to secrets-adsbx.json.



If you want to use the Twilio SMS library to send alerts, you'll need to install the [Twilio Python Helper Library](https://www.twilio.com/docs/libraries/python)...

	pip3 install twilio
	
Your Twilio SID and token will need to be added to secrets-twilio.json, as well as your _from_ and _to_ numbers.

planespotter.py is the main script, which runs continuously...

	python3 planespotter.py


## How to configure

The bulk of the configuration is done in planespotter-conf.yaml.  A sample configuration file is included.

