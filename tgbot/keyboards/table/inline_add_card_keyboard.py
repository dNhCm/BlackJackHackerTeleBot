from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from tgbot.utils.callback_datas.cards import Card


def inline_keyboard() -> InlineKeyboardMarkup:
    """
    Creating of the Inline Keyboard works in 3 stages:
    1. Initialization InlineKeyboardBuilder
    2. Make buttons with button() method; Use CallBackData subclass for better data experience (U can create one in tgbot.utils.callback_datas)
    3. Resize your keyboard by adjust() method; every argument is count of buttons in line

    :keyboard: variable with InlineKeyboardBuilder
    :return: Markup of the created InlineKeyboard
    """

    keyboard = InlineKeyboardBuilder()

    for card in ["A", "2", "J", "3", "Q", "4", "K", "5", "6", "7", "8", "9", "10"]:
        for whose in ["in_game", "own"]:
            keyboard.button(
                text=card,
                callback_data=Card(
                    card=card,
                    whose=whose
                )
            )

    keyboard.adjust(2)
    return keyboard.as_markup()
