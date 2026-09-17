from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

def options_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton
        (
        text = '🟢 ЧЕКЕР АККАУНТА',
        callback_data='steamid64_check'
        )
    )
    keyboard.add(InlineKeyboardButton
        (
        text='⚙️ СМЕНИТЬ РЕЖИМ',
        callback_data='on_start'
        )
    )
    return keyboard.as_markup()