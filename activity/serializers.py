from django.contrib.auth.models import User, Group
from rest_framework import serializers
from activity.models import *
from datetime import timedelta


class ActivitySerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Activity
        fields = ('date', 'duration', 'distance', 'repetition', 'owner', 'url')


class RunningSerializer(serializers.HyperlinkedModelSerializer):
    distance = serializers.FloatField()
    duration = serializers.DurationField()

    class Meta:
        model = Activity
        fields = ('date', 'duration', 'distance')
