from django.test import TestCase
from timetable.models import Teacher, TimeSlot, Allocation
from timetable.algorithms.clash_detector import check_clashes

class TimetableTests(TestCase):
    def setUp(self):
        self.teacher = Teacher.objects.create(name="Test Teacher", availability={"Monday": ["08:00-10:00"]})
        self.timeslot = TimeSlot.objects.create(day="Monday", start_time="08:00:00", end_time="09:00:00")

    def test_clash_detection(self):
        clashes = check_clashes(self.teacher.id, 1, self.timeslot.id)
        self.assertEqual(clashes, 0)  # No clashes initially