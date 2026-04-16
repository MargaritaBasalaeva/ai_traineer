import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import bot_token
from handlers import user

logging.basicConfig(level=logging.INFO)
bot = Bot(token=bot_token)
dp = Dispatcher()

async def main():
    dp.include_router(user)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())