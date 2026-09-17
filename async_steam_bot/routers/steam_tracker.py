from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from async_steam_bot.utils.messages import get_tracking_info
from async_steam_bot.keyboards.show_tracking_options import show_tracking_options
from aiogram.fsm.context import FSMContext
from async_steam_bot.states.tracker_states import UserTrackerState
from async_steam_bot.keyboards.tracking_methods_selector import tracking_methods_selector
from async_steam_bot.keyboards.to_method_selector import to_method_selector_tracker
from async_steam_bot.utils.links import LinksService
from async_steam_bot.models.database import Database
from async_steam_bot.models.schemas import Tracker, TrackMethod
from async_steam_bot.services.steam_api import SteamAPIService
from async_steam_bot.keyboards.delete_trackers_list import delete_trackers_list
from async_steam_bot.utils.validators import Validator
from async_steam_bot.business_logic.bot_logic import delete_message_after_delay
from async_steam_bot.keyboards.add_trackers_error import add_tracking_errors_keyboard
import asyncio
router = Router()

@router.callback_query(F.data == 'steam_tracking')

async def show_tracking_menu(callback: CallbackQuery):
    keyboard = show_tracking_options()
    database = Database()
    user_stats = await database.get_user_stats_from_db(callback.from_user.id)
    answer = await get_tracking_info(stats=user_stats, username=callback.from_user.username)
    #TODO: добавить нормальный парсер для MarkdownV2
    await callback.message.edit_text(text=answer, reply_markup=keyboard, parse_mode='MarkdownV2')
    await callback.answer()

@router.callback_query(F.data == 'add_tracker')

async def add_tracker_link_input(callback: CallbackQuery,
                      state: FSMContext,):
    database = Database()
    trackers_limit_check = (await database.get_user_stats_from_db(callback.from_user.id)).can_add_tracks()
    if not trackers_limit_check:
        answer = '**Вы не можете добавлять трекеров больше, чем позволяет Ваш лимит\\!**'
        await callback.message.answer(text=answer,
                                      parse_mode='MarkdownV2',)
        return
    answer = '**Введите ссылку на Steam профиль**'
    await state.set_state(UserTrackerState.steam_link)
    await callback.message.edit_text(text=answer, parse_mode='MarkdownV2')
    await callback.answer()

@router.message(UserTrackerState.steam_link)
async def track_type_selector(message: Message,
                                       state: FSMContext,):
    database = Database()
    steam_id_input = await LinksService(message.text).check_steamid_message()
    if not steam_id_input:
        input_error_msg = "❌ **Неверный SteamID\\. Введите SteamID снова или отмените действие\\!**"
        error_keyboard = add_tracking_errors_keyboard()
        await message.answer(text = input_error_msg,
                             reply_markup=error_keyboard,
                             parse_mode = 'MarkdownV2')
        return
    steam_user = await SteamAPIService(steam_id=int(steam_id_input)).get_steam_user_info()
    if not steam_user:
        error_keyboard = add_tracking_errors_keyboard()
        error_message = f'_Ошибка обращения к API\\! Проверьте корректность введенного SteamID или отмените действие\\!_'
        await message.answer(text = error_message,
            reply_markup=error_keyboard,
            parse_mode='MarkdownV2')
        return
    await state.update_data(steamid_input=steam_user)
    answer = '**Выберите трек\\-метод из предложенных ниже\\!**'
    vip_status = await database.check_user_vip(user_id=message.from_user.id)
    keyboard = await tracking_methods_selector(is_vip=vip_status)
    await message.answer(text=answer, parse_mode='MarkdownV2', reply_markup=keyboard)
    await state.set_state(UserTrackerState.track_type)


@router.callback_query(UserTrackerState.track_type, F.data.startswith('track_'))

async def add_track_type_selector(callback: CallbackQuery, state: FSMContext):
    track_type = callback.data.split('_')[1]
    data = await state.get_data()
    steam_user = data['steamid_input']
    steam_id = steam_user.steam_id
    tracker = Tracker(user_id=callback.from_user.id, track_type=track_type, steam_id=steam_id)
    database = Database()
    has_duplicate = await database.check_duplicate_tracker(tracker)
    if  has_duplicate:
        message = await callback.message.answer(f'_У Вас уже есть данный трекер\\! Выберите другой трек\\-метод из списка или измените SteamID_', parse_mode='MarkdownV2')
        asyncio.create_task(delete_message_after_delay(message, 10))
        return
    keyboard = to_method_selector_tracker(additions='add_tracker_finish')
    await database.add_tracker_info_to_db(steam_user)
    await database.add_tracker_to_db(tracker)
    await database.add_to_user_stats_trackers_count(user_id=callback.from_user.id)
    nickname = await Validator().escape_markdown(await database.get_tracker_username_from_db(steam_id=steam_id))
    answer = f"✅ Трекер **{track_type}** для профиля [{nickname}](https://steamcommunity.com/profiles/{steam_id}) добавлен\\!"
    await callback.message.edit_text(text = answer,
                                  reply_markup=keyboard,
                                  disable_web_page_preview=True,
                                  parse_mode='MarkdownV2')
    await state.clear()
    await callback.answer()

@router.callback_query(F.data == 'cancel_tracker_add')

async def cancel_tracking_add(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await show_tracking_menu(callback=callback)
    await callback.answer()

@router.callback_query(F.data == 'cancel_tracker_delete')

async def cancel_tracking_delete(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await show_tracking_menu(callback=callback)
    await callback.answer()

@router.callback_query(F.data == 'check_trackers')

async def check_user_trackers(callback: CallbackQuery):
    database = Database()
    answer = '*✅АКТИВНЫЕ ТРЕКЕРЫ:*\n\n' #[Tracker(user_id=680702513, steam_id=76561198895393980, track_type='online')]
    current_user_trackers = await database.get_user_trackers_from_db(callback.from_user.id)
    keyboard = to_method_selector_tracker(additions='my_trackers_menu')
    if not current_user_trackers:
        no_trackers_text = '**У Вас нет активных трекеров\\!**'
        await callback.message.edit_text(text = no_trackers_text,
                                      reply_markup=keyboard,
                                      parse_mode='MarkdownV2')
        return
    for number, tracker in enumerate(current_user_trackers, 1):
        nickname = await Validator().escape_markdown(await database.get_tracker_username_from_db(tracker.steam_id))
        display_name_track_type = TrackMethod.get_method_display_name(name=tracker.track_type)
        answer += (f'{number}\\. *[{nickname}](https://steamcommunity.com/profiles/{tracker.steam_id})* — '
                   f'*{display_name_track_type}*\n')
    await callback.message.edit_text(text=answer,
                                  reply_markup=keyboard,
                                  parse_mode='MarkdownV2',
                                  disable_web_page_preview=True)
    #TODO: переделать сообщение (сделать более красивым и читаемым)
    await callback.answer()

@router.callback_query(F.data == 'delete_tracker')
async def remove_user_tracker(callback: CallbackQuery):
    database = Database()
    keyboard = to_method_selector_tracker()
    current_user_trackers = await database.get_user_trackers_from_db(callback.from_user.id)
    if not current_user_trackers:
        no_trackers_text = '**Зачем удалять то, что нельзя удалить\\? : \\)**'
        await callback.message.edit_text(text = no_trackers_text,
                                      reply_markup=keyboard,
                                      parse_mode='MarkdownV2')
        return
    keyboard = await delete_trackers_list(user_id=callback.from_user.id)
    answer = '**Выберите трекер для удаления ниже:**'
    await callback.message.edit_text(text=answer,
                                  reply_markup=keyboard,
                                  parse_mode='MarkdownV2'
                                  )
    await callback.answer()

@router.callback_query(F.data.startswith('remove_tracker')) #remove_tracker_userid_steamid_tracktype

async def remove_user_tracker(callback: CallbackQuery):
    database = Database()
    callback_data = callback.data.split('_')
    user_id = int(callback_data[-3])
    steam_id = int(callback_data[-2])
    track_type = callback_data[-1]
    tracker = Tracker(user_id=user_id, track_type=track_type, steam_id=steam_id)
    deleted_tracker_check = await database.check_deleted_tracker(tracker=tracker)
    keyboard = to_method_selector_tracker(additions='successful_delete')
    if not deleted_tracker_check:
        answer = 'Произошла ошибка удаления: данный трекер уже был удален\\. Попробуйте обновить меню удаления\\!'
        await callback.message.edit_text(text=answer,
                                         parse_mode='MarkdownV2',
                                         reply_markup=keyboard,)
        return
    await database.remove_tracker_from_db(tracker=tracker)
    await database.delete_from_user_stats_trackers_count(user_id=callback.from_user.id)
    answer = f'**Выбранный трекер успешно удален\\!**'

    await callback.message.edit_text(text=answer,
                                  reply_markup=keyboard,
                                  parse_mode='MarkdownV2')
    await callback.answer()

@router.callback_query(F.data == 'tracker_help')

async def tracker_help(callback: CallbackQuery):
    answer = 'Воспользуйтесь нашим руководством —\\> [ТЫК](https://teletype.in/@drxgxnace/NF8kji4TjM4)'
    keyboard = to_method_selector_tracker()
    await callback.message.edit_text(text=answer,
                                  reply_markup=keyboard,
                                  parse_mode='MarkdownV2')
    await callback.answer()
@router.callback_query(F.data == 'vip_info')

async def vip_info(callback: CallbackQuery):
    answer = "⭐ VIP информация временно недоступна"
    keyboard = to_method_selector_tracker()
    await callback.message.edit_text(text=answer,
                                  reply_markup=keyboard,
                                  parse_mode='MarkdownV2')
    await callback.answer()
@router.callback_query(F.data == 'pair_notifications')

async def subscribe_notifications(callback: CallbackQuery):
    message = "Подпишитесь на уведомления, перейдя по [ссылке](https://t.me/tracking_notifies_bot)"
    keyboard = to_method_selector_tracker()
    await callback.message.edit_text(text = message,
                                  parse_mode='MarkdownV2',
                                  reply_markup=keyboard)
    await callback.answer()