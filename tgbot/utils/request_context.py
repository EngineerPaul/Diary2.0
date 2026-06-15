from contextvars import ContextVar

REQUEST_ID_HEADER = 'X-Request-ID'
request_id_var: ContextVar[str | None] = ContextVar('request_id', default=None)


def get_request_id() -> str | None:
    """Функция для получения request_id из контекста"""

    return request_id_var.get()


def set_request_id(request_id: str | None) -> None:
    """Функция для установки request_id в контекст"""

    request_id_var.set(request_id)


def merge_request_headers(headers: dict[str, str] | None = None) -> dict[str, str]:
    """Функция для слияния заголовков запроса"""

    merged = dict(headers or {})
    request_id = get_request_id()
    if request_id:
        merged[REQUEST_ID_HEADER] = request_id
    return merged
