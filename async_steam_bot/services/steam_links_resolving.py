import aiohttp
from async_steam_bot.services.steam_links_parsing import SteamLink, LinkType
from async_steam_bot.config import STEAM_API_KEY

class SteamLinkResolver:
    def __init__(self, steam_profile_link: SteamLink):
        self._steam_profile_link = steam_profile_link
        self._link_type = self._steam_profile_link.type
        self._link_value = self._steam_profile_link.value

    async def get_steamid_from_vanity_url(self) -> int | None:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    f'http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key={STEAM_API_KEY}&vanityurl={self._link_value}') as response:
                try:
                    data = await response.json()
                    if 'response' in data and 'steamid' in data['response']:
                        return data['response']['steamid']
                except Exception as e:
                    print(e)
                    return None

    async def resolve_steam_link(self) -> str | None:
        if self._link_type == LinkType.STEAM_ID:
            steam_id = self._link_value
            return steam_id
        elif self._link_type == LinkType.VANITY:
            steam_id = await self.get_steamid_from_vanity_url()
            return steam_id
        else:
            return None