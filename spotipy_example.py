import sys
import spotipy
import spotipy.util as util
import json
from json.decoder import JSONDecodeError

scope = 'user-library-read'
client_id = '13836d1c48c749a0837f0b50b0cfd076'
client_secret = '381761ce55b24d01a389e9135b707379'

if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    print ("Usage: %s username") % (sys.argv[0],)
    sys.exit()

token = util.prompt_for_user_token(username, scope, client_id=client_id, client_secret=client_secret, redirect_uri ='http://www.google.com')

if token:
    spotifyObject = spotipy.Spotify(auth=token)
    artistID = '69GGBxA162lTqCwzJG5jLp'

    # Extract album data
    albumResults = spotifyObject.artist_albums(artistID)
    albumResults = albumResults['items']

    for item in albumResults:
        print("ALBUM: " + item['name'])
        albumID = item['id']
        albumArt = item['images'][0]['url']

            # Extract track data
        trackResults = spotifyObject.album_tracks(albumID)
        trackResults = trackResults['items']
        for item in trackResults:
            track = item['name']
            print(track)


else:
    print ("Can't get token for" + username)
