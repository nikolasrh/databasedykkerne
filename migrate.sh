#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MIGRATIONS_DIR="${MIGRATIONS_DIR:-$SCRIPT_DIR/migrations}"
DATABASE_URL="postgres://postgres:password@localhost:5433/postgres?sslmode=disable"

docker run --rm \
    --network host \
    -v "$MIGRATIONS_DIR:/migrations" \
    migrate/migrate:v4.19.0 \
    -path=/migrations \
    -database="$DATABASE_URL" \
    "$@"
