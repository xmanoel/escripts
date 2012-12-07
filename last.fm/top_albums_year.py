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
        YEAR=int(argv[3])

    # get the start of the year to compare later on the dates
    # First of january, at 00:00:00
    year_start = datetime(YEAR,1,1,0,0,0)

    # dictionary to hold the album list
    year_albums = {}

    # connect and retrieve the user
    api = Api(API_KEY, no_cache = True)
    user = api.get_user(USERNAME)
    # now retrieve the favourite albums from last year
    top_albums = user.get_top_albums('12month')
   
    # loop through the albums
    for album in top_albums:
        
        #print "%s. %s (mbid: %s)" % (album.artist.name, album.name, album.mbid)
        # we will only consider the albums having a proper mbid (to simplify things)
        if album.mbid: 
            full_album=api.get_album( mbid=album.mbid )
            if full_album.release_date and year_start < full_album.release_date:
               year_albums[full_album.name] = full_album


    # print out the albums for the year
    print " Favourite albums for year %s " % YEAR
    print "-" * 64
    for name,album in year_albums.iteritems():
         # print the names just 30 characters, left aligned with spaces padding
        print u' {0:<30} - {1:<30} '.format( album.artist.name[:30], album.name[:30] )


    # now retrieve the favourite albums from last year
    top_tracks = user.get_top_tracks('12month')

    # print out the albums for the year
    print "\n"
    print " Favourite tracks for year %s " % YEAR
    print "-" * 95
    # loop through the tracks
    for track in top_tracks:
        # we will onlys consider the songs having mbid
        if track.mbid:
            full_track = api.get_track( track.name, mbid= track.mbid )
            if full_track.album and full_track.album.name in year_albums:
                print u'{0:30} - {1:<30} - {2:<30}'.format( full_track.artist.name, full_track.album.name, full_track.name )
