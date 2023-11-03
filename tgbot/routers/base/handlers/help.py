from typing import Any

from aiogram import Router
from aiogram.filters import Command
from aiogram.handlers import MessageHandler, MessageHandlerCommandMixin
from aiogram.methods import SendMessage


class HelpCommand(MessageHandler, MessageHandlerCommandMixin):
    async def handle(self) -> Any:
        return SendMessage(
            chat_id=self.from_user.id,
            text="""
Commands:
/start - Register in bot
/help - Available commands and how to use
/new_table - Creating new game table
/add_card <string: (own or in_game)> <string: (cards: 2, 3, 6, 9, J, A...)> - Add list of card to game table
/del_card <string: (own or in_game)> <string: (cards: 2, 3, 6, 9, J, A...)> - Delete list of card from game table

Handle with Table:
First column with cards names is cards your opponents (cards that in game)
Second column is for adding own cards to count chances (own cards)
Click to any button to add cards or that in game or to your own.
Text will be automatically updated where there are chances!
"""
        )


def register(router: Router):
    router.message.register(HelpCommand, Command("help"))
