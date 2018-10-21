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
alter database spotify_db owner to usuario_dba_1;

---------------------------------------------------------------------------------------------------------------