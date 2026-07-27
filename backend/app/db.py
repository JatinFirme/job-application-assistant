import psycopg
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import settings


# --- Raw connection (kept from Module 1, used only by /db-health) ---
def get_connection():
    """
    Opens a new raw connection to Postgres using the DATABASE_URL from
    settings. Kept around specifically for the simple /db-health check --
    everything else now goes through SQLAlchemy below.
    """
    return psycopg.connect(settings.database_url)


def check_db_connection() -> bool:
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1;")
                cur.fetchone()
        return True
    except Exception:
        return False


# --- SQLAlchemy setup (new in Module 2A) ---

# The "engine" manages a pool of connections to Postgres. You create it
# once per app, not once per request.
engine = create_engine(settings.database_url)

# SessionLocal is a factory: calling SessionLocal() gives you a new,
# independent "session" -- a workspace for a single unit of work
# (e.g. one API request), which you open, use, and close.
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    """
    Every SQLAlchemy model (like Resume) inherits from this. It's what lets
    SQLAlchemy discover all your table definitions in one place.
    """
    pass


def get_db():
    """
    A FastAPI "dependency": FastAPI will call this before running any
    endpoint that asks for it, hand the endpoint the yielded session, and
    guarantee the session is closed afterward -- even if the endpoint
    raises an error.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
