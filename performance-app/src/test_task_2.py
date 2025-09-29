"""
Task 2: Bli kjent med oppsettet del 2

Denne spørringen kjører også raskt!
Se på planen, og forklarer hvorfor til sidemannen.
"""
import random
from psycopg_pool import ConnectionPool
from pytest_benchmark.fixture import BenchmarkFixture

QUERY = "SELECT quantity FROM seller_inventory WHERE seller_id = %s AND product_id = %s"


def find_inventory_of_product_for_seller(db_pool: ConnectionPool, product_id: int, seller_id: int) -> int | None:
    """Find total inventory quantity for a product from a specific seller."""
    with db_pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(QUERY, (seller_id, product_id))
            result = cur.fetchone()
            return result[0] if result else None


def test_task_2(benchmark: BenchmarkFixture, db_pool: ConnectionPool, max_product_id: int, max_seller_id: int, explain_plan) -> None:
    explain_plan(QUERY)

    rng = random.Random(42)

    def run_query() -> int | None:
        product_id = rng.randint(1, max_product_id)
        seller_id = rng.randint(1, max_seller_id)
        return find_inventory_of_product_for_seller(db_pool, product_id, seller_id)

    benchmark.pedantic(run_query, rounds=10000, warmup_rounds=10, iterations=1)
