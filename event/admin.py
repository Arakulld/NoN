from django.contrib import admin
from .models import Event, Participant, News


@admin.register(Event)
class AdminEvents(admin.ModelAdmin):
    list_display = ('title', 'owner', 'description')


@admin.register(Participant)
class AdminParticipant(admin.ModelAdmin):
    list_display = ('qr_code',)


@admin.register(News)
class AdminNew(admin.ModelAdmin):
    list_display = ('slug', 'title', 'description')
