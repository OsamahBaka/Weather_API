import requests
from decouple import config

def fetch_weather_data(city):
    """
    Fetch weather data for a given city from the weather API.

    Args:
        city (str): The name of the city for which to fetch weather data.

    Returns:
        dict: Weather data for the specified city.
    """
    try:
        url = f"https://api.weatherapi.com/v1/current.json?q={city}&key={config('API_KEY')}"

        headers = {'accept': 'application/json'}

        response = requests.get(url, headers=headers)
        response.raise_for_status() 
        
        weather_data = response.json()

        return weather_data

    except requests.RequestException as e:
        return None

    except Exception as e:
        return None
