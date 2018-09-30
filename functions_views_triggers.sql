------------------------------------------------------------------------------------------------------------------------
--Top 10 musicas por popularidade--
create or replace function spotify_db.AttTrackPopularity() returns trigger as $$
begin
create or replace view top10MusicasporPopularidade as
select t.track_name, a.artist_name, t.track_popularity 
from spotify_db.track as t
inner join spotify_db.track_artist using (track_id)
inner join spotify_db.artist as a using(artist_id)
order by track_popularity desc
limit 10;
return new;
end;
$$ language plpgsql;

create trigger AttTrackPopularity after insert or delete or update on spotify_db.track
for each statement execute procedure spotify_db.AttTrackPopularity();

------------------------------------------------------------------------------------------------------------------------
--Top 10 artistas por popularidade--

create or replace function spotify_db.AttArtistPopularity() returns trigger as $$
begin

create or replace view top10ArtistasporPopularidade as
select  artist_name, artist_popularity 
from spotify_db.artist
order by artist_popularity desc
limit 10;
return new;
end;
$$ language plpgsql;

create trigger AttArtistPopularity after insert or delete or update on spotify_db.artist
for each statement execute procedure spotify_db.AttArtistPopularity();


------------------------------------------------------------------------------------------------------------------------
--Top 10 artistas por followers--

create or replace function spotify_db.AttArtistFollowers() returns trigger as $$
begin

create or replace view top10ArtistasporSeguidores as
select  artist_name, artist_followers 
from spotify_db.artist
order by artist_followers desc
limit 10;
return new;
end;
$$ language plpgsql;

create trigger AttArtistFollowers after insert or delete or update on spotify_db.artist
for each statement execute procedure spotify_db.AttArtistFollowers();


------------------------------------------------------------------------------------------------------------------------
--Top 10 musicas mais longas do banco--

create or replace function  spotify_db.top_musicas_mais_longas_view()
returns trigger as $$
begin
execute
'create or replace view spotify_db.musicas_longas
as select t.track_name, a.artist_name, t.track_duration
from spotify_db.track t join spotify_db.track_artist ta
on t.track_id = ta.track_id join spotify_db.artist a on
a.artist_id = ta.artist_id
order by track_duration desc limit 10';
return new;
end;
$$ language plpgsql;

create trigger atualiza_top_musicas_longas
after insert or update or delete on spotify_db.track
for each statement execute
procedure spotify_db.top_musicas_mais_longas_view()

------------------------------------------------------------------------------------------------------------------------
--Top 10 albuns com maior quantidade de musicas explicitas--

create or replace function spotify_db.top_albuns_explicit_view()
returns trigger as $$
begin
execute
'create or replace view spotify_db.albuns_explicit
as select a.album_name, art.artist_name, count(t.track_explicit) as quant
from spotify_db.album a join spotify_db.track_album ta on a.album_id = ta.album_id
join spotify_db.track t on t.track_id = ta.track_id join spotify_db.track_artist tart on
tart.track_id = t.track_id join spotify_db.artist art on art.artist_id = tart.artist_id
where t.track_explicit = True
group by (a.album_name, art.artist_name)
order by quant desc
limit 10';
return new;
end;
$$ language plpgsql;

create trigger atualiza_top_albuns_explicit
after insert or update or delete on spotify_db.track
for each statement execute
procedure spotify_db.top_albuns_explicit_view()

------------------------------------------------------------------------------------------------------------------------
-- Top 10 artistas com músicas mais dancantes

create or replace function spotify_db.artistas_dancantes() returns trigger as $$
	begin
		execute 'create or replace view spotify_db.artistas_dancantes_view as' ||
		 ' select distinct a.artist_name, t.track_dancebility
			from spotify_db.track t join spotify_db.track_artist q on t.track_id = q.track_id
			join spotify_db.artist a on a.artist_id = q.artist_id
			order by t.track_dancebility desc, a.artist_name
			limit 10';
		return new;
	end;
	$$ language plpgsql;

create trigger trigger_artistas_dancantes after insert or update or delete on spotify_db.track
for each statement execute procedure  spotify_db.artistas_dancantes();

------------------------------------------------------------------------------------------------------------------------
-- Top 10 albuns mais energerticos

create or replace function spotify_db.albuns_energiticos() returns trigger as $$
  begin
		execute ' create or replace view spotify_db.albuns_energeticos_view as ' ||
		 'select  distinct a.album_name, t.track_energy
			from spotify_db.album a join spotify_db.track_album q on a.album_id = q.album_id
			join spotify_db.track t on q.track_id = t.track_id
			order by t.track_energy desc
			limit 10';
		return new;
	end;
$$ language plpgsql;

create trigger trigger_albuns_energeticos after insert or update or delete on spotify_db.track
for each statement execute procedure  spotify_db.albuns_energiticos();

------------------------------------------------------------------------------------------------------------------------
-- Top 10 albuns mais populares com mais de 50% acustico

create or replace function spotify_db.album_acustico_popularidade() returns trigger as $$
	begin
		execute 'create or replace view spotify_db.album_acustico_popularidade_view as select distinct (a.album_name), t.track_popularity
			from spotify_db.track t join spotify_db.track_album q on t.track_id = q.track_id
			join spotify_db.album a on a.album_id = q.album_id
			where t.track_acousticness > 0.5
			order by t.track_popularity desc
			limit 10';
		return new;
	end;
$$ language plpgsql;


create trigger trigger_album_acustico_popularidade after insert or update or delete on spotify_db.track
for each statement execute procedure  spotify_db.album_acustico_popularidade();

------------------------------------------------------------------------------------------------------------------------
-- Distribuicao de artistas por genero

create or replace function spotify_db.artistas_por_genero_view()
returns trigger as $$
begin
execute
'create or replace view spotify_db.artistas_por_genero
as select count(a.artist_name) as quant, a.artist_genre
from spotify_db.artist a
where a.artist_genre is not null
group by a.artist_genre order by quant desc';
return new;
end;
$$ language plpgsql;

create trigger atualiza_artistas_por_genero
after insert or update or delete on spotify_db.artist
for each statement execute
procedure spotify_db.artistas_por_genero_view()
