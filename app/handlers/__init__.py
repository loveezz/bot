from .start import register_handlers_start
from .authorize import register_authorize_handler
from .apartament import register_apartament_handler
from .domofon import register_domofon_handler
from .open import register_open_door_handler
from .api_service import post_request, get_request
__all__ = [
    "register_handlers_start",
    "register_authorize_handler",
    "register_apartament_handler",
    "register_domofon_handler",
    "register_open_door_handler",
    "post_request",
    "get_request",
    
]
