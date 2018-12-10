from django.db import models
import datetime

# Create your models here.
class Feedsource(models.Model):
    source = models.CharField(max_length=250)
    title = models.CharField(max_length=700)
    datecreated = models.DateTimeField(default=datetime.datetime.now, blank=True)

class Feed(models.Model):
    feedsource = models.ForeignKey(Feedsource, on_delete=models.CASCADE)
    feedid = models.CharField(max_length=700)
    title = models.CharField(max_length=800)
    summary = models.TextField()
    destinationurl = models.CharField(max_length=800)
    thumbnail = models.CharField(max_length=800)
    datecreated = models.DateTimeField(default=datetime.datetime.now, blank=True)
