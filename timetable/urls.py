from django.urls import path
from . import views

urlpatterns = [
    path('generate/', views.generate_timetable_view, name='generate_timetable'),
    path('view/', views.view_timetable_view, name='view_timetable'),
    path('data/', views.get_timetable_data, name='timetable_data'),
]