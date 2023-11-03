from typing import Any

from aiogram import Router
from aiogram.filters import Command

from blackjack.blackjack import BlackJack
from tgbot.keyboards.table.inline_add_card_keyboard import inline_keyboard
from tgbot.misc.handlers.custom_callback_query_handler import CustomCallbackQueryHandler
from tgbot.misc.handlers.custom_message_handler import CustomMessageHandler
from tgbot.models.blackjack import BlackJackDatabase
from tgbot.utils.callback_datas.cards import Card
from tgbot.scripts.bads_scripts import no_user_table_script, no_inited_table_scripte


class AddCardCallbackQuery(CustomCallbackQueryHandler):
    async def handle(self) -> Any:
        data: Card = self.callback_data
        if data.whose == "own":
            await BlackJackDatabase.add_cards(user_id=self.from_user.id, cards=data.card)
        elif data.whose == "in_game":
            await BlackJackDatabase.add_cards(user_id=self.from_user.id, cards_in_game=data.card)

        table_data: dict = await BlackJackDatabase.get_user_table_data(user_id=self.from_user.id)
        if table_data:
            new_text = BlackJack.chances(cards_in_game=table_data["cards_in_game"], cards=table_data["cards"])
            await self.bot.edit_message_text(
                text=new_text,
                chat_id=self.from_user.id,
                message_id=table_data["table_message_id"],
                reply_markup=inline_keyboard()
            )
        else:
            await self.bot.send_message(chat_id=self.from_user.id, text="""
You don't have any table. Try create it by /new_table
If you can't, then please restart me. And write /start command again!
""")
        return self.update.callback_query.answer()


class AddCardCommand(CustomMessageHandler):
    async def handle(self) -> bool:
        args = self.update.message.text[len("add_card")+2:].split(' ')
        if len(args) >= 2:
            if not args[0] in ["own", "in_game"]:
                await self.update.message.answer("You don't choose where you want add card! (own or in_game)")
                return False
        else:
            await self.update.message.answer("/add_card <string (own or in_game)> <string (cards: 2, 3, 7, J, A ...)>")
            return False

        isOK = False
        if args[0] == "own":
            isOK = await BlackJackDatabase.add_cards(user_id=self.from_user.id, cards=" ".join(args[1:]))
        elif args[0] == "in_game":
            isOK = await BlackJackDatabase.add_cards(user_id=self.from_user.id, cards_in_game=" ".join(args[1:]))

        if not isOK:
            await no_user_table_script(self.from_user.id)
            return False

        table_data: dict = await BlackJackDatabase.get_user_table_data(user_id=self.from_user.id)
        if table_data:
            if table_data["table_message_id"] == 0:
                await no_inited_table_scripte(self.from_user.id)
            else:
                await self.update.message.reply(f"{', '.join(args[1:])} cards was successfully added!")
                await self.bot.edit_message_text(
                    text=BlackJack.chances(
                        cards_in_game=table_data["cards_in_game"],
                        cards=table_data["cards"]
                    ),
                    chat_id=self.from_user.id,
                    message_id=table_data["table_message_id"],
                    reply_markup=inline_keyboard()
                )
        else:
            await no_user_table_script(self.from_user.id)

        return True


class DelCardCommand(CustomMessageHandler):
    async def handle(self) -> bool:
        args = self.update.message.text[len("del_card")+2:].split(' ')

        if len(args) >= 2:
            if not args[0] in ["own", "in_game"]:
                await self.update.message.answer("You don't choose where you want add card! (own or in_game)")
                return False
        else:
            await self.update.message.answer("/add_card <string (own or in_game)> <string (cards: 2, 3, 7, J, A ...)>")
            return False

        deleted_cards: list[str] = []
        if args[0] == "own":
            deleted_cards = await BlackJackDatabase.del_cards(user_id=self.from_user.id, cards=" ".join(args[1:]))
        elif args[0] == "in_game":
            deleted_cards = await BlackJackDatabase.del_cards(user_id=self.from_user.id, cards_in_game=" ".join(args[1:]))

        if type(deleted_cards) is not list:
            await no_user_table_script(self.from_user.id)

        if deleted_cards:
            await self.update.message.reply(f"{', '.join(deleted_cards)} cards was successfully deleted!")
            table_data: dict = await BlackJackDatabase.get_user_table_data(user_id=self.from_user.id)
            if table_data:
                await self.bot.edit_message_text(
                    text=BlackJack.chances(
                        cards_in_game=table_data["cards_in_game"],
                        cards=table_data["cards"]
                    ),
                    chat_id=self.from_user.id,
                    message_id=table_data["table_message_id"],
                    reply_markup=inline_keyboard()
                )
            else:
                await no_user_table_script(self.from_user.id)
        else:
            await self.update.message.reply("No card was deleted! Did you may choose not inited ones?")

        return True


def register(router: Router):
    router.callback_query.register(AddCardCallbackQuery, Card.filter())
    router.message.register(AddCardCommand, Command('add_card'))
    router.message.register(DelCardCommand, Command('del_card'))
