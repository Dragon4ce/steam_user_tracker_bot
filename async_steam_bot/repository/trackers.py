from aiosqlite import Connection
from async_steam_bot.repository.base_repo import BaseRepository
from async_steam_bot.models.schemas import Tracker


class TrackersRepository(BaseRepository):
    """Репозиторий трекеров пользователей (таблица GeneralInfo)."""

    async def add(self, conn: Connection, tracker: Tracker):
        """
        Добавляет трекер в БД (в рамках переданной транзакции).

        Использует INSERT OR IGNORE — если такой трекер уже есть, вставка игнорируется
        (при наличии UNIQUE-индекса на (id, steamid, track)).

        :param conn: голое соединение (из transaction), лок уже удерживается снаружи.
        :param tracker: объект трекера (user_id, steam_id, track_type).
        """
        await conn.execute("INSERT OR IGNORE INTO GeneralInfo (id, steamid, track) VALUES (?, ?, ?)",
                                      (tracker.user_id, tracker.steam_id, tracker.track_type))

    async def delete(self, conn: Connection, tracker: Tracker):
        """
        Удаляет трекер из БД (в рамках переданной транзакции).

        Если строки нет — DELETE просто ничего не делает (не ошибка).

        :param conn: голое соединение (из transaction), лок уже удерживается снаружи.
        :param tracker: объект трекера (user_id, steam_id, track_type).
        """
        await conn.execute("DELETE FROM GeneralInfo WHERE id = ? AND steamid = ? AND track = ?",
                                 (tracker.user_id, tracker.steam_id, tracker.track_type))

    async def check_exists(self, conn: Connection, tracker: Tracker) -> bool:
        """
        Проверяет, существует ли трекер у пользователя (в рамках переданной транзакции).

        Используется и для проверки дубликата при добавлении, и для проверки
        существования при удалении.

        :param conn: голое соединение (из transaction), лок уже удерживается снаружи.
        :param tracker: объект трекера (user_id, steam_id, track_type).
        :return: True — трекер есть, False — нет.
        """
        async with conn.execute("SELECT id, steamid, track FROM GeneralInfo WHERE id = ? AND steamid = ? AND track = ?",
                     (tracker.user_id, tracker.steam_id, tracker.track_type)) as cursor:
            is_exist = await cursor.fetchone()
        return is_exist is not None


    async def get_user_trackers_list(self, user_id: int) -> tuple[Tracker] | None:
        """
        Возвращает все трекеры пользователя (одиночное чтение, вне транзакции).

        Использует обёртку соединения (self._connection), лок берётся автоматически.
        Возвращает домен (Tracker), а не сырые Row.

        :param user_id: ID пользователя бота.
        :return: кортеж Tracker (пустой, если трекеров нет).
        """
        raw_user_trackers = await self._connection.fetchall(sql="SELECT id, steamid, track FROM GeneralInfo WHERE id = ?", parameters=(user_id,))
        user_trackers = []
        for user_tracker in raw_user_trackers:
            tracker_object = dict(user_tracker)
            user_trackers.append(Tracker(user_id = tracker_object['id'], steam_id=tracker_object['steamid'], track_type=tracker_object['track']))
        return tuple(user_trackers) if user_trackers else None

    async def get_steamid_watchers(self, steam_id: int) -> tuple[int] | None:
        """
        Возвращает всех user_id, которые отслеживают указанный SteamID
        (одиночное чтение, вне транзакции).

        :param steam_id: SteamID64 отслеживаемого профиля.
        :return: список user_id (пустой список, если никто не отслеживает).
        """
        steamid_watchers = await self._connection.fetchall(sql="SELECT id FROM GeneralInfo WHERE steamid = ?",
                                                           parameters=(steam_id,))
        return tuple([watcher["id"] for watcher in steamid_watchers]) if steamid_watchers else None