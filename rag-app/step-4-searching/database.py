"""Database connection for step-4"""
import psycopg2
from pgvector.psycopg2 import register_vector


def create_connection():
    """Opprett tilkobling til PostgreSQL med pgvector"""
    conn = psycopg2.connect(
        host="localhost",
        port=5433,
        database="postgres",
        user="postgres",
        password="password"
    )
    register_vector(conn)
    return conn
