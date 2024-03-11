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
        # Construct the API URL
        url = f"https://api.weatherapi.com/v1/current.json?q={city}&key={config('API_KEY')}"

        # Set request headers
        headers = {'accept': 'application/json'}

        # Send GET request to the API
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise exception for non-2xx status codes

        # Parse JSON response
        weather_data = response.json()

        return weather_data

    except requests.RequestException as e:
        # Handle API request errors
        print(f"Error fetching weather data for {city}: {e}")
        return None

    except Exception as e:
        # Handle other exceptions
        print(f"Error: {e}")
        return None
