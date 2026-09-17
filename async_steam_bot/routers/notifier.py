from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

router = Router()

@router.message(Command('start'))
async def start(message: Message):
    await message.answer('Привет, ты подписался на уведомления\\! Они будут ждать тебя здесь\\!', parse_mode='MarkdownV2')