import ctypes
import os
from ActivityTracker import ActivityTracker
from time import sleep
import datetime

a = ActivityTracker(5)

lastloggedtime = datetime.datetime.now()

def t2s(t): #timedelta to seconds string
    return str(t.total_seconds()).split(".")[0]

def s2t(s): #seconds string to timedelta
    return datetime.timedelta(seconds=int(s))

def detectsleep():
    global lastloggedtime
    timediff = datetime.datetime.now() - lastloggedtime
    if timediff > datetime.timedelta(seconds=1):
        print "Slept:", t2s(timediff)
    lastloggedtime = datetime.datetime.now()

def mainloop():
    for i in range(50000):
        print datetime.datetime.now(), a.is_user_inactive()
        sleep(0.05) #0.05 seems fast enough to capture the 1 inactivity before suspend, at least on my system.

mainloop()