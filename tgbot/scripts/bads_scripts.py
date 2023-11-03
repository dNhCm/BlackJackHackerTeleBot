
from . import bot
from ..models.blackjack import BlackJackDatabase


async def no_user_table_script(chat_id: int):
    await BlackJackDatabase.insert_user_table(chat_id)
    await bot.send_message(
        chat_id=chat_id,
        text="Oh, I don't remember you.. Can you repeate your message, please?"
    )


async def no_inited_table_scripte(chat_id: int):
    await bot.send_message(
        chat_id=chat_id,
        text="""You don't have any created table yet...
Text me /new_table command to create it!"""
    )
