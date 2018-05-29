# Origin: https://github.com/flakas/Latte/blob/1a718adbd71acda22e30781ab4c76fdf9b590038/latte/UserActivityTracker.py

"""
Copyright (c) 2012 Tautvidas Sipavicius

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import ctypes
import os
from subprocess import Popen, PIPE
from shlex import split

"""
Usage:
        
a = ActivityTracker(5)
sleep(10)
print(a.is_user_inactive())
"""

class XScreenSaverInfo(ctypes.Structure):
    """ typedef struct { ... } XScreenSaverInfo; """
    _fields_ = [('window', ctypes.c_ulong),  # screen saver window
                ('state', ctypes.c_int),  # off,on,disabled
                ('kind', ctypes.c_int),  # blanked,internal,external
                ('since', ctypes.c_ulong),  # milliseconds
                ('idle', ctypes.c_ulong),  # milliseconds
                ('event_mask', ctypes.c_ulong)]  # events


class ActivityTracker(object):

    def __init__(self, inactivity_threshold):
        self.inactivity_threshold = inactivity_threshold * 1000
        self.user_inactive = False
        if 'DISPLAY' in os.environ:
                xlib = ctypes.cdll.LoadLibrary('libX11.so')
                self.dpy = xlib.XOpenDisplay(os.environ['DISPLAY'])
                self.root = xlib.XDefaultRootWindow(self.dpy)
                self.xss = ctypes.cdll.LoadLibrary('libXss.so.1')
                self.xss.XScreenSaverAllocInfo.restype = ctypes.POINTER(XScreenSaverInfo)
                self.xss_info = self.xss.XScreenSaverAllocInfo()
        else:
            print("Error: no $DISPLAY environment variable")
            
    def __del__(self):        
        self.xss.XFree(self.xss_info)
        self.xss.XCloseDisplay(self.dpy)

    def is_user_inactive(self):
        """ Checks whether the user is inactive based on inactivity threshold """
        """ Also checks if screen is locked """
        if self.get_screen_locked():
            return True
        inactivity_duration = self.get_inactivity_time()
        if inactivity_duration > self.inactivity_threshold:
            if not self.user_inactive:
                self.user_inactive = True
        else:
            self.user_inactive = False
        return self.user_inactive

    def get_inactivity_time(self):
        self.xss.XScreenSaverQueryInfo(self.dpy, self.root, self.xss_info)
        return self.xss_info.contents.idle 
        
    def get_screen_locked(self):
        bashCommand = "gdbus call -e -d com.canonical.Unity -o /com/canonical/Unity/Session -m com.canonical.Unity.Session.IsLocked"
        command2 = "grep -ioP \"(true)|(false)\""
        p1 = Popen(split(bashCommand), stdout=PIPE)
        p2 = Popen(split(command2), stdin=p1.stdout, stdout=PIPE) 
        p1.stdout.close()
        output = p2.communicate()
        return output[0].strip('\n') == "true"