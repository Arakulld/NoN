from django.forms import ModelForm
from .models import Event


class CreateEventForm(ModelForm):
    class Meta:
        model = Event
        exclude = ('owner', 'slug')
