from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from . models import Event
from . serializers import EventSerializer
from rest_framework.permissions import IsAuthenticated


# Create your views here.

@api_view(['GET'])
def event_list(request):
    """
    Retrieve all events
    """
    events = Event.objects.all()
    serializer = EventSerializer(events,many=True)
    return Response(serializer.data)
   

@api_view(['POST'])
def event_create(request):
    """
    Create a new event
    """
    serializer = EventSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['GET', 'PUT', 'DELETE'])
def event_detail(request, id):
    """
    Retrieve, update or delete an event.
    """
    try:
        event = Event.objects.get(id=id)
    except Event.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = EventSerializer(event)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = EventSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)