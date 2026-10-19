from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from async_steam_bot.models.database import Database
from async_steam_bot.rich_messages.template_messages import TEMPLATE_MESSAGES
from async_steam_bot.rich_messages.menus_messages import get_start_message
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
    answer = get_start_message()
    await message.answer_rich(rich_message=answer)

@router.callback_query(F.data == 'on_start')
async def back_to_start(callback: CallbackQuery):
    answer = TEMPLATE_MESSAGES['method_swap_message']
    await callback.message.edit_text(rich_message=answer)
    await callback.answer()
