import asyncio
from typing import Iterable, Any, AsyncIterator, Optional

import aiosqlite


class SerializedConnection:
    def __init__(self, conn: aiosqlite.Connection):
        self._conn = conn
        self._lock = asyncio.Lock()

    async def execute(self, sql: str, parameters: Iterable[Any] = ()) -> aiosqlite.Cursor:
        async with self._lock:
            return await self._conn.execute(sql, parameters)

    async def executemany(self, sql: str, parameters: Iterable[Iterable[Any]] = ()) -> aiosqlite.Cursor:
        async with self._lock:
            return await self._conn.executemany(sql, parameters)

    async def commit(self) -> None:
        async with self._lock:
            await self._conn.commit()

    async def fetchone(self, sql: str, parameters: Iterable[Any] = ()) -> Optional[aiosqlite.Row]:
        async with self._lock:
            async with self._conn.execute(sql, parameters) as cursor:
                return await cursor.fetchone()

    async def fetchall(self, sql: str, parameters: Iterable[Any] = ()) -> list[aiosqlite.Row]:
        async with self._lock:
            async with self._conn.execute(sql, parameters) as cursor:
                return await cursor.fetchall()


    async def transaction(self, func) -> AsyncIterator[None]:
        async with self._lock:
            try:
                result = await func(self._conn)
                await self._conn.commit()
                return result
            except Exception:
                await self._conn.rollback()
                raise

    async def close(self) -> None:
        async with self._lock:
            await self._conn.close()