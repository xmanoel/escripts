What's this?
------------

These are some Python scripts I have made to import my existing
websites into Tumblr. They were made for my personal use, but I am
sharing them in case they are of use for anyone. 

They are not out-of-thebox usable solution, neither are great Python
code to learn from. 

So far what is implemented:

  - posterous2tumblr.py : This one grabs the posts from a Posterous
    export (the ZIP file, the HTML files, not the XML ones) and
    inserts them in tumblr while keeping the original date (well
    somehow). For the posts with Images (most of my posterous posts had
    images) I rewrite the urls to point to the place where I have moved
    those pictures (they are available on the ZIP file from Posterous as
    well). 

   - tumblrtools.py: For the script to connect to Tumblr you need to
     get an application ID (get it http://www.tumblr.com/oauth/apps),
    and to register the script using oauth. This script does the steps to
    register oauth, but you have to manually get the tokens and add them
    to the config. It has also a function I use to delete all the posts
    with a certain tag (I used it to clean up while testing the importer).

Installation
------------

1) Download the repository (sorry I am placing all my python scripts
in one repository, so you will be getting extra stuff!!)

        git clone https://github.com/xmanoel/escripts.git

The scripts are in the `escripts/tumblr-importr`folder.

2) Installation:

The script was coded an run in Python 2.6. 

Dependencies:
    - BeautifulSoup 4 - I installed it using the command `easy_install beautifulsoup4` feel free to use pip instead.

Additional modules:
(This moudules could be installed on your system, but I have not
installed them, just copied them to the folder where my script, since 
I am not using them for other thing that this own script)
    
    - requests from https://github.com/kennethreitz/requests.git
    - requests-oauthlib from https://github.com/requests/requests-oauthlib.git
    - oauthlib - https://github.com/idan/oauthlib.git
    - ptython-tumblpy -  https://github.com/michaelhelmick/python-tumblpy.git  

What I did is I downloaded each one of this repositories doing a `git clone ....` for each one.
And then I copied the following folders and files to my
`escripts/tumblr-importr`folder:

    - `oauthlib/` 
    - `requests/`
    - `requests_oauthlib/`
    - `tumblpy.py`

(Summary, I copied tree folders from the 3 projects and then just
tumblpy.py from the last one, because it is like that simple)

3) Configuration

For the script to work, you need to have the keys and the oauth tokens
for Tumblr. 

    - The Key and The secret are obtained from http://www.tumblr.com/oauth/apps. No worries, you don't need to have a website or anything, to get them. I just got mine, and I entered my tumblr url as the app url. Once done, you have to long string of characters, the 'APP_KEY' and the 'APP_SECRET'. 

    - Add those two to the coonfig.py file, and then run `./tumblrtools.py get-token`. You will get an url, paste it in the browser and authorise your own APP_KEY. Then it redirects to your own blog, and you grab the last part of the URL, another ID. You enter it to the prompt and at the end you will get the two tokens. 

    - Add this last two tokens to the coonfig.py OAUTH_TOKEN' and 'OAUTH_TOKEN_SECRET'

I feel tired to write about this so if you don't mind I rather stop
here. The process works, and it is not that complex. But if you need
help better leave me a comment in GitHub. I will try to answer. 

Use
---

1) For Posterous

Get your exported ZIP file from Posterous. Inside of the file, the
posts are on the `posts/` folder. Unzip that.

Get your images: they are on the `image/` folder. Upload them to a
place where you can host the photos. (Sorry for this, I have a website
where I simply sftped them and I could keep the directories and so on)

Open the script and check at the start if the parameters are the ones
you would like to have set up. The version I have here updated has
just some dummy/sample values:

    # the rest of the configuration is here, freely editable
    IMAGES_URL = 'http://website.com/images/posterous/'
    BLOG_URL = 'AAAAAAAA.tumblr.net'
    POST_FILE_PATTERN = "*.html"
    DUPES_FILE = "dupes.txt"
    #parameter when creating the post
    STATE = 'published'
    TAGS = 'postPosterous'

The just simply run the script passing to it the place where you have
unzipped your `posts`folder. By default the script will crawl through
all the `*.html`files and will create a post on tumblr, while keeping
the original date. 

I usually define a specific tag for all this posts, so if something 
goes wrong on the import (I did not, it worked smoothly from the
start), to have the chance to delete them in a batch.

And this is all. 

Fun! 


Known Issues
------------

