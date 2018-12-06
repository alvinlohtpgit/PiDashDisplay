import requests
import datetime
from string import Template
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):

    # Grab the weather
    return render(request, 'PiDashDisplay/home.html')


def getTemperature(request):
    api_url = 'https://api.data.gov.sg/v1/environment/2-hour-weather-forecast'
    query_key = 'date_time'

    area_name = 'City'

    # Set the time to query for 3 minutes before
    history_time = datetime.datetime.now() - datetime.timedelta(minutes=3)
    history_time_string = history_time.strftime('%Y-%m-%dT%H:%M:00')

    url_to_send = Template('$apiurl?$querykey=$timestring')

    url_to_send = url_to_send.substitute(apiurl=api_url, querykey=query_key, timestring=history_time_string)

    # Send the entire request string to the API
    req = requests.get(url_to_send)

    # req will hold the entire JSON response
    jsonResponse = req.json()
    areaArray = jsonResponse['area_metadata']  # We do not need this as we already know the area name

    # Grab the forecast list
    forecastArray = jsonResponse["items"][0]["forecasts"]

    forecastValue = ""

    # Loop through the forecast array to match the city which we want to find
    for currentForecast in forecastArray:
        if currentForecast["area"] == area_name:
            forecastValue = currentForecast['forecast']
            break

    return HttpResponse(forecastValue)