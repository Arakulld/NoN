from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class Event(models.Model):
    slug = models.SlugField(max_length=255, unique_for_date='')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              related_name='events_created',
                              on_delete=models.CASCADE)

    title = models.CharField(max_length=32)
    price = models.IntegerField(default=0)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Participant(models.Model):
    event = models.ManyToManyField(Event,
                                   related_name='participants')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='participating_events')
    qr_code = models.ImageField(upload_to='participants/qr_codes/%Y/%m/%d')


class News(models.Model):
    parent_event = models.ForeignKey(Event,
                                     on_delete=models.CASCADE,
                                     related_name='news')

    slug = models.SlugField(max_length=255)
    title = models.CharField(max_length=32)
