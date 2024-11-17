from aiogram import Bot, Dispatcher
from aiogram.utils.executor import start_webhook
import os
from dotenv import load_dotenv
from handlers.start import register_handlers_start
from handlers.authorize import register_authorize_handler
from handlers.apartament import register_apartament_handler
from handlers.domofon import register_domofon_handler
from handlers.open import register_open_door_handler
from handlers.database import Init_Database, get_all_users

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
if TOKEN is None:
    raise ValueError("BOT_TOKEN is not set in .env file")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

WEBHOOK_HOST = "https://29e6-2a00-1fa2-4cd-d876-61f9-e10c-f34c-7d0e.ngrok-free.app"  # Здесь будет публичный URL от ngrok
WEBHOOK_PATH = f"/webhook/{TOKEN}"  # Уникальный путь для безопасности
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = int(os.getenv("PORT", 5000))  # Порт сервера

# Инициализация базы данных
Init_Database()
users = get_all_users()
print("Список пользователей в БД:")
for zxc in users:
    print(zxc)

# Регистрация обработчиков
register_handlers_start(dp)
register_authorize_handler(dp)
register_apartament_handler(dp)
register_domofon_handler(dp)
register_open_door_handler(dp)


async def on_startup(dispatcher):
    print("Установка Webhook...")
    await bot.set_webhook(WEBHOOK_URL)


async def on_shutdown(dispatcher):
    print("Удаление Webhook...")
    await bot.delete_webhook()
    await bot.session.close()


if __name__ == '__main__':
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
