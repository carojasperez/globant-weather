from django.urls import path
from rest_framework import routers
from . import views


app_name = "weather"

router = routers.SimpleRouter()

urlpatterns = [

    path('weather/', views.WeatherAPI.as_view())
]

urlpatterns += router.urls
