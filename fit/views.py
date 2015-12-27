from rest_framework import viewsets
from fit.serializers import UserSerializer, ActivitySerializer
from django.http import HttpResponse
from fit.models import UserProfile, Activity
from fit.permissions import IsOwnerOrReadOnly, IsOwner
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from rest_framework import permissions
from rest_framework.renderers import JSONRenderer
from fit.authentification import QuietBasicAuthentication


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
        activity = Activity.objects.filter(owner=user).order_by('-date')
        for obj in activity:
            if obj.distance is not None:
                distance_total += obj.distance
        data = ActivitySerializer(activity, many=True).data
        content = {'activity': data, 'distance_total': distance_total}
        print(content)
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
