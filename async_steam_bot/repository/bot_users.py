from async_steam_bot.repository.base_repo import BaseRepository

class BotUsersRepository(BaseRepository):

    async def start_add_to_db(self,user_id: int, username: str, start_time: str):
        """Функция добавления информации о юзере, впервые прожавшем /start в боте"""
        await self._connection.execute('''INSERT OR IGNORE INTO BotUsers (id, username, start_time) VALUES (?, ?, ?)''',
                                       (user_id, username, start_time))
