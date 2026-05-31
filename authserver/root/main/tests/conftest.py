import pytest
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.test import APIClient

from main.models import UserDetails
from utils.service_auth import SERVICE_TOKEN_HEADER


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def service_headers(settings):
    return {SERVICE_TOKEN_HEADER: settings.INTERNAL_SERVICE_TOKEN}


@pytest.fixture
def user_with_details(db):
    user = User.objects.create_user(username='testuser1', password='password1')
    UserDetails.objects.create(
        user_id=user,
        tg_user_id=1001,
        tg_username='test_nick',
        chat_id=424242,
        tg_activation_date=timezone.now(),
        timezone='Europe/Moscow',
    )
    return user
