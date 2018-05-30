import ctypes
import os
from ActivityTracker import ActivityTracker
import WindowTracker as w
from time import sleep
import datetime
now = datetime.datetime.now

a = ActivityTracker(5)


def download_html(url):
    pass

def mainloop():
    while True:
        sleep(0.05) #0.05 seems fast enough to capture the 1 inactivity before suspend, at least on my system.
        if a.is_user_inactive():
            print now(), "inactive"
        else:
            application = w.get_application()
            print application.window_title, "|", application.window_instance, "|", application.window_class, "|", application.wm_window_role, "|", application.is_browser
            if application.is_browser:
                url = application.url
                print now(), url
                download_html(url)
            elif application.has_document:
                print now(), application.document

mainloop()