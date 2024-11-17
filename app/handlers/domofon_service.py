#Файл для получения списка домофонов по ID квартиры . 

from typing import Optional , List , Dict , Any
from handlers.api_service import get_request

def get_domofons_by_apartment(apartment_id:int , tenant_id:int) -> Optional[List[Dict[str, Any]]]:
    """
    Получает список домофонов по ID квартиры.
    :param apartment: ID квартиры
    :param tenant_id: ID пользователя
    :return: Ответ от API
    """
    endpoint = f"domo.apartment/{apartment_id}/domofon"
    response = get_request(endpoint, params={"tenant_id": tenant_id})

    if response:
        print(f"[INFO] Список домофонов для квартиры {apartment_id}: {response} ")
    else:
        print(f"[ERROR] Не удалось получить список домофонов для квартиры {apartment_id}")
        
    return response