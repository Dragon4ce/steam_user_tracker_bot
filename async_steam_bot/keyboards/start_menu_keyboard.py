from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def greeting_menu_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton
        (
        text='🟢STEAM TRACKING🟢',
        callback_data='steam_tracking'
        )
    )
    keyboard.add(InlineKeyboardButton
        (
        text='🟢SteamID64 Info🟢',
        callback_data='steamid_info'
        )
    )
    return keyboard.as_markup()