from django.urls import path

from .views import PublickAPI, SecretAPI

urlpatterns = [
    path('publick', PublickAPI.as_view()),
    path('secret', SecretAPI.as_view()),
]
