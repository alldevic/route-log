from django.urls import path

from nav_client import views

urlpatterns = [
    path('devices/', views.DeviceListView.as_view()),
]
