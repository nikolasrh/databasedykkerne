import pytest
import re

from .database import create_db_pool


def convert_psycopg_to_postgres_params(sql_query: str) -> str:
    """Convert psycopg %s parameters to PostgreSQL $1, $2, etc. format"""
    counter = [0]

    def replace_param(_):
        counter[0] += 1
        return f"${counter[0]}"

    return re.sub(r'%s', replace_param, sql_query)


@pytest.fixture(scope="session")
def db_pool():
    """Create a shared connection pool for all tests"""
    with create_db_pool() as pool:
        yield pool


@pytest.fixture(scope="session")
def max_product_id(db_pool):
    """Get maximum product ID from database"""
    with db_pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT MAX(id) FROM products")
            return cur.fetchone()[0]


@pytest.fixture(scope="session")
def max_seller_id(db_pool):
    """Get maximum seller ID from database"""
    with db_pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT MAX(id) FROM sellers")
            return cur.fetchone()[0]


@pytest.fixture(scope="session")
def explain_plan(db_pool):
    """General fixture for displaying EXPLAIN plans"""
    def _explain(sql_query):
        converted_query = convert_psycopg_to_postgres_params(sql_query)
        explain_query = f"EXPLAIN (GENERIC_PLAN, BUFFERS, VERBOSE) {converted_query}"

        try:
            with db_pool.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(explain_query)

                    query_plan_lines = []
                    for row in cur.fetchall():
                        query_plan_lines.append(row[0])

                    query_plan = "\n  ".join(query_plan_lines)
                    print(f"\n\nEXPLAIN query plan:\n\n  {query_plan}")
        except Exception:
            print(f"\n\nEXPLAIN query failed:\n\n  {explain_query}")

    return _explain
