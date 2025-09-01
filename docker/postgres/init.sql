-- EF Core
CREATE DATABASE efcore_db;
CREATE USER efcore_user WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE efcore_db TO efcore_user;

-- Dapper/FluentMigrator
CREATE DATABASE dapper_fluentmigrator_db;
CREATE USER dapper_user WITH PASSWORD 'password';
CREATE USER fluentmigrator_user WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE dapper_fluentmigrator_db TO fluentmigrator_user;
GRANT CONNECT ON DATABASE dapper_fluentmigrator_db TO dapper_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO dapper_user;

-- Node.js/Express/Prisma
CREATE DATABASE node_express_prisma_db;
CREATE USER prisma_user WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE node_express_prisma_db TO prisma_user;

-- Django
CREATE DATABASE django_db;
CREATE USER django_user WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE django_db TO django_user;
