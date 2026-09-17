from async_steam_bot.models.database import Database
from async_steam_bot.services.steam_api import SteamAPIService
from async_steam_bot.business_logic.telegram_tracker_notifier import send_notification_to_all_watchers
import asyncio

'''Логика работы трекера (периодическое обновление данных об отслеживаемых трекерах)'''

async def update_single_user(steam_id: int):
    database = Database()
    old_data = await database.get_info_about_tracker(steam_id=steam_id)
    new_data = await SteamAPIService(steam_id=steam_id).get_steam_user_info()
    if old_data == new_data:
        return None
    await database.update_tracker_info(steam_user=new_data)
    changes = []
    old_data_dict = await old_data.to_dict()
    new_data_dict = await new_data.to_dict()
    for param in ['online', 'username', 'game', 'avatar', 'profileurl']:
        if old_data_dict[param] != new_data_dict[param]:
            changes.append((param, old_data_dict[param], new_data_dict[param]))
    return changes

async def database_cleanup():
    database = Database()
    steam_ids = await database.get_steamid_from_all_trackers_info()
    for steam_id in steam_ids:
        steam_id_watchers = await database.get_steamid_watchers(steam_id=steam_id)
        if not steam_id_watchers:
            await database.delete_tracker_info_from_db(steam_id=steam_id)
    return

async def update_all_trackers(bot):
    database = Database()
    steam_ids = await database.get_steamid_from_all_trackers()
    if not steam_ids:
        print('Ну короче бд пустая сидим втыкаем')
        return
    for steam_id in steam_ids:
        changes = await update_single_user(steam_id=steam_id)
        if changes:
            await send_notification_to_all_watchers(
                                                    steam_id = steam_id,
                                                    changes = changes,
                                                    bot = bot,
                                                    )

async def tracking_system_cycle(bot):
    print('Система трекинга инициализирована')
    while True:
        await database_cleanup()
        await update_all_trackers(bot)
        await asyncio.sleep(30)