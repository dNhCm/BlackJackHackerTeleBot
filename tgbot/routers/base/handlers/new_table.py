from typing import Any

from aiogram import Router
from aiogram.filters import Command
from aiogram.handlers import MessageHandler

from tgbot.keyboards.table.inline_add_card_keyboard import inline_keyboard
from tgbot.models.blackjack import BlackJackDatabase


class NewTable(MessageHandler):
    async def handle(self) -> Any:
        await self.bot.send_message(
            chat_id=self.from_user.id,
            text="""
New table was created!
First column with cards names is cards your opponents (cards that in game)
Second column is for adding own cards to count chances (own cards)
Click to any button to add cards or that in game or to your own.
Text will be automatically updated where there are chances!
Also you can use commands to handle. Text /help to see it. Good luck!
"""
        )
        message_response = await self.bot.send_message(
            chat_id=self.from_user.id,
            text="""
Own:
You don't really have own cards!

Cards in game:
No cards in game yet!

Chances:
No info(
""",
            reply_markup=inline_keyboard()
        )
        return await BlackJackDatabase.new_user_table(self.from_user.id, message_response.message_id)


def register(router: Router):
    router.message.register(NewTable, Command("new_table"))
