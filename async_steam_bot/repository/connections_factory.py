import aiosqlite
from async_steam_bot.repository.serialized_connections import SerializedConnection


async def create_serialized_connection(db_path: str) -> SerializedConnection:
     connection = await aiosqlite.connect(db_path)
     connection.row_factory = aiosqlite.Row
     await connection.execute('PRAGMA busy_timeout = 5000')
     try:
         await connection.execute('PRAGMA journal_mode = WAL')
     except aiosqlite.OperationalError:
         pass
     await connection.execute('PRAGMA foreign_keys = ON')
     return SerializedConnection(connection)

