from timetable.models import Allocation, Teacher, Room, TimeSlot
from django.db.models import Q

def check_clashes(teacher_id, room_id, timeslot_id):
    timeslot = TimeSlot.objects.get(id=timeslot_id)
    clashes = 0

    # Check teacher clash
    teacher_clashes = Allocation.objects.filter(
        teacher_id=teacher_id,
        timeslot__day=timeslot.day,
        timeslot__start_time__lte=timeslot.end_time,
        timeslot__end_time__gte=timeslot.start_time
    ).count()
    clashes += teacher_clashes

    # Check room clash
    room_clashes = Allocation.objects.filter(
        room_id=room_id,
        timeslot__day=timeslot.day,
        timeslot__start_time__lte=timeslot.end_time,
        timeslot__end_time__gte=timeslot.start_time
    ).count()
    clashes += room_clashes

    # Check teacher availability
    teacher = Teacher.objects.get(id=teacher_id)
    availability = teacher.availability.get(timeslot.day, [])
    time_ok = any(
        start <= str(timeslot.start_time) <= end and start <= str(timeslot.end_time) <= end
        for start, end in [(t.split('-') for t in availability)]
    )
    if not time_ok:
        clashes += 1

    return clashes