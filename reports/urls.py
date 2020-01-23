from django.urls import include, path
from rest_framework.routers import DefaultRouter

from reports import views


router = DefaultRouter()
router.register(r'', views.ReportsViewSet)

urlpatterns = [
    path('container-unloads/', views.ContanerUnloadsListView.as_view()),
    path('export-report/<int:id>/', views.ExportReportView.as_view()),
    path('', include(router.urls)),
]
