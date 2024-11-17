from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def create_back_keyboard():
    """
    Клавиатура с кнопкой "Назад".
    """
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("Назад"))
    return keyboard


def create_apartment_keyboard(apartments):
    """
    Клавиатура для выбора квартиры.
    :param apartments: Список квартир
    :return: ReplyKeyboardMarkup
    """
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for apartment in apartments:
        keyboard.add(KeyboardButton(text=f"Квартира {apartment['name']}"))
    return keyboard


def create_domofon_keyboard(domofons):
    """
    Клавиатура для выбора домофона.
    :param domofons: Список домофонов
    :return: ReplyKeyboardMarkup
    """
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for domofon in domofons:
        keyboard.add(KeyboardButton(text=f"Домофон {domofon['name']}"))
    return keyboard


def create_main_menu_keyboard():
    """
    Основная клавиатура с командами.
    """
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("Показать домофоны"))
    keyboard.add(KeyboardButton("Открыть дверь"))
    return keyboard