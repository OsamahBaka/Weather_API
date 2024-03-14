from channels.generic.websocket import AsyncWebsocketConsumer
from .utils import fetch_weather_data
import asyncio
import json

class LiveWeatherConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.cities = set()
        self.scheduler_started = False

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        cities = json.loads(text_data)
        self.cities.update(cities)
        
        if not self.scheduler_started:
            asyncio.create_task(self.start_weather_updates())
            self.scheduler_started = True

    async def start_weather_updates(self):
        while True:
            weather_data = await self.fetch_weather_for_cities()
            await self.send_weather_data(weather_data)
            await asyncio.sleep(60)

    async def fetch_weather_for_cities(self):
        weather_data = {}
        for city in self.cities:
            city_data = fetch_weather_data(city)
            if city_data:
                coordinates = {"lat": city_data.get("location", {}).get(
                    "lat"), "lon": city_data.get("location", {}).get("lon")}
                name = city_data.get("location", {}).get("name")
                temp = city_data.get("current", {}).get("temp_c")
                weather_data[city] = {
                    "Coordinates": coordinates, "Name": name, "Temp": temp}
            else:
                weather_data[city] = {"Error": "Failed to fetch weather data"}
        return weather_data

    async def send_weather_data(self, weather_data):
        await self.send(text_data=json.dumps(weather_data))
