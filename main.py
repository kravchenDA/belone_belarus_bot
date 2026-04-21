import os 
import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.types import WebhookInfo
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from config import BOT_TOKEN
from database import init_db
from handlers import router

# Настройка логирования
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

# Ваш токен из config.py
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
dp.include_router(router)

# URL вебхука (Render даст вам адрес вида https://ваш-бот.onrender.com)
# Эту переменную нужно добавить в Environment Variables на Render
WEBHOOK_URL = "https://your-app-name.onrender.com"  # <-- ЗАМЕНИТЕ на ваш реальный адрес!
WEBHOOK_PATH = "/webhook"  # Путь, по которому Telegram будет стучаться


async def on_startup() -> None:
    """При запуске бота устанавливаем вебхук"""
    await bot.delete_webhook()  # Сначала удаляем старый (на всякий случай)
    
    # Устанавливаем новый вебхук
    webhook_info = await bot.set_webhook(
        url=f"{WEBHOOK_URL}{WEBHOOK_PATH}",
        allowed_updates=["message", "callback_query"]  # Какие типы обновлений принимать
    )
    
    if webhook_info:
        logging.info(f"✅ Webhook установлен: {WEBHOOK_URL}{WEBHOOK_PATH}")
    else:
        logging.error("❌ Ошибка при установке webhook")


async def on_shutdown() -> None:
    """При остановке бота удаляем вебхук"""
    await bot.delete_webhook()
    await bot.session.close()
    logging.info("🔴 Webhook удалён, бот остановлен")


def main() -> None:
    """Запуск aiohttp сервера с вебхуком"""
    # Инициализируем базу данных
    init_db()
    
    # Создаём aiohttp приложение
    app = web.Application()
    
    # Настраиваем обработчик вебхука
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
    )
    webhook_requests_handler.register(app, path=WEBHOOK_PATH)
    
    # Настраиваем обработчики запуска и остановки
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    
    # Запускаем сервер на порту, который даст Render (обычно 10000)
    # Render автоматически передаёт порт через переменную PORT
    port = int(os.environ.get("PORT", 10000))
    
    logging.info(f"🚀 Запуск веб-сервера на порту {port}")
    web.run_app(app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
