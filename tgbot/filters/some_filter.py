from aiogram.types import Message
from aiogram.filters import BaseFilter


class TestFilter(BaseFilter):
    def __init__(self, my_text: str):
        self.my_text = my_text

    async def __call__(self, message: Message, **kwargs) -> bool:
        return message.text == self.my_text
