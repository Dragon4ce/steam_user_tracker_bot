from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def to_method_selector_checker(additions = None) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    if additions == 'caption':
        keyboard.add(InlineKeyboardButton(
            text='↩️НА ГЛАВНУЮ',
            callback_data='on_start_caption')
        )
        keyboard.add(InlineKeyboardButton(
            text='📋В МЕНЮ ЧЕКЕРА',
            callback_data='steamid_info_caption')
        )
    else:
        keyboard.add(InlineKeyboardButton(
            text='↩️НА ГЛАВНУЮ',
            callback_data='on_start')
        )
        keyboard.add(InlineKeyboardButton(
            text='📋В МЕНЮ ЧЕКЕРА',
            callback_data='steamid_info')
        )


    return keyboard.as_markup()

#TODO: Доделать вариативные клавиатуры для различных стадий взаимодействия с ботом
def to_method_selector_tracker(additions = None) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    default_adjust = 1
    if additions == 'add_tracker_finish':
        keyboard.add(InlineKeyboardButton(
            text = '📋 МОИ ТРЕКЕРЫ',
            callback_data='check_trackers'
        ))
        default_adjust = 2
    if additions == 'my_trackers_menu':
        keyboard.add(InlineKeyboardButton(
            text='➕ ДОБАВИТЬ',
            callback_data='add_tracker',
        )
        )

        keyboard.add(InlineKeyboardButton(
            text='➖УДАЛИТЬ',
            callback_data='delete_tracker'
        )
        )
        default_adjust = 2
    if additions == 'successful_delete':
        keyboard.add(InlineKeyboardButton(
            text='📋 МОИ ТРЕКЕРЫ',
            callback_data='check_trackers'
        )
        )

        keyboard.add(InlineKeyboardButton(
            text='➖УДАЛИТЬ',
            callback_data='delete_tracker'
        )
        )
        default_adjust = 2
    keyboard.add(InlineKeyboardButton
        (
        text = '↩️В МЕНЮ ТРЕКЕРА',
        callback_data='steam_tracking'
        )
    )
    keyboard.add(InlineKeyboardButton
        (
        text='⚙️ СМЕНИТЬ РЕЖИМ',
        callback_data='on_start'
        )
    )
    keyboard.adjust(default_adjust)
    return keyboard.as_markup()