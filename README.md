# ltt
ltt - Linux Time Tracker 

# Table of contents
- [ltt](#ltt)
- [Table of contents](#table-of-contents)
- [What is it?](#what-is-it)
- [How to use](#how-to-use)
- [Files](#files)
- [Architecture](#architecture)
- [Features](#features)
- [Why did I make this?](#why-did-i-make-this)
- [Feature requests](#feature-requests)
- [License](#license)

# What is it?

Basically [ManicTime](https://www.manictime.com) for Linux. If you're not familiar with ManicTime, there's a nice video tutorial [here](https://www.youtube.com/watch?v=3lBCzW9P5mY) and [here](https://www.youtube.com/watch?v=A-Wp24Lr37k).

# How to use

`python ltt.py` to start logging your activity

Better still put it in Startup Applications (command: `python /path/to/ltt.py`). 

Run ltt.py for as long as you want your time tracked, it's ok to start and stop it at any time, since it writes to the database every time you switch window focus. 

When you want to view your stats you can open `logs.db` using any sqlite viewer or:

`python Analyzer.py`

You can see the options in `Analyzer.py`. Note that you can use either `-x` (to see past x days) or `-s` + `-e` (to specify an interval of days to see) but you should not use both. 

# Files

`logs.db` contains all the windows logs showing you when you did what and for how long
`visited` contains all the html downloaded, so you can grep through it for something you've seen in the past

# Architecture

There are 2 components, the logger, which gathers data, and the visualizer, which visualizes the data. 

Logger's responsibilities:

- Log activity with timestamp and duration
    - Activity - if user is active or idle 
    - Instance - which application is active
    - Title - name of currently active window
    - Log the URL if using chromium with extension
- Download the html at URL and save it into a cache (avoiding duplicates) - this will be without authentication, so websites that require login will not be logged

Analyzer's responsibilities: 

- Show duration and % of active duration of each application
- Show duration and % of total chromium duration and % of active duration of each domain and URL

# Features 

Implemented:

- Track computer usage (idle vs active)
- Track name of active window
- Track application usage
- Analyzer shows you how much active time you spent in each application and window title, which domains and websites you spent most time on (Chromium only), sorted in descending order of duration
- Analyzer allows you to select a date range that the statistics will be computed over, e.g today, past week, or custom date range. 

Not implemented:

- Allow applications and websites to be tagged into groups for analysis
- Produce nice tagging UI that hides already-tagged websites and duplicates as well as allow you to drag or multi-select (like ctrl-click) websites to tag multiple websites together
- Support for documents
- Produce more powerful browser history, showing days and times where a particular URL was visited and for how long it was visited each day. 
- Maybe produce a nice chart/UI like ManicTime does
- Tags timeline, except instead of just tags it will be an "event" (/task) with category, tags and description


# Why did I make this? 

Because ManicTime doesn't have a Linux version, and I don't want to give up the convenience of Linux just so I can have a proper time tracking software. 

# Feature requests

This software is mainly for my own use. It is supposed to be used by individuals to track their own time (as an alternative to browser history perhaps), not by employers to monitor their employees.  

If you want a feature, ask for it. If I think it's useful, then I'll implement it. If I think it's useless, then either implement it yourself or pay me to implement it. 

I will not be maintaining this for distros that I'm not using. I'm currently using Ubuntu 16.04, so this software is only checked to work on Ubuntu 16.04. When I upgrade to a new distro (either Ubuntu 18.04 or 20.04) then this will be updated accordingly. 

# License

Currently using GPLv3 for the lulz, may use a different license in future if I need to use some components that are not compatible with GPLv3. 
