from aiogram import Router, Bot

from tgbot.data.config import get_config


async def startup(bot: Bot):
    admins = get_config().tgbot.admins
    for admin in admins:
        await bot.send_message(
            chat_id=admin,
            text="Bot was started!"
        )


async def shutdown(bot: Bot):
    admins = get_config().tgbot.admins
    for admin in admins:
        await bot.send_message(
            chat_id=admin,
            text="Bot was stopped!"
        )


def register(router: Router):
    router.startup.register(startup)
    router.shutdown.register(shutdown)
