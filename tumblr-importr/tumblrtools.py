#!/usr/bin/env python2.6
# vim: set fileencoding=utf-8 :

from __future__ import with_statement
import os, sys, urllib
from bs4 import BeautifulSoup
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



class TumblrTools(object):

    def __init__(self):
        pass


    def requestToken():
        # Go to http://www.tumblr.com/oauth/apps and click your
        # app to find out your dynamic callback url
        t = Tumblpy(app_key = APP_KEY,
                    app_secret = APP_SECRET,
                    callback_url = 'http://' + BLOG_URL)
        return
        auth_props = t.get_authentication_tokens()
        auth_url = auth_props['auth_url']

        oauth_token = auth_props['oauth_token']
        oauth_token_secret = auth_props['oauth_token_secret']

        print "token: %s"  % oauth_token
        print "token_secret: %s" % oauth_token_secret
        print "connect to tumblr via %s" % auth_url

        print "once connected obtain the value in the URL with the tag oauth_verifier"


        t = Tumblpy(app_key = APP_KEY,
                    app_secret = APP_SECRET,
                    oauth_token = oauth_token,
                    oauth_token_secret = oauth_token_secret)

        oauth_verifier = raw_input("inserta el oauth verifier: ")

        authorized_tokens = t.get_authorized_tokens(oauth_verifier)

        final_oauth_token = authorized_tokens['oauth_token']
        final_oauth_token_secret = authorized_tokens['oauth_token_secret']

        print "token: %s"  % final_oauth_token
        print "token_secret: %s" % final_oauth_token_secret



    def getPosts():
        t = Tumblpy(app_key = APP_KEY,
                    app_secret = APP_SECRET,
                    oauth_token = OAUTH_TOKEN,
                    oauth_token_secret = OAUTH_TOKEN_SECRET)

        # Print out the user info, let's get the first blog url...
        blog_url = t.post('user/info')
        blog_url = blog_url['user']['blogs'][0]['url']
        print "url: %s" % blog_url
        # Assume you are using the blog_url and Tumblpy instance from the previous section
        posts = t.get('posts', blog_url=blog_url)
        for post in posts['posts']:
            print "%s %s" % (post['date'],post['post_url'])


    def demoPost():
        t = Tumblpy(app_key = APP_KEY,
                    app_secret = APP_SECRET,
                    oauth_token = OAUTH_TOKEN,
                    oauth_token_secret = OAUTH_TOKEN_SECRET)

        # Print out the user info, let's get the first blog url...
        blog_url = t.post('user/info')
        blog_url = blog_url['user']['blogs'][0]['url']

        # Assume you are using the blog_url and Tumblpy instance from the previous sections
        post = t.post('post', blog_url=blog_url, params={'type':'text', 'state':'private', 'title':'titulo', 'body':'<p>This is a body</p>'})
        print post  # returns id if posted successfully

    def hidePosts():
        t = Tumblpy(app_key = APP_KEY,
                    app_secret = APP_SECRET,
                    oauth_token = OAUTH_TOKEN,
                    oauth_token_secret = OAUTH_TOKEN_SECRET)

        # Print out the user info, let's get the first blog url...
        blog_url = t.post('user/info')
        blog_url = blog_url['user']['blogs'][0]['url']
        print "url: %s" % blog_url
        # Assume you are using the blog_url and Tumblpy instance from the previous section
        posts = t.get('posts', blog_url=blog_url, params={'tag':"JustMigrate"})
        for post in posts['posts']:
            print "%s %s" % (post['date'],post['post_url'])
            id = post['id']
            post = t.post('edit', blog_url=blog_url, params={'id':id,'state':'private'})
            print "ahora está en estado %s" % post['state']

    def deletePosts(tag):
        t = Tumblpy(app_key = APP_KEY,
                    app_secret = APP_SECRET,
                    oauth_token = OAUTH_TOKEN,
                    oauth_token_secret = OAUTH_TOKEN_SECRET)

        # Print out the user info, let's get the first blog url...
        blog_url = t.post('user/info')
        blog_url = blog_url['user']['blogs'][0]['url']
        print "url: %s" % blog_url
        # Assume you are using the blog_url and Tumblpy instance from the previous section
        posts = t.get('posts', blog_url=blog_url, params={'tag':tag})
        for post in posts['posts']:
            print "%s %s" % (post['date'],post['post_url'])
            id = post['id']
            post = t.post('post/delete', blog_url=blog_url, params={'id':id})
            print "post deleted!!"


    if __name__ == "__main__":

        if len(sys.argv) > 1:
            command = sys.argv[1]
        elif len(sys.argv) > 1:
            command = sys.argv[1]
            option = sys.argv[2]
        else:
            print "usage: %s [get-token|delete-tag] [tag]" % os.path.basename(sys.argv[0])
            exit(-1)

        if command.lower() == 'get-token':
            requestToken()
        elif command.lower() == 'delete-tag' and option:
            deletePosts(option)
        

