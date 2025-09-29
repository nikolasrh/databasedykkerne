"""
Task 5: Søk på kategori og dato

Nå skal vi finne produkter i en bestemt kategori som ble lansert innenfor en periode.
Denne spørringen er ganske lik den i forrige oppgave, og fungerer bra med indexen som ble lagt til da.

Uansett - vi kan gjøre den enda raskere!

Diskusjon:
- Forklar og visualiser hvorfor denne indexen er bedre.
- Er denne indexen verdt det?
- Hvorfor er spørringen i denne oppgaven raskere enn den i forrige?
"""
import random
from datetime import datetime, timedelta
from psycopg_pool import ConnectionPool
from pytest_benchmark.fixture import BenchmarkFixture

QUERY = "SELECT * FROM products WHERE category = %s AND released_date >= %s AND released_date <= %s"


def find_products_by_category_and_released_date(db_pool: ConnectionPool, category: str, start_date: datetime, end_date: datetime) -> list:
    """Find products in a specific category within a date range."""
    with db_pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(QUERY, (category, start_date, end_date))
            results = cur.fetchall()
            return results


def test_task_5(benchmark: BenchmarkFixture, db_pool: ConnectionPool, explain_plan) -> None:
    explain_plan(QUERY)

    rng = random.Random(42)

    now = datetime(2025, 9, 29)
    categories = ['electronics', 'books',
                  'clothing', 'rare_collectibles', 'vintage']

    def run_query() -> list:
        category = rng.choice(categories)

        days_ago = rng.randint(7, 3650)
        end_date = now - timedelta(days=days_ago)
        start_date = end_date - timedelta(days=7)

        return find_products_by_category_and_released_date(db_pool, category, start_date, end_date)

    benchmark.pedantic(run_query, rounds=500, warmup_rounds=10, iterations=1)
