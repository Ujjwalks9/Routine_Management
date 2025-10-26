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
from allocation.models import Allocation

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