from django.urls import path
from .consumers import LiveWeatherConsumer
ws_urlpatterns = [
    path('weather/live/', LiveWeatherConsumer.as_asgi())
]
