"""
Task C: Keyset pagination for seller reviews med minimum rating

I stedet for OFFSET, bruk keyset pagination.
Send med siste review_date og id fra forrige page som "keys" for å fortelle hvor langt man har kommet.
Filtrering gjør fortsatt spørringen tregere, men man må ikke gjør det for å regne ut offset.

Oppgaver:
- Hva er pros and cons med keyset pagination?
- Sammenlign ytelsen for min_rating = 1 og min_rating = 5. Forklar resultatet.
- Nevn en god use-case for keyset pagination og offset pagination.

Du kan lese mer om keyset pagination her:
https://use-the-index-luke.com/blog/2013-07/pagination-done-the-postgresql-way
https://use-the-index-luke.com/sql/partial-results/fetch-next-page

Bonusoppgave:
Keyset-et kan inneholde så mange verdier man vil.
Hvordan kan man da gjøre spørringen raskere når man filtrerer reviews på rating?
"""
from datetime import date
from psycopg_pool import ConnectionPool
from pytest_benchmark.fixture import BenchmarkFixture

QUERY = """
SELECT sr.id, sr.seller_id, sr.rating, sr.review_date
FROM seller_reviews sr
WHERE sr.rating >= %s
  AND (sr.review_date, sr.id) > (%s, %s)
ORDER BY sr.review_date, sr.id
LIMIT 1000
"""


def find_seller_reviews_keyset(
    db_pool: ConnectionPool,
    min_rating: int,
    last_review_date: date = date(1900, 1, 1),
    last_id: int = 0
) -> list:
    """Find seller reviews with rating >= min_rating using keyset pagination."""
    with db_pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(QUERY, (min_rating, last_review_date, last_id))
            results = cur.fetchall()
            return results


def test_task_c(benchmark: BenchmarkFixture, db_pool: ConnectionPool, explain_plan) -> None:
    explain_plan(QUERY)
    min_rating = 5
    last_review_date = [date(1900, 1, 1)]  # Vilkårlig lav startverdi. Alternativt ikke ha med filteret i SQL-en for første kall.
    last_id = [0]  # Starter på ID 0

    def run_query() -> list:
        result = find_seller_reviews_keyset(db_pool, min_rating, last_review_date[0], last_id[0])

        if len(result) == 0:
            last_review_date[0] = date(1900, 1, 1)
            last_id[0] = 0
        else:
            last_row = result[-1]
            last_review_date[0] = last_row[3]  # review_date
            last_id[0] = last_row[0]  # id

        return result

    benchmark.pedantic(run_query, rounds=1000, iterations=1)
