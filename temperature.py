#!/usr/bin/python3

import urllib.request
import json
import time
import datetime

url = "http://api.openweathermap.org/data/2.5/weather?"
url = url + "q=manila"
url = url + "&"
url = url + "APPID="

while True:
    date_and_time = datetime.datetime.now()
    #contents = urllib.request.urlopen("http://api.openweathermap.org/data/2.5/weather?q=manila&APPID=").read()
    contents = urllib.request.urlopen(url).read()    
    wdata = json.loads(contents)
    pressure = wdata["main"]["pressure"]
    temperature = wdata["main"]["temp"]
    humidity = wdata["main"]["humidity"]
    print(date_and_time.strftime("%c"), 'Temperature: {0}'.format(temperature/10))
    time.sleep(1800) # Delay for 30 minutes (1800 seconds)
