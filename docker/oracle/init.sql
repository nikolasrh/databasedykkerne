ALTER SESSION SET CONTAINER=FREEPDB1;

CREATE USER efcore_user IDENTIFIED BY password;
GRANT CREATE SESSION TO efcore_user;
GRANT CREATE TABLE TO efcore_user;

CREATE USER fluentmigrator_user IDENTIFIED BY password;
GRANT CREATE SESSION TO fluentmigrator_user;
GRANT RESOURCE TO fluentmigrator_user;

CREATE USER dapper_user IDENTIFIED BY password;
GRANT CREATE SESSION TO dapper_user;
GRANT SELECT ANY TABLE, INSERT ANY TABLE, UPDATE ANY TABLE, DELETE ANY TABLE TO dapper_user;

CREATE USER prisma_user IDENTIFIED BY password;
GRANT CREATE SESSION TO prisma_user;
GRANT RESOURCE TO prisma_user;

CREATE USER django_user IDENTIFIED BY password;
GRANT CREATE SESSION TO django_user;
GRANT RESOURCE TO django_user;

CREATE USER java_spring_jpa_user IDENTIFIED BY password;
GRANT CREATE SESSION TO java_spring_jpa_user;
GRANT RESOURCE TO java_spring_jpa_user;
