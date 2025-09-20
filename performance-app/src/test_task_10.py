"""
Task 10: Finn laveste pris per produkt i en kategori og by

Omsider må du begynne å skrive SQL-en selv!

For hvert produkt av en kategori, i en by, finn selgeren med laveste pris
med produktet på lager.

"""
from psycopg_pool import ConnectionPool
from pytest_benchmark.fixture import BenchmarkFixture

QUERY = """

"""


def find_lowest_price_sellers_by_category_and_city(
    db_pool: ConnectionPool,
    category: str,
    city: str,
    offset: int = 0
) -> list:
    """Find sellers with lowest price for each product in a category and city."""
    with db_pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(QUERY, (category, city, city, offset))
            results = cur.fetchall()
            return results


def test_task_10(benchmark: BenchmarkFixture, db_pool: ConnectionPool, explain_plan) -> None:
    explain_plan(QUERY)
    offset = [0]

    def run_query() -> list:
        result = find_lowest_price_sellers_by_category_and_city(
            db_pool,
            category="electronics",
            city="oslo",
            offset=offset[0]
        )

        if len(result) == 0:
            offset[0] = 0
        else:
            offset[0] += 1000

        return result

    benchmark.pedantic(run_query, rounds=2, iterations=1)
