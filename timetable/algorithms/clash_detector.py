from django.db.models import Q
from timetable.models import Teacher, Room, TimeSlot
from allocation.models import Allocation
from datetime import datetime
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def _parse_time_str(s):
    if not s or not isinstance(s, str):
        return None
    s = s.strip()
    for fmt in ("%H:%M:%S", "%H:%M"):
        try:
            return datetime.strptime(s, fmt).time()
        except ValueError:
            continue
    logger.warning(f"Failed to parse time string: {s}")
    return None

def check_clashes(teacher_id, room_id, timeslot_id):
    try:
        timeslot = TimeSlot.objects.get(id=timeslot_id)
    except TimeSlot.DoesNotExist:
        logger.error(f"Timeslot ID {timeslot_id} does not exist")
        return 1

    clashes = 0
    existing_allocations = Allocation.objects.filter(
        timeslot__day=timeslot.day,
        timeslot__start_time__lte=timeslot.end_time,
        timeslot__end_time__gte=timeslot.start_time
    ).filter(
        Q(teacher_id=teacher_id) | Q(room_id=room_id)
    ).exclude(
        teacher_id=teacher_id, room_id=room_id, timeslot_id=timeslot_id
    )

    if existing_allocations.exists():
        clashes += existing_allocations.count()
        logger.debug(f"Clashes found: {clashes} (Teacher ID: {teacher_id}, Room ID: {room_id}, Timeslot ID: {timeslot_id})")

    try:
        teacher = Teacher.objects.get(id=teacher_id)
    except Teacher.DoesNotExist:
        logger.error(f"Teacher ID {teacher_id} does not exist")
        return clashes + 1

    availability = teacher.availability.get(timeslot.day, []) if isinstance(teacher.availability, dict) else []
    time_ok = False
    for entry in availability:
        if not isinstance(entry, str):
            logger.warning(f"Invalid availability entry for teacher {teacher_id}: {entry}")
            continue
        parts = entry.split("-")
        if len(parts) != 2:
            logger.warning(f"Malformed availability range for teacher {teacher_id}: {entry}")
            continue
        start = _parse_time_str(parts[0])
        end = _parse_time_str(parts[1])
        if start is None or end is None:
            continue
        if start <= timeslot.start_time and timeslot.end_time <= end:
            time_ok = True
            break

    if not time_ok:
        logger.debug(f"Teacher {teacher_id} not available for timeslot {timeslot.day} {timeslot.start_time}-{timeslot.end_time}")
        clashes += 1

    return clashes