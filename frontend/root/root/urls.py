from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse


def healthcheck(_request):
    return JsonResponse({"status": "ok", "service": "frontend"})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', healthcheck),
    path('', include('main.urls'))
]
