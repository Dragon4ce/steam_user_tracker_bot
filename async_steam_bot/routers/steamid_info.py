from aiogram import Router, F
from aiogram.utils.markdown import hide_link
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from async_steam_bot.states.checker_states import UserCheckerState
from async_steam_bot.keyboards.steamid_info_options import options_keyboard
from async_steam_bot.keyboards.to_method_selector import to_method_selector_checker
from async_steam_bot.utils.links import LinksService
from async_steam_bot.services.steam_api import SteamAPIService
from async_steam_bot.utils.messages import get_steam_profile_info

router = Router()

@router.callback_query(F.data == 'steamid_info')
async def steamid_info(callback: CallbackQuery):
    from async_steam_bot.utils.messages import get_checker_info
    answer = get_checker_info()
    markup = options_keyboard()
    await callback.message.edit_text(answer,
                                  reply_markup=markup,
                                  parse_mode='MarkdownV2')

@router.callback_query(F.data == 'steamid64_check')
async def steamid64_check(
        callback: CallbackQuery,
        state: FSMContext
                          ):
    message = '*Введите ссылку на Steam профиль или SteamID64*'
    await state.set_state(UserCheckerState.steamid)
    await callback.message.edit_text(message,
                                  parse_mode='MarkdownV2')

@router.message(UserCheckerState.steamid)
async def steamid64_check(
        message: Message,
        state: FSMContext
        ):
    steamid_input = message.text.strip()
    steamid_valid_check = await LinksService(steamid_input).check_steamid_message()
    if steamid_valid_check:
        steam_profile_info = await SteamAPIService(int(steamid_valid_check)).get_steam_user_info()
        await state.update_data(steamid=steamid_valid_check)
        answer_info = await get_steam_profile_info(steam_profile_info)
        keyboard = to_method_selector_checker()
        await message.answer(
            f"{hide_link(steam_profile_info.avatar)}"
            f"{answer_info}", parse_mode='HTML', reply_markup=keyboard)
        await state.clear()
    else:
        answer = '*Неверный SteamID\\. Попробуйте еще раз*'
        await message.answer(text=answer,
                             parse_mode='MarkdownV2')

