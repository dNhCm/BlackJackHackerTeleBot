
from aiogram.types import ReplyKeyboardMarkup, KeyboardButtonPollType
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def reply_keyboard() -> ReplyKeyboardMarkup:
    """
    Creating of the Inline Keyboard works in 4 stages:
    1. Initialization InlineKeyboardBuilder
    2. Make buttons with button() method; You can use request parameters to take some info from sender
    3. Resize your keyboard by adjust() method; every argument is count of buttons in line
    4. Setup markup with resize, changed input_field_placeholder, one_time parameters

    :keyboard: ReplyKeyboardBuilder object
    :return: Markup of keyboard
    """
    keyboard = ReplyKeyboardBuilder()

    keyboard.button(text="Hello")
    keyboard.button(text="How to play?")
    keyboard.button(text="My phone number is...", request_contact=True)
    keyboard.button(text="I'm here...", request_location=True)
    keyboard.button(text="Create poll", request_poll=KeyboardButtonPollType(type="regular"))

    keyboard.adjust(2, 2)

    return keyboard.as_markup(
        resize_keyboard=True,
        input_field_placeholder="Send message from buttons that is bottom",
        one_time_keyboard=True
    )
