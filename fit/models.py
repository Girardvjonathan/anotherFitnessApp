from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


# http://www.roguelynn.com/words/django-custom-user-models/

class FitUserManager(BaseUserManager):
    def _create_user(self, username, email, password, is_superuser, **extra_fields):
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(email=email, username=username,
                          date_joined=now, is_superuser=is_superuser, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username=None, email=None, password=None, **extra_fields):
        return self._create_user(username, email, password, False,
                                 **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        return self._create_user(username, email, password, True,
                                 **extra_fields)


class UserProfile(PermissionsMixin, AbstractBaseUser):
    email = models.EmailField('email address', unique=True)
    username = models.CharField(max_length=50, unique=True)
    date_joined = models.DateTimeField('date joined', default=timezone.now)
    weight = models.FloatField(blank=True, null=True)
    objects = FitUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
