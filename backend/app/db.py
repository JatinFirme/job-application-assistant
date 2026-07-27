import psycopg

from app.core.config import settings


def get_connection():
    """
    Opens a new raw connection to Postgres using the DATABASE_URL from
    settings. We're using plain psycopg (no ORM) for now, on purpose --
    you should see exactly what a database connection looks like before
    we hide it behind an ORM in the next module.
    """
    return psycopg.connect(settings.database_url)


def check_db_connection() -> bool:
    """
    Opens a connection, runs the simplest possible query (SELECT 1), and
    returns True/False.
    """
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1;")
                cur.fetchone()
        return True
    except Exception:
        return False
