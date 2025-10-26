
from django.urls import path, include
from . import views
from .views import MyTokenObtainPairView, TeacherViewSet, SubjectViewSet, ClassViewSet, RoomViewSet, TimeSlotViewSet
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'teachers', TeacherViewSet)
router.register(r'subjects', SubjectViewSet)
router.register(r'classes', ClassViewSet)
router.register(r'rooms', RoomViewSet)
router.register(r'timeslots', TimeSlotViewSet)

urlpatterns = [
    path('generate/', views.generate_timetable_view, name='generate_timetable'),
    path('view/', views.view_timetable, name='view_timetable'),
    path('data/', views.get_timetable_data, name='timetable_data'),
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include(router.urls)),
]