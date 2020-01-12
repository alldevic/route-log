from django.contrib import admin
from django.urls import path, include

admin.site.site_header = "Адмнистрирование маршрутного журнала"
admin.site.site_title = "Адмнистрирование маршрутного журнала"
admin.site.index_title = "Маршрутный журнал"


urlpatterns = [
    path('admin/', admin.site.urls),
    path('sb/', include('django_sb_admin.urls')),
]
