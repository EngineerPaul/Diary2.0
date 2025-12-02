from django.urls import path, include
from django.conf.urls.static import static

from root import settings


urlpatterns = [
    path('api/', include('main.urls'))
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
