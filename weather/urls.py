from django.urls import path
from . import views

urlpatterns = [
    path('bulk/', views.WeatherBulkView.as_view(), name='weather_bulk'),
    path('statistics/', views.WeatherStatisticsView.as_view(), name='weather_statistics'),
    path('<str:city>/', views.WeatherByCityView.as_view(), name='weather_by_city'),
]
