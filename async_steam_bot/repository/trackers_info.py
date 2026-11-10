from aiosqlite import Connection
from async_steam_bot.repository.base_repo import BaseRepository
from async_steam_bot.models.schemas import SteamUser


class TrackersInfoRepository(BaseRepository):
    """Репозиторий информации о Steam-профилях (таблица TrackInfo)."""

    async def add_tracker_details(self, conn: Connection, steam_profile_info: SteamUser):
        """
        Добавляет информацию о Steam-профиле в TrackInfo (в рамках переданной транзакции).

        Использует INSERT OR IGNORE — если профиль уже есть, вставка игнорируется.

        :param conn: голое соединение (из transaction), лок уже удерживается снаружи.
        :param steam_profile_info: доменная модель SteamUser с данными профиля.
        """
        await conn.execute(
                        "INSERT OR IGNORE INTO TrackInfo (steamid, game, username, online, avatar, profile_url, timecreated, lastlogoff, privacy_state) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (
                            steam_profile_info.steam_id,
                            steam_profile_info.current_game,
                            steam_profile_info.username,
                            steam_profile_info.online_status,
                            steam_profile_info.avatar_url,
                            steam_profile_info.profile_url,
                            steam_profile_info.time_created,
                            steam_profile_info.last_logoff,
                            steam_profile_info.privacy_state
                        )
        )
    async def update_tracker_details(self, steam_profile_info: SteamUser):
        """
        Обновляет информацию о Steam-профиле в TrackInfo (в рамках переданной транзакции).

        Используется при фоновом обновлении данных о всех трекерах.

        :param conn: голое соединение (из transaction), лок уже удерживается снаружи.
        :param steam_profile_info: доменная модель SteamUser с актуальными данными.
        """
        await self._connection.execute(sql="UPDATE TrackInfo SET game = ?, username = ?,online = ?, avatar = ?, profile_url = ?, timecreated = ?, lastlogoff = ?, privacy_state = ? WHERE steamid = ?",
                                 parameters=
                                    (steam_profile_info.current_game,
                                    steam_profile_info.username,
                                    steam_profile_info.online_status,
                                    steam_profile_info.avatar_url,
                                    steam_profile_info.profile_url,
                                    steam_profile_info.timecreated,
                                    steam_profile_info.lastlogoff,
                                    steam_profile_info.privacy_state,
                                    steam_profile_info.steam_id))

    async def get_tracker_details(self, steam_id: int) -> SteamUser | None:
        """
        Возвращает информацию о Steam-профиле из БД (одиночное чтение, вне транзакции).

        :param steam_id: SteamID64 профиля.
        :return: SteamUser или None, если профиля нет в БД.
        """

        row = dict(await self._connection.fetchone(sql="SELECT steamid, game, username, online, avatar, profile_url, timecreated, lastlogoff, privacy_state FROM TrackInfo WHERE steamid = ?",
                                                   parameters=(steam_id,)))
        if row:
            user_info = SteamUser.model_validate(row, by_alias=True)
            return user_info
        return None