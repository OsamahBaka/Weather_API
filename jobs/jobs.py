from weather.utils import fetch_weather_data
from django_redis import get_redis_connection
import json


def schedule_api():
    """
    This function is responsible for scheduling the API calls to fetch weather data.
    """
    redis_conn = get_redis_connection()
    all_keys = redis_conn.keys('weather:*')

    if not all_keys:
        return

    cities = []
    for key in all_keys:
        city = key.decode('utf-8').split(':')[1]
        cities.append(city)

    for city in cities:
        weather_data = fetch_weather_data(city)

        if weather_data:
            cache_key = f'weather:{city}'
            weather_data_str = json.dumps(weather_data)
            redis_conn.set(cache_key, weather_data_str, ex=3600)
