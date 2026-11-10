from async_steam_bot.repository.serialized_connections import SerializedConnection

class BaseRepository:
    def __init__(self, connection: SerializedConnection):
        self._connection = connection

    @property
    def connection(self) -> SerializedConnection:
        return self._connection