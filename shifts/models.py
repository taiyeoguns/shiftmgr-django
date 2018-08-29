from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)

class Manager(models.Model):
    """ Manager """
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Member(models.Model):
    """ Member """
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Shift(models.Model):
    """Shift object"""

    manager = models.ForeignKey('Manager', on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now, help_text='Enter Shift Date')

    def __str__(self):
        return str(self.date)


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