#!/bin/bash

# MSSQL does not run scripts mounted to /docker-entrypoint-initdb.d or similar.
# This script is a workaround to run init.sql after the first successful healthcheck.

# Marker file to track if initialization has been completed
INIT_MARKER="/tmp/mssql-init-complete"
INIT_SQL="/init.sql"

# Healthcheck
if ! /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P "$MSSQL_SA_PASSWORD" -Q "SELECT 1" -C >/dev/null 2>&1; then
    # Failed healthcheck
    exit 1
fi

# Passed healthcheck, check if initialization is completed
if [ -f "$INIT_MARKER" ]; then
    # Initialization has already been completed
    exit 0
fi

# Run initialization
/opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P "$MSSQL_SA_PASSWORD" -i "$INIT_SQL" -C -b
    
if [ $? -eq 0 ]; then
    # Mark initialization as completed
    touch "$INIT_MARKER"
    exit 0
else
    # Initialization failed
    exit 1
fi
