from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_view


# Create your views here.
from account.forms import UserRegistrationForm
from account.models import Profile


def dashboard(request):
    return render(request, 'dashboard.html')


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
