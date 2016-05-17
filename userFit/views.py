from rest_framework import viewsets
from userFit.serializers import UserSerializer
from userFit.models import UserProfile
from userFit.permissions import  IsOwner
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
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


class UserList(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer
