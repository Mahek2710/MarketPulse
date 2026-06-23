import psycopg2
from psycopg2 import pool
from contextlib import contextmanager
from config.settings import DATABASE_URL

_pool = None

def init_pool():
    global _pool
    _pool = psycopg2.pool.SimpleConnectionPool(
        minconn=1,
        maxconn=10,
        dsn=DATABASE_URL
    )

def get_pool():
    global _pool
    if _pool is None:
        init_pool()
    return _pool

@contextmanager
def get_connection():
    conn = get_pool().getconn()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        get_pool().putconn(conn)

@contextmanager
def get_cursor():
    with get_connection() as conn:
        with conn.cursor() as cur:
            yield cur