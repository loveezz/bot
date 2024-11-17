 # Точка входа. Здесь будет запускаться бот  и все обработчики
import os
from aiogram import Bot , Dispatcher
from aiogram.utils import executor
from handlers.start import register_handlers_start
from handlers.authorize import register_authorize_handler
from handlers.apartament import register_apartament_handler
from handlers.domofon import register_domofon_handler
from handlers.open import register_open_door_handler
from dotenv import load_dotenv
from handlers.database import Init_Database , get_all_users

load_dotenv()  # Загрузка TOKEN из.env файла


TOKEN = os.getenv("BOT_TOKEN")

if TOKEN is None :
    raise ValueError("BOT_TOKEN is not set in .env file")
else:
    print("Token is set")

qwe = """
            (          
     )      )\ )    )  
  ( /(    )(()/( ( /(  
  )\())( /( /(_)))\()) 
 ((_)\ )\()|_))_((_)\  
 /  (_|(_)\| |_ | |(_) 
| () |\ \ /| __|| / /  
 \__/ /_\_\|_|  |_\_\  
                       
"""
print(qwe)
Init_Database()
users = get_all_users()
print("Список пользователей в БД:")
for zxc in users:
    print(zxc)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

register_handlers_start(dp)
register_authorize_handler(dp)
register_apartament_handler(dp)
register_domofon_handler(dp)
register_open_door_handler(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)