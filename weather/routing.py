from django.urls import path
from .consumers import LiveWeatherConsumer, LiveWeatherConsumer_c
ws_urlpatterns = [
    path('weather/live/', LiveWeatherConsumer.as_asgi()),
    path('weather/live-radar/', LiveWeatherConsumer_c.as_asgi()),
]
