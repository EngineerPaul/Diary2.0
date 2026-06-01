from django.urls import path, include
from django.conf.urls.static import static
from django.http import JsonResponse

from root import settings


def healthcheck(_request):
    return JsonResponse({"status": "ok", "service": "backend"})


urlpatterns = [
    path('health/', healthcheck),
    path('api/', include('main.urls'))
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
