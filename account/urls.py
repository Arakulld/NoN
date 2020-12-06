from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.CustomLogin.as_view(), name='login'),
    path('', views.dashboard, name='dashboard'),
    path('logout/', views.CustomLogout.as_view(), name='logout'),
    path('event_info/', views.info_about_event, name='event_info'),
    path('register/', views.register, name='register'),
    path('events_today/', views.events_for_today, name='events_today'),
    path('events_this_week', views.events_for_this_week, name='events_this_week')
]
