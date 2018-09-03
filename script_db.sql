-- SCHEMA: spotify_db

create schema spotify_db
    authorization postgres;

-- Table: spotify_db.playlist

create table spotify_db.playlist(
    playlist_id varchar primary_key,
    playlist_name varchar not null,
    playlist_qty_followers int not null default 0,
    playlist_collaborative boolean not null,
)

alter table spotify_db.playlist owner to postgres;
