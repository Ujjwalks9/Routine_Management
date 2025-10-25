from django.urls import path
from . import views
from timetable.views import admin_dashboard, professor_dashboard, student_dashboard

urlpatterns = [
    path('generate/', views.generate_timetable_view, name='generate_timetable'),
    path('view/', views.view_timetable, name='view_timetable'),
    path('data/', views.get_timetable_data, name='timetable_data'),
    path('api/admin/dashboard/', admin_dashboard),
    path('api/professor/dashboard/', professor_dashboard),
    path('api/student/dashboard/', student_dashboard),
]