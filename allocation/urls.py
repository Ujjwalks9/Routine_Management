from django.urls import path
from . import views

urlpatterns = [
    path('allocate/', views.allocate_teacher_view, name='allocate_teacher'),
]