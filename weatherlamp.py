#!/usr/bin/python3

import urllib.request
import json
import time
import datetime
import os
import colorsys as cs
import math
import subprocess
from urllib.request import Request, urlopen
from urllib.error import  URLError


logfile = "muntinlupa.txt";

lightdev = os.open("/dev/led_controller", os.O_RDWR);
idfile = open("appid.txt", "r");

url = "http://api.openweathermap.org/data/2.5/weather?"
url = url + "q=muntinlupa"
url = url + "&"

def build_lightcmd(led_id, pwm, duration):
    cmdstr = "1 " + str(led_id);
    cmdstr = cmdstr + " " + str(pwm);
    cmdstr = cmdstr + " " + str(duration);
    return cmdstr;

def display_state(state):
    leds  = [16, 17, 18];
    for i in leds:
        lightcmd = build_lightcmd(i, state, 0);
        os.write(lightdev, lightcmd.encode());

def red_sequence(intensity):
    reds = [0, 3, 6, 9];
    for i in reds:
        lightcmd = build_lightcmd(i, intensity, 0);
        os.write(lightdev, lightcmd.encode());
        time.sleep(0.05);
        display_state(0);
        time.sleep(0.05);

def green_sequence(intensity):
    greens = [1, 4, 7, 10];
    for i in greens:
        lightcmd = build_lightcmd(i, intensity, 0);
        os.write(lightdev, lightcmd.encode());
        time.sleep(0.07);
        display_state(0);
        time.sleep(0.05);

def pwm_threshold(x, thresh_max, thresh_min):
    if (x > thresh_max):
        return thresh_max;
    elif (x < thresh_min):
        return thresh_min;
    else:
        return x;

def display_direct(h, s, l):
    r,g,b = cs.hls_to_rgb(h, l, s);

    r = pwm_threshold(math.ceil(255 * r), 255, 0);
    g = pwm_threshold(math.ceil(255 * g), 255, 0);
    b = pwm_threshold(math.ceil(255 * b), 255, 0);
    
    print('Red: {0}'.format(r), 'Green: {0}'.format(g), 'Blue: {0}'.format(b));
    print('Red: {0}'.format(r), 'Green: {0}'.format(g), 'Blue: {0}'.format(b), file=open(logfile,"a"));

    rcmd = build_lightcmd(16, r, 0);
    gcmd = build_lightcmd(17, g, 0);
    bcmd = build_lightcmd(18, b, 0);

    os.write(lightdev, rcmd.encode());
    os.write(lightdev, gcmd.encode());
    os.write(lightdev, bcmd.encode());

def rescale_input(x, in_max, in_min, out_max, out_min):
    y = (((out_max - out_min)*(x - in_min)) / (in_max - in_min)) + out_min;
    return y;

while True:
    
    date_and_time = datetime.datetime.now();
    #contents = urllib.request.urlopen(url).read() 

    if (idfile.mode == 'r'):
        appid = idfile.read();
        url += appid;
        req = Request(url);
        try:
            response = urlopen(req);
        except URLError as e:
            if hasattr(e, 'reason'):
                print('We failed to reach a server.')
                print('Reason: ', e.reason)
            elif hasattr(e, 'code'):
                print('The server couldn\'t fulfill the request.')
                print('Error code: ', e.code)
        else:
           contents = response.read();

    wdata = json.loads(contents);

    pressure = wdata["main"]["pressure"]
    temperature = wdata["main"]["temp"]
    humidity = wdata["main"]["humidity"]

    print(date_and_time.strftime("%c"));
    print(date_and_time.strftime("%c"), file=open(logfile, "a"));

    print('Temp: {0}'.format(temperature/10), 'Hum: {0}'.format(humidity), 'Press: {0}'.format(pressure));
    print('Temp: {0}'.format(temperature/10), 'Hum: {0}'.format(humidity), 'Press: {0}'.format(pressure), file=open(logfile,"a"));

    h = rescale_input(temperature/10, 30.43, 29.7, 0.1, 0.9);
    s = rescale_input(humidity, 100, 50, 0.9, 0.5);
    l = rescale_input(pressure, 1015, 1008, 0.5, 0.1);

    print('Hue: {0}'.format(h), 'Sat: {0}'.format(s), 'Lum: {0}'.format(l));
    print('Hue: {0}'.format(h), 'Sat: {0}'.format(s), 'Lum: {0}'.format(l), file=open(logfile,"a"));

    display_direct(h, s, l);
    time.sleep(1800) # Delay for 30 minutes (1800 seconds)
