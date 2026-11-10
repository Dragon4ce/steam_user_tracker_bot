from typing import List
from async_steam_bot.models.schemas import SteamUser


def find_updated_params(old_data, new_data: SteamUser) -> List[str] | None:
    updated_params = []
    if old_data.online_status != new_data.online_status:
        updated_params.append('online')
    if old_data.username != new_data.username:
        updated_params.append('username')
    if old_data.current_game != new_data.current_game:
        updated_params.append('game')
    if old_data.avatar_url != new_data.avatar_url:
        updated_params.append('avatar')
    return updated_params if updated_params else None