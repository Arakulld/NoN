from django.contrib import admin
from .models import Event


@admin.register(Event)
class AdminEvents(admin.ModelAdmin):
    list_display = ('title',)
