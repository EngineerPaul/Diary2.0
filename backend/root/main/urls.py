from django.urls import path

from .views import (
    PublickAPI, SecretAPI,
    RecordContent,
)

urlpatterns = [
    path('publick', PublickAPI.as_view()),
    path('secret', SecretAPI.as_view()),
    path('get-record-content/<int:record_id>/', RecordContent.as_view()),
]
