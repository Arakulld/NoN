from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.contrib import messages
from .forms import CreateEventForm
from . import models
import qrcode
import os


def generate_qr_code(data):
    qr_code = qrcode.make(data)
    qr_code_path = settings.TEMP_PATH + 'temp'
    qr_code.save(qr_code_path)
    return qr_code_path


def add_qr_code_to_participant(data, participant, user, event):
    old_path = generate_qr_code(data)
    new_path = settings.QR_CODE_SAVE_NAME.format(namespace=user.username, user_id=user.pk,
                                                 event_id=event.id, ext=settings.QR_CODE_EXT)
    participant.qr_code.save(new_path, open(old_path, "rb"), True)
    os.remove(old_path)


def add_image_to_event(event):
    old_path = event.image.path
    ext = old_path.rsplit('.', 1)[1].lower()
    event.image.save(f'{event.owner.username}/{event.slug + event.created.strftime("%Y-""%d-""%m")}.{ext}',
                     open(old_path, "rb"), True)
    os.remove(old_path)


@login_required
def add_participant(request, slug, year, month, day):
    if request.method == 'POST':
        event = get_object_or_404(models.Event,
                                  slug=slug,
                                  year=year,
                                  month=month,
                                  day=day)
        try:
            participant = event.participants.get(user=request.user)
        except models.Participant.DoesNotExist:
            raise Http404
        add_qr_code_to_participant('',
                                   participant=participant,
                                   event=event,
                                   user=request.user)
        messages.success(request, 'Registered successfully.')
        redirect('')
    else:
        raise Http404


@login_required
def events_list(request):
    if 'display_my' in request.GET and request.GET['display_my'] == 'participating':
        list_events = models.Event.objects.filter(owner=request.user)
    elif 'display_my' in request.GET and request.GET['display_my'] == 'created':
        list_events = models.Event.objects.filter(participants__user=request.user)
    else:
        list_events = models.Event.objects.all()
    paginator = Paginator(list_events, 20)
    page = request.GET.get('page')
    try:
        events = paginator.page(page)
    except PageNotAnInteger:
        events = paginator.page(1)
    except EmptyPage:
        events = paginator.page(paginator.num_pages)
    return render(request,
                  '',
                  {'page': page,
                   'events': events})


@login_required
def list_participants(request, slug, year, month, day):
    participants = get_object_or_404(models.Event,
                                     created__slug=slug,
                                     created__year=year,
                                     created__month=month,
                                     created__day=day).participants.all()
    return render(request,
                  '',
                  {'participants': participants})


@login_required
def event_detail(request, slug, year, month, day):
    event = get_object_or_404(models.Event,
                              created__slug=slug,
                              created__year=year,
                              created__month=month,
                              created__day=day)
    return render(request,
                  '',
                  {'even': event})


def test_view(request):
    form = CreateEventForm()
    return render(request,
                  'form_test.html',
                  {'form': form})
