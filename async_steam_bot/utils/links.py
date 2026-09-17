from async_steam_bot.services.steam_api import SteamAPIService
class LinksService:
    def __init__(self, link):
        self._link = link

    async def resolve_url(self):
        try:
            if 'steamcommunity.com/id' in self._link:
                url_parts = self._link.split('/')
                custom_id = ''
                for part in url_parts:
                    if part and part != 'profiles' and part != 'id' \
                            and not part.startswith('http') \
                            and not part.startswith('steam'):
                        custom_id = part
                        break
                steam_id = await SteamAPIService.resolve_vanity_url(custom_id=custom_id)
                return steam_id if steam_id else None
            if 'steamcommunity.com/profiles/7656' in self._link:
                url_parts = self._link.split('/')
                for part in url_parts:
                    if part and part != 'profiles' and not part.startswith('http') and not part.startswith('steam'):
                        steamid = part
                        return int(steamid)
            else:
                return None
        except Exception as e:
            print(f'ERROR. Class: Links, func: resolve_url', e)
            return None

    async def check_steamid_message(self) -> str | None:
        try:
            if self._link.isdigit() and len(self._link) == 17:
                return self._link

            if 'steamcommunity.com' in self._link:
                return await self.resolve_url()

            return None

        except Exception as e:
            print(f'ERROR. LinksService.check_steamid_message: {e}')
            return None

