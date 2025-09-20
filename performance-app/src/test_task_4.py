"""
Task 4: Søk på dato

Her skal vi finne hvilke produkter som ble lansert innenfor en ukes tidsperiode. Og det skal gå raskt!
"""
import random
from datetime import datetime, timedelta
from psycopg_pool import ConnectionPool
from pytest_benchmark.fixture import BenchmarkFixture

QUERY = "SELECT * FROM products WHERE released_date >= %s AND released_date <= %s"


def find_products_by_released_date(db_pool: ConnectionPool, start_date: datetime, end_date: datetime) -> list:
    """Find products released within a specific date range."""
    with db_pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(QUERY, (start_date, end_date))
            results = cur.fetchall()
            return results


def test_task_4(benchmark: BenchmarkFixture, db_pool: ConnectionPool, explain_plan) -> None:
    explain_plan(QUERY)

    rng = random.Random(42)

    now = datetime(2025, 9, 29)

    def run_query() -> list:
        days_ago = rng.randint(7, 3650)
        end_date = now - timedelta(days=days_ago)
        start_date = end_date - timedelta(days=7)

        return find_products_by_released_date(db_pool, start_date, end_date)

    benchmark.pedantic(run_query, rounds=500, warmup_rounds=10, iterations=1)
