import spotipy
import psycopg2 as driver
import spotipy.oauth2 as oauth2

########################################################################################################################

# Autorizacao na API do Spotify
client_id = '13836d1c48c749a0837f0b50b0cfd076'
client_secret = '8268a0c34dbf4d93addc0731f5fb048a'

# Conexao com a API do Spotify por meio da lib spotipy
credentials = oauth2.SpotifyClientCredentials(
        client_id=client_id,
        client_secret=client_secret)

token = credentials.get_access_token()

########################################################################################################################

# Matrizes de armazenamento das tuplas que serao persistidas
Malbum = []
Martist = []
Mtrack_artist = []
Mtrack_playlist = []
Mtrack_album = []
Mplaylist = []
Mtrack = []

# Listas de ids das tabelas para verificacao de ids ja existentes no banco
lista_id_album = []
lista_id_artist = []
lista_id_track = []
lista_id_playlist = []
lista_id_track_artist = []
lista_id_track_playlist = []
lista_id_track_album = []

########################################################################################################################

# Entradas do usuario para conexao com o banco
host = input('Host:')
banco_de_dados = input('Database:')
usuario = input('User:')
password = input('Password:')

########################################################################################################################

# Conexao com o banco de dados por meio do driver de conexao psycopg2
con = driver.connect(host=host, database=banco_de_dados, user=usuario, password=password)
cur = con.cursor()

########################################################################################################################

# Recupera os ids de tuplas que ja existem no banco para nao haver tuplas repetidas
sql = 'select album_id from spotify_db.album'
cur.execute(sql)
lista_id_album = cur.fetchall()

sql = 'select artist_id from spotify_db.artist'
cur.execute(sql)
lista_id_artist = cur.fetchall()

sql = 'select * from spotify_db.track_artist'
cur.execute(sql)
lista_id_track_artist = cur.fetchall()

sql = 'select playlist_id from spotify_db.playlist'
cur.execute(sql)
lista_id_playlist = cur.fetchall()

sql = 'select track_id from spotify_db.track'
cur.execute(sql)
lista_id_track = cur.fetchall()

sql = 'select * from spotify_db.track_playlist'
cur.execute(sql)
lista_id_track_playlist = cur.fetchall()

sql = 'select * from spotify_db.track_album'
cur.execute(sql)
lista_id_track_album = cur.fetchall()

########################################################################################################################
# Obtencao de dados pelas API e tratamento dos mesmos
if token:
    spotifyObject = spotipy.Spotify(auth=token)

    # Extrai playlists de uma categoria especifica
    category = spotifyObject.category_playlists(category_id='rock')
    playlist_name = category['playlists']['items']

    for playlist_index in playlist_name:
    # for playlist_index in playlist_name[:2]:
        playlist_id = playlist_index['id']
        playlist_name = playlist_index['name']
        playlist_collaborative = playlist_index['collaborative']

        print("PLAYLIST: " + playlist_name)

        # Insere a playlist na lista de tuplas
        if (playlist_id,) not in lista_id_playlist:
            lista_id_playlist.append((playlist_id,))
            Mplaylist.append((playlist_id, playlist_name,playlist_collaborative))

        # Extrai tracks de uma  playlist
        tracks = spotifyObject.user_playlist(user = "", playlist_id=playlist_index['id'])


        for track_index in tracks['tracks']['items']:
            print('------------------------------')

            # Extrai dados de uma track
            if track_index['track'] is not None:
                track_id = track_index['track']['id']
                track_name = track_index['track']['name']
                track_explicit = track_index['track']['explicit']
                track_popularity = track_index['track']['popularity']
                track_number = track_index['track']['track_number']


                # Extrai informacoes de um album
                album_id = track_index['track']['album']['id']

                track_album = spotifyObject.album(album_id)

                album_popularity = track_album['popularity']
                album_release_date = track_album['release_date']
                album_name = track_album['name']
                album_genre = track_album["genres"]


                # Insere album na lista de tuplas
                if (album_id,) not in lista_id_album:
                    Malbum.append((album_id, album_name, album_release_date, album_popularity))
                    lista_id_album.append((album_id,))
                    print(album_id, album_name, album_release_date, album_popularity)

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

                # Insere artista na lista de tuplas
                if (artist_id,) not in lista_id_artist:
                    Martist.append((artist_id, artist_name, artist_genre, artist_popularity,artist_followers))
                    lista_id_artist.append((artist_id,))
                    print(artist_id, artist_name, artist_popularity, artist_genre, artist_followers)


                # Extrai features de uma track
                track_features = spotifyObject.audio_features(track_index['track']['id'])

                if track_features[0] != None:
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

                        # Insere track_artista na lista de tuplas
                        if (track_id, artist_id) not in lista_id_track_artist:
                            Mtrack_artist.append((track_id, artist_id))
                            lista_id_track_artist.append((track_id, artist_id))

                        # Insere track_playlist na lista de tuplas
                        if (track_id, playlist_id) not in lista_id_track_playlist:
                            Mtrack_playlist.append((track_id, playlist_id))
                            lista_id_track_playlist.append((track_id, playlist_id))

                        # Insere track_album na lista de tuplas
                        if (track_id, album_id) not in lista_id_track_album:
                            Mtrack_album.append((track_id, album_id))
                            lista_id_track_album.append((track_id, album_id))

                        # Insere track na lista de tuplas
                        if (track_id,) not in lista_id_track:
                            Mtrack.append((track_id,track_name,track_liveness, track_speechiness, track_explicit,
                                           track_tempo,track_valence, track_popularity, track_number, track_energy,
                                           track_acousticness,track_instrumentalness, track_danceability, track_duration))
                            lista_id_track.append((track_id,))
                            print(track_id,track_name,track_liveness, track_speechiness, track_explicit,
                                           track_tempo,track_valence, track_popularity, track_number, track_energy,
                                           track_acousticness,track_instrumentalness, track_danceability, track_duration)
else:
    print ("Can't get token")

# Percorre as listas de tupla e insere as tuplas no banco pelo drive de conexao
for item in Mplaylist:
    cur.execute('insert into spotify_db.playlist values (%s, %s,%s)', item)
for item in Mtrack:
    cur.execute('insert into spotify_db.track values (%s, %s,%s,%s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', item)
for item in Martist:
    cur.execute('insert into spotify_db.artist values (%s, %s,%s,%s,%s)', item)
for item in Malbum:
    cur.execute('insert into spotify_db.album values (%s, %s,%s,%s)', item)
for item in Mtrack_artist:
    cur.execute('insert into spotify_db.track_artist values (%s, %s)', item)
for item in Mtrack_playlist:
    cur.execute('insert into spotify_db.track_playlist values (%s, %s)', item)
for item in Mtrack_album:
    cur.execute('insert into spotify_db.track_album values (%s, %s)', item)

con.commit()

# Fecha conexoes com o banco
cur.close()
con.close()
