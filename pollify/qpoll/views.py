from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import QPoll
from .serializers import QPollSerializer

@api_view(['GET', 'POST'])
def qpolls(request):
  if request.method == 'POST':
    serializer = QPollSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
  elif request.method == 'GET':
    qpolls = QPoll.objects.prefetch_related('questions').all()
    serializer = QPollSerializer(qpolls, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
  return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def qpoll(request, id):
  qpoll = get_object_or_404(QPoll.objects.prefetch_related('questions__options'), pk=id)

  if request.method == 'GET':
    serializer = QPollSerializer(qpoll)
    return Response(serializer.data, status=status.HTTP_200_OK)
  elif request.method == 'PUT':
    serializer = QPollSerializer(qpoll, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_200_OK)
    else:
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  elif request.method == 'DELETE':
    serializer = QPollSerializer(qpoll)
    json_response = Response(serializer.data, status=status.HTTP_200_OK)
    qpoll.delete()
    return json_response
