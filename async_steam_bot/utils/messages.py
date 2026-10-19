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

ONLINE_STATUS = {
        0: "🔴 Оффлайн",
        1: "🟢 Онлайн",
        2: "🔴 Занят",
        3: "🌙 Отошёл",
        4: "💤 Спит",
        5: "🎮 Ищет игру"
    }

async def get_steam_profile_info(user_info: SteamUser) -> str:
    from async_steam_bot.utils.validators import Validator
    from async_steam_bot.utils.time_utils import Time

    username = await Validator.escape_markdown(user_info.username)

    online = user_info.get_online_status_text()
    if user_info.privacy_state != 3:
        private_profile_answer = (
            f"<b>Данный профиль является приватным или частично скрытым. Доступ к основным данным может быть недоступен!</b>\n\n"
            f"👤 <b>Ник:</b> <b>{username}</b>\n\n"
            f"🆔 <b>SteamID 64:</b> <code>{user_info.steam_id}</code>\n\n"
            f"🔗 <b>Ссылка:</b> <a href='{user_info.profile_url}'>профиль</a>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
        )
        return private_profile_answer
    else:
        timecreated = Time(user_info.timecreated)
        lastlogoff = Time.time_since_last_logoff(user_info.lastlogoff)
        public_profile_answer = (
            f"👤 <b>Ник:</b> <b>{username}</b>\n\n"
            f"<b>Зарегистрирован:</b> {timecreated.pretty_time()} <i>— примерно {timecreated.past_days_from_registration()} дней назад</i>\n\n"
            f"📊 <b>Статус:</b> {online}\n"
            f"🎮 <b>Активность:</b> {user_info.game or 'Не играет'}\n"
            f"🕦 <b>Последний раз в сети:</b> {lastlogoff}\n"
            f"🆔 <b>SteamID 64:</b> <code>{user_info.steam_id}</code>\n\n"
            f"🔗 <b>Ссылка:</b> <a href='{user_info.profile_url}'>профиль</a>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"<b>Сканирование завершено!</b> ✅"
        )
        return public_profile_answer

async def format_notifier_message(changes: list, username: str, link: str) -> list:
    """Возвращает список сообщений для всех изменений"""
    message = ''

    for track_type, old_value, new_value in changes:
        if track_type == 'online':
            if new_value == 0:
                message += f'🔴 Пользователь **[{username}]({link})** вышел из сети\\!\n'
            elif new_value == 1:
                message += f'🟢 Пользователь **[{username}]({link})** теперь в сети\\!\n'
            else:
                message += f'У пользователя **[{username}]({link})** изменился онлайн\\-статус: \n\n Старый: {ONLINE_STATUS.get(old_value)} \n\n Новый: {ONLINE_STATUS.get(new_value)}\n'

        elif track_type == 'game':
            if new_value:
                message += f"🎮 **[{username}]({link})** теперь играет в **{new_value}**\n"
            else:
                message += f"🎮 **[{username}]({link})** больше не играет\n"

        elif track_type == 'username':
            message += f"📝У пользователя **[{username}]({link})** изменился никнейм: **{old_value}** → **{new_value}**\n"

        elif track_type == 'avatar':
            message += f"🖼️ У **[{username}]({link})** обновился аватар\n"

        else:
            message += f"📢 У **[{username}]({link})** изменился параметр **{track_type}**\n"
    return message


UNKNOWN_COMMAND = 'Извините, но я не понимаю Вас! Воспользуйтесь командами из списка команд в /help'
NO_TRACKERS = 'У вас нету отслеживаемых пользователей'
INVALID_LINK = 'Некорректные данные, перепроверьте введенную ссылку / SteamID64'
ADD_TRACKER_PROMPT = '*Воспользуйтесь предложенными методами отслеживания ниже!*'
DELETE_PROMPT = 'Выберите трекер для удаления:'
HELP_TEXT = """
Доступные команды:
/start - перезапуск бота
"""
METHOD_SWAP_MSG = InputRichMessage(blocks = [
    InputRichBlockSectionHeading(text = RichTextBold(text = 'Выберите один из режимов ниже!'), size = 4),
    InputRichBlockButtons(buttons=[
        RichMessageButton(
            text='🟢STEAM TRACKING🟢',
            style='success',
            callback_data='steam_tracking'
        ),
        RichMessageButton(
            text='🟢SteamID64 Info🟢',
            style='success',
            callback_data='steamid_info'
        )
    ], align='center'),
])


MESSAGES = {
    'unknown_command': UNKNOWN_COMMAND,
    'no_trackers': NO_TRACKERS,
    'invalid_link': INVALID_LINK,
    'add_tracker_prompt': ADD_TRACKER_PROMPT,
    'delete_prompt': DELETE_PROMPT,
    'help': HELP_TEXT,
    'method_swap_message': METHOD_SWAP_MSG
}

