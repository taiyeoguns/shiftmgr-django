from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver


class Profile(models.Model):
    """
    Profile model to hold extra user information
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, null=True, blank=True)


@receiver(post_save, sender=User)
def create_update_profile(sender, instance, created, **kwargs):
    """
    Signal to automatically create/save Profile from User
    """
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


@receiver(pre_delete, sender=User)
def delete_profile(sender, instance, **kwargs):
    """
    Signal to automatically delete Profile from User
    """
    if instance:
        profile = Profile.objects.get(user=instance)
        profile.delete()


class Manager(models.Model):
    """ Manager model """
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.user.first_name} {self.user.last_name}"


class Member(models.Model):
    """ Member model """
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.user.first_name} {self.user.last_name}"


class Shift(models.Model):
    """
    Shift model to describe details about a shift such as date etc
    """

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
