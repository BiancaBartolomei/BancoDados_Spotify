--Cria role DBA e o usuário
create role DBA with superuser password 'senha'
create user DBA1 with password 'DBA1' in role DBA

--Cria a role para uma usuário que so pode dar select nas views
create role userview;
grant all on schema spotify_db to userview;
grant select on pg_catalog.pg_views to userview;
create user userview1 with password 'userview' in role userview;

--Cria um usuário que tem os comandos DML
create role userdml;
grant all on schema spotify_db to userdml;
grant select, delete, update, insert on all tables in schema spotify_db to userdml;
create user userdml1 with password 'userdml1'
