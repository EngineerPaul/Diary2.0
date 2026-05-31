import pytest
from rest_framework import status


@pytest.mark.django_db
def test_get_user_info_requires_service_token(api_client, user_with_details):
    response = api_client.post(
        '/auth/users/user-info',
        {'chat_id': user_with_details.userdetails.chat_id},
        format='json',
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_get_user_info_with_service_token(api_client, user_with_details, service_headers):
    response = api_client.post(
        '/auth/users/user-info',
        {'chat_id': user_with_details.userdetails.chat_id},
        format='json',
        headers=service_headers,
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data['success'] is True
    assert response.data['user_id'] == user_with_details.id
    assert response.data['timezone'] == 'Europe/Moscow'


@pytest.mark.django_db
def test_users_info_by_ids(api_client, user_with_details, service_headers):
    response = api_client.post(
        '/auth/users/info-by-ids',
        {'user_ids': [user_with_details.id]},
        format='json',
        headers=service_headers,
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data['success'] is True
    assert len(response.data['data']) == 1
    assert response.data['data'][0]['user_id'] == user_with_details.id
    assert response.data['data'][0]['chat_id'] == user_with_details.userdetails.chat_id


@pytest.mark.django_db
def test_get_user_info_not_found(api_client, service_headers):
    response = api_client.post(
        '/auth/users/user-info',
        {'chat_id': 999999},
        format='json',
        headers=service_headers,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['success'] is False
