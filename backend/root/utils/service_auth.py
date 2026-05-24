from django.conf import settings

SERVICE_TOKEN_HEADER = 'X-Service-Token'


def service_auth_headers() -> dict[str, str]:
    token = settings.INTERNAL_SERVICE_TOKEN
    if not token:
        return {}
    return {SERVICE_TOKEN_HEADER: token}
