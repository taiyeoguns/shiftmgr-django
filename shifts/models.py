from django.db import models
from django.utils import timezone


# Create your models here.
class Shift(models.Model):
    """Shift object"""

    date = models.DateField(default=timezone.now, help_text='Enter Shift Date')

    def __str__(self):
        return self.date


class Task(models.Model):
    """Task object"""

    shift = models.ForeignKey(
        'Shift', on_delete=models.CASCADE, help_text='Enter Shift Id')
    title = models.CharField(max_length=50, help_text='Enter Task Title')
    start = models.DateTimeField(
        default=timezone.now, help_text='Enter Start Time')
    end = models.DateTimeField(
        null=True, blank=True, help_text='Enter End Time')

    def __str__(self):
        return self.title