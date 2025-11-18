#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "============================================="
echo "Starting PostgreSQL..."
echo "============================================="

docker compose down postgres
docker compose up postgres -d --wait

echo "============================================="
echo "Running migrations..."
echo "============================================="

$SCRIPT_DIR/migrate.sh up

echo "============================================="
echo "Seeding database..."
echo "============================================="

python "$SCRIPT_DIR/src/seed_database.py" "$@"

echo "============================================="
echo "Restarting PostgreSQL with resource limits..."
echo "============================================="

docker compose -f "$SCRIPT_DIR/docker-compose.yml" stop postgres
docker compose -f "$SCRIPT_DIR/docker-compose.yml" -f "$SCRIPT_DIR/docker-compose.resources.yml" up postgres -d --wait

echo "============================================="
echo "Setup complete!"
echo "============================================="
echo
echo "Run first performance test: pytest src/test_oppgave_1.py"
