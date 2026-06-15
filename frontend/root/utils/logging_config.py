import json
import logging
import os
import sys
from datetime import datetime, timezone
from typing import Any

from utils.request_context import get_request_id


def get_service_name() -> str:
    return os.getenv('SERVICE_NAME', 'frontend')


class JsonFormatter(logging.Formatter):
    """Форматтер для JSON логирования"""

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            'ts': datetime.now(timezone.utc).isoformat(),
            'level': record.levelname,
            'service': get_service_name(),
            'logger': record.name,
            'msg': record.getMessage(),
        }
        request_id = get_request_id()
        if request_id:
            payload['request_id'] = request_id
        if record.exc_info:
            payload['exc_info'] = self.formatException(record.exc_info)
        extra = getattr(record, 'extra_fields', None)
        if isinstance(extra, dict):
            payload.update(extra)
        return json.dumps(payload, ensure_ascii=False)


class PlainFormatter(logging.Formatter):
    """Форматтер для простого логирования"""

    def __init__(self) -> None:
        super().__init__(
            fmt='%(asctime)s %(levelname)s service=%(service)s request_id=%(request_id)s '
                '%(name)s: %(message)s',
            datefmt='%Y-%m-%dT%H:%M:%S',
        )

    def format(self, record: logging.LogRecord) -> str:
        record.service = get_service_name()
        record.request_id = get_request_id() or '-'
        return super().format(record)


def setup_logging(service_name: str | None = None) -> None:
    """Функция для настройки логирования"""

    if service_name:
        os.environ['SERVICE_NAME'] = service_name

    root = logging.getLogger()
    if getattr(root, '_diary_logging_configured', False):
        return

    level_name = os.getenv('LOG_LEVEL', 'INFO').upper()
    level = getattr(logging, level_name, logging.INFO)
    use_json = os.getenv('LOG_FORMAT', 'json').lower() != 'plain'

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter() if use_json else PlainFormatter())

    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(level)
    root._diary_logging_configured = True


def get_logging_config() -> dict[str, Any]:
    """Функция для получения конфигурации логирования в settings.py"""

    setup_logging()
    use_json = os.getenv('LOG_FORMAT', 'json').lower() != 'plain'
    formatter_name = 'json' if use_json else 'plain'
    level = os.getenv('LOG_LEVEL', 'INFO')

    return {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'json': {'()': 'utils.logging_config.JsonFormatter'},
            'plain': {'()': 'utils.logging_config.PlainFormatter'},
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': formatter_name,
            },
        },
        'root': {
            'handlers': ['console'],
            'level': level,
        },
        'loggers': {
            'django': {
                'handlers': ['console'],
                'level': 'INFO',
                'propagate': False,
            },
            'django.request': {
                'handlers': ['console'],
                'level': 'WARNING',
                'propagate': False,
            },
        },
    }
