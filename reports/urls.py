from django.urls import include, path
from rest_framework.routers import DefaultRouter

from reports import views


router = DefaultRouter()
router.register(r'reports-set', views.ReportsViewSet)
router.register(r'unloads-set', views.ContanerUnloadsListView)
router.register(r'container-types', views.ContainerTypeListView)

urlpatterns = [
    path('export-report/<int:id>/', views.ExportReportView.as_view()),
    path('make-report/', views.GenerateReportView.as_view()),
    path('', include(router.urls)),
]
