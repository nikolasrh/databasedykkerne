ALTER SESSION SET CONTAINER=FREEPDB1;

-- EF Core
CREATE USER efcore_user IDENTIFIED BY password;
GRANT CREATE SESSION TO efcore_user;

-- Dapper/FluentMigrator
CREATE USER dapper_user IDENTIFIED BY password;
CREATE USER fluentmigrator_user IDENTIFIED BY password;
GRANT CREATE SESSION TO fluentmigrator_user;
GRANT CREATE SESSION TO dapper_user;
GRANT SELECT ANY TABLE, INSERT ANY TABLE, UPDATE ANY TABLE, DELETE ANY TABLE TO dapper_user;

-- Node.js/Express/Prisma
CREATE USER prisma_user IDENTIFIED BY password;
GRANT CREATE SESSION TO prisma_user;

-- Django
CREATE USER django_user IDENTIFIED BY password;
GRANT CREATE SESSION TO django_user;
