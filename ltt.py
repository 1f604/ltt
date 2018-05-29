import ctypes
import os
from ActivityTracker import ActivityTracker
from time import sleep

a = ActivityTracker(5)


for i in range(50000):
    print(a.is_user_inactive())
    sleep(0.05)
    