from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from userFit.models import *
# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class Activity(models.Model):
    # type = models.
    date = models.DateTimeField()
    duration = models.TimeField()
    distance = models.FloatField(blank=True, null=True)
    repetition = models.IntegerField(blank=True, null=True)
    owner = models.ForeignKey(UserProfile, related_name='activities')
