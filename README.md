# Weather API

## Functionality
The project allows users to monitor weather data for various locations in real-time. Users can view weather information such as temperature, location name, and coordinates.

## Components
- **Django**: The backend framework used for handling HTTP requests and serving the frontend.
- **Django Channels**: An extension to Django for handling WebSocket connections, enabling real-time communication between clients and the server.
- **WebSockets**: Used to establish a bidirectional communication channel between the client's browser and the server, allowing instant updates without the need for continuous HTTP requests.
- **Frontend**: Implemented using HTML, JavaScript, and Leaflet.js for displaying maps.
- **Backend Logic**: Utilizes Python scripts to fetch weather data from an external API or source.

## Features
- **Real-time Updates**: Weather data is updated in real-time and displayed to users as soon as it's available.
- **Interactive Map**: Users can click on the map to select specific coordinates, prompting the server to fetch and display weather data for the selected location.
- **Error Handling**: The project includes error handling mechanisms to gracefully handle exceptions that may occur during data retrieval or WebSocket communication.

## Architecture
- The backend consists of Django views and Django Channels consumers.
- Django views handle HTTP requests for rendering initial pages and serving static assets.
- Django Channels consumers manage WebSocket connections and handle WebSocket events, such as connecting, disconnecting, and receiving messages.
- Frontend components interact with the server via WebSocket connections to fetch and display weather data dynamically.

## External Services
The project likely interacts with external weather APIs or data sources to fetch weather information based on user requests or predefined locations.

## Installation

### Prerequisites

  ```
  pip install pipenv
  ```

### Setting up Redis

1. Pull the Redis Docker image:

    ```
    docker pull redis
    ```

2. Run a Redis container named `my-redis`:

    ```
    docker run --name my-redis -p 6379:6379 -d redis
    ```

### Project Setup

1. Create a virtual environment using Pipenv:

    ```
    pipenv install
    ```

2. Activate the virtual environment:

    ```
    pipenv shell
    ```

3. Run the Django development server:

    ```
    python manage.py runserver
    ```

4. Access the application in your web browser at `http://localhost:8000`.


### Additional Notes

- Ensure the Redis container (`my-redis`) is running to enable caching functionality for improved performance.
- Customize the project settings and frontend as needed to fit your requirements.
- For production deployment, consider configuring a more robust setup with load balancing, database replication, and security measures.
