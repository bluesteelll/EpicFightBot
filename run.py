import asyncio
import logging

from aiogram import Bot, Dispatcher
from config import TOKEN
from core.handlers import router

bot = Bot(token=TOKEN)
dp = Dispatcher()


async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

# Enter point
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
