from django.db import models
from timetable.models import Teacher, Subject

class TeacherPreference(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    priority = models.IntegerField(default=1)  # 1 (highest) to 5 (lowest)

    def __str__(self):
        return f"{self.teacher} prefers {self.subject} (Priority: {self.priority})"