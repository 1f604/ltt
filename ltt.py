import ctypes
import os
from ActivityTracker import ActivityTracker
from time import sleep

a = ActivityTracker(5)
sleep(10)
print(a.get_inactivity_time())
print(a.is_user_inactive())