from django.contrib.auth.models import User, Group
from rest_framework import serializers
from fit.models import *


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserProfile
        # activities = serializers.PrimaryKeyRelatedField(many=True, queryset=Activity.objects.all())
        fields = ('username', 'email', 'weight', 'height',
                  # 'activities',
                  'weight', 'height',
                  )

        def __init__(self, request):
            context = {'request': request}


class ActivitySerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Activity
        fields = ('date', 'duration', 'distance', 'repetition', 'owner')
