from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware, Dispatcher
from aiogram.dispatcher.flags import get_flag
from aiogram.types import Message
from aiogram.utils.chat_action import ChatActionSender


class ExampleChatAction(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        chat_action = get_flag(data, "chat_action")
        if not chat_action:
            return await handler(event, data)

        async with ChatActionSender(
                bot=event.bot,
                chat_id=event.chat.id,
                action=chat_action
        ):
            return await handler(event, data)


def register(dp: Dispatcher):
    dp.message.middleware.register(ExampleChatAction())
