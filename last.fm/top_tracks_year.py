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
    if len(argv) < 4:
        print >> stderr, 'Usage: %s <last.fm API key> <last.fm username> <year>' % basename(argv[0])
        print >> stderr, 'Example: %s 91009080e1635307d49a60be883e616 jp 2012' % basename(argv[0])
    else:
        API_KEY=argv[1]
        USERNAME=argv[2]
        YEAR=argv[3]
        
    # connect and retrieve the user
    api = Api(API_KEY, no_cache = True)
    user = api.get_user(USERNAME)

    # now retrieve the favourite albums from last year
    top_tracks = user.get_top_tracks('12month')

    # print out the albums for the year
    print " Favourite tracks "
    print "-" * 120
    # loop through the tracks
    for track in top_tracks:
        # we will onlys consider the songs having mbid
        if track.mbid:
            full_album = api.get_album( album=track.album.name, artist=track.artist.name )
            track_year = ''
            if type(full_album.release_date) is datetime:
                track_year =  datetime.strftime( full_album.release_date, '%Y')
            if track_year and track_year == YEAR:
                print u'{0:30} - {1:<30} - {2:<30} - {3:<4}'.format( track.artist.name[:30], track.album.name[:30], 
                        track.name[:30], track_year)
