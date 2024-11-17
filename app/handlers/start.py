# Обработчик команда /start

from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram import Dispatcher

start_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
start_keyboard.add(KeyboardButton('Отправить контакт', request_contact= True))

async def start_handler(message:types.Message):
    await message.answer('Добро пожаловать! Отправьте ваш контакт для авторизации.', reply_markup=start_keyboard)


def register_handlers_start(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands=['start'])