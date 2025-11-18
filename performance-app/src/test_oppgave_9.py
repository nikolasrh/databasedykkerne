"""
Oppgave 9: Paginer gjennom seller reviews med minimum rating

Nå er vi kun interessert i seller reviews med 5 stjerner.

I denne oppgaven holder det å svare på spørsmålet:
Hvorfor er denne spørringen tregere enn den i forrige oppgave?

Bonusoppgave:
Få spørringen til å yte like godt som forrige oppgave med offset pagination.
Det kan være nødvendig å endre spørringen til å sortere på andre felter.
"""
from datetime import date
from psycopg_pool import ConnectionPool
from pytest_benchmark.fixture import BenchmarkFixture

QUERY = """
SELECT sr.id, sr.seller_id, sr.rating, sr.review_date
FROM seller_reviews sr
WHERE sr.rating >= %s
ORDER BY sr.review_date, sr.id
LIMIT 1000
OFFSET %s
"""


def find_seller_reviews_by_rating(db_pool: ConnectionPool, min_rating: int, offset: int = 0) -> list:
    """Find seller reviews with rating >= min_rating ordered by review_date."""
    with db_pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(QUERY, (min_rating, offset))
            results = cur.fetchall()
            return results


def test_oppgave_9(benchmark: BenchmarkFixture, db_pool: ConnectionPool, explain_plan) -> None:
    explain_plan(QUERY)
    offset = [0]
    min_rating = 5

    def run_query() -> list:
        result = find_seller_reviews_by_rating(db_pool, min_rating, offset[0])

        if len(result) == 0:
            offset[0] = 0
        else:
            offset[0] += len(result)

        return result

    benchmark.pedantic(run_query, rounds=100, iterations=1)
