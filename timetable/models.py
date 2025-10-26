from django.db import models

class Teacher(models.Model):
    name = models.CharField(max_length=100)
    availability = models.JSONField(default=dict)  # e.g., {"Monday": ["08:00-12:00"]}

    def __str__(self):
        return self.name

class Subject(models.Model):
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Class(models.Model):
    name = models.CharField(max_length=50)
    department = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Room(models.Model):
    name = models.CharField(max_length=50)
    capacity = models.IntegerField()

    def __str__(self):
        return self.name

class TimeSlot(models.Model):
    DAYS = (
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
    )
    day = models.CharField(max_length=10, choices=DAYS)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.day} {self.start_time}-{self.end_time}"