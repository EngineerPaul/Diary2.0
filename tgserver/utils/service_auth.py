from config import INTERNAL_SERVICE_TOKEN
from utils.request_context import merge_request_headers

SERVICE_TOKEN_HEADER = 'X-Service-Token'


def service_auth_headers() -> dict[str, str]:
    """Функция для добавления service_token в запрос"""

    headers = merge_request_headers()
    if INTERNAL_SERVICE_TOKEN:
        headers[SERVICE_TOKEN_HEADER] = INTERNAL_SERVICE_TOKEN
    return headers
