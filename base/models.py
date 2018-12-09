from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone = models.CharField(max_length=20, null=True, blank=True)
    is_manager = models.BooleanField('manager status', default=False)
    is_member = models.BooleanField('member status', default=False)
