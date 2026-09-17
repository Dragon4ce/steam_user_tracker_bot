from async_steam_bot.models.database import Database
from async_steam_bot.utils.messages import format_notifier_message
from async_steam_bot.utils.validators import Validator
from aiogram.types import URLInputFile

async def send_notification_to_all_watchers(steam_id: int, changes: list, bot):
    database = Database()
    watchers_dict = await database.get_watchers_dict_for_notifier(steam_id=steam_id)
    user_info = await database.get_info_about_tracker(steam_id=steam_id)
    avatar = URLInputFile(user_info.avatar)
    if not watchers_dict:
        print(f"Нет подписчиков для steam_id {steam_id}")
        return

    username = await database.get_tracker_username_from_db(steam_id=steam_id)
    valid_username = await Validator().escape_markdown(username)

    for user_id, track_types_list in watchers_dict.items():
        if 'fulltrack' in track_types_list:
            should_send_notification = True
        else:
            should_send_notification = any(track in [c[0] for c in changes] for track in track_types_list)
        if should_send_notification:
            message = await format_notifier_message(changes=changes,
                                              username=valid_username,
                                              link = f'https://steamcommunity.com/profiles/{steam_id}'
                                              )
            try:
                await bot.send_photo(photo=avatar,
                                     chat_id=user_id,
                                     caption=message,
                                     parse_mode="MarkdownV2")
                print(f"✅ Уведомление отправлено пользователю {user_id}")
            except Exception as e:
                print(f"❌ Ошибка отправки пользователю {user_id}: {e}")



