--Cria role DBA e o usuário
create role DBA with superuser password 'senha';
create user dba1 with password 'dba1' in role DBA;
alter user dba1 to superuser;
ALTER DATABASE >>>>>COLOQUEONOMEDOBANCOAQUI<<<<< OWNER TO dba1;

--Cria a role para uma usuário que so pode dar select nas views
create role userview;
grant all on schema spotify_db to userview;
grant select on pg_catalog.pg_views to userview;
create user userview1 with password 'userview1' in role userview;
grant select on spotify_db.musicas_longas to userview1;
grant select on spotify_db.top10MusicasporPopularidade to userview1;
grant select on spotify_db.top10ArtistasporPopularidade to userview1;
grant select on spotify_db.top10ArtistasporSeguidores to userview1;
grant select on spotify_db.albuns_explicit to userview1;
grant select on spotify_db.artistas_dancantes_view to userview1;
grant select on spotify_db.albuns_energeticos_view to userview1;
grant select on spotify_db.album_acustico_popularidade_view to userview1;
grant select on spotify_db.artistas_por_genero to userview1;
grant select on spotify_db.musicas_instrumentais to userview1;

--Cria um usuário que tem os comandos DML
create role userdml;
grant all on schema spotify_db to userdml;
create user userdml1 with password 'userdml1'
grant all on schema spotify_db to userdml1 with grant option;
grant select, update, delete, insert on spotify_db.album to userdml1 with grant option;
grant select, update, delete, insert on spotify_db.artist to userdml1 with grant option;
grant select, update, delete, insert on spotify_db.playlist to userdml1 with grant option;
grant select, update, delete, insert on spotify_db.track to userdml1 with grant option;
grant select, update, delete, insert on spotify_db.track_album to userdml1 with grant option;
grant select, update, delete, insert on spotify_db.track_artist to userdml1 with grant option;
grant select, update, delete, insert on spotify_db.track_playlist to userdml1 with grant option;