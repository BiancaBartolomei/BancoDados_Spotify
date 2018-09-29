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
