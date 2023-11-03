from aiogram.filters.callback_data import CallbackData


class Card(CallbackData, prefix="card"):
    card: str
    whose: str
