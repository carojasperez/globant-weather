# Technical test: WeatherAPI

Technical test Globant.

Django project that retrieve data from [Openweather](https://openweathermap.org/api) and format it in a human readable format.

The project serves an API with from the following url:
```
 http://<host>/weather?city=<city>&country=<country>
```

Response:
```json
{
    "requested_time": "2022-06-26 22:00:15",
    "location_name": "Bogota, CO",
    "temperature": "11.82 °C",
    "temperaturef": "53.28 °F",
    "wind": "Light Air, 1.02 m/s, SouthEast",
    "cloudiness": "overcast clouds",
    "pressure": "1017 hpa",
    "humidity": "87 %",
    "sunrise": "10:47:29",
    "sunset": "23:10:42",
    "geo_cordinates": [
        4.6097,
        -74.0817
    ],
    "forecast": { .... }
}
```

***this project uses Redis for managing Cache, the timeout of the cache can be configured in the .env file.***

## Using a different Cache.

It's possible to use a different Cache server.

Example with database cache:

```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'my_cache_table',
    }
}
```
For more information go to [django documentation](https://docs.djangoproject.com/en/4.0/topics/cache/)

## Installation
Use [virtualenv](https://virtualenv.pypa.io/en/latest/) to create a Python virtual enviroment

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install dependencies.

[Redis](https://redis.io/) server is required for memory cache.

Start Redis Server

```bash
$ redis-server 
```



```bash
# Create the virtual enviroment
vitualenv env

# Install the project dependencies
pip install -r requirements.txt

# Make the project Database migrations
python manage.py makemigrations

# Create the models in the database
python manage.py migrate

# Run the Django Development Server
python manage.py runserver

# Optional if DB Storage is enabled
python manage.py createsuperuser

# Admin panel URL
http://localhost:8000/admin
```

## .env file is required. Sample Env file: 

```python
SECRET_KEY='secret-key'
OPEN_WEATHER_KEY='owa-key'
OPEN_WEATHER_URL='http://api.openweathermap.org/data/2.5/'
WEATHER_UNITS='metric'
WEATHER_EXCLUDE='current,minutely,alerts'
REDIS_URL='redis://127.0.0.1:6379/1'
CACHE_TIMEOUT=120
DB_STORAGE=True
```

- **SECRET_KEY**: Django secret key.
- **OPEN_WEATHER_API**: API Key for [Openweathermap](https://openweathermap.org/).
- **OPEN_WEATHER_URL**: URL of the Open weather API.
- **WEATHER_UNITS**: standard, metric, imperial, units (This project assumes the use of metric units).
- **WEATHER_EXCLUDE**: current, minutely, alerts, daily (Could be limited in the free version of Openweathermap)
- **REDIS_URL**: Url to the Redis Server
- **CATHE_TIMEOUT**: Data store time in the cache (2 minutes for this technical test)
- **DB_STORAGE**: Optional: True/False