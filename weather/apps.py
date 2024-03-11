from django.apps import AppConfig


class WeatherConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'weather'

    def ready(self):
        """
        This function is called when the application starts.
        It starts a background task that updates the weather data.
        """
        from jobs import updater
        updater.start()
