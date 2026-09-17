import aiohttp
from typing import Optional
from async_steam_bot.models.schemas import SteamUser
from async_steam_bot.config import STEAM_API_KEY

class SteamAPIService:
    def __init__(self, steam_id: int):
        self._steam_id = steam_id
        self._user: Optional[SteamUser] = None

    async def get_steam_user_info(self) -> Optional[SteamUser]:
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
                        player = data['response']['players'][0]
                        self._user = SteamUser(
                            steam_id=int(player.get('steamid', 0)),
                            username=player.get('personaname', 'Unknown'),
                            online=player.get('personastate', 0),
                            game=player.get('gameextrainfo'),
                            avatar=player.get('avatarfull'),
                            timecreated=player.get('timecreated', None),
                            profile_url=player.get('profileurl', '')
                        )
                        return self._user
                except Exception as e:
                    print(f"Ошибка API. SteamAPIService.get_steam_user_info: {e}")
                    return None


    async def get_username(self) -> str:
        if not self._user:
            await self.get_steam_user_info()
        return self._user.username if self._user else 'Unknown'
    @staticmethod
    async def resolve_vanity_url(custom_id: str) -> int | None:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    f'http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key={STEAM_API_KEY}&vanityurl={custom_id}') as response:
                try:
                    data = await response.json()
                    if 'response' in data and 'steamid' in data['response']:
                        return data['response']['steamid']
                except Exception as e:
                    print(e)
                    return None
                                                                                 
