from config import INTERNAL_SERVICE_TOKEN

SERVICE_TOKEN_HEADER = 'X-Service-Token'


def service_auth_headers() -> dict[str, str]:
    if not INTERNAL_SERVICE_TOKEN:
        return {}
    return {SERVICE_TOKEN_HEADER: INTERNAL_SERVICE_TOKEN}
