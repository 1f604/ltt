#https://github.com/flakas/Latte/blob/1a718adbd71acda22e30781ab4c76fdf9b590038/latte/Log.py
# -*- coding: utf-8 -*-

"""
Copyright (c) 2012 Tautvidas Sipavicius

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from sqlalchemy import Column, Integer, DateTime, Unicode, Boolean #, UnicodeText
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class LogEntry(Base):
    __tablename__ = 'logs'

    id = Column(Integer, primary_key=True)
    activity_state = Column(Unicode)
    window_title = Column(Unicode)
    window_class = Column(Unicode)
    window_instance = Column(Unicode)
    url = Column(Unicode)
    texthash = Column(Unicode)
    timestamp = Column(DateTime)
    duration = Column(Integer)

    def __init__(self, activity, window_title, window_class, window_instance, date,
                duration, url, texthash):
        self.activity_state = activity
        self.window_title = window_title
        self.window_class = window_class
        self.window_instance = window_instance
        self.timestamp = date
        self.duration = duration
        self.url = url
        self.texthash = texthash

    def __repr__(self):
        return "<LogEntry(%s, %s, %s, %s, %s, %s, %s, %s)>" % \
               (self.activity_state, self.window_title, self.window_class, self.window_instance,
                str(self.timestamp), str(self.duration), self.url, self.texthash)

class urlEntry(Base):
    __tablename__ = 'urls'

    id = Column(Integer, primary_key=True)
    unexpiredhash = Column(Unicode)
    url = Column(Unicode)
    last_checked = Column(DateTime)
    is_being_downloaded = Column(Boolean)
    #text = Column(UnicodeText)

    def __init__(self, url, unexpiredhash, last_checked,is_being_downloaded):
        self.url = url
        self.unexpiredhash = unexpiredhash
        self.last_checked = last_checked
        self.is_being_downloaded = is_being_downloaded

    def __repr__(self):
        return "<urlEntry(%s, %s, %s, %s)>" % \
               (self.url, self.unexpiredhash, self.last_checked, str(self.is_being_downloaded))
                