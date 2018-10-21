create or replace view spotify_db.top_musicas_populares as
  select t.track_name, a.artist_name, p.track_popularity,
  p.data_popularidade, a.artist_genre
  from spotify_db.track as t
  inner join spotify_db.track_artist using (track_id)
  inner join spotify_db.artist as a using(artist_id)
  inner join spotify_db.track_popularity as p using (track_id)
  order by track_popularity desc;