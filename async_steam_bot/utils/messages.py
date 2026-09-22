from async_steam_bot.models.schemas import UserStats, SteamUser

START_MESSAGE = ("*Доброго времени суток\\! Тебя приветствует бот для трекинга Steam\\-профилей\\. "
                 "Давай немножно введу тебя в курс дела и расскажу, что я умею:*")
ONLINE_STATUS = {
        0: "🔴 Оффлайн",
        1: "🟢 Онлайн",
        2: "🔴 Занят",
        3: "🌙 Отошёл",
        4: "💤 Спит",
        5: "🎮 Ищет игру"
    }


# MARKDOWN_PARSE_EXAMPLE_MESSAGE = ('''bold \*text*
# _italic \*text_
# __underline__
# ~strikethrough~
# ||spoiler||
# bold _italic bold ~italic bold strikethrough ||italic bold strikethrough spoiler||~ __underline italic bold___ bold*
# [inline URL](http://www.example.com/)
# [inline mention of a user](tg://user?id=123456789)
# ![👍](tg://emoji?id=5368324170671202286)
# `inline fixed-width code`
# `​`​`
# pre-formatted fixed-width code block
# `​`​`
# `​`​`python
# pre-formatted fixed-width code block written in the Python programming language
# `​`​`
# >Block quotation started
# >Block quotation continued
# >Block quotation continued
# >Block quotation continued
# >The last line of the block quotation
# **>The second expandable block quotation started right after the previous
# >It is separated from the previous block quotation by an empty bold entity
# >Expandable block quotation continued
# >Hidden by default part of the expandable block quotation started
# >Expandable block quotation continued
# >The last line of the expandable block quotation with the expandability mark||''')



def get_start_message(greeting: str) -> str:
    return (
        f"*{greeting}*\n\n"
        f"*📋 ОПИСАНИЕ СИСТЕМЫ:*\n\n"
        f"Бот предназначен для отслеживания активности пользователей Steam\\.\n\n"
        f"*Предоставляет два основных режима работы:*\n\n"
        f"• *Трекинг\\-система* — автоматическое отслеживание изменений статуса, игры, никнейма и аватара с уведомлениями\n\n"
        f"• *Проверка профиля* — ручной поиск информации об аккаунте по ссылке или SteamID\n\n"
        f"**>*⚙️ ФУНКЦИОНАЛ:*\n"
        f">├ 🔍 Поиск пользователей Steam\n"
        f">├ 📊 Отслеживание активности\n"
        f">├ 🔔 Уведомления об изменениях\n"
        f">├ 🖼️ Получение аватара\n"
        f">└ 📁 История трекеров пользователя\n>\n"
        f">*⏱️ ТЕХНИЧЕСКАЯ ИНФОРМАЦИЯ:*\n"
        f">├ 🔄 Частота проверки трекеров — 30 секунд\n"
        f">├ 🌐 Источник данных — Steam\n"
        f">├ 🆔 Поддерживаемые форматы: SteamID64, Vanity URL, Profile URL\n"
        f">└ 💾 Сохранение данных в локальной базе||\n\n"
        f"*Для продолжения выберите режим работы в меню ниже\\.*\n"
    )


async def get_tracking_info(stats: UserStats, username: str) -> str:
    return (
        "\n"
        "🎮 **STEAM TRACKER**\n"
        "*Система мониторинга*\n"
        "\n\n"
        f"👤 *Пользователь:* `{username}`\n"
        f"🆔 *ID:* `{stats.user_id}`\n"
        f"📊 *Активных трекеров:* `{stats.tracks_count}/{stats.get_limits()}`\n"
        f"💎 *VIP статус:* {'✅ **Активен**' if stats.vip_status else '❌ **Не активен**'}\n\n"
        "**>━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        ">\n"
        ">🔍 *О СИСТЕМЕ:*\n"
        ">├ 🤖 Режим работы: Парсинг Steam API\n"
        ">├ ⏱️ Проверка каждые **30 сек**\n"
        ">└ 🔔 Мгновенные уведомления\n>\n"
        ">📊 *ПАРАМЕТРЫ:*\n"
        ">├ 🟢 `online`  — онлайн статус\n"
        ">├ 🎮 `game`    — текущая игра\n"
        ">├ 🖼️ `avatar`  — аватарка\n"
        ">├ 📝 `username`— никнейм\n"
        ">└ 🔥 `fulltrack`— *ВСЁ СРАЗУ\\!*\n>\n"
        ">⚡ *ЛИМИТЫ:*\n"
        ">├ 👤 *FREE* \\(10 трекеров\\)\n"
        ">│  └ Базовые параметры\n"
        ">├ 👑 *VIP* \\(25 трекеров\\)\n"
        ">│  ├ 🔥 **FULLTRACK** режим\n"
        ">│  └ ⚡ Приоритетные уведомления\n"
        ">└─────────────────\n"
        ">\n"
        ">🔥 *FULLTRACK* – отслеживает:\n"
        ">   ✅ Онлайн \\+ Игра \\+ Аватар \\+ Ник\n"
        ">   ✅ 1 трекер вместо 4\n"
        ">   ✅ Мгновенные уведомления\n"
        ">\n"
        ">📌 *ПРИМЕРЫ:*\n"
        ">🟢 Dragon4ce зашел в сеть\\!\n"
        ">🎮 Dragon4ce играет в CS2\n"
        ">📝 Dragon4ce → Dragon\n"
        ">🖼️ Аватар обновлен\n"
        ">\n"
        ">\n"
        ">━━━━━━━━━━━━━━━━━━━━━━━━━||\n\n"
        "*ВАЖНО:* Для работы уведомлений требуется подключить их по кнопке ниже\\!\n\n"
        "⬇️ *ВЫБЕРИТЕ ДЕЙСТВИЕ* ⬇️"
    )
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
        lastlogoff = Time(user_info.lastlogoff).time_since_last_logoff()
        public_profile_answer = (
            f"👤 <b>Ник:</b> <b>{username}</b>\n\n"
            f"<b>Зарегистрирован:</b> {timecreated.pretty_time()} <i>— примерно {timecreated.past_days_from_registration()} дней назад</i>\n\n"
            f"📊 <b>Статус:</b> {online}\n"
            f"🎮 <b>Активность:</b> {user_info.game or 'Не играет'}\n"
            f"🎮 <b>Последний раз в сети:</b> {lastlogoff}\n"
            f"🆔 <b>SteamID 64:</b> <code>{user_info.steam_id}</code>\n\n"
            f"🔗 <b>Ссылка:</b> <a href='{user_info.profile_url}'>профиль</a>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"<b>Сканирование завершено!</b> ✅"
        )
        return public_profile_answer


def get_checker_info() -> str:
    reply_message = '''🎮 **STEAM CHECKER**
*Система мгновенного поиска*

━━━━━━━━━━━━━━━━━━━━━━━━━

🔍 **О СИСТЕМЕ:**
├ 🤖 Режим работы: Парсинг Steam API
├ ⚡ Скорость ответа: **до 2 секунд**
└ 📊 Полная информация об аккаунте

📊 **ДОСТУПНЫЕ ДАННЫЕ:**
├ 🟢 `online`  — онлайн статус
├ 🎮 `game`    — текущая игра
├ 📝 `username`— никнейм
├ 🖼️ `avatar`  — аватар
├ 🆔 `steamid` — уникальный идентификатор
├ 📅 `created` — дата регистрации
└ 🔗 `profile` — ссылка на профиль

━━━━━━━━━━━━━━━━━━━━━━━━━

📋 **СПОСОБЫ ВВОДА:**
├ 🔗 Ссылка на профиль
│  `https://steamcommunity.com/id/username/`
│  `https://steamcommunity.com/profiles/steamid64`
├ 🆔 SteamID64
│  `76561198895393980`
└ 🆔 Custom ID
│  `Dragon4ce`

━━━━━━━━━━━━━━━━━━━━━━━━━'''
    return reply_message


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
METHOD_SWAP_MSG = '**Выберите один из предложенных режимов ниже\\!**'


MESSAGES = {
    'greeting': START_MESSAGE,
    'unknown_command': UNKNOWN_COMMAND,
    'no_trackers': NO_TRACKERS,
    'invalid_link': INVALID_LINK,
    'add_tracker_prompt': ADD_TRACKER_PROMPT,
    'delete_prompt': DELETE_PROMPT,
    'help': HELP_TEXT,
    'method_swap_message': METHOD_SWAP_MSG
}

