import requests
import datetime
import json
from string import Template
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from PiDashDisplay.models import Feedsource, Feed

# Create your views here.
def home(request):

    # Grab the weather
    return render(request, 'PiDashDisplay/home.html')


def getWeather(request):
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

    # Truncate the Day and Night in brackets after the weather string, we don't really care about Day and Night
    if forecastValue.find(" (") > 0:
        forecastValue = forecastValue[0:forecastValue.find(" (")]

    return HttpResponse(forecastValue)

def getTemperature(request):
    import requests
    from string import Template
    import datetime

    api_url = 'https://api.data.gov.sg/v1/environment/air-temperature'
    query_key = 'date_time'

    area_name = 'Scotts Road'

    # Set the time to query for 3 minutes before
    history_time = datetime.datetime.now() - datetime.timedelta(minutes=10)
    history_time_string = history_time.strftime('%Y-%m-%dT%H:%M:00')

    url_to_send = Template('$apiurl?$querykey=$timestring')

    url_to_send = url_to_send.substitute(apiurl=api_url, querykey=query_key, timestring=history_time_string)

    # Send the entire request string to the API
    print(url_to_send)
    req = requests.get(url_to_send)

    # req will hold the entire JSON response
    jsonResponse = req.json()
    stationsArray = jsonResponse['metadata']['stations']

    # Look for Scotts Road device_id
    device_ID = '';

    for currentStation in stationsArray:
        if currentStation['name'] == area_name:
            device_ID = currentStation['device_id']
            break

    # Get all the readings for all the stations
    readingsArray = jsonResponse['items'][0]['readings']
    stationTemperatureReading = 0.0

    # print("Looking for Device ID %s" % device_ID)

    for currentReading in readingsArray:
        #   print("Searching Station ID %s" % currentReading['station_id'])
        if currentReading['station_id'] == device_ID:
            stationTemperatureReading = currentReading['value']
            break

    return HttpResponse(stationTemperatureReading)

@csrf_exempt
def feederendpoint(request):
    if request.method == "POST":
        postString = request.body
        jsonArray = json.loads(postString)

        # Parse the source feed first
        sourceFeedUrl = jsonArray.get('status').get('feed')
        print('Source Feed URL ' + sourceFeedUrl)

        # Parse the source feed title
        sourceFeedTitle = jsonArray.get('title')
        print('Source Feed Title ' + sourceFeedTitle)

        # Create the source feed if it does not exist
        countSourceFeed = Feedsource.objects.filter(source=sourceFeedUrl).count()

        fs = Feedsource()

        if countSourceFeed == 0:
            # Create the source
            fs = Feedsource(source=sourceFeedUrl, title=sourceFeedTitle)
            fs.save()

        else:
            # Load the feed source
            fs = Feedsource.objects.filter(source=sourceFeedUrl).first()


        # Loop through the returned items and add them to the feed source
        for currentItem in jsonArray.get('items'):
            itemFeedID = currentItem.get('id')
            itemTitle = currentItem.get('title')
            itemPermaLink = currentItem.get('permalinkUrl')
            itemSummary = currentItem.get('summary')
            itemThumbnail = ''

            if currentItem.get('standardLinks').get('thumbnail') != None:
                itemThumbnail = currentItem.get('standardLinks').get('thumbnail')[0].get('href')

            #print('Feed : ' + itemFeedID)
            #print('Title : ' + itemTitle)
            #print('Link : ' + itemPermaLink)
            #print('Summary : ' + itemSummary)
            #print('Thumbnail : ' + itemThumbnail)


            # Check if the feedid already exist, if don't exist then we write to database
            countFeed = Feed.objects.filter(feedid=itemFeedID).count()

            # Write to db
            if countFeed < 1:
                newEntry = fs.feed_set.create(feedid=itemFeedID, title=itemTitle, summary=itemSummary, destinationurl=itemPermaLink, thumbnail=itemThumbnail)
                print("Inserted " + itemFeedID)

    return HttpResponse('Ok')