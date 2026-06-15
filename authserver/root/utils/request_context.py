from contextvars import ContextVar

REQUEST_ID_HEADER = 'X-Request-ID'
request_id_var: ContextVar[str | None] = ContextVar('request_id', default=None)


def get_request_id() -> str | None:
    return request_id_var.get()


def set_request_id(request_id: str | None) -> None:
    request_id_var.set(request_id)


def merge_request_headers(headers: dict[str, str] | None = None) -> dict[str, str]:
    merged = dict(headers or {})
    request_id = get_request_id()
    if request_id:
        merged[REQUEST_ID_HEADER] = request_id
    return merged
