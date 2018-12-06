from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('getWeather', views.getWeather, name='getWeather'),
    path('getTemp', views.getTemperature, name='getTemp'),
]
