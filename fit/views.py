from rest_framework import viewsets
from fit.serializers import UserSerializer
from django.http import HttpResponse
from fit.models import UserProfile
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


# @csrf_exempt
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    # User = get_user_model()
    queryset = UserProfile.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class user_list(generics.ListCreateAPIView):
    """
    List all snippets, or create a new snippet.
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer


class user_detail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """

    def get_object(self, pk):
        try:
            return UserProfile.objects.get(pk=pk)
        except UserProfile.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = UserSerializer(snippet, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = UserSerializer(snippet, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
