---------------------------------------------------------------------------------------------------------------
-- Top 10 musicas por popularidade
create or replace view spotify_db.top10MusicasporPopularidade as
select t.track_name, a.artist_name, p.track_popularity
from spotify_db.track as t
inner join spotify_db.track_artist using (track_id)
inner join spotify_db.artist as a using(artist_id)
inner join spotify_db.track_popularity as p using (track_id)
order by track_popularity desc
limit 10;

---------------------------------------------------------------------------------------------------------------
--Top 10 artistas por popularidade
create or replace view spotify_db.top10ArtistasporPopularidade as
select  artist_name, artist_popularity
from spotify_db.artist
order by artist_popularity desc
limit 10;

---------------------------------------------------------------------------------------------------------------
--Top 10 artistas por seguidores
create or replace view spotify_db.top10ArtistasporSeguidores as
select  artist_name, artist_followers
from spotify_db.artist
order by artist_followers desc
limit 10;

---------------------------------------------------------------------------------------------------------------
--Top 10 albuns com explicit
create or replace view spotify_db.albuns_explicit
as select a.album_name, art.artist_name, count(t.track_explicit) as quant
from spotify_db.album a join spotify_db.track_album ta on a.album_id = ta.album_id
join spotify_db.track t on t.track_id = ta.track_id join spotify_db.track_artist tart on
tart.track_id = t.track_id join spotify_db.artist art on art.artist_id = tart.artist_id
where t.track_explicit = True
group by (a.album_name, art.artist_name)
order by quant desc
limit 10;


---------------------------------------------------------------------------------------------------------------
--Top 10 artistas com mais musicas dancantes
create or replace view spotify_db.artistas_dancantes_view as
select distinct a.artist_name, t.track_dancebility
			from spotify_db.track t join spotify_db.track_artist q on t.track_id = q.track_id
			join spotify_db.artist a on a.artist_id = q.artist_id
			order by t.track_dancebility desc, a.artist_name
			limit 10;

---------------------------------------------------------------------------------------------------------------
--Top 10 albuns energeticos
create or replace view spotify_db.albuns_energeticos_view as
select  distinct a.album_name, t.track_energy
			from spotify_db.album a join spotify_db.track_album q on a.album_id = q.album_id
			join spotify_db.track t on q.track_id = t.track_id
			order by t.track_energy desc
			limit 10;

---------------------------------------------------------------------------------------------------------------
--Top 10 albuns acusticos mais populares
create or replace view spotify_db.album_acustico_popularidade_view as select distinct (a.album_name), p.track_popularity
			from spotify_db.track t join spotify_db.track_album q on t.track_id = q.track_id
			join spotify_db.album a on a.album_id = q.album_id
			join spotify_db.track_popularity p on t.track_id = p.track_id
			where t.track_acousticness > 0.5
			order by p.track_popularity desc
			limit 10;

---------------------------------------------------------------------------------------------------------------
--Agrupamento de artistas por genero musical
create or replace view spotify_db.artistas_por_genero
as select count(a.artist_name) as quant, a.artist_genre
from spotify_db.artist a
where a.artist_genre is not null
group by a.artist_genre order by quant desc;

---------------------------------------------------------------------------------------------------------------
--Top 10 musicas mais instrumentais
create or replace view spotify_db.musicas_instrumentais
as select t.track_name, a.artist_name, t.track_instrumentalness
from spotify_db.track t join spotify_db.track_artist ta
on t.track_id = ta.track_id join spotify_db.artist a on
a.artist_id = ta.artist_id
order by track_instrumentalness desc limit 10;

---------------------------------------------------------------------------------------------------------------
--Top 10 musicas mais longas
create or replace view spotify_db.musicas_longas
as select t.track_name, a.artist_name, t.track_duration
from spotify_db.track t join spotify_db.track_artist ta
on t.track_id = ta.track_id join spotify_db.artist a on
a.artist_id = ta.artist_id
order by track_duration desc limit 10;

