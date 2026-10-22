from async_steam_bot.models.database import Database
from async_steam_bot.models.schemas import UserStats, SteamUser
from aiogram.types import (
    InputRichBlockBlockQuotation,
    InputRichBlockDivider,
    InputRichBlockFooter,
    InputRichBlockMathematicalExpression,
    InputRichBlockParagraph,
    InputRichBlockSectionHeading,
    InputRichBlockDetails,
    InputRichBlockTable,
    InputRichMessage,
    Message,
    RichBlockTableCell,
    RichTextAnchor,
    RichTextAnchorLink,
    RichTextBold,
    RichTextCode,
    RichTextItalic,
    RichTextSpoiler,
    RichTextSuperscript,
    InputRichBlockList,
    InputRichBlockListItem,
    InputRichBlockPullQuotation,
    CallbackQuery,
    CopyTextButton,
    DisabledButton,
    InputRichBlockButtons,
    InputRichBlockParagraph,
    InputRichBlockSectionHeading,
    InputRichMessage,
    Message,
    RichMessageButton,
    RichTextButton, InputRichBlockPhoto, InputMediaPhoto, RichTextUrl,
)
from async_steam_bot.utils.time_utils import Time
from async_steam_bot.models.schemas import Tracker, SteamUser, TrackMethod

def get_tracking_info(stats: UserStats, username: str) -> InputRichMessage:
    vip_status_text = '✅ Активен' if stats.vip_status else '❌ Не активен'
    answer = InputRichMessage(blocks=[
        InputRichBlockSectionHeading(text = RichTextBold(text='STEAM TRACKER'), size = 2),
        InputRichBlockSectionHeading(text = RichTextBold(text='Система мониторинга'), size = 4),
        InputRichBlockDetails(summary = RichTextBold(text='📈ИНФОРМАЦИЯ О ПОЛЬЗОВАТЕЛЕ'), blocks = [
            InputRichBlockDivider(),
            InputRichBlockParagraph(text = RichTextBold(text = f'👤Пользователь: {username}')),
            InputRichBlockParagraph(text = RichTextBold(text = f'🆔ID: {stats.user_id}')),
            InputRichBlockParagraph(text = RichTextBold(text = f'📊Активных трекеров {stats.tracks_count}/{stats.get_limits()}')),
            InputRichBlockParagraph(text = RichTextBold(text = f'💎VIP статус: {vip_status_text}'))
        ], is_open=False),
        InputRichBlockDetails(summary = RichTextBold(text = '💬ОПИСАНИЕ ТРЕКИНГ СИСТЕМЫ'), blocks = [
            InputRichBlockDivider(),
            InputRichBlockParagraph(text = [
                RichTextBold(text = '🔍О СИСТЕМЕ\n\n'),
                "🤖 Режим работы: Парсинг Steam AP\n",
                "⏱️ Проверка каждые",
                RichTextBold(text = ' 30 секунд\n'),
                "🔔 Мгновенные уведомления\n\n",
            ]),
            InputRichBlockDivider(),
            InputRichBlockParagraph(text = [
                RichTextBold(text="📊 ПАРАМЕТРЫ:\n\n"),
                RichTextCode(text = '🟢 online '),
                "—  онлайн статус\n",
                RichTextCode(text='🎮 game '),
                "—  текущая игра\n",
                RichTextCode(text='🖼️ avatar '),
                "—  аватарка\n",
                RichTextCode(text='📝 username '),
                "—  никнейм\n",
                RichTextCode(text='🔥 fulltrack '),
                "—  ВСЁ СРАЗУ!\n",
            ], is_open=False),
            InputRichBlockDivider(),
            InputRichBlockParagraph(text = [
                RichTextBold(text = '⚡ЛИМИТЫ:\n\n'),
                RichTextBold(text="👤 FREE"),
                " (10 трекеров)\n",
                " └ Базовые параметры\n",
                RichTextBold(text = "👑 VIP"),
                " (25 трекеров)\n",
                " ├ 🔥 FULLTRACK режим\n"
                " └ ⚡ Приоритетные уведомления\n"
            ]),
            InputRichBlockDivider(),
            InputRichBlockParagraph(text = [
                RichTextBold(text="🔥 FULLTRACK"),
                " отслеживает:\n\n",
                "✅ Онлайн + Игра + Аватар + Ник\n",
                "✅ 1 трекер вместо 4\n",
                "✅ Приоритетные уведомления\n"
            ]),
            InputRichBlockDivider(),
            InputRichBlockParagraph(text = [
                RichTextBold(text = "📌ПРИМЕРЫ УВЕДОМЛЕНИЙ:\n\n"),
                "🟢 Dragon4ce теперь в сети!\n"
                "🎮 Dragon4ce теперь играет в CS2\n"
                "📝 У пользователя DragonAce изменился никнейм: ✞ DragonAce ✞ → DragonAce\n"
                "🖼️ У пользователя DragonAce обновился аватар!\n"
            ])
        ]),

        InputRichBlockSectionHeading(text = RichTextBold(text = "Подключение уведомлений"), size = 4),
        InputRichBlockParagraph(text = [
            RichTextBold(text = 'Для работы уведомлений требуется подключить их по кнопке ниже!\n')
        ]),
        InputRichBlockPullQuotation(text = [
            RichTextBold(text = "⬇️ ВЫБЕРИТЕ ДЕЙСТВИЕ ⬇️")
        ]),
        InputRichBlockButtons(buttons = [
            RichMessageButton(
                text = '📋 МОИ ТРЕКЕРЫ',
                style = 'primary',
                callback_data = 'check_trackers'
            ),
            RichMessageButton(
                text = '⭐ VIP',
                style = 'primary',
                callback_data = 'vip_info'
            ),
        ], align='center'),
        InputRichBlockButtons(buttons = [
            RichMessageButton(
                text='❓ ПОМОЩЬ',
                style='primary',
                callback_data='tracker_help'
            ),
            RichMessageButton(
                text='⚙️ СМЕНИТЬ РЕЖИМ',
                style='primary',
                callback_data='on_start',
            ),
        ], align='center'),
        InputRichBlockButtons(buttons = [
            RichMessageButton(
                text='🔔ПОДКЛЮЧИТЬ УВЕДОМЛЕНИЯ',
                style='success',
                callback_data='pair_notifications'
            )
        ], align='center'),
    ])
    return answer

async def format_one_tracker(tracker_object: Tracker) -> InputRichBlockDetails:
    database = Database()
    tracker_info = await database.get_info_about_tracker(steam_id=tracker_object.steam_id)
    tracker_details = InputRichBlockDetails(summary = [RichTextBold(text = f'{tracker_info.username}'),
                                                       RichTextBold(text = f' — {TrackMethod.get_method_display_name(name=tracker_object.track_type)}')], blocks = [
        InputRichBlockPhoto(photo = InputMediaPhoto(
        media=tracker_info.avatar)),
        InputRichBlockParagraph(text = [
            RichTextBold(text = '👤Никнейм: '),
            f'{tracker_info.username}\n',
            RichTextBold(text = '📊 Онлайн статус: '),
            f'{tracker_info.get_online_status_text()}\n',
            RichTextBold(text='🎮 Активность: '),
            f'{tracker_info.game if tracker_info.game else "Не играет"}\n',
            RichTextBold(text='🕦 Последний раз в сети: '),
            f'{Time.time_since_last_logoff(lastlogoff_time=tracker_info.lastlogoff)}\n',
            RichTextBold(text='🆔 SteamID 64: '),
            RichTextCode(text = f'{tracker_info.steam_id}\n'),
            RichTextBold(text='🔗 Ссылка на профиль: '),
            RichTextUrl(url=f'https://steamcommunity.com/profiles/{tracker_info.steam_id}', text='профиль'),
            f' '
        ]),
        InputRichBlockButtons(buttons = [
            RichMessageButton(
                text='➖ УДАЛИТЬ ТРЕКЕР',
                style = 'danger',
                callback_data = f'remove_tracker_{tracker_object.user_id}_{tracker_object.steam_id}_{tracker_object.track_type}'
            )
        ], align='center'),
    ])
    return tracker_details

async def format_tracker_menu(user_trackers: list) -> InputRichMessage:
    answer_blocks = [InputRichBlockSectionHeading(text = RichTextBold(text = '✅АКТИВНЫЕ ТРЕКЕРЫ:'), size=2)]
    for tracker in user_trackers:
        new_tracker_info = await format_one_tracker(tracker)
        answer_blocks.append(new_tracker_info)
    answer_blocks.extend([
        InputRichBlockButtons(buttons = [
            RichMessageButton(
                text = '➕ ДОБАВИТЬ ТРЕКЕР',
                style = 'success',
                callback_data = 'add_tracker'
            )
    ], align='center'),
        InputRichBlockButtons(buttons = [
            RichMessageButton(
                text='📋В МЕНЮ',
                style='primary',
                callback_data='steam_tracking'
            ),
            RichMessageButton(
                text='⚙️ СМЕНИТЬ РЕЖИМ',
                style='primary',
                callback_data='on_start'
            )
        ], align='center'),
    ])
    return InputRichMessage(blocks = answer_blocks)
