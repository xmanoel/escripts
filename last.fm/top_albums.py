from sys import argv, stderr, exit
from os.path import basename
from datetime import datetime
from lastfm import Api

# Place here your API Key
API_KEY = ''
# username we are getting data from
USERNAME = ''

if __name__ == "__main__":
    if len(argv) < 3:
        print >> stderr, 'Usage: %s <last.fm API key> <last.fm username>' % basename(argv[0])
        print >> stderr, 'Example: %s 91009080e1635307d49a60be883e616 jp' % basename(argv[0])
    else:
        API_KEY=argv[1]
        USERNAME=argv[2]

    # connect and retrieve the user
    api = Api(API_KEY, no_cache = True)
    user = api.get_user(USERNAME)
    # now retrieve the favourite albums from last year
    top_albums = user.get_top_albums('12month')
   
    # print out the albums for the year
    print " Favourite albums"
    print "-" * 64

    # loop through the albums
    for album in top_albums:
         # print the names just 30 characters, left aligned with spaces padding
         print u' {0:<30} - {1:<30} '.format( album.artist.name[:30], album.name[:30] )


