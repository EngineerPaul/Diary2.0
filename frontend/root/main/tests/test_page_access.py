from unittest.mock import patch

import pytest


PROTECTED_PAGES = [
    '/',
    '/settings',
    '/searching',
    '/notes/1/',
    '/notices/1/',
]

PUBLIC_PAGES = [
    '/login',
    '/registration',
    '/help',
    '/other',
]

AUTH_USER = {
    'id': 1,
    'username': 'testuser',
    'role': 'user-role',
}


@pytest.mark.django_db
@pytest.mark.parametrize('url', PROTECTED_PAGES)
def test_protected_pages_redirect_guest_to_login(client, url):
    response = client.get(url)

    assert response.status_code == 302
    assert response.url == '/login'


@pytest.mark.django_db
@pytest.mark.parametrize('url', PUBLIC_PAGES)
def test_public_pages_available_without_auth(client, url):
    response = client.get(url)

    assert response.status_code == 200


@pytest.mark.django_db
@patch('main.middlewares.AuthMiddleware.verify', return_value=AUTH_USER)
@pytest.mark.parametrize('url', PROTECTED_PAGES)
def test_protected_pages_available_for_authenticated_user(mock_verify, client, url):
    client.cookies['access_token'] = 'valid-access-token'
    response = client.get(url)

    assert response.status_code == 200
    mock_verify.assert_called_once()
