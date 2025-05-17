import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import logging
from handlers import router
import config
from aiogram.types import KeyboardButtonPollType
import kb


async def main():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
    )
    logger = logging.getLogger(__name__)
    dp = Dispatcher()
    bot = Bot(token=config.BOT_TOKEN)
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    KeyboardButtonPollType = kb.main
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')
