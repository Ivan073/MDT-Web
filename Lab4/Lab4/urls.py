from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', include('HotelSite.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "\"Отель сайт\""
admin.site.site_title = "\"Отель сайт\""
admin.site.index_title = "Админ-панель"