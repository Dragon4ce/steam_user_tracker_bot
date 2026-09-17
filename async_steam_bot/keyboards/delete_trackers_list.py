from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from async_steam_bot.models.database import Database

async def delete_trackers_list(user_id: int) -> InlineKeyboardMarkup:
    database = Database()
    keyboard = InlineKeyboardBuilder()
    user_trackers = await database.get_user_trackers_from_db(user_id=user_id) ##[Tracker(user_id=680702513, steam_id=76561198895393980, track_type='online')]
    for number, tracker in enumerate(user_trackers, 1):
        nickname = await database.get_tracker_username_from_db(tracker.steam_id)
        keyboard.add(InlineKeyboardButton(
            text = f'{number}. Никнейм: {nickname}. Трекер: {tracker.track_type}',
            callback_data=f'remove_tracker_{tracker.user_id}_{tracker.steam_id}_{tracker.track_type}'))
    keyboard.add(InlineKeyboardButton(text='Отменить удаление',
                                      callback_data='cancel_tracker_delete'))
    keyboard.adjust(1)
    return keyboard.as_markup()



