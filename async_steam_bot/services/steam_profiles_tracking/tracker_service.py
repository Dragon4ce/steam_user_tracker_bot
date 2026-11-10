from aiosqlite import Connection
from enum import Enum
from async_steam_bot.models.schemas import Tracker, SteamUser
from async_steam_bot.repository.serialized_connections import SerializedConnection
from async_steam_bot.repository.user_stats import UserStatsRepository
from async_steam_bot.repository.trackers import TrackersRepository
from async_steam_bot.repository.trackers_info import TrackersInfoRepository

class TrackerAddStatus(str, Enum):
    ADDED = 'added'
    DUPLICATE = 'duplicate'
    LIMIT_EXCEEDED = 'limit exceeded'
    INVALID = 'invalid'

class TrackerDeleteStatus(str, Enum):
    SUCCESSFULLY_DELETED = 'successfully deleted'
    ALREADY_DELETED = 'already deleted'
    NO_TRACKERS = 'no trackers found'


class TrackerService:
    """Сервис (use case) для работы с трекерами пользователя.
    Оркеструет репозитории и обеспечивает атомарность операций
    (добавление/удаление) через общую транзакцию."""

    def __init__(self, connection: SerializedConnection,
                 user_stats_repo: UserStatsRepository,
                 trackers_repo: TrackersRepository,
                 trackers_info_repo: TrackersInfoRepository):
        """
        :param connection: обёртка над соединением (открывает транзакции).
        :param user_stats_repo: репозиторий статистики пользователя.
        :param trackers_repo: репозиторий трекеров (GeneralInfo).
        :param trackers_info_repo: репозиторий информации о Steam-профилях (TrackInfo).
        """

        self._connection = connection
        self._user_stats_repo = user_stats_repo
        self._trackers_repo = trackers_repo
        self._trackers_info_repo = trackers_info_repo

    async def add_tracker_transaction(self, tracker: Tracker, steam_user: SteamUser):

        """
        Атомарно добавляет трекер пользователю.

        Внутри одной транзакции:
            1. Проверяет, нет ли уже такого трекера у пользователя (дубликат).
            2. Проверяет лимит трекеров (VIP/обычный).
            3. Добавляет трекер в GeneralInfo.
            4. Увеличивает счётчик активных трекеров в UserStats.
            5. Добавляет/обновляет информацию о Steam-профиле в TrackInfo.

        :param tracker: объект трекера (user_id, steam_id, track_type).
        :param steam_user: данные Steam-профиля для сохранения в TrackInfo.
        :return: статус операции (ADDED / DUPLICATE / LIMIT_EXCEEDED).
        """

        async def _do(conn: Connection):
            if await self._trackers_repo.check_exists(conn, tracker):
                return TrackerAddStatus.DUPLICATE
            user_stats = await self._user_stats_repo.get_user_stats(conn, tracker.user_id)
            if not user_stats.can_add_tracks():
                return TrackerAddStatus.LIMIT_EXCEEDED
            await self._trackers_repo.add(conn, tracker)
            await self._user_stats_repo.increase_user_trackers_count(conn, tracker.user_id)
            await self._trackers_info_repo.add_tracker_details(conn, steam_user)
            return TrackerAddStatus.ADDED

        return await self._connection.transaction(func=_do)

    async def delete_tracker_transaction(self, tracker: Tracker):

        """
        Атомарно удаляет трекер пользователя.

        Внутри одной транзакции:
            1. Проверяет, есть ли у пользователя вообще трекеры.
            2. Проверяет, существует ли именно этот трекер.
            3. Удаляет трекер из GeneralInfo.
            4. Уменьшает счётчик активных трекеров в UserStats.

        :param tracker: объект трекера (user_id, steam_id, track_type).
        :return: статус операции (SUCCESSFULLY_DELETED / ALREADY_DELETED / NO_TRACKERS).
        """

        async def _do(conn: Connection):
            user_stats = await self._user_stats_repo.get_user_stats(conn, tracker.user_id)
            if user_stats.tracks_count == 0:
                return TrackerDeleteStatus.NO_TRACKERS
            if not(await self._trackers_repo.check_exists(conn, tracker)):
                return TrackerDeleteStatus.ALREADY_DELETED
            await self._trackers_repo.delete(conn, tracker)
            await self._user_stats_repo.decrease_user_trackers_count(conn, tracker.user_id)
            return TrackerDeleteStatus.SUCCESSFULLY_DELETED

        return await self._connection.transaction(func=_do)


import asyncio, os, dotenv
from async_steam_bot.repository.connections_factory import create_serialized_connection
dotenv.load_dotenv(dotenv_path=r'C:\Users\grmld\PycharmProjects\async_telegram_bot\.env')
db_path = os.environ.get("DATABASE_PATH")

async def main():
    connection = await create_serialized_connection(db_path)
    try:
        trackers_repo = TrackersRepository(connection)
        user_stats_repo = UserStatsRepository(connection)
        trackers_info_repo = TrackersInfoRepository(connection)

        service = TrackerService(
            connection=connection,
            user_stats_repo=user_stats_repo,
            trackers_repo=trackers_repo,
            trackers_info_repo=trackers_info_repo,
        )

        tracker = Tracker(user_id=575085617, steam_id=76561199466124723, track_type="online")
        steam_user = SteamUser(steam_id=76561199466124722,
                               username="Test",
                               online_status=0,
                               privacy_state=0,
                               time_created=0,
                               last_logoff=0,
                               current_game='None',
                               profile_url='None',
                               avatar_url='None',)

        print(await service.add_tracker_transaction(tracker, steam_user))

        # проверка: прочитать из БД
        #rows = await trackers_repo.get_user_trackers_list(user_id=680702513)
        #print("Trackers:", *[f'{row}' for row in rows], sep="\n")
        #watchers = await trackers_repo.get_steamid_watchers(steam_id=76561199466124723)
        #print(watchers)
        #print(await trackers_info_repo.get_tracker_details(steam_id=76561199466124722))
        row = await user_stats_repo.get_user_vip_status(user_id=680702513)
        print(row['vip_status'])
    finally:
        await connection.close()

asyncio.run(main())