from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class Participant(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='participating_events')
    qr_code = models.ImageField(upload_to='participants/qr_codes/%Y/%m/%d')


class News(models.Model):
    slug = models.SlugField(max_length=255)



class Event(models.Model):
    slug = models.SlugField(max_length=255, unique_for_date='')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              related_name='events_created',
                              on_delete=models.CASCADE)

    participants = models.ManyToManyField(Participant,
                                          related_name='events',
                                          blank=True)

    title = models.TextField
    price = models.IntegerField(default=0)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
