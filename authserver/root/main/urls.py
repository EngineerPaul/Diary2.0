from django.urls import path

from .views import (
    Registration, VerifyToken, ObtainTokens, Logout, RefreshTokens,
    AuthCheck,
    TGAuthDate, TGAuthCheck, TGAuthDetails, GetInfoByChatId, GetUserInfo,
    TestRequest,
)


urlpatterns = [
    # ======== Auth API ========
    path('registration', Registration.as_view()),
    path('verify', VerifyToken.as_view()),
    path('obtain', ObtainTokens.as_view()),
    path('refresh', RefreshTokens.as_view()),
    path('logout', Logout.as_view()),
    path('auth-check', AuthCheck.as_view()),

    # ======== Telegram API ========
    path('tg-auth/date', TGAuthDate.as_view()),  # Начало активации Tg бота
    path('tg-auth/save', TGAuthDetails.as_view()),  # Завершение активации Tg бота
    path('tg-auth/check', TGAuthCheck.as_view()),  # Получение nickname в front
    path('users/info-by-ids', GetInfoByChatId.as_view()),  # Получение info по списку user_id
    path('users/user-info', GetUserInfo.as_view()),  # Получение user_id и timezone по chat_id

    path('test', TestRequest.as_view()),
]
