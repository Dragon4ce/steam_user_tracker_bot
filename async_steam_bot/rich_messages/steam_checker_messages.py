from aiogram.types import (
    InputRichBlockDivider,
    InputRichBlockDetails,
    RichTextBold,
    RichTextCode,
    InputRichBlockButtons,
    InputRichBlockParagraph,
    InputRichBlockSectionHeading,
    InputRichMessage,
    RichMessageButton,
)

def get_checker_info() -> InputRichMessage:
    answer = InputRichMessage(blocks=[
        InputRichBlockSectionHeading(text = RichTextBold(text = '🎮 STEAM CHECKER'), size = 2),
        InputRichBlockDetails(summary = RichTextBold(text = '🔍 О СИСТЕМЕ'), blocks=[
            InputRichBlockDivider(),
            InputRichBlockParagraph(text = ['🤖 Режим работы:  Парсинг Steam API\n'
                                           '⚡ Скорость ответа: ',
                                            RichTextBold(text = 'до 2 секунд\n'),
                                            '📊 Полная информация об аккаунте'])

        ], is_open=True),
        InputRichBlockDetails(summary = RichTextBold(text='📊 ДОСТУПНЫЕ ДАННЫЕ'), blocks=[
            InputRichBlockDivider(),
            InputRichBlockParagraph(text = [RichTextCode(text = '🟢 online'),
                                            '  — онлайн статус\n',
                                            RichTextCode(text='🎮 game'),
                                            '  — текущая игра\n',
                                            RichTextCode(text='📝 username'),
                                            '  — никнейм\n',
                                            RichTextCode(text='🖼️ avatar'),
                                            '  — аватар\n',
                                            RichTextCode(text='🆔 steamid'),
                                            '  — уникальный идентификатор\n',
                                            RichTextCode(text='📅 created'),
                                            '  — дата регистрации\n',
                                            RichTextCode(text='🔗 profile'),
                                            '  — ссылка на профиль\n'])
        ], is_open=True),
        InputRichBlockDetails(summary = RichTextBold(text ='📋 СПОСОБЫ ВВОДА SteamID'), blocks=[
            InputRichBlockDivider(),
            InputRichBlockParagraph(text = ['🔗 Ссылка на профиль\n',
                                            RichTextCode(text = 'https://steamcommunity.com/id/username/'),
                                            '\n🆔 SteamID64\n',
                                            RichTextCode(text = 'https://steamcommunity.com/profiles/steamid64')])
        ], is_open=True),
        InputRichBlockButtons(buttons = [
            RichMessageButton(
                text='🟢 ЧЕКЕР АККАУНТА',
                style = 'success',
                callback_data='steamid64_check'
            ),
            RichMessageButton(
                text='⚙️ СМЕНИТЬ РЕЖИМ',
                style = 'success',
                callback_data='on_start'
            )
        ], align='center'),
    ])
    return answer