from aiogram.types import (
    InputRichBlockDivider,
    InputRichBlockDetails,
    RichTextBold,
    InputRichBlockPullQuotation,
    InputRichBlockButtons,
    InputRichBlockParagraph,
    InputRichBlockSectionHeading,
    InputRichMessage,
    RichMessageButton,
)

def get_start_message() -> InputRichMessage:
    answer = InputRichMessage(blocks=[
    InputRichBlockPullQuotation(text = RichTextBold(text = 'Доброго времени суток!\n'
                                                           'Тебя приветствует бот для трекинга Steam-профилей.\n'
                                                            'Давай немножно введу тебя в курс дела и расскажу, что я умею')),
    InputRichBlockSectionHeading(text = RichTextBold(text = '📋 ОПИСАНИЕ БОТА'), size=2),
    InputRichBlockDetails(summary = RichTextBold(text = '⚙️ ФУНКЦИОНАЛ БОТА'), blocks = [
        InputRichBlockDivider(),
        InputRichBlockParagraph(text = '🔍 Поиск пользователей Steam\n'
                                       '📊 Отслеживание активности Steam-профилей\n'
                                       '🔔 Уведомления об изменениях\n'
                                       '🖼️ Получение аватарок Steam-профилей\n'
                                       '📁 Информация о профиле Steam')

    ], is_open=True),
    InputRichBlockDetails(summary= RichTextBold(text= '⏱️ ТЕХНИЧЕСКАЯ ИНФОРМАЦИЯ'), blocks = [
        InputRichBlockDivider(),
        InputRichBlockParagraph(text = '🔄 Частота проверки трекеров — 30 секунд\n'
                                       '🌐 Источник данных — SteamAPI\n'
                                       '🆔 Поддерживаемые форматы: SteamID64, Vanity URL, Profile URL\n')
    ], is_open=True),
    InputRichBlockSectionHeading(text = RichTextBold(text = 'Для продолжения выберите режим работы ниже:'), size=6),
    InputRichBlockButtons(buttons = [
        RichMessageButton(
            text = '🟢STEAM TRACKING🟢',
            style = 'success',
            callback_data='steam_tracking'
        ),
        RichMessageButton(
            text= '🟢SteamID64 Info🟢',
            style= 'success',
            callback_data='steamid_info'
        )
    ], align='center'),
    ])
    return answer