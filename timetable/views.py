# from django.shortcuts import render, redirect
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from .algorithms.timetable_generator import generate_timetable
# from .models import Allocation, TimeSlot

# @csrf_exempt
# def generate_timetable_view(request):
#     if request.method == 'POST':
#         generate_timetable()
#         return redirect('view_timetable')
#     return render(request, 'timetable/generate_timetable.html')

# @csrf_exempt
# def view_timetable(request):
#     allocations = Allocation.objects.all()
#     timeslots = TimeSlot.objects.all()
#     return render(request, 'timetable/view_timetable.html', {
#         'allocations': allocations,
#         'timeslots': timeslots
#     })

# @csrf_exempt
# def get_timetable_data(request):
#     allocations = Allocation.objects.select_related('teacher', 'subject', 'class_id', 'room', 'timeslot')
#     data = [{
#         'title': f"{a.teacher} - {a.subject} ({a.room})",
#         'start': f"{a.timeslot.day} {a.timeslot.start_time}",
#         'end': f"{a.timeslot.day} {a.timeslot.end_time}",
#         'className': a.class_id.name
#     } for a in allocations]
#     return JsonResponse(data, safe=False)


from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .algorithms.timetable_generator import generate_timetable
from .models import TimeSlot
from allocation.models import Allocation, Teacher, Subject, Class, Room
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import viewsets, permissions
from .serializers import TeacherSerializer, SubjectSerializer, ClassSerializer, RoomSerializer, TimeSlotSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# API ViewSets for CRUD operations (authenticated users only)
class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [permissions.IsAuthenticated]

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [permissions.IsAuthenticated]

class ClassViewSet(viewsets.ModelViewSet):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    permission_classes = [permissions.IsAuthenticated]

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAuthenticated]

class TimeSlotViewSet(viewsets.ModelViewSet):
    queryset = TimeSlot.objects.all()
    serializer_class = TimeSlotSerializer
    permission_classes = [permissions.IsAuthenticated]

@csrf_exempt
def generate_timetable_view(request):
    if request.method == 'POST':
        generate_timetable()
        return redirect('view_timetable')
    return render(request, 'timetable/generate_timetable.html')

@csrf_exempt
def view_timetable(request):
    allocations = Allocation.objects.all()
    timeslots = TimeSlot.objects.all()
    return render(request, 'timetable/view_timetable.html', {
        'allocations': allocations,
        'timeslots': timeslots
    })

@csrf_exempt
def get_timetable_data(request):
    allocations = Allocation.objects.select_related('teacher', 'subject', 'class_id', 'room', 'timeslot')
    data = []
    day_map = {
        'Monday': '2025-10-27',
        'Tuesday': '2025-10-28',
        'Wednesday': '2025-10-29',
        'Thursday': '2025-10-30',
        'Friday': '2025-10-31'
    }
    for a in allocations:
        start = f"{day_map[a.timeslot.day]}T{a.timeslot.start_time}"
        end = f"{day_map[a.timeslot.day]}T{a.timeslot.end_time}"
        data.append({
            'title': f"{a.teacher} - {a.subject} ({a.room})",
            'start': start,
            'end': end,
            'className': a.class_id.name
        })
    return JsonResponse(data, safe=False)