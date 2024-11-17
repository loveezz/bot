from aiogram import types
from handlers.api_service import post_request
from handlers.keyboards import create_apartment_keyboard , create_domofon_keyboard , create_back_keyboard , create_main_menu_keyboard 
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram import Dispatcher
from handlers.api_service import get_request

async def get_domofons_by_apartment(apartment_id, tenant_id):
    endpoint = f"domo.apartment/{apartment_id}/domofon"
    response = get_request(endpoint, params={"tenant_id": tenant_id})
    return response

async def select_domofon_handler(message: types.Message):
    """
    Обработчик выбора квартиры и получения списка домофонов.
    """
    print(f"[DEBUG] Обработчик вызван для выбора квартиры: {message.text}")
    apartments = message.bot.get("apartments", [])
    tenant_id = message.bot.get("tenant_id")

    # Проверяем, выбрана ли квартира
    selected_apartment_name = message.text.replace("Квартира ", "").strip()
    selected_apartment = next((a for a in apartments if a["name"] == selected_apartment_name), None)

    if not selected_apartment:
        await message.answer("Квартира не найдена. Попробуйте снова.")
        return

    # Получаем список домофонов для выбранной квартиры
    apartment_id = selected_apartment["id"]
    try:
        domofons = await get_domofons_by_apartment(apartment_id, tenant_id)
    except Exception as e:
        print(f"[ERROR] Не удалось получить список домофонов: {e}")
        await message.answer("Произошла ошибка при получении списка домофонов. Попробуйте позже.")
        return

    if not domofons or len(domofons) == 0:
        await message.answer(f"Для квартиры {selected_apartment_name} нет доступных домофонов.")
        return

    # Формируем клавиатуру с домофонами
    keyboard = create_domofon_keyboard(domofons)
    await message.answer("Выберите домофон:", reply_markup=keyboard)
    message.bot["selected_apartment_id"] = apartment_id
    message.bot["domofons"] = domofons
    
# Обработчик для получения снимка с камеры епта сучка
async def get_domofon_image_handler(message: types.Message):
    print(f"Обработчик вызван для: {message.text}")
    apartments = message.bot.get("domofons", [])  # Список квартир
    tenant_id = message.bot.get("tenant_id")
    apartment_name = message.text

    # Проверяем, выбрана ли квартира
    selected_apartment = next((a for a in apartments if a["name"] == apartment_name), None)

    if not selected_apartment:
        await message.answer("Выбранная квартира не найдена. Попробуйте снова.")
        return

    apartment_id = selected_apartment["id"]

    # Получаем список домофонов для квартиры
    domofons = await get_domofons_by_apartment(apartment_id, tenant_id)

    if not domofons or len(domofons) == 0:
        await message.answer("Для этой квартиры нет доступных домофонов.")
        return

    # Используем ID первого домофона
    domofon_id = domofons[0]["id"]

    # Запрос к API для получения снимков
    data = {
        "intercoms_id": [domofon_id],
        "media_type": ["JPEG"]
    }
    response = post_request("domo.domofon/urlsOnType", data, params={"tenant_id": tenant_id})

    if response:
        print("Ответ от API:", response)
        if len(response) == 0:  # Если API вернул пустой список
            await message.answer(f"Для домофона {domofons[0]['name']} нет доступных снимков.")
        else:
            # Обрабатываем первый элемент ответа
            result = response[0]
            image_url = result.get("jpeg", None)
            hls_url = result.get("hls", None)
            rtsp_url = result.get("rtsp", None)

            # Отправляем изображение, если доступно
            if image_url:
                await message.answer_photo(image_url, caption=f"Снимок с домофона {domofons[0]['name']}.")
            else:
                await message.answer("Не удалось получить изображение.", reply_markup=create_back_keyboard)

            # Отправляем потоковые ссылки, если доступны
            if hls_url or rtsp_url:
                streams = []
                if hls_url:
                    streams.append(f"HLS поток: {hls_url}")
                if rtsp_url:
                    streams.append(f"RTSP поток: {rtsp_url}")
                await message.answer("\n".join(streams))
    else:
        print("Ошибка при получении данных от API")
        await message.answer("Ошибка при получении снимка с камеры.", reply_markup=create_back_keyboard)
        

# обработчик
def register_domofon_handler(dp: Dispatcher):
    dp.register_message_handler(
        get_domofon_image_handler,
        lambda message: message.text in [d["name"] for d in message.bot.get("domofons", [])]
    )
    