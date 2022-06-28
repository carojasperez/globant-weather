

from weather.models import Weather
from django.conf import settings
import time
import requests
from django.core.cache import cache
from datetime import datetime


def weather_from_api(location):
    '''
    Handle the weather Data.
    Forecast Stored as JSON
    '''
    current = requests.get(settings.OPEN_WEATHER_URL + 'weather',
                params={
                    'q': location,
                    'appid': settings.OPEN_WEATHER_KEY,
                    'units': settings.WEATHER_UNITS})

    '''
    Retrieve forecast (Limited by free openweather account)
    recommended forecast/daily in pro version
    '''
    forecast = requests.get(settings.OPEN_WEATHER_URL + 'forecast',
                    params={'q': location,
                            'appid': settings.OPEN_WEATHER_KEY,
                            'units': settings.WEATHER_UNITS,
                            'exclude': settings.WEATHER_EXCLUDE, 
                            'cnt': 5})

    jsonCurrent = current.json()
    jsonForecast = forecast.json()

    if jsonCurrent.get('cod') != 200:
        '''
        Raise exception when OpenWeathermap can't find the queried data
        '''
        raise Exception("not found")

    weather_model = handle_json(jsonCurrent, jsonForecast)

    # DB Storage: Optional
    if settings.DB_STORAGE:
        Weather.objects.create(**weather_model)
        
    # Post DB Storage add human readable text to: temp, pressure, humidity
    weather_model.update({
        'temperature': str(weather_model['temperature']) + ' °C',
        'temperaturef': str(weather_model['temperaturef']) + ' °F',
        'pressure': str(weather_model['pressure']) + ' hpa',
        'humidity': str(weather_model['humidity']) + ' %'
        })
    
    # Save the data in the Cache
    cache.set(location, weather_model)

    return weather_model


def handle_json(jsonCurrent, jsonForecast):
    '''
    Handle the json from Openweathermap
    '''
    windSpeed = jsonCurrent['wind']['speed']
    windDeg = jsonCurrent['wind']['deg']
    windDescrip = beaufort_scale(windSpeed) + ', ' + str(windSpeed)  + ' m/s, ' + wind_direction(windDeg)

    lat = jsonCurrent['coord']['lat']
    lon = jsonCurrent['coord']['lon']

    geoCoordinates = [lat, lon]

    weather = {
        "requested_time": datetime.fromtimestamp(jsonCurrent['dt']).strftime('%Y-%m-%d %H:%M:%S'),
        "location_name": jsonCurrent['name'] + ', ' + jsonCurrent['sys']['country'],
        "temperature": jsonCurrent['main']['temp'],
        "temperaturef": round(jsonCurrent['main']['temp'] * 1.8 + 32, 2),
        "wind": windDescrip,
        "cloudiness":  jsonCurrent['weather'][0]['description'],
        "pressure": jsonCurrent['main']['pressure'],
        "humidity":  jsonCurrent['main']['humidity'],
        "sunrise": time.strftime('%H:%M:%S', time.localtime(jsonCurrent['sys']['sunrise'])),
        "sunset": time.strftime('%H:%M:%S', time.localtime(jsonCurrent['sys']['sunset'])),
        "geo_cordinates": geoCoordinates,
        "forecast": jsonForecast,
    }

    return weather


def beaufort_scale(wind):
    '''
    Uses the Beaufort Scale to show a human readable data about wind intensitivity.
    Scale and texts from: https://en.wikipedia.org/wiki/Beaufort_scale
    '''
    if wind < 1:
        windDesc = 'Calm'
    elif (wind >= 1 and wind <= 3):
        windDesc = 'Light Air'
    elif wind <= 7:
        windDesc = 'Light Breeze'
    elif wind <= 12:
        windDesc = 'Gentle Breeze'
    elif wind <= 18:
        windDesc = 'Moderate Breeze'
    elif wind <= 24:
        windDesc = 'Fresh Breeze'
    elif wind <= 31:
        windDesc = 'Strong Breeze'
    elif wind <= 38:
        windDesc = 'Near Gale'
    elif wind <= 46:
        windDesc = 'Gale'
    elif wind <= 54:
        windDesc = 'Strong Gale'
    elif wind <= 63:
        windDesc = 'Storm'
    elif wind <= 72:
        windDesc = 'Violent Storm'
    else:
        windDesc = 'Hurricane'
    return windDesc


def wind_direction(degree):
    '''
    Convert Wind Degree to a human readable wind direction.
    references: 
        http://snowfence.umn.edu/Components/winddirectionanddegrees.htm
        https://en.wikipedia.org/wiki/Cardinal_direction
    '''
    wdirs = {
        "N": "North",
        "NNE": "North-NorthEast",
        "NE": "NorthEast",
        "ENE": "East-NorthEast",
        "E": "East",
        "ESE": "East-SouthEast",
        "SE": "SouthEast",
        "SSE": "South-SouthEast",
        "S": "South",
        "SSW": "South-SouthWest",
        "SW": "SouthWest",
        "WSW": "West-SouthWest",
        "W": "West",
        "WNW": "West-NorthWest",
        "NW": "NorthWest",
        "NNW": "North-NorthWest",
    }
    calc = int(round(degree/(360. / len(wdirs))))

    return wdirs[list(wdirs.keys())[calc % len(wdirs)]]


def validate_input_data(city, country):
    
    if city is None or country is None:
        return {
               "error": True,
               "message": "Country and City are mandatory",
             }
    if len(country) != 2:
        return {
               "error": True,
               "message": "Country code must have 2 characters",
             }
    if country.isupper():
        return {
               "error": True,
               "message": "Country code must be lowercase",
             }
    else:
        return {"error": False}
