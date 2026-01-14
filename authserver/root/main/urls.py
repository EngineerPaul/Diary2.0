from django.urls import path

from .views import (
    Registration, VerifyToken, ObtainTokens, Logout, RefreshTokens,
    AuthCheck,
    TGAuthDate, TGAuthDetails, GetChatIds, GetUserId,
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
    path('api/tg-auth/date', TGAuthDate.as_view()),  # Начало активации Tg бота
    path('api/tg-auth/save', TGAuthDetails.as_view()),  # Завершение активации Tg бота
    path('api/users/chat-ids', GetChatIds.as_view()),  # Получение chat_id по списку user_id
    path('api/users/user-id', GetUserId.as_view()),  # Получение user_id по chat_id

    path('test', TestRequest.as_view()),
]
