import aiohttp
from typing import Optional
from refactoring_files.pydantic_schemas import SteamUser
from async_steam_bot.config import STEAM_API_KEY

class SteamAPIService:
    def __init__(self, steam_id: int):
        self._steam_id = steam_id
        self._user: Optional[SteamUser] = None

    async def get_steam_user_info(self) -> SteamUser | None:
        url = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/"
        params = {
            'key': STEAM_API_KEY,
            'steamids': self._steam_id
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url, params=params) as response:
                try:
                    data = await response.json()
                    if 'response' in data and 'players' in data['response']:
                        player_model = data['response']['players'][0]
                        self._user = SteamUser.model_validate(player_model)
                        return self._user
                    else:
                        return None
                except Exception as e:
                    print(f"Ошибка API. SteamAPIService.get_steam_user_info: {e}")
                    return None


    async def get_username(self) -> str:
        if not self._user:
            await self.get_steam_user_info()
        return self._user.username if self._user else 'Unknown'

