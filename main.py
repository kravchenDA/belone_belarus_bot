import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from database import init_db
from handlers import router

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
dp.include_router(router)

async def main():
    init_db()
    await bot.delete_webhook()  # Удаляем вебхук на случай, если был
    print("🚀 Бот BelONE запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
