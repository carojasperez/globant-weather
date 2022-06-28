from django.contrib import admin

from weather.models import Weather


@admin.register(Weather)
class WeatherAdmin(admin.ModelAdmin):
    list_display = ('id', 'requested_time', 'location_name')
