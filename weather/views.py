from rest_framework import views
from rest_framework.response import Response
from django_redis import get_redis_connection
import json
import requests
from decouple import config
from statistics import mean


class WeatherByCityView(views.APIView):
    def get(self, request, city):
        """
        Get the current weather for a given city.

        Args:
            request (HttpRequest): The incoming request.
            city (str): The name of the city for which to retrieve weather data.

        Returns:
            Response: A JSON response containing the current weather for the specified city.

        Raises:
            ValueError: If the city parameter is not provided.
            HTTPError: If the API request returns an error.
        """
        try:
            cache_key = f'weather:{city}'

            redis_conn = get_redis_connection()

            weather_data = redis_conn.get(cache_key)
            if not weather_data:
                url = f"https://api.weatherapi.com/v1/current.json?q={city}&key={config('API_KEY')}"
                headers = {'accept': 'application/json'}
                response = requests.get(url, headers=headers)

                response.raise_for_status()

                weather_data = json.dumps(response.json())
                redis_conn.set(cache_key, weather_data, ex=3600)

            weather_data = json.loads(weather_data)

            return Response(weather_data)

        except ValueError as ve:
            return Response({"error": str(ve)}, status=400)

        except requests.RequestException as re:
            return Response({"error": "Failed to fetch weather data"}, status=500)

        except Exception as e:
            return Response({"error": str(e)}, status=500)


class WeatherBulkView(views.APIView):
    def post(self, request):
        """
        Endpoint for retrieving the current weather for a list of cities.

        Args:
            request (HttpRequest): The incoming request.

        Returns:
            Response: A JSON response containing the current weather for the specified cities.

        Raises:
            ValueError: If the request body does not contain a list of cities.
            HTTPError: If the API request returns an error.
        """
        try:
            data = request.data
            cities = data.get('cities')

            if not cities:
                raise ValueError("No cities provided in the request")

            weather_data_list = []

            redis_conn = get_redis_connection()

            for city in cities:
                cache_key = f'weather:{city}'

                weather_data = redis_conn.get(cache_key)
                if not weather_data:
                    url = f"https://api.weatherapi.com/v1/current.json?q={city}&key={config('API_KEY')}"
                    headers = {'accept': 'application/json'}
                    response = requests.get(url, headers=headers)

                    response.raise_for_status()

                    weather_data = json.dumps(response.json())
                    redis_conn.set(cache_key, weather_data, ex=3600)

                weather_data = json.loads(weather_data)

                weather_data_list.append(weather_data)

            return Response(weather_data_list)

        except ValueError as ve:
            return Response({"error": str(ve)}, status=400)

        except requests.RequestException as re:
            return Response({"error": "Failed to fetch weather data"}, status=500)

        except Exception as e:
            return Response({"error": str(e)}, status=500)


class WeatherStatisticsView(views.APIView):
    def get(self, request):
        """
        Get aggregated statistics for the weather data.

        Args:
            request (HttpRequest): The incoming request.

        Returns:
            Response: A JSON response containing aggregated statistics for the weather data.

        Raises:
            HTTPError: If there is an issue retrieving weather data from the cache.
        """
        try:
            temperatures = []
            city_names = []

            redis_conn = get_redis_connection()

            cache_keys = redis_conn.keys('weather:*')

            if not cache_keys:
                return Response({"error": "No weather data found"}, status=404)

            for cache_key in cache_keys:
                weather_data = redis_conn.get(cache_key)

                weather_data = json.loads(weather_data)

                temp_celsius = weather_data['current']['temp_c']
                city_name = weather_data['location']['name']

                temperatures.append(temp_celsius)
                city_names.append(city_name)

            average_temp = mean(temperatures)
            max_temp = max(temperatures)
            min_temp = min(temperatures)

            total_cities = len(city_names)

            response_data = {
                "total_cities": total_cities,
                "city_names": city_names,
                "average_temperature": round(average_temp, 2),
                "highest_temperature": max_temp,
                "lowest_temperature": min_temp,
            }

            return Response(response_data)

        except Exception as e:
            return Response({"error": str(e)}, status=500)