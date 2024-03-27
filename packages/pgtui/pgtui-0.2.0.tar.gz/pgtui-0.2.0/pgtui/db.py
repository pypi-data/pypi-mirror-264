import logging
from contextlib import asynccontextmanager

from psycopg import AsyncConnection
from psycopg.rows import TupleRow

from pgtui.entities import DbInfo

logger = logging.getLogger(__name__)


async def fetch_db_info() -> DbInfo:
    query = """
    SELECT current_database() AS database,
           current_user AS user,
           current_schema AS schema;
    """

    async with connect() as conn:
        cursor = await conn.execute(query)
        row = await cursor.fetchone()
        assert row is not None
        database, user, schema = row

        return DbInfo(
            host=conn.pgconn.host.decode(),
            host_address=conn.pgconn.hostaddr.decode(),
            port=conn.pgconn.port.decode(),
            database=database,
            schema=schema,
            user=user,
        )


async def fetch_databases() -> list[str]:
    query = """
    SELECT datname
    FROM pg_database
    WHERE datallowconn AND NOT datistemplate;
    """

    rows = await select(query)
    return [r[0] for r in rows]


async def select(query: str) -> list[TupleRow]:
    async with execute(query) as cursor:
        return await cursor.fetchall()


@asynccontextmanager
async def execute(query: str):
    logger.info(f"Running query: {query}")
    async with connect() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(query.encode())
            yield cursor


@asynccontextmanager
async def connect():
    conn = await AsyncConnection.connect()
    async with conn:
        yield conn
