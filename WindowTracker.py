# Origin: https://github.com/flakas/Latte/blob/1a718adbd71acda22e30781ab4c76fdf9b590038/latte/latte.py

"""
Copyright (c) 2012 Tautvidas Sipavicius

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

chromium_title_suffix = " - Chromium"

import subprocess
import sys  
from urlparse import urlparse
reload(sys)  
sys.setdefaultencoding('utf8')

def rchop(thestring, ending):
  if thestring.endswith(ending):
    return thestring[:-len(ending)]
  else:
    print("Error: Expected Chromium window title to end with", ending)
    #exit(1)
  return thestring

class ApplicationInfo(object):
    def __init__(self):
        self.is_browser = False
        self.has_document = False
        self.application_name = None
        self.wm_title_class = None
        self.window_title = None
        self.window_class = None
        self.window_instance = None
        self.url = None
        self.domainname = None
        self.document = None

def get_chromium_url(a):
    a.window_title = rchop(a.window_title, chromium_title_suffix)
    if " |url:" not in a.window_title:
        a.url = None
        return
    s = a.window_title.split(" |url:")
    a.window_title = s[0]
    s = s[-1]#.split(" ")[0]
    if s:
        a.domainname = urlparse(s).hostname
        a.url = s

def get_application():
    """ Fetches active window info using xprop. """
    a = ApplicationInfo()
    active = subprocess.Popen(["xprop", "-root", "_NET_ACTIVE_WINDOW"],
                              stdout=subprocess.PIPE)
    active_id = active.communicate()[0].strip().split()[-1]
    window = subprocess.Popen(["xprop", "-id", active_id, "WM_NAME"],
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)
    title = window.communicate()[0].strip().split('"', 1)[-1][:-1]
    wm_class = subprocess.Popen(["xprop", "-id", active_id, "WM_CLASS"],
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)
    wm_class_message = wm_class.communicate()[0].strip().split('"')
    if len(wm_class_message) > 3:
        window_class = wm_class_message[1]
        window_instance = wm_class_message[3]
    else:
        window_class = None
        window_instance = None
    a.window_title = unicode(title)
    a.window_class = unicode(window_class)
    a.window_instance = unicode(window_instance)
    if window_class == "chromium-browser":
        a.is_browser = True
        get_chromium_url(a)
    return a



