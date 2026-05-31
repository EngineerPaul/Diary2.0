from unittest.mock import patch

import pytest
from django.contrib.auth.models import User
from rest_framework import status

from main.models import UserDetails


@pytest.mark.django_db
@patch('main.views.create_root_folders', return_value=True)
def test_registration_success(mock_create_roots, api_client):
    response = api_client.post(
        '/auth/registration',
        {
            'username': 'newuser1',
            'password': 'secret12',
            'timezone': 'Europe/Moscow',
        },
        format='json',
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['username'] == 'newuser1'
    assert response.data['timezone'] == 'Europe/Moscow'
    assert 'access' in response.data
    assert 'refresh' in response.data
    assert User.objects.filter(username='newuser1').exists()
    assert UserDetails.objects.filter(user_id__username='newuser1').exists()
    mock_create_roots.assert_called_once()


@pytest.mark.django_db
def test_registration_duplicate_username(api_client, user_with_details):
    response = api_client.post(
        '/auth/registration',
        {
            'username': user_with_details.username,
            'password': 'secret12',
            'timezone': 'Europe/Moscow',
        },
        format='json',
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data['success'] is False
    assert 'уже существует' in response.data['error']


@pytest.mark.django_db
def test_registration_invalid_username(api_client):
    response = api_client.post(
        '/auth/registration',
        {
            'username': 'bad name',
            'password': 'secret12',
            'timezone': 'Europe/Moscow',
        },
        format='json',
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data['success'] is False


@pytest.mark.django_db
@patch('main.views.create_root_folders', return_value=True)
def test_obtain_and_verify_tokens(mock_create_roots, api_client):
    api_client.post(
        '/auth/registration',
        {
            'username': 'loginuser',
            'password': 'secret12',
            'timezone': 'UTC',
        },
        format='json',
    )

    obtain_response = api_client.post(
        '/auth/obtain',
        {'username': 'loginuser', 'password': 'secret12'},
        format='json',
    )
    assert obtain_response.status_code == status.HTTP_200_OK
    assert obtain_response.data['success'] is True
    assert obtain_response.data['username'] == 'loginuser'
    access_token = obtain_response.cookies['access_token'].value

    verify_response = api_client.post(
        '/auth/verify',
        {'token': access_token},
        format='json',
    )
    assert verify_response.status_code == status.HTTP_200_OK
    assert verify_response.data['is_valid'] is True
    assert verify_response.data['username'] == 'loginuser'


@pytest.mark.django_db
def test_verify_invalid_token(api_client):
    response = api_client.post(
        '/auth/verify',
        {'token': 'not-a-valid-token'},
        format='json',
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['is_valid'] is False
