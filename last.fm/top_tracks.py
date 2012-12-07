from sys import argv, stderr, exit
from os.path import basename
from datetime import datetime
from lastfm import Api

# Place here your API Key
API_KEY = ''
# Year we are reviewing the favourite tracks
YEAR = 0
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
    top_tracks = user.get_top_tracks('12month')

    # print out the albums for the year
    print "Favourite tracks "
    print "-" * 94
    # loop through the tracks
    for track in top_tracks:
        # we will onlys consider the songs having mbid
        if track.mbid:
            full_track = api.get_track( track.name, mbid= track.mbid )
            print u'{0:30} - {1:<30} - {2:<30} '.format( full_track.artist.name[:30], full_track.album.name[:30], 
                                        full_track.name[:30])
            
