from django.urls import path

from nav_client import views

urlpatterns = [
    path('devices/', views.DeviceListView.as_view()),
    path('geozones-nav/', views.GeozoneListView.as_view()),
    path('geozones-mt/', views.NavMtIdListView.as_view()),
]
