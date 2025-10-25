from django.shortcuts import render, redirect
from django.http import JsonResponse
from .algorithms.timetable_generator import generate_timetable
from .models import Allocation, TimeSlot

def generate_timetable_view(request):
    if request.method == 'POST':
        generate_timetable()
        return redirect('view_timetable')
    return render(request, 'timetable/generate_timetable.html')

def view_timetable(request):
    allocations = Allocation.objects.all()
    timeslots = TimeSlot.objects.all()
    return render(request, 'timetable/view_timetable.html', {
        'allocations': allocations,
        'timeslots': timeslots
    })

def get_timetable_data(request):
    allocations = Allocation.objects.select_related('teacher', 'subject', 'class_id', 'room', 'timeslot')
    data = [{
        'title': f"{a.teacher} - {a.subject} ({a.room})",
        'start': f"{a.timeslot.day} {a.timeslot.start_time}",
        'end': f"{a.timeslot.day} {a.timeslot.end_time}",
        'className': a.class_id.name
    } for a in allocations]
    return JsonResponse(data, safe=False)