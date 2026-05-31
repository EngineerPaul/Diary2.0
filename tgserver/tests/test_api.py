from unittest.mock import AsyncMock, patch

from tests.conftest import (
    CREATE_NOTICE_PAYLOAD,
    NOTICE_LIST_PAYLOAD,
    NOTICE_SHIFT_PAYLOAD,
)


def test_set_notice_list_requires_service_token(client):
    response = client.post('/tgapi/set-notice-list/', json=NOTICE_LIST_PAYLOAD)

    assert response.status_code == 403


def test_set_notice_list_with_service_token(client, service_headers):
    response = client.post(
        '/tgapi/set-notice-list/',
        json=NOTICE_LIST_PAYLOAD,
        headers=service_headers,
    )

    assert response.status_code == 200
    assert response.json() == {'success': True}


@patch('api.api.send_create_notice', new_callable=AsyncMock)
def test_create_notice_success(mock_send, client):
    mock_send.return_value = (201, 'created')

    response = client.post('/tgapi/bot/create-notice/', json=CREATE_NOTICE_PAYLOAD)

    assert response.status_code == 201
    assert response.json() == {'success': True}
    mock_send.assert_awaited_once()


@patch('api.api.send_create_notice', new_callable=AsyncMock)
def test_create_notice_backend_error(mock_send, client):
    mock_send.return_value = (400, 'error')

    response = client.post('/tgapi/bot/create-notice/', json=CREATE_NOTICE_PAYLOAD)

    assert response.status_code == 400
    assert response.json() == {'success': False}


@patch('api.api.send_notice_shift', new_callable=AsyncMock)
def test_notice_shift_success(mock_send, client):
    mock_send.return_value = (200, 'ok')

    response = client.post('/tgapi/bot/notice-shift/', json=NOTICE_SHIFT_PAYLOAD)

    assert response.status_code == 200
    assert response.json() == {'success': True}


@patch('api.api.get_userinfo', new_callable=AsyncMock)
def test_dispatch_user_info_success(mock_send, client):
    mock_send.return_value = (200, '{"user_id": 1, "timezone": "UTC"}')

    response = client.post(
        '/tgapi/bot/get-user-info/',
        json={'chat_id': 424242},
    )

    assert response.status_code == 200
    assert response.json()['success'] is True
    assert response.json()['user_info']['timezone'] == 'UTC'


def test_debug_test_django_get(client):
    response = client.get('/tgapi/test-django/')

    assert response.status_code == 200
    assert response.json() == {'detail': 'success'}
