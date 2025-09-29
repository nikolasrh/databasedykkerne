"""
Task 8: Finn produkter med vurdering

Her henter vi ut 1000 produkter om gangen med gjennomsnittlig vurdering.
Etter å ha hentet ut de 1000 første, hentes 1001-2000, og så videre.
De er sortert på product_id.

- Legg til en index du tenker gir mening
- Prøv å skrive om spørringen slik at den blir raskere
- Hva er fordeler og ulemper med å bruke offset pagination?

Øk rounds argumentet fra 20 hvis du får til en bra spørring.
Hvor mange pages rekker du på 10 sekunder?
"""
from psycopg_pool import ConnectionPool
from pytest_benchmark.fixture import BenchmarkFixture

QUERY = """
SELECT p.id, p.category, p.released_date, AVG(pr.rating) as avg_rating
FROM products p
LEFT JOIN product_reviews pr ON p.id = pr.product_id
GROUP BY p.id, p.category, p.released_date
ORDER BY p.id
LIMIT 1000
OFFSET %s
"""


def find_products_with_avg_reviews_by_id(db_pool: ConnectionPool, offset: int = 0) -> list:
    """Find products with their average ratings, ordered by product ID."""
    with db_pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(QUERY, (offset,))
            results = cur.fetchall()
            return results


def test_task_8(benchmark: BenchmarkFixture, db_pool: ConnectionPool, explain_plan) -> None:
    explain_plan(QUERY)
    results = []
    offset = [0]

    def run_query() -> list:
        result = find_products_with_avg_reviews_by_id(db_pool, offset[0])

        if len(results) < 2:
            results.append(result)

        if len(result) == 0:
            offset[0] = 0
        else:
            offset[0] += 1000

        return result

    benchmark.pedantic(run_query, rounds=20, iterations=1)

    page1 = results[0]
    page2 = results[1]
    assert len(page1) == 1000
    assert len(page2) == 1000
    assert 1 == page1[0][0]
    assert 1000 == page1[999][0]
    assert 1001 == page2[0][0]
    assert 2000 == page2[999][0]
