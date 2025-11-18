"""
Oppgave 3: Finn samlet inventory for en selger

Denne spørringen er treig.

Lag to SQL-filer for "up" og "down" migreringer:
./migrations/002_add_index.up.sql
./migrations/002_add_index.down.sql

Syntax for å lage og å droppe:
CREATE INDEX tablename_column1_column2_idx ON tablename (column1, column2);
DROP INDEX IF EXISTS tablename_column1_column2_idx;

Kjøre migreringen:
./migrate.sh up

Rulle tilbake én migreringen:
./migrate.sh down 1

Bonus: Hvordan kan spørringen gjøres raskere uten å lage en ekstra index?
"""
import random
from psycopg_pool import ConnectionPool
from pytest_benchmark.fixture import BenchmarkFixture

QUERY = "SELECT SUM(quantity) as total_inventory FROM seller_inventory WHERE seller_id = %s"


def find_total_inventory_for_seller(db_pool: ConnectionPool, seller_id: int) -> int | None:
    """Find total inventory quantity for a specific seller."""
    with db_pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(QUERY, (seller_id,))
            result = cur.fetchone()
            return result[0] if result and result[0] else 0


def test_oppgave_3(benchmark: BenchmarkFixture, db_pool: ConnectionPool, max_seller_id: int, explain_plan) -> None:
    explain_plan(QUERY)

    rng = random.Random(42)

    def run_query() -> int | None:
        seller_id = rng.randint(1, max_seller_id)
        return find_total_inventory_for_seller(db_pool, seller_id)

    benchmark.pedantic(run_query, rounds=10000, warmup_rounds=10, iterations=1)
