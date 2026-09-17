from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def show_tracking_options() -> InlineKeyboardMarkup:
    #TODO: настроить показ клавиатур с фулл треком и без
    tracking_system_options = {
        '📋 МОИ ТРЕКЕРЫ': 'check_trackers',
        '⭐ VIP': 'vip_info',
        '➕ ДОБАВИТЬ': 'add_tracker',
        '➖ УДАЛИТЬ': 'delete_tracker',
        '❓ ПОМОЩЬ': 'tracker_help',
        '⚙️ СМЕНИТЬ РЕЖИМ': 'on_start',
        '🔔ПОДКЛЮЧИТЬ УВЕДОМЛЕНИЯ': 'pair_notifications'
    }
    keyboard = InlineKeyboardBuilder()
    for (button_text, callback) in tracking_system_options.items():
        keyboard.add(InlineKeyboardButton(text=button_text, callback_data=callback))
    keyboard.adjust(2)
    return keyboard.as_markup()