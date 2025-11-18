"""
Oppgave 6: Finn topp 100 selgere

Legg til den indexen som du tror gir best ytelse.
Se på planen. Hva ser du?

Denne spørringen blir kjørt mye, og tar tross alt litt tid.
Hvilke andre løsninger finnes for å begrense last på databasen og gi raskere responstid?
"""
from psycopg_pool import ConnectionPool
from pytest_benchmark.fixture import BenchmarkFixture

QUERY = "SELECT seller_id, AVG(rating) as avg_rating FROM seller_reviews GROUP BY seller_id ORDER BY avg_rating DESC LIMIT %s"


def find_top_sellers(db_pool: ConnectionPool, limit: int) -> list:
    """Find top N sellers by average rating."""
    with db_pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(QUERY, (limit,))
            results = cur.fetchall()
            return results


def test_oppgave_6(benchmark: BenchmarkFixture, db_pool: ConnectionPool, explain_plan) -> None:
    explain_plan(QUERY)

    def run_query() -> list:
        return find_top_sellers(db_pool, 100)

    result = benchmark.pedantic(
        run_query, rounds=1, warmup_rounds=1, iterations=1)

    seller_id, avg_rating = result[0]
    assert 255 == seller_id
    assert 4.85 == round(float(avg_rating), 2)
