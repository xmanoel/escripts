#!/usr/bin/env python2.6
# vim: set fileencoding=utf-8 :

"""
extractbody.py
"""

from __future__ import with_statement
import os, sys, urllib
#from xml.etree import ElementTree
import re
import time
import datetime
import locale
import fnmatch
import os

from bs4 import BeautifulSoup
import htmlentitydefs
from tumblpy import Tumblpy

from cooonfig import config

# leave this info in the config file since it is private
APP_KEY = config['APP_KEY']
APP_SECRET = config['APP_SECRET']
OAUTH_TOKEN = config['OAUTH_TOKEN']
OAUTH_TOKEN_SECRET = config['OAUTH_TOKEN_SECRET']

# the rest of the configuration is here, freely editable
IMAGES_URL = 'http://website.com/images/posterous/'
BLOG_URL = 'AAAAAAAA.tumblr.net'
POST_FILE_PATTERN = "*.html"
DUPES_FILE = "dupes.txt"
#parameter when creating the post
STATE = 'published'
TAGS = 'postPosterous'

class PosterousToTumblr(object):

    # map holding the dupes log info
    dupes_log = {}
    dupes_log_file = ""

    def __init__(self):
        pass

    def postInTumblr(self,title,date,body):
        t = Tumblpy(app_key = APP_KEY,
                    app_secret = APP_SECRET,
                    oauth_token = OAUTH_TOKEN,
                    oauth_token_secret = OAUTH_TOKEN_SECRET)

        # Assume you are using the blog_url and Tumblpy instance from the previous sections
        photo = open('/Users/xmanoel/Documents/Development/posterous-verter/gotasdechuva.jpg', 'rb')
        post = t.post('post', blog_url=BLOG_URL, params={'type':'text', 'state':STATE, 'title':title, 'body':body, 'date':date, 'tags':TAGS})
        print post  # returns id if posted successfully


    def convertDate(self,dateString):
        # converts format like:
        #   January 12 2013, 11:00 AM
        dateStruc = time.strptime(dateString,"%B %d %Y, %I:%M %p")
        # time from posterous is Pacific Time, I will just add 8 hours to get
        # aprox the hour the post was made (this should be done in a much more
        # precise way using TimeZone utils from Python but it was not worth 
        # the efford for me)
        pacificTime = datetime.datetime(*dateStruc[:6])
        pacificToGMT=datetime.timedelta(hours=8)
        gmtTime = pacificTime + pacificToGMT
        # to date in format GTM like:
        #   2013-02-20 21:51:00 GMT
        convertedString = gmtTime.strftime("%Y-%m-%d %H:%M:%S GMT")
        return convertedString

    def fixBody(self,body):
        # search for imgs that are pointing to relative locations
        # and substitute that URL with the URL were the images
        # are stored now (we are not changing the names of the images or anything else)
        imgs = body("img")
        for img in imgs:
            src = img['src']
            if src.startswith("../../../image/"):
                src = src.replace("../../../image/",IMAGES_URL)
                img['src'] = src

        # some other corrections in the body can be added here

        return body

    def parseSoup(self,file):
        # open file and insert it into BeautifoulSoup
        f = open(file)
        soup = BeautifulSoup(f)

        # extract different parts of the message 
        headerHTML = soup.find("div", attrs={'class':'post_header'})
        bodyHTML = soup.find("div",attrs={'class':'post_body'})
        dateHTML = soup.find("span", attrs={'class':'post_time'})

        # extract the values of some of the fields from the html
        date = dateHTML.string
        title = headerHTML.h3.string
        dateGMT = self.convertDate(date)

        # correct the urls of the images in the body
        self.fixBody(bodyHTML)

        #print "date:%s" % date
        print "date:%s" % dateGMT
        print "title:%s" % title
        #print "body:%s" %  bodyHTML

        bodyText = str(bodyHTML)

        # make a short sleep of 30 seconds to not overload the 
        # tumblr server (I have plenty of time )
        time.sleep(10)

        self.postInTumblr(title,dateGMT,bodyText)

        self.dupesLogLog(file)
  
        f.close()


    def traverseFiles(self,folder,pattern):
        print "searching for %s in %s" % (pattern,folder)
        matches = []
        for root, dirnames, filenames in os.walk(folder):
            for filename in fnmatch.filter(filenames, pattern):
                matches.append(os.path.join(root, filename))
        return matches
        

    def dupesLog(self,folder):
        self.dupes_log_file = folder+"/"+DUPES_FILE
        if os.path.exists(self.dupes_log_file):
            f = open(DUPES_FILE,'r')
            self.dupes_log = {}
            for line in f:
                filename = line.rstrip(os.linesep)
                self.dupes_log[line] = filename
            f.close()
            print "%s" % self.dupes_log

    def dupesLogWrite(self):
        f = open(self.dupes_log_file,'w')
        for filename in self.dupes_log:
            f.write(filename)
            f.write(os.linesep)
        f.close()

    def dupesLogCheck(self,filename):
        if filename in self.dupes_log:
            return True
        else:
            return False

    def dupesLogLog(self,filename):
      self.dupes_log[filename] = filename



if __name__ == "__main__":

    file = ""

    locale.setlocale(locale.LC_ALL, 'en_US')


    if len(sys.argv) == 2:
        dirname = sys.argv[1]
    else:
        print "usage: %s path" % os.path.basename(sys.argv[0])
        exit(-1)

    if os.path.exists(dirname) and os.path.isdir(dirname):
        extractor = PosterousToTumblr()
        # to avoid having duplicated posts because of repeated runs
        # we will keep a log with the file names already posted
        script_path = os.path.dirname(os.path.abspath(sys.argv[0]))
        extractor.dupesLog(script_path)
        #extractor.parseSoup(filename)
        # app works for the .html files provided by the Posterous export ZIP
        pattern = POST_FILE_PATTERN
        filelist = extractor.traverseFiles(dirname,pattern)
        for filename in filelist:
            if not extractor.dupesLogCheck(filename):
                extractor.parseSoup(filename)
        extractor.dupesLogWrite()
    else:
        print "%s does not exist or it is not a folder" % dirname
        exit(-1)


