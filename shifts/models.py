from django.db import models
from django.utils import timezone
from django.conf import settings
import uuid


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
    shifts = models.ManyToManyField("Shift", related_name="members")

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    def __repr__(self):
        return f"<Member: {self.user.username}>"


class Shift(models.Model):
    """
    Shift model to describe details about a shift such as date etc
    """

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    manager = models.ForeignKey("Manager", on_delete=models.CASCADE)
    date = models.DateField(
        default=timezone.now, unique=True, help_text="Enter Shift Date"
    )

    def __str__(self):
        return str(self.date)

    def __repr__(self):
        return f"<Shift: {str(self.date)}>"


class Task(models.Model):
    """Task object"""

    shift = models.ForeignKey(
        "Shift", on_delete=models.CASCADE, help_text="Enter Shift Id"
    )
    handler = models.ForeignKey(
        "Member", on_delete=models.CASCADE, help_text="Enter Member Id"
    )
    title = models.CharField(max_length=50, help_text="Enter Task Title")
    start = models.DateTimeField(default=timezone.now, help_text="Enter Start Time")
    end = models.DateTimeField(null=True, blank=True, help_text="Enter End Time")
    priority = models.ForeignKey(
        "Priority", on_delete=models.CASCADE, help_text="Enter Priority Id"
    )
    status = models.ForeignKey(
        "Status", on_delete=models.CASCADE, help_text="Enter Status Id"
    )

    def __str__(self):
        return self.title

    def __repr__(self):
        return f"<Task: {self.title}>"


class Priority(models.Model):
    """ Priority object """

    title = models.CharField(max_length=50, help_text="Enter Priority Title")

    def __str__(self):
        return self.title

    def __repr__(self):
        return f"<Priority: {self.title}>"


class Status(models.Model):
    """ Status object """

    title = models.CharField(max_length=50, help_text="Enter Status Title")

    def __str__(self):
        return self.title

    def __repr__(self):
        return f"<Status: {self.title}>"
