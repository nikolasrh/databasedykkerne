"""
Oppgave 7: Finn topp 10 selgere i Trondheim

Sjekk den planen, da!

Sammenlignet med forrige oppgave sjekker vi nå også `location` og at selgeren har minst 10 reviews.
Hvorfor fungerer index(er) bedre nå?
"""
from psycopg_pool import ConnectionPool
from pytest_benchmark.fixture import BenchmarkFixture

QUERY = """
SELECT s.id, s.location, AVG(sr.rating) as avg_rating, COUNT(sr.id) as review_count
FROM sellers s
JOIN seller_reviews sr ON s.id = sr.seller_id
WHERE s.location = %s
GROUP BY s.id, s.location
HAVING COUNT(sr.id) >= %s
ORDER BY avg_rating DESC
LIMIT %s
"""


def find_top_sellers_by_location(db_pool: ConnectionPool, location: str, min_reviews: int, limit: int) -> list:
    """Find top-rated sellers in a specific location with minimum review count."""
    with db_pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(QUERY, (location, min_reviews, limit))
            results = cur.fetchall()
            return results


def test_oppgave_7(benchmark: BenchmarkFixture, db_pool: ConnectionPool, explain_plan) -> None:
    explain_plan(QUERY)

    def run_query() -> list:
        return find_top_sellers_by_location(db_pool, location="trondheim", min_reviews=10, limit=10)

    result = benchmark.pedantic(
        run_query, rounds=10, warmup_rounds=1, iterations=1)

    assert len(result) == 10
    seller_id, location, avg_rating, review_count = result[0]
    assert 1656 == seller_id
    assert "trondheim" == location
    assert 4.45 == round(float(avg_rating), 2)
    assert 253 == review_count
