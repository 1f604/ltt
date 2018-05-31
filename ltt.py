import urllib
from ActivityTracker import ActivityTracker
import WindowTracker as w
from time import sleep
import datetime
from datetime import timedelta
import dateutil.parser
from collections import defaultdict
import hashlib
now = datetime.datetime.now

a = ActivityTracker(5)
laststate = None
laststatechange = now()

lasthtmlhash = defaultdict(str)
lastchecked = defaultdict(lambda: datetime(1900,01,01))

def getDateTimeFromISO8601String(s):
    d = dateutil.parser.parse(s)
    return d

def download_html(url):
    f = urllib.urlopen(url)
    x = f.read()
    f.close()
    return x

def check_url_updated(url):
    lasthash = lasthtmlhash[url]
    x = download_html(url)
    newhash = hashlib.md5(x).hexdigest()
    if lasthash != newhash:
        #TODO: write html to file
        lasthash[url] = newhash
    pass

def statechange(state):
    global laststate
    global laststatechange
    if laststate != state:
        print laststate, laststatechange, now() - laststatechange
        laststate = state
        laststatechange = now()
        return True
    return False


def mainloop():
    while True:
        sleep(0.05) #0.05 seems fast enough to capture the 1 inactivity before suspend, at least on my system.
        if a.is_user_inactive():
            statechange("inactive")
        else:
            application = w.get_application()
            changed = statechange((application.window_title, application.window_class))
            if not changed: continue #if same as before, don't log. We only log durations
            print application.window_title, "|", application.window_instance, "|", application.window_class, "|", application.wm_window_role, "|", application.is_browser
            if application.is_browser:
                url = application.url
                print now(), url
                #if lastchecked[url] - now() > timedelta(days=1):
                    #check_url_updated(url)
                #lastchecked[url] = now()
                #print lastchecked[url]
                #download_html(url)
            elif application.has_document:
                print now(), application.document

mainloop()