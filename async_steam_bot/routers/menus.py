from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from async_steam_bot.models.database import Database
from async_steam_bot.utils.messages import MESSAGES, get_start_message
from async_steam_bot.keyboards.start_menu_keyboard import greeting_menu_keyboard
import datetime


router = Router()

@router.message(Command('start'))

async def start_message(message: Message):

    """Вызов главного стартового меню при использовании команды /start с выборами режима работы."""

    database = Database()
    await database.start_add_to_db(
        user_id = message.from_user.id, username = message.from_user.username, start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    await database.start_add_to_user_stats(user_id=message.from_user.id,)
    greeting = get_start_message(greeting = MESSAGES['greeting'])
    greet_keyboard = greeting_menu_keyboard()
    await message.answer(greeting, reply_markup=greet_keyboard, parse_mode='MarkdownV2')

@router.callback_query(F.data == 'on_start')
async def back_to_start(callback: CallbackQuery):
    answer = MESSAGES['method_swap_message']
    reply_keyboard = greeting_menu_keyboard()
    await callback.message.edit_text(answer, reply_markup=reply_keyboard, parse_mode='MarkdownV2')

# @router.message(Command('test1'))
#
# async def test(message: Message):
#     await message.answer(text=TEST_MESSAGE1, parse_mode='MarkdownV2')