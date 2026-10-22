from aiogram.types import (
    InputRichBlockBlockQuotation,
    InputRichBlockDivider,
    InputRichBlockFooter,
    InputRichBlockMathematicalExpression,
    InputRichBlockParagraph,
    InputRichBlockSectionHeading,
    InputRichBlockDetails,
    InputRichBlockTable,
    InputRichMessage,
    Message,
    RichBlockTableCell,
    RichTextAnchor,
    RichTextAnchorLink,
    RichTextBold,
    RichTextCode,
    RichTextItalic,
    RichTextSpoiler,
    RichTextSuperscript,
    InputRichBlockList,
    InputRichBlockListItem,
    InputRichBlockPullQuotation,
    CallbackQuery,
    CopyTextButton,
    DisabledButton,
    InputRichBlockButtons,
    InputRichBlockParagraph,
    InputRichBlockSectionHeading,
    InputRichMessage,
    Message,
    RichMessageButton,
    RichTextButton,
)
UNKNOWN_COMMAND = 'Извините, но я не понимаю Вас! Воспользуйтесь командами из списка команд в /help'
INVALID_LINK = 'Некорректные данные, перепроверьте введенную ссылку / SteamID64'
ADD_TRACKER_PROMPT = '*Воспользуйтесь предложенными методами отслеживания ниже!*'
DELETE_PROMPT = 'Выберите трекер для удаления:'
HELP_TEXT = """
Доступные команды:
/start - перезапуск бота
"""
NO_TRACKERS = InputRichMessage(blocks=[
    InputRichBlockSectionHeading(text = RichTextBold(text = 'У Вас нет активных трекеров!'), size = 4),
InputRichBlockButtons(buttons = [
            RichMessageButton(
                text='➕ ДОБАВИТЬ ТРЕКЕР',
                style='success',
                callback_data='add_tracker'
            ),
        ], align='center'),
        InputRichBlockButtons(buttons = [
            RichMessageButton(
                text='📋В МЕНЮ',
                style='primary',
                callback_data='steam_tracking'
            ),
            RichMessageButton(
                text='⚙️ СМЕНИТЬ РЕЖИМ',
                style='primary',
                callback_data='on_start',
            ),
        ], align='center'),
])
METHOD_SWAP_MSG = InputRichMessage(blocks = [
    InputRichBlockSectionHeading(text = RichTextBold(text = 'Выберите один из режимов ниже!'), size = 4),
    InputRichBlockButtons(buttons=[
        RichMessageButton(
            text='🟢STEAM TRACKING🟢',
            style='success',
            callback_data='steam_tracking'
        ),
        RichMessageButton(
            text='🟢SteamID64 Info🟢',
            style='success',
            callback_data='steamid_info'
        )
    ], align='center'),
])


TEMPLATE_MESSAGES = {
    'unknown_command': UNKNOWN_COMMAND,
    'no_trackers': NO_TRACKERS,
    'invalid_link': INVALID_LINK,
    'add_tracker_prompt': ADD_TRACKER_PROMPT,
    'delete_prompt': DELETE_PROMPT,
    'help': HELP_TEXT,
    'method_swap_message': METHOD_SWAP_MSG,
    'no_current_trakers': NO_TRACKERS,
}
ONLINE_STATUS = {
        0: "🔴 Оффлайн",
        1: "🟢 Онлайн",
        2: "🔴 Занят",
        3: "🌙 Отошёл",
        4: "💤 Спит",
        5: "🎮 Ищет игру"
    }