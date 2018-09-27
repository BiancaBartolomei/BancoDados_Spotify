import sys
import spotipy
import spotipy.util as util
import json
import numpy as np
import psycopg2 as driver
import pandas as pd
import spotipy.oauth2 as oauth2
from json.decoder import JSONDecodeError

scope = 'user-library-read'
client_id = '13836d1c48c749a0837f0b50b0cfd076'
client_secret = '381761ce55b24d01a389e9135b707379'

credentials = oauth2.SpotifyClientCredentials(
        client_id=client_id,
        client_secret=client_secret)

token = credentials.get_access_token()

#Cria as matrizes de armazenamento
Malbum = []
Martist = []
Mtrack_artist = []
Mtrack_playlist = []
Mplaylist = []
Mtrack = []

lista_id_album = []
lista_id_artist = []
lista_id_track = []
lista_id_playlist = []
lista_id_track_artist = []
lista_id_track_playlist = []



if token:
    spotifyObject = spotipy.Spotify(auth=token)
    #artistID = '69GGBxA162lTqCwzJG5jLp'

    # Extrai playlist de uma categoria
    category = spotifyObject.category_playlists(category_id='party')
    playlist_name = category['playlists']['items']
    for playlist_index in playlist_name:

        print(playlist_index['id'])
        playlist_id = playlist_index['id']
        playlist_name = playlist_index['name']
        playlist_collaborative = playlist_index['collaborative']
        print (playlist_index.keys())

        print(playlist_name)

        if playlist_id not in lista_id_playlist:
            lista_id_playlist.append(playlist_id)
            Mplaylist.append((playlist_id, playlist_name,playlist_collaborative))
        # Extrai tracks de uma  playlist
        tracks = spotifyObject.user_playlist(user = "", playlist_id=playlist_index['id'])
        track_name = tracks['tracks']['items']
        for track_index in track_name:
            print('---------TRACK---------------------')

            # Extrai dados de uma track
            track_id = track_index['track']['id']
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


            #Append na matris album
            if album_id not in lista_id_album:
                Malbum.append((album_id, album_name, album_genre, album_release_date, album_popularity))
                lista_id_album.append(album_id)
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
            if artist_id not in lista_id_artist:
                Martist.append((artist_id, artist_name, artist_genre, artist_popularity,artist_followers))
                lista_id_artist.append(artist_id)
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

                #Append na matriz track_artists
                if (track_id, artist_id) not in lista_id_track_artist:
                    Mtrack_artist.append((track_id, artist_id))
                    lista_id_track_artist.append((track_id, artist_id))

                #Append na matriz track_playlist
                if (track_id, playlist_id) not in lista_id_track_playlist:
                    Mtrack_playlist.append((track_id, playlist_id))
                    lista_id_track_playlist.append((track_id, playlist_id))

                #Append na martiz tracks
                if track_id not in lista_id_track:
                    Mtrack.append((track_id,track_name,track_liveness, track_speechiness, track_explicit, track_tempo,
                               track_valence, track_popularity, track_number, track_energy, track_acousticness,
                               track_instrumentalness, track_danceability, track_duration))
                    lista_id_track.append(track_id)
                #print(track_liveness, track_speechiness, track_tempo, track_valence, track_energy, track_acousticness, track_instrumentalness, track_danceability, track_duration)


else:
    print ("Can't get token")

con = driver.connect(host='localhost', database='spotify_db_26_09',
                             user='postgres', password='19972015')
cur = con.cursor()

for item in Mplaylist:
    cur.execute('insert into spotify_db.playlist values (%s, %s,%s)', item)
for item in Mtrack:
    cur.execute('insert into spotify_db.track values (%s, %s,%s,%s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', item)
for item in Martist:
    cur.execute('insert into spotify_db.artist values (%s, %s,%s,%s,%s)', item)
for item in Malbum:
    cur.execute('insert into spotify_db.album values (%s, %s,%s,%s, %s)', item)
for item in Mtrack_artist:
    cur.execute('insert into spotify_db.track_artist values (%s, %s)', item)
for item in Mtrack_playlist:
    cur.execute('insert into spotify_db.track_playlist values (%s, %s)', item)

con.commit()

cur.close()
con.close()