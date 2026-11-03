from dataclasses import dataclass
from typing import Optional, List, Any, Dict
import asyncio
from typing import Optional
from pydantic import BaseModel, Field, field_validator, create_model, AliasChoices


class SteamUser(BaseModel):

    #Неизменные постоянные параметры от SteamAPI
    steam_id: int = Field(validation_alias='steamid', serialization_alias='steamid')
    profile_url: str = Field(validation_alias=AliasChoices('profileurl', 'profile_url'), serialization_alias='profile_url')
    username: str = Field(validation_alias=AliasChoices('personaname', 'username'), serialization_alias='username')
    privacy_state: int = Field(validation_alias=AliasChoices('communityvisibilitystate', 'privacy_state'), serialization_alias='privacy_state')
    time_created: int = Field(validation_alias='timecreated', serialization_alias='timecreated')
    avatar_url: str = Field(validation_alias=AliasChoices('avatarfull', 'avatar'), serialization_alias='avatar')
    online_status: int = Field(validation_alias=AliasChoices('personastate', 'online'), serialization_alias='online')

    #Опциональные параметры
    current_game: Optional[str] = Field(validation_alias=AliasChoices('gameextrainfo', 'game'), serialization_alias='game', default=None)
    last_logoff: Optional[int] = Field(validation_alias='lastlogoff', serialization_alias='lastlogoff', default=None)





@dataclass
class Tracker:
    """Датакласс Tracker. Хранит основную информацию о трекере"""
    user_id: int
    steam_id: int
    track_type: str

    VALID_TRACK_TYPES = ['online', 'game', 'avatar', 'username', 'fulltrack']

    def is_fulltrack(self) -> bool:
        return self.track_type == 'fulltrack'

    def should_notify(self, changed_params: List[str]) -> bool:
        if self.track_type == 'fulltrack':
            return True
        return self.track_type in changed_params

    @classmethod
    def from_db_row(cls, row: tuple) -> 'Tracker':
        """Из строки БД (steamid, track)"""
        return cls(
            user_id= row[0],
            steam_id= row[1],
            track_type= row[2]
        )

@dataclass
class ChangesInfo:
    steam_id: int
    changes: List[str]  # список изменённых полей
    old_data: SteamUser  # старые данные
    new_data: SteamUser  # новые данные

    def format_messages(self) -> List[str]:
        """Форматирует сообщения для каждого изменения"""
        messages = []

        for field in self.changes:
            if field == 'online':
                old_status = self.old_data.get_online_status_text()
                new_status = self.new_data.get_online_status_text()
                messages.append(f"🟢 {self.new_data.username} → {new_status}")

            elif field == 'game':
                if self.new_data.game:
                    messages.append(f"🎮 {self.new_data.username} теперь играет в **{self.new_data.game}**")
                else:
                    messages.append(f"🎮 {self.new_data.username} больше не играет")

            elif field == 'username':
                messages.append(f"📝 {self.old_data.username} → **{self.new_data.username}**")

            elif field == 'avatar':
                messages.append(f"🖼️ У {self.new_data.username} обновился аватар")

        return messages


@dataclass

class UserStats:
    user_id: int
    tracks_count: int
    vip_status: bool = False
    limit: int = 10 #default limits for non VIP

    def __post_init__(self):
        if self.vip_status:
            self.limit = 25
        else:
            self.limit = 10
    def get_limits(self) -> int:
        return self.limit

    def can_add_tracks(self):
        '''Check if user can add tracks with no limit break'''
        return self.tracks_count < self.limit

    def get_remaining_slots(self):
        '''Func to get remaining slots'''
        return self.limit - self.tracks_count

@dataclass

class TrackMethod:
    name: str
    display_name: str = ''


    METHODS = {
        'online': ('🟢 Онлайн', 'online'),
        'game': ('🎮 Игра', 'game'),
        'username': ('📝 Никнейм', 'username'),
        'avatar': ('🖼️ Аватар', 'avatar'),
        'fulltrack': ('🔥 FULLTRACK', 'fulltrack')
    }

    @staticmethod
    def get_method_display_name(name: str) -> str:
        return TrackMethod.METHODS[name][0]

    @classmethod
    def get_free_methods(cls) -> list['TrackMethod']:
        return [
            cls(name='online', display_name='🟢 Онлайн'),
            cls(name='game', display_name='🎮 Игра'),
            cls(name='username', display_name='📝 Никнейм'),
            cls(name='avatar', display_name='🖼️ Аватар'),
        ]

    @classmethod
    def get_vip_methods(cls) -> list['TrackMethod']:
        return [
            cls(name='online', display_name='🟢 Онлайн'),
            cls(name='game', display_name='🎮 Игра'),
            cls(name='username', display_name='📝 Никнейм'),
            cls(name='avatar', display_name='🖼️ Аватар'),
            cls(name='fulltrack', display_name='🔥 FULLTRACK')
        ]

    @classmethod
    def get_method_by_name(cls, callback_data: str) -> "TrackMethod":
        for name, (display, _) in cls.METHODS.items():
            if f'add_track_{name}' in callback_data:
                return cls(name=name, display_name=display)
        return None

@dataclass

class SteamLink:
    raw_link: str
    steam_id: Optional[int] = None
    is_valid: bool = False

    def get_steam_id(self) -> Optional[int]:
        return self.steam_id


