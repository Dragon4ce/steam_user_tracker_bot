import asyncio
import aiosqlite
from async_steam_bot.config import db_path
from async_steam_bot.models.schemas import Tracker, SteamUser, UserStats
import logging

class Database:

    """Класс-модель базы данных, включающий в себя методы работы с ней"""

    def __init__(self, db_file = db_path):
        self.db_file = db_file
        self.lock = asyncio.Lock()


    async def start_add_to_db(self,user_id: int, username: str, start_time: str):

        """Функция добавления информации о юзере, впервые прожавшем /start в боте"""

        async with aiosqlite.connect(self.db_file) as db:
            await db.execute('''INSERT OR IGNORE INTO BotUsers (id, username, start_time) VALUES (?, ?, ?)''',
                             (user_id, username, start_time))
            await db.commit()
            print('DB DEBUG: start_add_to_db: обработано')

    async def start_add_to_user_stats(self, user_id: int,):

        """Функция инициализации данных о статистике пользователя. Выполняется одновременно с первым вызовом /start пользователем."""

        async with aiosqlite.connect(self.db_file) as db:
            await db.execute("INSERT OR IGNORE INTO UserStats (user_id, active_trackers, vip_status) VALUES (?, ?, ?)", (user_id, 0, False))
            await db.commit()
            logging.info('DB DEBUG: start_add_to_user_stats: обработано')

    async def add_tracker_to_db(self, tracker: Tracker):

        """Функция добавления трекера. Принимает dataclass типа Traker, откуда и берет данные для внесения в БД."""

        async with self.lock:
            async with aiosqlite.connect(self.db_file) as connection:
                await connection.execute("INSERT OR IGNORE INTO GeneralInfo (id, steamid, track) VALUES (?, ?, ?)",
                                      (tracker.user_id, tracker.steam_id, tracker.track_type))
                await connection.commit()
                logging.info('DB DEBUG: add_tracker_to_db: обработано')

    async def add_tracker_info_to_db(self, steam_user: SteamUser):

        """Функция добавления информации из SteamAPI об отслеживаемом аккаунте.
         Выполняется одновременно с добавлением трекера в БД пользователем."""

        async with self.lock:
            async with aiosqlite.connect(self.db_file) as connection:
                await connection.execute("INSERT OR IGNORE INTO TrackInfo (steamid, game, username, online, avatar, profile_url, timecreated) VALUES (?, ?, ?, ?, ?, ?, ?)", (steam_user.steam_id,
                                                                       steam_user.game,
                                                                       steam_user.username,
                                                                        steam_user.online,
                                                                       steam_user.avatar,
                                                                       steam_user.profile_url,
                                                                        steam_user.timecreated))
                await connection.commit()
                logging.info('DB DEBUG: add_tracker_info_to_db: обработано')

    async def check_duplicate_tracker(self, tracker) -> bool:

        """Мини-функция проверки на наличие дубликата трекера в Базе Данных.
        Помогает избежать повторного добавления одного и того же трекера пользователем через интерфейс бота."""

        async with self.lock:
            async with aiosqlite.connect(self.db_file) as connection:
                async with connection.execute("SELECT id, steamid, track FROM GeneralInfo WHERE id = ? AND steamid = ? AND track = ?",
                                              (tracker.user_id, tracker.steam_id, tracker.track_type)) as cursor:
                    has_duplicate = await cursor.fetchone()
                    if has_duplicate:
                        return True
                    return False

    async def get_user_trackers_from_db(self, user_id: int):

        """Функция, позволяющая получить все текущие трекеры пользователя в формате кортежа с вложенными кортежами."""

        async with self.lock:
            async with aiosqlite.connect(self.db_file) as connection:
                async with connection.execute("SELECT steamid, track FROM GeneralInfo WHERE id = ?",
                                       (user_id,)) as cursor:
                    user_tracks = await cursor.fetchall()
                    result = []
                    for track in user_tracks:
                        result.append(Tracker.from_db_row((user_id, track[0], track[1])))
                    return result

    async def get_tracker_username_from_db(self, steam_id: int):

        """Мини-функция, позволяющая быстро получить никнейм отслеживаемого профиля Steam, не используя кэширование."""

        async with self.lock:
            async with aiosqlite.connect(self.db_file) as connection:
                async with connection.execute("SELECT username FROM TrackInfo WHERE steamid = ?", (steam_id,)) as cursor:
                    user_tracks = await cursor.fetchone()
                    return user_tracks[0] if user_tracks else 'Unknown'

    async def remove_tracker_from_db(self, tracker: Tracker):

        """Функция, удаляющая трекер из базы данных.
         Принимает на вход dataclass типа Tracker, откуда и берет информацию для SQL-запроса."""

        async with self.lock:
            async with aiosqlite.connect(self.db_file) as connection:
                await connection.execute("DELETE FROM GeneralInfo WHERE id = ? AND steamid = ? AND track = ?",
                                         (tracker.user_id, tracker.steam_id, tracker.track_type))
                await connection.commit()
                logging.info('DB DEBUG: remove_tracker_from_db: обработано')

    async def get_user_stats_from_db(self, user_id: int) -> UserStats:

        """Функция для получения статистики пользователя (user_id, кол-во активных трекеров, лимиты, вип-статус).
         Принимает на вход ID пользователя, возвращает dataclass типа UserStats."""

        async with self.lock:
            async with aiosqlite.connect(self.db_file) as connection:
                async with connection.execute("SELECT active_trackers, vip_status FROM UserStats WHERE user_id = ?", (user_id,)) as cursor:
                    user_stats_from_db = await cursor.fetchone() #(680702513, 0, 0)
                    user_stats = UserStats(user_id=user_id, tracks_count=user_stats_from_db[0], vip_status=True if user_stats_from_db[1] else False)
                    #print(user_stats) #UserStats(user_id=680702513, tracks_count=0, vip_status=True, limit=25)
                    return user_stats

    async def add_to_user_stats_trackers_count(self, user_id: int):

        """Простая быстрая функция для редактирования статистики кол-ва текущих трекеров пользователя в Базе Данных (в данном случае плюсует трекеры)"""

        async with self.lock:
            async with aiosqlite.connect(self.db_file) as connection:
                await connection.execute("UPDATE UserStats SET active_trackers = active_trackers + 1 WHERE user_id = ?",
                                         (user_id,))
                await connection.commit()

    async def delete_from_user_stats_trackers_count(self, user_id: int):

        """Простая быстрая функция для редактирования статистики кол-ва текущих трекеров пользователя в Базе Данных (в данном случае отнимает трекеры)"""

        async with self.lock:
            async with aiosqlite.connect(self.db_file) as connection:
                await connection.execute("UPDATE UserStats SET active_trackers = active_trackers - 1 WHERE user_id = ?",
                                         (user_id,))
                await connection.commit()
                logging.info('DB DEBUG: delete_from_user_stats_trackers_count: обработано')

    async def get_info_about_tracker(self, steam_id: int) -> SteamUser:

        """Функция для получения информации о Steam-профиле из БД. Пример выходных данных:
        ('0', '✞ DragonAce ✞', 0, 'https://avatars.steamstatic.com/8df3fbb9717a9433d4c709138700c25228676cb9_full.jpg')"""

        async with self.lock:
            async with aiosqlite.connect(self.db_file) as connection:
                async with connection.execute("SELECT game, username, online, avatar, profile_url, timecreated FROM TrackInfo WHERE steamid = ?", (steam_id,)) as cursor:
                    info_about_tracker = await cursor.fetchone()
                    formatted_info_about_tracker = SteamUser(
                                                            steam_id=steam_id,
                                                            game=info_about_tracker[0],
                                                            username=info_about_tracker[1],
                                                            online=info_about_tracker[2],
                                                            avatar=info_about_tracker[3],
                                                            profile_url=info_about_tracker[4],
                                                            timecreated=info_about_tracker[5]
                                                            )
                return formatted_info_about_tracker

    async def update_tracker_info(self, steam_user: SteamUser):

        """Функция для обновления информации о трекере. Используется при каждом вызове обновления информации о всех трекерах в БД."""

        async with self.lock:
            async with aiosqlite.connect(self.db_file) as connection:
                await connection.execute(
                    """UPDATE TrackInfo 
                       SET game = ?, username = ?, online = ?, avatar = ?, profile_url = ?, timecreated = ?
                       WHERE steamid = ?""",
                    (
                        steam_user.game,
                        steam_user.username,
                        steam_user.online,
                        steam_user.avatar,
                        steam_user.profile_url,
                        steam_user.timecreated,
                        steam_user.steam_id
                    )
                )
                await connection.commit()
                logging.info('DB DEBUG: update_tracker_info: обработано')

    async def get_steamid_watchers(self, steam_id: int) -> tuple:

        """Функция для получения кортежа со всеми user_id, отслеживающими переданный в функцию SteamID."""

        async with self.lock:
            async with aiosqlite.connect(self.db_file) as connection:
                async with connection.execute("SELECT id FROM GeneralInfo WHERE steamid = ?", (steam_id,)) as cursor:
                    steamid_watchers = await cursor.fetchall()
                    return steamid_watchers

    async def delete_tracker_info_from_db(self, steam_id: int):

        """Функция для удаления информации об аккаунте Steam из базы данных.
         Вызывается при чистке БД, если профиль с таким SteamID не имеет ни одного watcher."""

        async with self.lock:
            async with aiosqlite.connect(self.db_file) as connection:
                await connection.execute("DELETE FROM TrackInfo WHERE steamid = ?", (steam_id,))
                await connection.commit()

    async def get_steamid_from_all_trackers(self) -> list[int]:

        """Мини-функция для получения всех SteamID, присутствующих в БД на момент вызова.
         Данные берутся из таблицы с информацией о трекерах пользователей."""

        async with self.lock:
            async with aiosqlite.connect(self.db_file) as connection:
                async with connection.execute("SELECT steamid FROM GeneralInfo") as cursor:
                    steamid_from_all_trackers = await cursor.fetchall()
                    return [int(steam_id_tuple[0]) for steam_id_tuple in steamid_from_all_trackers]

    async def get_steamid_from_all_trackers_info(self) -> list[int]:

        """Мини-функция для получения всех SteamID, присутствующих в БД на момент вызова.
         Данные берутся из таблицы с информацией о Steam профилях трекеров."""

        async with self.lock:
            async with aiosqlite.connect(self.db_file) as connection:
                async with connection.execute("SELECT steamid FROM TrackInfo") as cursor:
                    steamid_from_all_trackers = await cursor.fetchall()
                    return [int(steam_id_tuple[0]) for steam_id_tuple in steamid_from_all_trackers]

    async def get_watchers_dict_for_notifier(self, steam_id: int) -> dict:

        """Функция для форматирования словаря, который впоследствии передается в notifier для более удобной структуризации данных."""

        async with self.lock:
            async with aiosqlite.connect(self.db_file) as connection:
                async with connection.execute("SELECT id, track FROM GeneralInfo WHERE steamid = ?", (steam_id,)) as cursor:
                    watchers_list = await cursor.fetchall()
                    watchers_dict = {}
                    for user_id, track_type in watchers_list:
                        if watchers_dict.get(user_id) is None:
                            watchers_dict[user_id] = []
                        watchers_dict[user_id].append(track_type)
                    return watchers_dict

    async def check_deleted_tracker(self, tracker: Tracker) -> bool:

        """Функция для проверки: удален ли трекер или нет. Используется для предотвращения удаления несуществующего трекера из БД.
         В противном случае возможны нестабильности в системе удаления трекеров
         (двойное удаление/уход user_current_tracker_count в отрицательные значения)."""

        async with self.lock:
            async with aiosqlite.connect(self.db_file) as connection:
                async with connection.execute("SELECT id, steamid, track FROM GeneralInfo WHERE id = ? AND steamid = ? AND track = ?", (tracker.user_id,
                                                                                                                     tracker.steam_id,
                                                                                                                     tracker.track_type)) as cursor:
                    tracker_info = await cursor.fetchone()
                    logging.info('check_deleted_tracker: ', tracker_info)
                    return True if tracker_info else False

    async def check_user_vip(self, user_id: int) -> bool:

        """Мини-функция для проверки vip-статуса пользователя"""

        async with self.lock:
            async with aiosqlite.connect(self.db_file) as connection:
                async with connection.execute("SELECT vip_status FROM UserStats WHERE user_id = ?", (user_id,)) as cursor:
                    user_vip_status = await cursor.fetchone()
                    return True if user_vip_status[0] == 1 else False
