from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import Group
from rest_framework.parsers import JSONParser
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from fit.serializers import UserSerializer
from django.http import HttpResponse
from fit.models import UserProfile
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


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


# @csrf_exempt
@api_view(['GET', 'POST'])
def user_list(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        user = UserProfile.objects.all()
        serializer = UserSerializer(user, context={'request': request}, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, pk, format=None):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        print('allo')
        user = UserProfile.objects.get(pk=pk)
        print(user)
    except UserSerializer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = UserSerializer(user, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
