from django.contrib.auth.models import User, Group
from rest_framework import serializers
from fit.models import UserProfile


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('url', 'username', 'email')
