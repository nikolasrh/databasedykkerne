from psycopg_pool import ConnectionPool


def create_db_pool():
    """Create a connection pool for PostgreSQL database"""
    connstring = "postgresql://postgres:password@localhost:5433/postgres"

    return ConnectionPool(
        connstring,
        min_size=10,
        max_size=10,
        open=True,
        timeout=5,
        reconnect_timeout=5
    )
