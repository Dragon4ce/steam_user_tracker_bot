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
    RichTextButton,
)
def get_tracking_info(stats: UserStats, username: str) -> InputRichMessage:
    answer = InputRichMessage(blocks=[
        InputRichBlockSectionHeading(text = RichTextBold(text='STEAM TRACKER'), size = 2),
        InputRichBlockSectionHeading(text = RichTextBold(text='Система мониторинга'), size = 4),
        InputRichBlockDetails(summary = RichTextBold(text='📈ИНФОРМАЦИЯ О ПОЛЬЗОВАТЕЛЕ'), blocks = [
            InputRichBlockDivider(),
            InputRichBlockParagraph(text = RichTextBold(text = f'👤Пользователь: {username}')),
            InputRichBlockParagraph(text = RichTextBold(text = f'🆔ID: {stats.user_id}')),
            InputRichBlockParagraph(text = RichTextBold(text = f'📊Активных трекеров {stats.tracks_count}/{stats.get_limits()}')),
            InputRichBlockParagraph(text = RichTextBold(text = f'💎VIP статус: {'✅ Активен' if stats.vip_status else '❌ Не активен'}'))
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
                text='➕ ДОБАВИТЬ',
                style='success',
                callback_data='add_tracker'
            ),
            RichMessageButton(
                text='➖ УДАЛИТЬ',
                style='danger',
                callback_data='delete_tracker'
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