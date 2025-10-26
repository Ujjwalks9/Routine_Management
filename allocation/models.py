from django.db import models
from timetable.models import Teacher, Subject, Class, Room, TimeSlot

class Allocation(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    timeslot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.teacher} - {self.subject} ({self.class_id})"

    class Meta:
        db_table = 'timetable_allocation'  # Explicitly set to match sample_data.sql

class TeacherPreference(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    priority = models.IntegerField()

    def __str__(self):
        return f"{self.teacher} prefers {self.subject} (Priority: {self.priority})"

    class Meta:
        db_table = 'timetable_teacherpreference'  # Explicitly set to match sample_data.sql