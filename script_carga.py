import sys
import spotipy
import spotipy.util as util
import json
import numpy as np
import psycopg2
import pandas as pd
from json.decoder import JSONDecodeError

scope = 'user-library-read'
client_id = '13836d1c48c749a0837f0b50b0cfd076'
client_secret = '381761ce55b24d01a389e9135b707379'

if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    # print ("Usage: %s username") % (sys.argv[0],)
    sys.exit()

token = util.prompt_for_user_token(username, scope, client_id=client_id, client_secret=client_secret, redirect_uri ='http://www.google.com')

#Cria as matrizes de armazenamento
Malbum = []
Martist = []
Mcategory = [["party"]]
Mplaylist = []
Mtrack = []


if token:
    spotifyObject = spotipy.Spotify(auth=token)
    #artistID = '69GGBxA162lTqCwzJG5jLp'

    # Extrai playlist de uma categoria
    category = spotifyObject.category_playlists(category_id='party')
    playlist_name = category['playlists']['items']
    for playlist_index in playlist_name:

        print(playlist_index['id'])
        playlist_name = playlist_index['name']
        #playlist_followers = playlist_index['followers']['total']
        # playlist_category = playlist_index['category']
        print (playlist_index.keys())

        print(playlist_name)#,playlist_followers)
        Mplaylist.append([playlist_name])
        # Extrai tracks de uma  playlist
        tracks = spotifyObject.user_playlist(user = "", playlist_id=playlist_index['id'])
        track_name = tracks['tracks']['items']
        for track_index in track_name:
            print('---------TRACK---------------------')
            #print(track_index['track']['id'])

            # Extrai dados de uma track
            track_name = track_index['track']['name']
            track_explicit = track_index['track']['explicit']
            track_popularity = track_index['track']['popularity']
            track_number = track_index['track']['track_number']

            #insert tracks into array

            #print(track_name, track_explicit, track_popularity, track_number)


            # print(json.dumps(track_index['track'], sort_keys=True, indent=4))
            album_id = track_index['track']['album']['id']

            # Extrai informacoes de um album
            track_album = spotifyObject.album(album_id)
            album_popularity = track_album['popularity']
            album_release_date = track_album['release_date']
            album_name = track_album['name']
            album_genre = track_album["genres"]
            album_artist = track_album['artists'][0]['name']

            #Append na matris album
            Malbum.append([album_popularity, album_release_date, album_name, album_genre, album_artist])
            #print(album_popularity, album_release_date, album_name, album_genre, album_artist)


            # Extrai informacoes de um artist_name
            artist_id = track_index['track']['artists'][0]['id']
            artist = spotifyObject.artist(artist_id)
            artist_name = artist['name']
            artist_popularity = artist['popularity']
            if artist['genres']:
                artist_genre = artist['genres'][0]
            else:
                artist_genre = None
            artist_followers = artist['followers']['total']
            #Append na matrix artista
            Martist.append([artist_name, artist_popularity, artist_genre, artist_followers])
            #print(artist_name, artist_popularity, artist_genre, artist_followers)


            # Extrai features de uma track
            track_features = spotifyObject.audio_features(track_index['track']['id'])
            for features_index in track_features:
                track_liveness = features_index['liveness']
                track_speechiness = features_index['speechiness']
                track_tempo = features_index['tempo']
                track_valence = features_index['valence']
                track_energy = features_index['energy']
                track_acousticness = features_index['acousticness']
                track_instrumentalness = features_index['instrumentalness']
                track_danceability = features_index['danceability']
                track_duration = features_index['duration_ms']
                #Append na martis tracks
                Mtrack.append([track_index,track_name, track_explicit, track_popularity, track_number,track_liveness, track_speechiness, track_tempo, track_valence, track_energy, track_acousticness, track_instrumentalness, track_danceability, track_duration])
                #print(track_liveness, track_speechiness, track_tempo, track_valence, track_energy, track_acousticness, track_instrumentalness, track_danceability, track_duration)
    #salva em arquivos .csv (evitar retrabalho de rede pra quando funcionar hehe)
    df = pd.DataFrame(Malbuns)
    df.to_csv("Album.csv")
    df = pd.DataFrame(Martist)
    df.to_csv("Artist.csv")
    df = pd.DataFrame(Mcategory)
    df.to_csv("Category.csv")
    df = pd.DataFrame(Mplaylist)
    df.to_csv("Playlist.csv")
    df = pd.DataFrame(Mtrack)
    df.to_csv("Tracks.csv")

else:
    print ("Can't get token for" + username)
