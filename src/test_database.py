import pytest


def test_db_pool(db_pool):
    """Test that we can successfully connect to PostgreSQL database via connection pool"""
    with db_pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT 1")
            result = cur.fetchone()
            assert result[0] == 1
