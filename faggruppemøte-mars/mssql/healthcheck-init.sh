#!/bin/bash

# MSSQL does not run scripts mounted to /docker-entrypoint-initdb.d or similar.
# This script is a workaround to run init.sql after the first successful healthcheck.

INIT_SQL="/init.sql"

# Healthcheck
if ! /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P "$MSSQL_SA_PASSWORD" -Q "SELECT 1" -C >/dev/null 2>&1; then
    exit 1
fi

# Check if demo_db already exists — skip init if it does
DB_EXISTS=$(/opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P "$MSSQL_SA_PASSWORD" -C \
    -Q "SET NOCOUNT ON; SELECT COUNT(*) FROM sys.databases WHERE name = 'demo_db'" \
    -h -1 2>/dev/null | tr -d '[:space:]')

if [ "$DB_EXISTS" = "1" ]; then
    exit 0
fi

# Run initialization
/opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P "$MSSQL_SA_PASSWORD" -i "$INIT_SQL" -C -b

if [ $? -eq 0 ]; then
    exit 0
else
    exit 1
fi
