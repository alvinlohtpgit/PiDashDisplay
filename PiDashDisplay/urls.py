from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('getWeather', views.getWeather, name='getWeather'),
    path('getTemp', views.getTemperature, name='getTemp'),
    path('feederendpoint', views.feederendpoint, name='feederendpoint'),
    path('newspaneldisplay', views.newspaneldisplay, name='newspaneldisplay'),
    path('testpush', views.testPush, name='testpush'),
]
