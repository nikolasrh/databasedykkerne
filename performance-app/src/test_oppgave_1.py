"""
Oppgave 1: Bli kjent med oppsettet

Før testen printes planen for den uparametriserte spørringen med EXPLAIN.
Det kan man også gjøre i sitt foretrukne databaseverktøy, typisk ved å trykke F10.
Da gjør IDE-en samme EXPLAIN-spørring, men man får en litt finere visualisering.

Les mer her: https://www.postgresql.org/docs/current/using-explain.html

"Plan-reading is an art that requires some experience to master"

Denne testen kjøres 10000 ganger med pytest-benchmark og tar i underkant av 4 sekunder.

For å sammenligne resultater kan man se på den totale kjøretiden for testen som logges til slutt:

=== 1 passed in 3.39s ===

Testene har en 10 sekunders timeout, slik at de feiler hvis du har en for dårlig spørring eller index.

Denne spørringen kjører allerede raskt.
Se på planen, og forklarer hvorfor den kjører raskt til sidemannen.
"""
import random
from psycopg_pool import ConnectionPool
from pytest_benchmark.fixture import BenchmarkFixture

QUERY = "SELECT * FROM products WHERE id = %s"


def find_product_by_id(db_pool: ConnectionPool, product_id: int) -> tuple[str, float] | None:
    """Find a product by its ID."""
    with db_pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(QUERY, (product_id,))
            result = cur.fetchone()
            return result if result else None


def test_oppgave_1(benchmark: BenchmarkFixture, db_pool: ConnectionPool, max_product_id: int, explain_plan) -> None:
    explain_plan(QUERY)

    rng = random.Random(42)

    def run_query() -> tuple[str, float] | None:
        product_id = rng.randint(1, max_product_id)
        return find_product_by_id(db_pool, product_id)

    benchmark.pedantic(run_query, rounds=10000, warmup_rounds=10, iterations=1)
