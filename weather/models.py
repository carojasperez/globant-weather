from django.db import models


class Weather(models.Model):
    requested_time = models.DateTimeField(auto_now_add=True)
    location_name = models.CharField(max_length=200)
    temperature = models.FloatField()
    temperaturef = models.FloatField()
    wind = models.CharField(max_length=200)
    cloudiness = models.CharField(max_length=200)
    pressure = models.FloatField()
    humidity = models.FloatField()
    sunrise = models.TimeField()
    sunset = models.TimeField()
    geo_cordinates = models.CharField(max_length=200)
    forecast = models.JSONField()
