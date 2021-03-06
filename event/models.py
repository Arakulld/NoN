from django.db import models
from django.shortcuts import reverse
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.text import slugify
from datetime import datetime
import os


class Event(models.Model):
    slug = models.SlugField(max_length=255, unique_for_date='created')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              related_name='events_created',
                              on_delete=models.CASCADE)
    company = models.CharField(max_length=64, blank=True, null=True)

    title = models.CharField(max_length=32, blank=True)
    image = models.ImageField(upload_to='events/images',
                              blank=True)
    price = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    max_participants = models.IntegerField(default=10)
    support_number = models.CharField(blank=True, max_length=13)
    start_time = models.DateTimeField(default=datetime.now())
    end_time = models.DateTimeField(default=datetime.now())
    place = models.CharField(max_length=250, blank=True)
    # longitude = models.CharField(max_length=32, blank=True, null=True)
    # latitude = models.CharField(max_length=32, blank=True, null=True)

    created = models.DateTimeField(default=datetime.now())

    class Meta:
        ordering = ('-created',)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Event, self).save()
        return self

    def get_absolute_url(self):
        return reverse('event_detail', args=[self.slug,
                                             self.created.year,
                                             self.created.month,
                                             self.created.day,
                                             self.created.hour,
                                             self.created.minute,
                                             self.created.second])

    def get_ad_participant_url(self):
        return reverse('add_participant', args=[self.slug,
                                                self.created.year,
                                                self.created.month,
                                                self.created.day,
                                                self.created.hour,
                                                self.created.minute,
                                                self.created.second])

    def __str__(self):
        return self.title


class Participant(models.Model):
    event = models.ForeignKey(Event,
                              related_name='participants',
                              on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='participating_events',
                             on_delete=models.CASCADE, )
    qr_code = models.ImageField(upload_to='participants/qr_codes/',
                                blank=True)

    def __str__(self):
        return str(self.event) + '|' + str(self.user)

    def delete(self, *args, **kwargs):
        if self.qr_code:
            os.remove(self.qr_code.path)
        super(Participant, self).delete(*args, **kwargs)


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


class Attendance(models.Model):
    participant = models.ForeignKey(Participant,
                                    on_delete=models.CASCADE,
                                    related_name='attendance')
    date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-date',)

    def __str__(self):
        return str(self.participant) + str(self.date)


class Question(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                related_name='created_themes')
    related_event = models.ForeignKey(Event,
                                      on_delete=models.CASCADE,
                                      related_name='questions')
    slug = models.CharField(max_length=64)
    editable = models.BooleanField(default=False)
    title = models.CharField(max_length=64)
    message = models.TextField()


class Comment(models.Model):
    related_question = models.ForeignKey(settings.AUTH_USER_MODEL,
                                         on_delete=models.CASCADE,
                                         related_name='question_comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name='author_comments')
    message = models.TextField()
    created = models.DateTimeField(default=datetime.now())
