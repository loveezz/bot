import requests
from typing import Optional, Dict, Any

DOMO_API_URL = "https://domo-dev.profintel.ru/tg-bot"
API_KEY = "SecretToken"


def send_request(
    method: str,
    endpoint: str,
    headers: Optional[Dict[str, str]] = None,
    params: Optional[Dict[str, Any]] = None,
    data: Optional[Dict[str, Any]] = None,
) -> Optional[Dict[str, Any]]:
    """
    Универсальная функция для отправки запросов к API.
    :param method: HTTP метод (GET, POST и т.д.)
    :param endpoint: Конечная точка API
    :param headers: Заголовки
    :param params: Параметры строки запроса
    :param data: Данные запроса
    :return: Ответ от API в формате JSON
    """
    url = f"{DOMO_API_URL}/{endpoint}"
    if headers is None:
        headers = {
            "x-api-key": API_KEY,
            "Content-Type": "application/json"
        }

    try:
        print(f"--- Запрос {method.upper()} ---")
        print(f"URL: {url}")
        print(f"Headers: {headers}")
        print(f"Query Params: {params}")
        print(f"Body: {data}")

        if method.upper() == "GET":
            response = requests.get(url, headers=headers, params=params)
        elif method.upper() == "POST":
            response = requests.post(url, headers=headers, json=data, params=params)
        else:
            raise ValueError(f"Неподдерживаемый метод HTTP: {method}")

        response.raise_for_status()
        print(f"--- Ответ ---")
        print(f"Статус: {response.status_code}")
        print(f"Тело ответа: {response.text}")
        return response.json()
    except requests.RequestException as e:
        print(f"[ERROR] Ошибка при выполнении {method.upper()}-запроса: {e}")
        return None


def open_door(domofon_id: int, tenant_id: int, door_id: int) -> Optional[Dict[str, Any]]:
    """
    Открывает дверь через домофон.
    :param domofon_id: ID домофона
    :param tenant_id: ID пользователя
    :param door_id: ID двери
    :return: Ответ от API
    """
    return send_request(
        "POST",
        f"domo.domofon/{domofon_id}/open",
        params={"tenant_id": tenant_id},
        data={"door_id": door_id}
    )


def get_request(endpoint: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
    """
    Выполняет GET-запрос.
    :param endpoint: Конечная точка API
    :param params: Параметры строки запроса
    :return: Ответ от API
    """
    return send_request("GET", endpoint, params=params)


def get_domofons_by_apartment(apartment_id: int, tenant_id: int) -> Optional[Dict[str, Any]]:
    """
    Получает список домофонов по ID квартиры.
    :param apartment_id: ID квартиры
    :param tenant_id: ID пользователя
    :return: Ответ от API
    """
    endpoint = f"domo.apartment/{apartment_id}/domofon"
    response = get_request(endpoint, params={"tenant_id": tenant_id})
    return response


def post_request(endpoint: str, data: Dict[str, Any], params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
    """
    Выполняет POST-запрос.
    :param endpoint: Конечная точка API
    :param data: Данные запроса
    :param params: Параметры строки запроса
    :return: Ответ от API
    """
    return send_request("POST", endpoint, params=params, data=data)


def get_doors_by_domofon(domofon_id: int, tenant_id: int) -> Optional[Dict[str, Any]]:
    """
    Получает список дверей домофона.
    :param domofon_id: ID домофона
    :param tenant_id: ID пользователя
    :return: Ответ от API
    """
    return send_request(
        "GET",
        f"domo.domofon/{domofon_id}/doors",
        params={"tenant_id": tenant_id}
    )