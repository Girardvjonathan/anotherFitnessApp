from rest_framework import viewsets
from activity.serializers import UserSerializer, ActivitySerializer, RunningSerializer
from django.http import HttpResponse
from datetime import timedelta
from activity.models import UserProfile, Activity
from activity.permissions import IsOwnerOrReadOnly, IsOwner
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from django.db.models import Sum
from datetime import date
import datetime
from rest_framework import generics
from rest_framework import permissions
from rest_framework.renderers import JSONRenderer
from activity.authentification import QuietBasicAuthentication


class AuthView(APIView):
    authentication_classes = (QuietBasicAuthentication,)
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        return Response(self.serializer_class(request.user).data)


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsOwner,)
    queryset = UserProfile.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class ActivityViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)
    queryset = Activity.objects.all().order_by('-date')
    serializer_class = ActivitySerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserActivity(APIView):
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)
    # serializer_class = ActivitySerializer
    renderer_classes = (JSONRenderer,)

    def get(self, request, format=None):
        user = request.user
        distance_total = 0
        if not request.query_params.get('date'):
            date = datetime.date.today()
        else:
            date = datetime.datetime.strptime(request.query_params['date'], "%d-%m-%Y").date()

        start_week = date - datetime.timedelta(date.weekday())
        end_week = start_week + datetime.timedelta(7)

        activity = Activity.objects.filter(owner=user,
                                           date__range=(start_week, end_week),
                                           distance__gte=0).extra(
            {'date': "date(date)", 'duration': "datetime.timedelta(duration)"}).values('date').order_by(
            'date').annotate(distance=Sum('distance')) \
            .annotate(duration=Sum('duration'))
        for obj in activity:
            if obj['distance'] is not None:
                distance_total += obj['distance']
        print(activity)
        data = RunningSerializer(activity, many=True).data
        content = {'activity': data, 'distance_total': distance_total}
        return Response(content)


class UserList(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer


class ActivityList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ActivityDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
