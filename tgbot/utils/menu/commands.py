from aiogram import Bot
from aiogram.types import BotCommand


async def register_my_commands(bot: Bot):
    return await bot.set_my_commands(
        [
            BotCommand(
                command="help",
                description="Help message"
            ),
            BotCommand(
                command="new_table",
                description="Create new game table"
            ),
            BotCommand(
                command="add_card",
                description="Add card to game table"
            ),
            BotCommand(
                command="del_card",
                description="Delete card from game table"
            )
        ]
    )
