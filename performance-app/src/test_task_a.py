"""
Task A: Paginer gjennom seller reviews sortert på review_date

Hent ut 1000 seller reviews om gangen, sortert etter review_date.
Lag en index som gjør spørringen rask!

- Hvorfor må vi sortere på ID etter dato?
- Hvordan blir ytelsen for høyere offsets?
"""
import time
from datetime import date
from psycopg_pool import ConnectionPool
from pytest_benchmark.fixture import BenchmarkFixture
import matplotlib.pyplot as plt

QUERY = """
SELECT sr.id, sr.seller_id, sr.rating, sr.review_date
FROM seller_reviews sr
ORDER BY sr.review_date, sr.id
LIMIT 1000
OFFSET %s
"""


def find_seller_reviews(db_pool: ConnectionPool, offset: int = 0) -> list:
    """Find seller reviews ordered by review_date."""
    with db_pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(QUERY, (offset,))
            results = cur.fetchall()
            return results


def test_task_a(benchmark: BenchmarkFixture, db_pool: ConnectionPool, explain_plan) -> None:
    explain_plan(QUERY)
    offset = [0]
    timing_data = []

    def run_query() -> list:
        start_time = time.perf_counter()
        result = find_seller_reviews(db_pool, offset[0])
        end_time = time.perf_counter()

        timing_data.append((offset[0], (end_time - start_time) * 1000))

        if len(result) == 0:
            offset[0] = 0
        else:
            offset[0] += len(result)

        return result

    benchmark.pedantic(run_query, rounds=100, iterations=1)

    offsets = [data[0] for data in timing_data]
    times_ms = [data[1] for data in timing_data]

    plt.figure(figsize=(12, 6))
    plt.scatter(offsets, times_ms, alpha=0.6, s=20)
    plt.xlabel('Offset')
    plt.ylabel('Query Time (ms)')
    plt.title('Task A: Pagination Performance - Query Time vs Offset')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('task_a_results.png', dpi=150)
    print(f"\nPlot saved to task_a_results.png")
