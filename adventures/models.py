import datetime

from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


# Create your models here.
from django.urls import reverse


class AdventureLocation(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    author = models.CharField(max_length=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.FloatField(default=5)
    num_reviews = models.IntegerField(default=0)
    img = models.CharField(max_length=100, default='')
    alt = models.CharField(max_length=100)
    date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('adventures:adventure_location_detail', args=[self.id])

class Review(models.Model):
    adventureLocation = models.ForeignKey(AdventureLocation, on_delete=models.CASCADE)
    author = models.CharField(max_length=30)
    date = models.DateTimeField(default=datetime.now)
    review = models.TextField()
    rating = models.FloatField(default=5)

    def __str__(self):
        return self.author

class AdventureTrip(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    author = models.CharField(max_length=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.now)
    img = models.CharField(max_length=100, default='')
    alt = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('adventures:adventure_location_detail', args=[self.id])
