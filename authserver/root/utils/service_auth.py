from django.conf import settings

from utils.request_context import merge_request_headers

SERVICE_TOKEN_HEADER = 'X-Service-Token'


def service_auth_headers() -> dict[str, str]:
    headers = merge_request_headers()
    token = settings.INTERNAL_SERVICE_TOKEN
    if token:
        headers[SERVICE_TOKEN_HEADER] = token
    return headers
