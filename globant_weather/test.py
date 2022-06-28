from django.test import TestCase
from globant_weather.functions import beaufort_scale, validate_input_data, weather_from_api, wind_direction

class TestFunctions(TestCase):
    def test_WeatherAPI(self):
        '''
        Expected response status
        200: City located by the openweathermap API
        204: Openweathermap Can't find the combination of city + country
        400: Bad request when city or country are not supplied
        '''
        response = self.client.get('/weather/?city=Lima&country=pe')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/weather/?city=Lima&country=co')
        self.assertEqual(response.status_code, 204)

        response = self.client.get('/weather/')
        self.assertEqual(response.status_code, 400)

    def test_weather_from_api(self):
        '''
        Validates if raised the controlled exception.
        City not found
        '''
        with self.assertRaises(Exception):
            weather_from_api('eiofnweiofwebof,pe')

    def test_beaufort_scale(self):
        '''
        Tests the expected result with different values
        '''
        assert beaufort_scale(0) == 'Calm'
        assert beaufort_scale(3) == 'Light Air'
        assert beaufort_scale(18) == 'Moderate Breeze'
        assert beaufort_scale(33) == 'Near Gale'
        assert beaufort_scale(40) == 'Gale'
        assert beaufort_scale(52) == 'Strong Gale'
        assert beaufort_scale(63) == 'Storm'
        assert beaufort_scale(72) == 'Violent Storm'
        assert beaufort_scale(999) == 'Hurricane'

    def test_wind_direction(self):
        '''
        Tests the expected result with different values
        '''
        assert wind_direction(0) == "North"
        assert wind_direction(90) == "East"
        assert wind_direction(180) == "South"
        assert wind_direction(320) == "NorthWest"
        assert wind_direction(280) == "West"
    
    def test_validate_input_data(self):
        '''
        test_validate_input data to validate the expected result
        '''
        self.assertTrue(validate_input_data(None, 'pe').get('error'))
        self.assertTrue(validate_input_data(None, None).get('error'))
        self.assertTrue(validate_input_data('Bogota', None).get('error'))
        self.assertTrue(validate_input_data('Bogota', 'colombia').get('error'))
        self.assertTrue(validate_input_data('Bogota', 'CO').get('error'))

        self.assertFalse(validate_input_data('Lima', 'pe').get('error'))
        self.assertFalse(validate_input_data('Bogota', 'co').get('error'))
