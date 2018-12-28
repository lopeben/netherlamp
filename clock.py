#!/usr/bin/python3

import time
import datetime
import os
import math
import subprocess

#subprocess.call(['sudo','chmod', '0777','/dev/display_digits']);
timedev = os.open("/dev/display_digits", os.O_RDWR);

def build_timecmd(hour, minute, colon):

    if (hour < 10):
        x = "X";
    elif (hour == 0):
        x = "0";
    else:
        x = "";

    if (colon):
        cmdstr = x + str(hour) + ":" + str(minute).zfill(2);
    else:
        cmdstr = x + str(hour) + " " + str(minute).zfill(2);
    return cmdstr;

def show_time(t, toggle):
    timecmd = build_timecmd(t.hour, t.minute, toggle);
    os.write(timedev, timecmd.encode());

def run_clock():
    toggle = 0;
    while True:
        date_and_time = datetime.datetime.now();
        if (toggle):
            show_time(date_and_time, toggle);
            toggle = 0;
        else:
            show_time(date_and_time, toggle);
            toggle = 1;
        time.sleep(1);


run_clock();
