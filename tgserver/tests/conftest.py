import os

import pytest
from fastapi.testclient import TestClient

# Defaults for local/CI runs before config import.
os.environ.setdefault('TGTOKEN', '123456789:ci-tg-token-for-tests')
os.environ.setdefault('MY_TG_ID', '1')
os.environ.setdefault('REDIS_WORKS', 'false')
os.environ.setdefault('REDIS_HOST', 'redis')
os.environ.setdefault('REDIS_PORT', '6379')
os.environ.setdefault('REDIS_USER', 'redisuser')
os.environ.setdefault('REDIS_USER_PASSWORD', 'redis-password')
os.environ.setdefault(
    'PROJECT_HOSTS',
    '{"backend":"http://back:8000/","auth_server":"http://authserver:8000/",'
    '"tg_server":"http://botapi:8000/"}',
)
os.environ.setdefault('INTERNAL_SERVICE_TOKEN', 'ci-internal-service-token')
os.environ.setdefault('DEBUG', 'true')

from main import app  # noqa: E402
from utils.service_auth import SERVICE_TOKEN_HEADER


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def service_headers():
    return {SERVICE_TOKEN_HEADER: os.environ['INTERNAL_SERVICE_TOKEN']}


NOTICE_LIST_PAYLOAD = {
    'notice_list': [
        {
            'chat_id': 424242,
            'text': 'Test reminder',
            'user_id': 1,
            'reminder_id': 10,
        }
    ],
    'next_date': '2026-12-25T19:00:00',
}

CREATE_NOTICE_PAYLOAD = {
    'username': 'testuser',
    'title': 'Test notice',
    'date': '2026-12-25T19:00:00',
    'chat_id': 424242,
}

NOTICE_SHIFT_PAYLOAD = {
    'user_id': 1,
    'reminder_id': 10,
    'mode': 'hour',
    'chat_id': 424242,
}
