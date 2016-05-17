from django.contrib.auth.models import User, Group
from rest_framework import serializers
from activity.models import *
from datetime import timedelta


class UserSerializer(serializers.HyperlinkedModelSerializer):
    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user

    class Meta:
        model = UserProfile
        # activities = serializers.PrimaryKeyRelatedField(many=True, queryset=Activity.objects.all())
        fields = ('username', 'email', 'weight', 'height', 'password',
                  # 'activities',
                  )
        extra_kwargs = {'password': {'write_only': True}}

        def __init__(self, request):
            context = {'request': request}

