from django import views
from rest_framework import views
from rest_framework.response import Response
from django.core.cache import cache
from rest_framework import status
from globant_weather.functions import validate_input_data, weather_from_api


class WeatherAPI(views.APIView):
    '''
    Endpoint to get Weather information.
    Parameters:
        city: String.
        country: (2) Char lowecase.
    Expected request:  weather?city=$City&country=$Country&
    '''
    http_method_names = ['get']

    def get(self,request):
        city = self.request.query_params.get('city', None)
        country = self.request.query_params.get('country', None)

        validation = validate_input_data(city, country)
        
        if validation.get('error'):
            return Response(
                {"message": validation.get('message')},
                status=status.HTTP_400_BAD_REQUEST
            )

        location = city + ',' + country

        if cache.get(location):
            #  Hit Cache
            weather = cache.get(location)
        else:
            #  Hit API
            try:
                weather = weather_from_api(location)
            except:
                return Response(
                {"message": 'We couldn\'t find the required data'},
                status=status.HTTP_204_NO_CONTENT
            )

        return Response(weather)
