from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class Event(models.Model):
    slug = models.SlugField(max_length=255, unique_for_date='')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              related_name='events_created',
                              on_delete=models.CASCADE)

    title = models.CharField(max_length=32, blank=True)
    price = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    start_time = models.DateTimeField(blank=True)
    end_time = models.DateTimeField(blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title


class Participant(models.Model):
    event = models.ForeignKey(Event,
                              related_name='participants',
                              on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='participating_events',
                             on_delete=models.CASCADE,)
    attended = models.BooleanField(default=False)
    qr_code = models.ImageField(upload_to='participants/qr_codes/%Y/%m/%d')

    def __str__(self):
        return str(self.event)


class News(models.Model):
    event = models.ForeignKey(Event,
                              on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               null=True)

    slug = models.SlugField(max_length=255)
    title = models.CharField(max_length=32, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ('-pk',)

    def __str__(self):
        return self.title + str(self.event)
