from aiogram import types 
from handlers.api_service import get_request
from handlers.keyboards import   create_domofon_keyboard , create_main_menu_keyboard , create_back_keyboard
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram import Dispatcher
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.DEBUG,  # Уровень логирования: DEBUG, INFO, WARNING, ERROR, CRITICAL
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("bot.log", mode="a", encoding="utf-8"),  # Лог-файл
        logging.StreamHandler()  # Вывод в консоль
    ]
)

logger = logging.getLogger(__name__)

# Клавиатура для возвратаВыб
back_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
back_keyboard.add(KeyboardButton('Назад'))

async def select_apartament_handler(message:types.Message):
    print("[DEBUG] Обработчик вызван для выбора квартиры")

    tenant_id =  message.bot.get("tenant_id")
    response = get_request("apartment", params={"tenant_id": tenant_id})

    if not response or len(response) == 0:
        await message.answer("У вас нет квартир. Пожалуйста, свяжитесь с администратором.")
        return
    
    keyboard = create_domofon_keyboard(response)
    await message.answer("ерите квартиру:", reply_markup=keyboard)
    message.bot["apartmets"] = response
    
# Функция для создания клавиатуры с домофонами
def create_domofon_keyboard(domofons):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for zxc in domofons:  # ZXC
        keyboard.add(KeyboardButton(text=f'{zxc["name"]}'))
    return keyboard
async def list_domofon_handlers(message: types.Message):
    """
    Обработчик для получения списка домофонов.
    """
    logger.info(f"[LIST_DOMOFONS] Обработчик вызван. Пользователь: {message.from_user.username}")
    tenant_id = message.bot.get("tenant_id")
    logger.debug(f"[LIST_DOMOFONS] Tenant ID из message.bot: {tenant_id}")

    if not tenant_id:
        logger.error("[LIST_DOMOFONS] Tenant ID отсутствует. Пользователь не авторизован.")
        await message.answer(
            "Вы не авторизованы. Пожалуйста, начните с команды /start",
            reply_markup=create_back_keyboard()
        )
        return

    logger.info(f"[LIST_DOMOFONS] Отправляем запрос к API для tenant_id: {tenant_id}")
    response = get_request("domo.apartment", params={"tenant_id": tenant_id})
    logger.debug(f"[LIST_DOMOFONS] Ответ от API: {response}")

    if response:
        domofons = [{"id": d["id"], "name": d["name"]} for d in response]
        message.bot["domofons"] = domofons
        domofon_keyboard = create_domofon_keyboard(domofons)
        logger.info(f"[LIST_DOMOFONS] Найдено {len(domofons)} домофонов.")
        await message.answer("Выберите домофон:", reply_markup=domofon_keyboard)
    else:
        logger.error("[LIST_DOMOFONS] Ошибка получения данных от API.")
        await message.answer(
            "Ошибка получения списка домофонов. Пожалуйста, попробуйте позже.",
            reply_markup=back_keyboard
        )

def register_apartament_handler(dp: Dispatcher):
    dp.register_message_handler(list_domofon_handlers, text="Показать домофоны")