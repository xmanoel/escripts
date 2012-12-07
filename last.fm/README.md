What's this?
------------

This are just a few python scripts I made because I wanted to check what were the songs from this year
that I had listened the most (to make best-of-year list and this kind of stuff).

Since the last.fm charts were not allowing me to filter by the issue date, I just thought about using
the API and playing a little with Python.

No license or copyright on these, if you check the code you will know why!! The code is quite 
documented. 

Have fun!!


Installation
------------

1) Download the repository (sorry I am placing all my python scripts in one repository, so you will be getting extra stuff!!)

        git clone https://github.com/xmanoel/escripts.git
       
2) Obtain the python-lastfm module (it is branched in several githubs, I got the one from jc):
    
        git clone https://github.com/jc/python-lastfm.git

3) Don't install the module, just copy the lastfm folder to where you have dowloaded my scripts:

        cp python-lastfm/lastfm

4) When trying to execute the whole stuff you may get this error: "ImportError: No module named decorator". 
   It is simply because the `decorator` module is in your system (I thought this was standard in all new 
   python installations. Well, the solution is not complicated. 

        easy_install decorator

  (If you don't have `easy_install` in your system, well, try to have it, I think is not worth playing around with Python
  without such tool)

5) *IMPORTANT*: Get a last.fm API Key: it is for free and I am not sharing mine with you!! http://www.last.fm/api/account/create

Use
---

Very simply, I did not even made the scripts executable, just run them with a post 2.6 Python:

      python top_albums_year.py 91009........................616 xmanoel 2012
      python top_tracks_year.py 91009........................616 xmanoel 2012
      python top_albums.py 91009........................616 xmanoel 
      python top_tracks.py 91009........................616 xmanoel 

You could get this lists from other users not just xmanoel or yours, feel free to check the favourite songs from your last.fm friends



Known Issues
------------

When searching by year, the output is slow, because may queries to the API should be made. That is not a big issue, just let it 
retrieve the data, and meanwhile browse the web or do other stuff.


If you redirect the output of the scripts to a file or to less you will get this nice error:

    Traceback (most recent call last):
    File "top_albums.py", line 32, in <module>
        print u' {0:<30} - {1:<30} '.format( album.artist.name[:30], album.name[:30] )
    UnicodeEncodeError: 'ascii' codec can't encode character u'\xf1' in position 43: ordinal not in range(128)

This is because there are unicode characters in the names of albums, artists or tracks (I do listen a lot of foreign and strangely named bands).
This only crashes when redirecting the output to a file (to the console it works fine). I do not know why Python works difrently
with Unicode between the console and a file, and maybe it is not Python fault. Anyway I am not fixing it. I may check it later on
in the future but just for knowledge, I think this scripts are Ok as they are.
