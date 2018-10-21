--Cria indices para o banco
create index track_popularity_i on spotify_db.track using btree(track_popularity);
create index track_energy_i on spotify_db.track using btree(track_energy);
create index track_explicit_i on spotify_db.track using btree(track_explicit);
create index track_dancebility_i on spotify_db.track using btree(track_dancebility);
create index track_instrumentalness_i on spotify_db.track using btree(track_instrumentalness);
create index track_duration_i on spotify_db.track using btree(track_duration);
create index track_acusticness_i on spotify_db.track using btree(track_acousticness);

create index artist_genre_i on spotify_db.artist using btree(artist_genre);
create index artist_popularity_i_i on spotify_db.artist using btree(artist_popularity);
create index artist_name_i on spotify_db.artist using btree(artist_name);
create index artist_followers_i_i on spotify_db.artist using btree(artist_followers);