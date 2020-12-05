from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.CustomLogin.as_view(), name='login'),
    path('logout/', views.CustomLogout.as_view(), name='logout'),
    path('event_info/', views.info_about_event, name='event_info'),
    path('register/', views.register, name='register')
]
