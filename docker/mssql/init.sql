CREATE DATABASE efcore_db;
GO
USE efcore_db;
GO
CREATE LOGIN efcore_user WITH PASSWORD = 'Password123!';
CREATE USER efcore_user FOR LOGIN efcore_user;
ALTER ROLE db_owner ADD MEMBER efcore_user;
GO

CREATE DATABASE dapper_fluentmigrator_db;
GO
USE dapper_fluentmigrator_db;
GO
CREATE LOGIN dapper_user WITH PASSWORD = 'Password123!';
CREATE USER dapper_user FOR LOGIN dapper_user;
ALTER ROLE db_datareader ADD MEMBER dapper_user;
ALTER ROLE db_datawriter ADD MEMBER dapper_user;
GO
CREATE LOGIN fluentmigrator_user WITH PASSWORD = 'Password123!';
CREATE USER fluentmigrator_user FOR LOGIN fluentmigrator_user;
ALTER ROLE db_owner ADD MEMBER fluentmigrator_user;
GO

CREATE DATABASE node_express_prisma_db;
GO
USE node_express_prisma_db;
GO
CREATE LOGIN prisma_user WITH PASSWORD = 'Password123!';
CREATE USER prisma_user FOR LOGIN prisma_user;
ALTER ROLE db_owner ADD MEMBER prisma_user;
GO

CREATE DATABASE django_db;
GO
USE django_db;
GO
CREATE LOGIN django_user WITH PASSWORD = 'Password123!';
CREATE USER django_user FOR LOGIN django_user;
ALTER ROLE db_owner ADD MEMBER django_user;
GO

CREATE DATABASE java_spring_jpa_db;
GO
USE java_spring_jpa_db;
GO
CREATE LOGIN java_spring_jpa_user WITH PASSWORD = 'Password123!';
CREATE USER java_spring_jpa_user FOR LOGIN java_spring_jpa_user;
ALTER ROLE db_owner ADD MEMBER java_spring_jpa_user;
GO
