import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import bot_token
from handlers import user
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token=bot_token)
# Диспетчер
dp = Dispatcher()

async def main():
    dp.include_router(user)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())