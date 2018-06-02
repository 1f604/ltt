inactivity_timeout = 6
recheck_url_days = 1

import urllib2
import threading
from threading import Thread
import DBStructures 
from bs4 import BeautifulSoup
from ActivityTracker import ActivityTracker
import WindowTracker as w
from time import sleep
import datetime
from datetime import timedelta
import dateutil.parser
from collections import defaultdict
import hashlib
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
now = datetime.datetime.now

AT = ActivityTracker(inactivity_timeout)
laststate = ("inactive",None)
laststatechange = now()
http_timeout = 10

lasthtmlhash = defaultdict(str)
lastchecked = defaultdict(lambda: datetime.datetime(1900,01,01))

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

session = sessionmaker()
engine = create_engine('sqlite:///sqlalchemy_example.db', connect_args={'check_same_thread': False}, echo=False)
session.configure(bind=engine)
DBStructures.Base.metadata.create_all(engine)
s = session()


def getDateTimeFromISO8601String(s):
    d = dateutil.parser.parse(s)
    return d

def get_text_from_html(html):
    soup = BeautifulSoup(html, "lxml")
    for script in soup(["script", "style"]):
        script.extract()    # rip it out
    text = soup.get_text()
    return text

def download_text(url):
    req = urllib2.Request(url, headers=hdr)
    text = None
    try:
        f = urllib2.urlopen(req, timeout=http_timeout)
        http_message = f.info()        
        main = http_message.maintype # 'text'
        if main != "text":
            print "not text"
            return -1
        html = f.read()
        f.close()
        text = get_text_from_html(html)
    except Exception as e:
        print e
    return text

def check_url_updated(url, entry_id):
    lastchecked[url] = now()
    lasthash = lasthtmlhash[url]
    x = download_text(url)
    if x == -1:
        print "url not text:", url
        return
    entry = s.query(DBStructures.LogEntry).get(entry_id)
    if x == None:
        print "failed to download url:", url
        lastchecked[url] = datetime.datetime(1900,01,01) #reset so we can re-download next time. 
        entry.texthash = u"failed to download"
        s.commit()        
        return
    newhash = unicode(hashlib.sha256(x.encode('utf-8')).hexdigest())
    entry.texthash = newhash
    s.commit()
    if lasthash != newhash:
        print "new text detected"
        print x
        #TODO: write html to file
        lasthtmlhash[url] = newhash
        return
    print "old text detected"


def statechange(state):
    statetitle = state[0]
    global laststate
    global laststatechange
    if laststate[0] != statetitle:
        for thread in threading.enumerate(): print(thread.name)
        duration = (now() - laststatechange).total_seconds()
        if laststate[0] == "inactive":
            s.add(DBStructures.LogEntry(unicode(laststate[0]), None, None, None, now(), duration, None, None))
        else:
            app = laststate[1]
            s.add(DBStructures.LogEntry(unicode("active"), app.window_title, app.window_class, app.window_instance, now(), duration, app.url, None))            
        s.commit()
        laststate = state
        laststatechange = now()
        return True
    return False


def mainloop():
    while True:
        sleep(0.05) #0.05 seems fast enough to capture the 1 inactivity before suspend, at least on my system.
        if AT.is_user_inactive():
            statechange(("inactive",None))
        else:
            application = w.get_application()
            statechange((application.window_title+application.window_class,application))
            

mainloop()