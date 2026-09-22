import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from async_steam_bot.routers import menus, steamid_info, steam_tracker, notifier
from async_steam_bot.business_logic.tracker_logic import tracking_system_cycle
from async_steam_bot.config import TELEGRAM_MAIN_BOT_TOKEN, TELEGRAM_NOTIFIER_BOT_TOKEN

async def main():
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(message)s")
    """Основная функция для запуска поллинга ботов и включения систем трекинга"""

    main_bot = Bot(token=TELEGRAM_MAIN_BOT_TOKEN,
              defaults=DefaultBotProperties(
                  parse_mode=ParseMode.MARKDOWN_V2
                )
              )
    notifier_bot = Bot(token=TELEGRAM_NOTIFIER_BOT_TOKEN, defaults=DefaultBotProperties(
                  parse_mode=ParseMode.MARKDOWN_V2
                ))
    main_dp = Dispatcher()
    notifier_dp = Dispatcher()

    # Подключаем роутеры к основному боту
    main_dp.include_router(menus.router)
    main_dp.include_router(steamid_info.router)
    main_dp.include_router(steam_tracker.router)
    logging.info('Роутеры подключены')

    notifier_dp.include_router(notifier.router)


    asyncio.create_task(tracking_system_cycle(bot=notifier_bot))
    await main_bot.delete_webhook(drop_pending_updates=True)
    await notifier_bot.delete_webhook(drop_pending_updates=True)
    await asyncio.gather(
        main_dp.start_polling(main_bot),
        # notifier_dp.start_polling(notifier_bot)
    )
    logging.info('Bots polling started')

if __name__ == '__main__':
    asyncio.run(main())
