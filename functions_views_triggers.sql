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