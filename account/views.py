from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_view


# Create your views here.
from account.forms import UserRegistrationForm, UserEditForm, ProfileEditForm
from account.models import Profile


def dashboard(request):
    return render(request, 'dashboard.html')


def events_for_today(request):
    return render(request, 'today.html')


def events_for_this_week(request):
    return render(request, 'week.html')


class CustomLogin(auth_view.LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True


class CustomLogout(auth_view.LogoutView):
    template_name = 'login.html'


def info_about_event(request):
    return render(request, 'more-info.html')


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            return redirect('login')
    else:
        user_form = UserRegistrationForm()
    return render(request, 'register.html')


@login_required
def account(request):
    return render(request, 'user_account.html')


@login_required
def edit_account(request):
    if request.method == 'POST':
        try:
            Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            Profile.objects.create(user=request.user)

        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect(request, 'dashboard')
        else:
            messages.error(request, 'Error updating profile')
    return render(request, 'edit_account.html')
