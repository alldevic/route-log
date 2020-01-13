from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

admin.site.site_header = "Адмнистрирование маршрутного журнала"
admin.site.site_title = "Адмнистрирование маршрутного журнала"
admin.site.index_title = "Маршрутный журнал"


urlpatterns = [
    path('admin/', admin.site.urls),
    path('sb/', include('django_sb_admin.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('route_log.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
