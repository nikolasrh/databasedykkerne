"""
Task 9: Sortert etter lanseringsdato

Hent ut 1000 produkter sortert etter lanseringsdato.
Nyeste først. Sorteringen må være deterministisk.

Bonus: Legg til avg_rating som i forrige oppgave
"""
from datetime import date
from psycopg_pool import ConnectionPool
from pytest_benchmark.fixture import BenchmarkFixture

QUERY = """
SELECT p.id, p.released_date
FROM products p
ORDER BY p.released_date DESC
LIMIT 1000
OFFSET %s
"""


def find_products_with_avg_reviews_by_date(db_pool: ConnectionPool, offset: int = 0) -> list:
    """Find products with their average ratings, ordered by release date descending."""

    with db_pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(QUERY, (offset,))
            results = cur.fetchall()
            return results


def test_task_9(benchmark: BenchmarkFixture, db_pool: ConnectionPool, explain_plan) -> None:
    explain_plan(QUERY)
    results = []
    # TODO: Fix
    # https://use-the-index-luke.com/sql/partial-results/fetch-next-page
    # https://use-the-index-luke.com/blog/2013-07/pagination-done-the-postgresql-way
    offset = [0]

    def run_query() -> list:
        result = find_products_with_avg_reviews_by_date(db_pool, offset[0])

        if len(results) < 2:
            results.append(result)

        if len(result) == 0:
            offset[0] = 0
        else:
            offset[0] += 1000

        return result

    benchmark.pedantic(run_query, rounds=2, iterations=1)

    page1 = results[0]
    page2 = results[1]
    assert len(page1) == 1000
    assert len(page2) == 1000
    assert 8074 == page1[0][0]
    assert 1707001 == page1[999][0]
    assert 1707424 == page2[0][0]
    assert 1262576 == page2[999][0]
    assert date(2025, 9, 29) == page1[0][1]
    assert date(2025, 9, 28) == page1[999][1]
    assert date(2025, 9, 28) == page2[0][1]
    assert date(2025, 9, 26) == page2[999][1]
