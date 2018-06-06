# -*- coding: utf-8 -*-

finalhour = 23
import DBStructures
from DBStructures import LogEntry
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import func
import argparse
from datetime import datetime
from datetime import timedelta
import dateutil.parser
 # construct the argument parse and parse the arguments
today = datetime.now() - timedelta(days=1) 
today = today.replace(hour=finalhour, minute=0, second=0, microsecond=0)
ap = argparse.ArgumentParser()
ap.add_argument("-x", "--last", type=int, default=0,
	help="last x days, 0 means today, 1 means yesterday+today")
ap.add_argument("-s", "--start", type=str, default=None,
	help="start date, format 20080931")
ap.add_argument("-e", "--end", type=str, default=None,
	help="end date, usage: python Analyzer.py -s 20180517 -e 20180602")
ap.add_argument("-n", "--num", type=int, default=20,
	help="limit number of entries to display each table")
ap.add_argument("-d", "--dur", type=int, default=60,
	help="limit number of entries to display each table")
ap.add_argument("-a", "--all", action='store_true',
	help="display all entries")
args = vars(ap.parse_args())
last = args["last"]
start = args["start"] 
end = args["end"]
num = args["num"]
dur = args["dur"]
dall = args["all"]
ordering = func.sum(LogEntry.duration).desc()
if start != None and end != None:
    start = dateutil.parser.parse(start) - timedelta(days=1) 
    start = start.replace(hour=finalhour, minute=0, second=0, microsecond=0)
    end = dateutil.parser.parse(end)
    end = end.replace(hour=finalhour, minute=0, second=0, microsecond=0)
else:
    start = today - timedelta(days=last)
    end = datetime.now()
    
print start,end

def tf(interval):
    return str(timedelta(seconds=interval)).split('.')[0]

def f2p(num):
    return str(num*100)[0:4]+"%"
    
def printlog(logs, title, index, attribute):
    log = logs.group_by(attribute).order_by(ordering)
    if not dall:
        log = log.having(func.sum(LogEntry.duration) >= dur)
        log = log.limit(num)
    if log.count() <= 0:
        print "The logs are empty"
        return
    print title+":"
    for l in log:
        if l[index] != None:
            if attribute == LogEntry.domainname or attribute == LogEntry.url and chromium_duration > 0:
                print tf(l[0]), f2p(l[0] / chromium_duration), f2p(l[0] / active_duration), l[index]
            else:
                print tf(l[0]), f2p(l[0] / active_duration), l[index]
    print "======================================"
def main():
    global active_duration
    global chromium_duration
    chromium_duration = 0
    session = sessionmaker()
    engine = create_engine('sqlite:///logs.db')
    session.configure(bind=engine)
    DBStructures.Base.metadata.create_all(engine)
    s = session()
    # return count of user "id" grouped
    # by "name"
    logs = s.query(func.sum(LogEntry.duration).label('duration'), 
                   LogEntry.activity_state, LogEntry.window_title, 
                   LogEntry.window_instance, LogEntry.domainname, 
                   LogEntry.url)
    
    logs = logs.filter(LogEntry.timestamp > start)
    logs = logs.filter(LogEntry.timestamp < end)
    
    activities = logs.group_by(LogEntry.activity_state).order_by(ordering)    
    
    if activities.count() < 2:
        print "data insufficient in time range"
        return
        
    # now we have active, inactive, and total durations
    active_duration = activities.filter(LogEntry.activity_state.like(u"active"))[0][0]
    inactive_duration = activities.filter(LogEntry.activity_state.like(u"inactive"))[0][0]
    total_duration = active_duration + inactive_duration
    print "Active:", tf(active_duration), "out of", tf(total_duration)
    
    # create logs
    applications = logs.group_by(LogEntry.window_instance).order_by(ordering)
    chromium = activities.filter(LogEntry.window_instance.like(u"Chromium-browser"))
    if chromium.count() == 1:
        chromium_duration = chromium[0][0]
        print chromium_duration
    titles = logs.group_by(LogEntry.window_title).order_by(ordering)
    urls = logs.group_by(LogEntry.url).order_by(ordering)
    domains = logs.group_by(LogEntry.domainname).order_by(ordering)
    logss = [applications, titles, urls, domains, activities]
    # limit each log to limits set in parameters
    for log in logss:
        if not dall:
            log = log.having(func.sum(LogEntry.duration) >= dur)
            log = log.limit(num)
        if log.count() <= 0:
            print "The logs are empty"
            return
            
    # print applications
    printlog(applications,"applications",3,LogEntry.window_instance)
    printlog(titles,"titles",2,LogEntry.window_title)
    printlog(domains,"domains",4,LogEntry.domainname)
    printlog(urls,"urls",5,LogEntry.url)
    total_duration = end - start
    print total_duration
    
    print(logs)
    
main()