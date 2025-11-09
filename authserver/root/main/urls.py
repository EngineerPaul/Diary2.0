from django.urls import path

from .views import (
    Registration, VerifyToken, ObtainTokens, Logout, RefreshTokens,
    TestRequest, AuthCheck
)


urlpatterns = [
    path('registration', Registration.as_view()),
    path('verify', VerifyToken.as_view()),
    path('obtain', ObtainTokens.as_view()),
    path('refresh', RefreshTokens.as_view()),
    path('logout', Logout.as_view()),
    path('auth-check', AuthCheck.as_view()),

    path('test', TestRequest.as_view()),
]
