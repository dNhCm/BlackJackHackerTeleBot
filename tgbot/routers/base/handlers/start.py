
from typing import Any

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.handlers import MessageHandler, MessageHandlerCommandMixin
from aiogram.methods import SendMessage

from tgbot.models.blackjack import BlackJackDatabase


class StartHandler(MessageHandler, MessageHandlerCommandMixin):
    async def handle(self) -> Any:
        isNewUser = await BlackJackDatabase.insert_user_table(self.from_user.id)
        if isNewUser:
            return SendMessage(
                chat_id=self.from_user.id,
                text="""
Hello, I'm bot that will help you with increasing your chances to win in BlackJack game!
Text me /help command to know how bot works!"""
            )
        else:
            return SendMessage(
                chat_id=self.from_user.id,
                text="""
I see you don't know what to do yet. So text me /help command, and you will discover my possibilities!
Or if you know all then create new play table by /new_table command"""
            )


def register(router: Router):
    router.message.register(StartHandler, CommandStart())
