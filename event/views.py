from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.contrib import messages
from django.utils.text import slugify
from .forms import CreateEventForm
from . import models
from datetime import datetime
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
    event.image.save(f'{event.owner.username}/{event.slug + event.created.strftime("%Y-%d-%m-%H-%M-%S")}.{ext}',
                     open(old_path, "rb"), True)
    os.remove(old_path)


def add_event(request):
    if request.method == 'POST':
        form = CreateEventForm(data=request.POST, files=request.FILES)
        print(form.errors.as_json())
        if form.is_valid():
            form = form.save(commit=False)
            form.owner = request.user
            form.slug = slugify(form.title)
            form = form.save(commit=True)
            if form.image:
                add_image_to_event(form)
            return redirect('dashboard')
        else:
            raise Http404
    else:
        return render(request, 'add_event_form.html')


@login_required
def add_participant(request, slug, year, month, day, hour, minute, second):
    if request.method == 'POST':
        event = get_object_or_404(models.Event,
                                  slug=slug,
                                  created__year=year,
                                  created__month=month,
                                  created__day=day,
                                  created__hour=hour,
                                  created__minute=minute,
                                  created__second=second
                                  )
        try:
            participant = event.participants.create(user=request.user, event=event)
        except models.Participant.DoesNotExist:
            raise Http404
        add_qr_code_to_participant('',
                                   participant=participant,
                                   event=event,
                                   user=request.user)
        messages.success(request, 'Registered successfully.')
        redirect('dashboard')
    else:
        raise Http404


@login_required
def check_attendance_participant(request, event_id):
    event = get_object_or_404(models.Event, pk=event_id)
    try:
        participant = event.participants.get(user=request.user)
        time_now = datetime.now()
        try:
            participant.attendance.get(date__year=time_now.year, date__month=time_now.month,
                                       date__day=time_now.minute)
            return HttpResponse()
        except models.Attendance.DoesNotExist:
            if event.start_time < time_now < event.end_time:
                models.Attendance.objects.create(participant=participant, date=time_now)
            return HttpResponse()

    except models.Participant.DoesNotExist:
        return HttpResponse()


@login_required
def list_participants(request, slug, year, month, day, hour, minute, second):
    participants = get_object_or_404(models.Event,
                                     slug=slug,
                                     created__year=year,
                                     created__month=month,
                                     created__day=day,
                                     created__hour=hour,
                                     created__minute=minute,
                                     created__second=second).participants.all()
    return render(request,
                  '',
                  {'participants': participants})


@login_required
def event_detail(request, slug, year, month, day, hour, minute, second):
    event = get_object_or_404(models.Event,
                              slug=slug,
                              created__year=year,
                              created__month=month,
                              created__day=day,
                              created__hour=hour,
                              created__minute=minute,
                              created__second=second)
    return render(request,
                  'more-info.html',
                  {'event': event})


def test_view(request):
    form = CreateEventForm()
    return render(request,
                  'form_test.html',
                  {'form': form})
