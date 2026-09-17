from dataclasses import dataclass
from typing import Optional, List, Any, Dict
import asyncio
@dataclass
class SteamUser:
    """Данные пользователя Steam"""
    steam_id: int
    username: str
    online: int  # 0 - оффлайн, 1 - онлайн, 2 - занят, 3 - отошёл, 4 - сон, 5 - ищет игру
    game: Optional[str]
    avatar: Optional[str]
    timecreated: Optional[int]
    profile_url: str

    ONLINE_STATUS = {
        0: "🔴 Оффлайн",
        1: "🟢 Онлайн",
        2: "🔴 Занят",
        3: "🌙 Отошёл",
        4: "💤 Спит",
        5: "🎮 Ищет игру"
    }
    def is_online(self) -> bool:
        return self.online != 0


    def get_online_status_text(self) -> str:
        """Получить текстовый статус онлайн"""
        return self.ONLINE_STATUS.get(self.online, "❓ Неизвестно")

    async def to_dict(self) -> Dict[str, Any]:
        """Преобразует в словарь для сохранения в кэш/БД"""
        return {
            'online': self.online,
            'username': self.username,
            'game': self.game,
            'avatar': self.avatar,
            'profileurl': self.profile_url
        }

    def diff(self, other: 'SteamUser') -> List[str]:
        """Возвращает список полей, которые изменились"""
        changed = []
        if self.online != other.online:
            changed.append('online')
        if self.username != other.username:
            changed.append('username')
        if self.game != other.game:
            changed.append('game')
        if self.avatar != other.avatar:
            changed.append('avatar')
        return changed

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

    def to_tuple(self) -> tuple:
        return (self.user_id, self.steam_id, self.track_type)


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


