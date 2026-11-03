from typing import List
from refactoring_files.pydantic_schemas import SteamUser


class SteamUserProcessing:
    def __init__(self, steam_user: SteamUser):
        self._user = steam_user
        self._ONLINE_STATUS = {
        0: "🔴 Оффлайн",
        1: "🟢 Онлайн",
        2: "🔴 Занят",
        3: "🌙 Отошёл",
        4: "💤 Спит",
        5: "🎮 Ищет игру"
    }

    def find_updated_params(self, new_data: SteamUser) -> List[str] | None:
        updated_params = []
        if self._user.online_status != new_data.online_status:
            updated_params.append('online')
        if self._user.username !=  new_data.username:
            updated_params.append('username')
        if self._user.current_game != new_data.current_game:
            updated_params.append('game')
        if self._user.avatar_url != new_data.avatar_url:
            updated_params.append('avatar')
        return updated_params if updated_params else None

    def get_online_status_text(self) -> str:
        """Получить текстовый статус онлайн"""
        return self._ONLINE_STATUS.get(self._user.online_status, "❓ Неизвестно")

