import re

from dataclasses import dataclass
from enum import Enum
from typing import Optional
from async_steam_bot.models.schemas import SteamLink

class LinkType(str, Enum):
    STEAM_ID = "steam_id"
    VANITY = "vanity"
    INVALID = "invalid"

@dataclass
class SteamLink:
    type: LinkType
    value: Optional[str]

    def __post_init__(self):
        if self.type is LinkType.STEAM_ID:
            if not (self.value.isdigit() and len(self.value) == 17):
                raise ValueError('Invalid STEAM_ID format')
        elif self.type is LinkType.VANITY:
            if not (self.value and re.fullmatch(r"[a-zA-Z0-9-_]+", self.value)):
                raise ValueError(f"VANITY требует валидный Vanity-URL, получено: {self.value!r}")
        elif self.type is LinkType.INVALID:
            if self.value is not None:
                raise ValueError("INVALID не должен иметь значения")

    @staticmethod
    def parse_steamid_link(raw_link: str) -> SteamLink:
        raw_link = raw_link.strip()
        if raw_link.isdigit() and len(raw_link) == 17:
            return SteamLink(LinkType.STEAM_ID, raw_link)
        elif id_match := re.search(r"steamcommunity\.com/id/([a-zA-Z0-9-_]+)", raw_link):
            return SteamLink(LinkType.VANITY, id_match.group(1))
        elif id_match := re.search(r"steamcommunity\.com/profiles/(\d+)", raw_link):
            return SteamLink(LinkType.STEAM_ID, id_match.group(1))
        else:
            return SteamLink(LinkType.INVALID, None)
