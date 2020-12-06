from django.contrib import admin
from .models import Event, Participant, News, Attendance


@admin.register(Event)
class AdminEvents(admin.ModelAdmin):
    list_display = ('title', 'owner', 'description')


@admin.register(Participant)
class AdminParticipant(admin.ModelAdmin):
    list_display = ('event', 'user', 'qr_code')


@admin.register(News)
class AdminNew(admin.ModelAdmin):
    list_display = ('slug', 'title', 'description')


@admin.register(Attendance)
class AdminAttendance(admin.ModelAdmin):
    list_display = ('participant', 'date')
