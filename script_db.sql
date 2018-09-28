-- SCHEMA: spotify_db
create schema spotify_db;

--------------------------------------------------------------------------------
-- Table: spotify_db.playlist
create table spotify_db.playlist(
    playlist_id varchar primary key,
    playlist_name varchar not null,
    playlist_collaborative boolean not null
);

--------------------------------------------------------------------------------
-- Table: spotify_db.track
create table spotify_db.track(
   track_id varchar primary key,
   track_name varchar not null,
   track_liveness double precision not null,
   track_speechness double precision not null,
   track_explicit boolean not null,
   track_tempo double precision not null,
   track_valence double precision not null,
   track_popularity smallint not null,
   track_number int not null,
   track_energy double precision not null,
   track_acousticness double precision not null,
   track_instrumentalness double precision not null,
   track_dancebility double precision not null,
   track_duration int not null
);

--------------------------------------------------------------------------------
--Table: spotify_db.track_playlist -> Relação n-n

create table spotify_db.track_playlist(
    track_id varchar,
    foreign key (track_id) references spotify_db.track(track_id),
    playlist_id varchar,
    foreign key (playlist_id) references spotify_db.playlist(playlist_id),
    primary key(track_id, playlist_id)
);

--------------------------------------------------------------------------------
--Table: spotify_db.artist

create table spotify_db.artist(
	artist_id varchar primary key,
	artist_name varchar not null,
	artist_genre varchar,
	artist_popularity smallint not null,
	artist_followers varchar not null
);

--------------------------------------------------------------------------------
--Table: spotify_db.album

create table spotify_db.album(
	album_id varchar primary key,
	album_name varchar not null,
	album_release_date varchar not null,
	album_popularity smallint not null
);

--------------------------------------------------------------------------------
-- Table spotify_db.track_artist

create table spotify_db.track_artist(
	track_id varchar,
	foreign key (track_id) references spotify_db.track(track_id),
	artist_id varchar,
	foreign key (artist_id) references spotify_db.artist(artist_id),
	primary key(track_id, artist_id)
);

--------------------------------------------------------------------------------
-- Table spotify_db.track_artist

create table spotify_db.track_album(
	track_id varchar,
	foreign key (track_id) references spotify_db.track(track_id),
	album_id varchar,
	foreign key (album_id) references spotify_db.album(album_id),
	primary key(track_id, album_id)
);
