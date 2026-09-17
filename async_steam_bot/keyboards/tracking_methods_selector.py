from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from async_steam_bot.models.schemas import TrackMethod

#TODO: Дописать фуллтрек вилку
async def tracking_methods_selector(is_vip: bool) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    if is_vip:
        methods = TrackMethod.get_vip_methods()
    else:
        methods = TrackMethod.get_free_methods()
    for method in methods:
        keyboard.add(InlineKeyboardButton(text=method.display_name,
                                          callback_data=f'track_{method.name}')
        )
    keyboard.add(InlineKeyboardButton(
        text = '🆙Изменить SteamID',
        callback_data = 'add_tracker'
    ))
    keyboard.add(InlineKeyboardButton(text = '🚫Отменить добавление',
                                      callback_data='cancel_tracker_add'))
    keyboard.adjust(2)
    return keyboard.as_markup()

