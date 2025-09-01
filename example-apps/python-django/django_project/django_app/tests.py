
import unittest
from django.test import TestCase

# Create your tests here.


@unittest.skip("Database disabled")
class SQLiteConnectionTest(TestCase):
    """
    Test SQLite database connection with Django.
    """

    databases = ['default']

    def test_sqlite_connection(self):
        """Test SQLite connection."""
        try:
            from django.db import connections
            connection = connections['default']
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1 as test_value")
                result = cursor.fetchone()

                self.assertEqual(result[0], 1)

        except Exception as e:
            self.fail(f"SQLite query failed: {e}")


@unittest.skip("Database disabled")
class PostgreSQLConnectionTest(TestCase):
    """
    Test PostgreSQL database connection without Django.
    """

    def test_postgres_connection(self):
        """Test PostgreSQL connection."""
        try:
            import psycopg2

            connection = psycopg2.connect(
                host='host.docker.internal',
                port='5432',
                database='postgres',
                user='postgres',
                password='password'
            )
            cursor = connection.cursor()
            cursor.execute("SELECT 1 as test_value")
            result = cursor.fetchone()

            self.assertEqual(result[0], 1)

            cursor.close()
            connection.close()

        except Exception as e:
            self.fail(f"PostgreSQL query failed: {e}")


@unittest.skip("Database disabled")
class OracleConnectionTest(TestCase):
    """
    Test Oracle database connection without Django.
    """

    def test_oracle_connection(self):
        """Test Oracle connection."""
        try:
            import oracledb

            dsn = oracledb.makedsn(
                "host.docker.internal", 1521, service_name="FREEPDB1")
            connection = oracledb.connect(
                user="django_user", password="password", dsn=dsn)
            cursor = connection.cursor()
            cursor.execute("SELECT 1 FROM dual")
            result = cursor.fetchone()

            self.assertEqual(result[0], 1, )

            cursor.close()
            connection.close()

        except Exception as e:
            self.fail(f"Oracle query failed: {e}")
