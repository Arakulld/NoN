from django.urls import path, include
from . import views

urlpatterns = [
    path('test/', views.test_view, name='test'),
    path('add_event_form/', views.add_event, name='add_event'),
    path('<slug:slug>/<int:year>/<int:month>/<int:day>/<int:hour>/<int:minute>/<int:second>/', views.event_detail,
         name='event_detail'),
    path('check_attendance/<int:event_id>', views.check_attendance_participant, name='check_attendance'),
    path('add_participant/<slug:slug>/<int:year>/<int:month>/<int:day>/<int:hour>/<int:minute>/<int:second>/',
         views.add_participant, name='add_participant')
]
