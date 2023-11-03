import asyncio
from asyncio import CancelledError

from bot import main as tgbot_main
from misc.logger import logger


async def main():
    await asyncio.gather(
        tgbot_main()
    )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit, CancelledError):
        logger.warning('Bot was stopped')
