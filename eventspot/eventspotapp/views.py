from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from . models import Event
from . serializers import EventSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from collections import OrderedDict


# Create your views here.
class OneByOneItems(PageNumberPagination):
    page_size = 1

    def get_paginated_response(self, data):
        return Response(OrderedDict([
             ('count', self.page.paginator.count),
             ('total', self.page_size),
             ('current', self.page.number),
             ('next', self.get_next_link()),
             ('previous', self.get_previous_link()),
             ('results', data)
         ]))
        
@api_view(['GET'])
def event_list(request):
    """
    Retrieve all events
    """
    paginator = OneByOneItems()

    events = Event.objects.all()
    context = paginator.paginate_queryset(events, request)

    serializer = EventSerializer(context,many=True)
    
    return paginator.get_paginated_response(serializer.data)
   

@api_view(['POST'])
def event_create(request):
    """
    Create a new event
    """
    
    serializer = EventSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save(user=request.user)
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