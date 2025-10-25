from django.test import TestCase
from allocation.models import TeacherPreference
from timetable.models import Teacher, Subject

class AllocationTests(TestCase):
    def setUp(self):
        self.teacher = Teacher.objects.create(name="Test Teacher")
        self.subject = Subject.objects.create(name="Math", department="CS")

    def test_teacher_preference(self):
        pref = TeacherPreference.objects.create(teacher=self.teacher, subject=self.subject, priority=1)
        self.assertEqual(pref.priority, 1)