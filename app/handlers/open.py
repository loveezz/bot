from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from handlers.api_service import get_doors_by_domofon, open_door
from aiogram import Dispatcher


async def open_door_handler(message: types.Message):
    """
    Обработчик команды /Открыть дверь.
    Формирует список домофонов для выбора.
    """
    print("[DEBUG] Обработчик вызван: /Открыть дверь")
    domofons = message.bot.get("domofons", [])
    tenant_id = message.bot.get("tenant_id")

    # Проверяем, есть ли доступные домофоны
    if not domofons:
        await message.answer("Нет доступных домофонов. Сначала авторизуйтесь.")
        return

    # Создаём клавиатуру с доступными домофонами
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for domofon in domofons:
        keyboard.add(KeyboardButton(text=f"Домофон {domofon['name']}"))

    await message.answer("Выберите домофон для открытия двери:", reply_markup=keyboard)


async def choose_door_handler(message: types.Message):
    """
    Обработчик выбора домофона.
    Формирует список доступных дверей.
    """
    print(f"[DEBUG] Обработчик выбора домофона: {message.text}")
    domofons = message.bot.get("domofons", [])
    tenant_id = message.bot.get("tenant_id")

    # Проверяем, выбран ли домофон
    selected_domofon_name = message.text.replace("Домофон ", "")
    selected_domofon = next((d for d in domofons if d["name"] == selected_domofon_name), None)

    if not selected_domofon:
        await message.answer("Домофон не найден. Попробуйте снова.")
        return

    # Получаем список дверей
    domofon_id = selected_domofon["id"]
    doors = get_doors_by_domofon(domofon_id, tenant_id)
    if not doors or len(doors) == 0:
        await message.answer(f"Для домофона {selected_domofon_name} нет доступных дверей.")
        return

    # Создаём клавиатуру с доступными дверями
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for door in doors:
        keyboard.add(KeyboardButton(text=f"Дверь {door['number']}"))

    await message.answer("Выберите дверь для открытия:", reply_markup=keyboard)
    message.bot["selected_domofon_id"] = domofon_id
    message.bot["doors"] = doors


async def confirm_open_door_handler(message: types.Message):
    """
    Обработчик подтверждения открытия двери.
    Отправляет запрос на открытие выбранной двери.
    """
    print(f"[DEBUG] Подтверждение открытия двери: {message.text}")
    domofon_id = message.bot.get("selected_domofon_id")
    tenant_id = message.bot.get("tenant_id")
    doors = message.bot.get("doors", [])

    # Проверяем, указан ли корректный номер двери
    try:
        door_number = int(message.text.split(" ")[-1])
    except ValueError:
        await message.answer("Введите корректный номер двери.")
        return

    # Проверяем, существует ли указанная дверь
    selected_door = next((d for d in doors if d["number"] == door_number), None)
    if not selected_door:
        await message.answer("Дверь не найдена. Попробуйте снова.")
        return

    # Открываем дверь
    door_id = selected_door["number"]
    response = open_door(domofon_id, tenant_id, door_id)

    if response:
        await message.answer(f"Дверь {door_number} успешно открыта! 🚪")
    else:
        await message.answer(f"Не удалось открыть дверь {door_number}. Попробуйте снова.")


def register_open_door_handler(dp: Dispatcher):
    """
    Регистрация обработчиков для открытия двери.
    """
    dp.register_message_handler(open_door_handler, commands=["Открыть дверь"])
    dp.register_message_handler(
        choose_door_handler, lambda message: message.text.startswith("Домофон")
    )
    dp.register_message_handler(
        confirm_open_door_handler, lambda message: message.text.startswith("Дверь")
    )