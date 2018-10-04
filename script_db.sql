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
--Table: spotify_db.track_playlist

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


---------------------------------------------------------------------------------------------------------------
-- Top 10 musicas por popularidade
create or replace view spotify_db.top10MusicasporPopularidade as
select t.track_name, a.artist_name, t.track_popularity
from spotify_db.track as t
inner join spotify_db.track_artist using (track_id)
inner join spotify_db.artist as a using(artist_id)
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
create or replace view spotify_db.album_acustico_popularidade_view as select distinct (a.album_name), t.track_popularity
			from spotify_db.track t join spotify_db.track_album q on t.track_id = q.track_id
			join spotify_db.album a on a.album_id = q.album_id
			where t.track_acousticness > 0.5
			order by t.track_popularity desc
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
--------------------------------------------------------------------------------
--Cria um usuário que tem os comandos DML
create role usuariodml1;
grant usage on schema spotify_db to usuariodml1;
create user usuariodml_2 with password 'senha' in role usuariodml1;

grant select, update, delete, insert on spotify_db.album to usuariodml1;
grant select, update, delete, insert on spotify_db.artist to usuariodml1;
grant select, update, delete, insert on spotify_db.playlist to usuariodml1;
grant select, update, delete, insert on spotify_db.track to usuariodml1;
grant select, update, delete, insert on spotify_db.track_album to usuariodml1;
grant select, update, delete, insert on spotify_db.track_artist to usuariodml1;
grant select, update, delete, insert on spotify_db.track_playlist to usuariodml1;

grant select on spotify_db.musicas_longas to usuariodml1;
grant select on spotify_db.top10MusicasporPopularidade to usuariodml1;
grant select on spotify_db.top10ArtistasporPopularidade to usuariodml1;
grant select on spotify_db.top10ArtistasporSeguidores to usuariodml1;
grant select on spotify_db.albuns_explicit to usuariodml1;
grant select on spotify_db.artistas_dancantes_view to usuariodml1;
grant select on spotify_db.albuns_energeticos_view to usuariodml1;
grant select on spotify_db.album_acustico_popularidade_view to usuariodml1;
grant select on spotify_db.artistas_por_genero to usuariodml1;
grant select on spotify_db.musicas_instrumentais to usuariodml1;

------------------------------------------------------------------------------------------------------------
--Cria a role para uma usuário que so pode dar select nas views
create role usuario_view;
grant usage on schema spotify_db to usuario_view;
create user usuario_view_1 with password 'senha' in role usuario_view;

grant select on spotify_db.musicas_longas to usuario_view;
grant select on spotify_db.top10MusicasporPopularidade to usuario_view;
grant select on spotify_db.top10ArtistasporPopularidade to usuario_view;
grant select on spotify_db.top10ArtistasporSeguidores to usuario_view;
grant select on spotify_db.albuns_explicit to usuario_view;
grant select on spotify_db.artistas_dancantes_view to usuario_view;
grant select on spotify_db.albuns_energeticos_view to usuario_view;
grant select on spotify_db.album_acustico_popularidade_view to usuario_view;
grant select on spotify_db.artistas_por_genero to usuario_view;
grant select on spotify_db.musicas_instrumentais to usuario_view;

--------------------------------------------------------------------------------------------------------------
--Cria role DBA e o usuário
create role usuario_dba with superuser password 'senha';
create user usuario_dba_1 with password 'senha' in role usuario_dba;
alter user usuario_dba_1 with superuser;
alter database spotify owner to usuario_dba_1;
