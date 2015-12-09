from django.contrib.auth.models import User, Group
from rest_framework import serializers
from fit.models import *


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('url', 'username', 'email', 'weight', 'height',)


class ActivitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Activity
        fields = ('date', 'duration', 'distance', 'repetition',)
