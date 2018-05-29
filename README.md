# ltt
ltt - Linux Time Tracker 

# Table of contents
- [ltt](#ltt)
- [Table of contents](#table-of-contents)
- [What is it?](#what-is-it)
- [How to use](#how-to-use)
- [Architecture](#architecture)
- [Features](#features)
- [Why did I make this?](#why-did-i-make-this)
- [Feature requests](#feature-requests)
- [License](#license)

# What is it?

Basically [ManicTime](https://www.manictime.com) for Linux. If you're not familiar with ManicTime, there's a nice video tutorial [here](https://www.youtube.com/watch?v=3lBCzW9P5mY) and [here](https://www.youtube.com/watch?v=A-Wp24Lr37k).

# How to use

...to be written...

# Architecture

There are 2 components, the logger, which gathers data, and the visualizer, which visualizes the data. 

Logger's responsibilities:

- Timestamp data with duration
- Determine if user is active or idle 
- Determine what application is active
- Log the window name
- Log the URL or document name if applicable
- Download the html at URL and save it into a cache (avoiding duplicates) - this will be without authentication, so websites that require login will not be logged
- Link the cache with the records in the log (maybe use an ID)

Visualizer's responsibilities: 

- Summary statistics, on activity, application, document, and tag level, to sort applications/URLs/tags by time spent in a time range
- Bar charts and timelines
- Allow viewing chunks by full URL, host name, or domain name
- UI for tagging chunks of time and selecting chunks by URL/application 
- Allow tagging applications / URLs forever or by time period, e.g time spent on youtube could be either study or procrastination
- Full text browser history search (non-authenticated pages only)

# Features 

Implemented:

- Nothing

Todo:

- Track computer usage (idle vs active), like the activity timeline in ManicTime
- Track name of active window
- Track application usage, like the application timeline in ManicTime
- Allow applications and websites to be tagged into groups so you can tag games as procrastination and IDE as programming for summary statistics
- Produce nice tagging UI that hides already-tagged websites and duplicates as well as allow you to drag or multi-select (like ctrl-click) websites to tag multiple websites together
- Produce nice summary statistics showing how much active time you spent in each application, which documents you spent time editing, which websites you spent most time on, which tags you spent time on etc
- Produce more powerful browser history, showing days and times where a particular URL was visited and for how long it was visited each day. 
- Summary for individual days, weeks, months and so on. Allow users to select a date range that the statistics will be computed over. 
- Allow for easy browsing over each day to see day duration, active times, top applications, top documents (including websites). 
- Maybe track individual documents as well (not sure how ManicTime does it)
- Maybe produce a nice chart/UI like ManicTime does
- Tags timeline, except instead of just tags it will be an "event" (/task) with category, tags and description


# Why did I make this? 

Because ManicTime doesn't have a Linux version, and I don't want to give up the convenience of Linux just so I can have a proper time tracking software. 

# Feature requests

This software is mainly for my own use. It is supposed to be used by individuals to track their own time (as an alternative to browser history perhaps), not by employers to monitor their employees.  

If you want a feature, ask for it. If I think it's useful, then I'll implement it. If I think it's useless, then either implement it yourself or pay me to implement it. 

I will not be maintaining this for distros that I'm not using. I'm currently using Ubuntu 16.04, so this software is only checked to work on Ubuntu 16.04. When I upgrade to a new distro (either Ubuntu 18.04 or 20.04) then this will be updated appropriately. 

# License

Currently using GPLv3 for the lulz, may use a different license in future if I need to use some components that are not compatible with GPLv3. 
