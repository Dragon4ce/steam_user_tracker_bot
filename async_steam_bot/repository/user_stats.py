from aiosqlite import Connection
from async_steam_bot.models.schemas import UserStats
from async_steam_bot.repository.base_repo import BaseRepository

class UserStatsRepository(BaseRepository):
    """Репозиторий статистики пользователей (таблица UserStats)."""

    async def start_add_to_user_stats(self, user_id: int,):
        """
        Инициализирует запись статистики для нового пользователя (одиночная запись).

        Вызывается при первом /start. INSERT OR IGNORE — если запись уже есть,
        повторно не создаётся.

        :param user_id: ID пользователя бота.
        """
        await self._connection.execute(sql="INSERT OR IGNORE INTO UserStats (user_id, active_trackers, vip_status) VALUES (?, ?, ?)",
                                       parameters = (user_id, 0, False))

    async def increase_user_trackers_count(self, conn: Connection, user_id: int):
        """
        Увеличивает счётчик активных трекеров пользователя на 1 (в рамках транзакции).

        :param conn: голое соединение (из transaction), лок уже удерживается снаружи.
        :param user_id: ID пользователя бота.
        """
        await conn.execute("UPDATE UserStats SET active_trackers = active_trackers + 1 WHERE user_id = ?",
                                       (user_id,))
    async def decrease_user_trackers_count(self, conn: Connection, user_id: int):
        """
        Уменьшает счётчик активных трекеров пользователя на 1 (в рамках транзакции).

        :param conn: голое соединение (из transaction), лок уже удерживается снаружи.
        :param user_id: ID пользователя бота.
        """
        await conn.execute("UPDATE UserStats SET active_trackers = active_trackers - 1 WHERE user_id = ?",
                                       (user_id,))

    async def get_user_stats(self, conn: Connection, user_id: int) -> UserStats:
        """
        Возвращает статистику пользователя (в рамках транзакции).

        Используется внутри транзакций для атомарной проверки лимитов.

        :param conn: голое соединение (из transaction), лок уже удерживается снаружи.
        :param user_id: ID пользователя бота.
        :return: UserStats или None, если записи нет.
        """
        async with conn.execute("SELECT user_id, active_trackers, vip_status FROM UserStats WHERE user_id = ?",
                                      (user_id,)) as cursor:
            raw_stats = dict(await cursor.fetchone())  # (680702513, 0, 0)
            user_stats = UserStats(user_id=raw_stats['user_id'], tracks_count=raw_stats['active_trackers'],
                                   vip_status=True if raw_stats['vip_status'] else False)
            return user_stats

    async def get_user_vip_status(self, user_id: int):
        """
        Возвращает VIP-статус пользователя (одиночное чтение, вне транзакции).

        :param user_id: ID пользователя бота.
        :return: True — VIP, False — обычный (или если записи нет).
        """
        user_vip_status = await self._connection.fetchone("SELECT vip_status FROM UserStats WHERE user_id = ?", (user_id,))
        return user_vip_status

