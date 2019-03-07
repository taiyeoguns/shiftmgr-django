from django.db import models
from django.utils import timezone
from django.conf import settings


class Manager(models.Model):
    """ Manager model """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    def __repr__(self):
        return f"<Manager: {self.user.username}>"


class Member(models.Model):
    """ Member model """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    def __repr__(self):
        return f"<Member: {self.user.username}>"


class Shift(models.Model):
    """
    Shift model to describe details about a shift such as date etc
    """

    manager = models.ForeignKey("Manager", on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now, help_text="Enter Shift Date")

    def __str__(self):
        return str(self.date)

    def __repr__(self):
        return f"<Shift: {str(self.date)}>"


class Task(models.Model):
    """Task object"""

    shift = models.ForeignKey(
        "Shift", on_delete=models.CASCADE, help_text="Enter Shift Id"
    )
    title = models.CharField(max_length=50, help_text="Enter Task Title")
    start = models.DateTimeField(default=timezone.now, help_text="Enter Start Time")
    end = models.DateTimeField(null=True, blank=True, help_text="Enter End Time")

    def __str__(self):
        return self.title

    def __repr__(self):
        return f"<Task: {self.title}>"
