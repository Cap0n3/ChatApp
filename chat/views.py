from django.shortcuts import render
from django.views.generic import ListView
from chat.models import Room, Message
from core.settings import logger

class RoomListView(ListView):
    '''
    Get all the rooms and return them to the template.
    '''
    model = Room
    template_name = 'chat/index.html'
    context_object_name = 'rooms'

    def get_queryset(self):
        return Room.objects.all()

class RoomView(ListView):
    '''
    Get the room name from the URL and return the room object. If the room does not exist, it is created.
    '''
    model = Room
    template_name = 'chat/room.html'
    context_object_name = 'room'

    def get_queryset(self):
        chat_room, created = Room.objects.get_or_create(name=self.kwargs['room_name'])
        
        if created:
            logger.info(f"Room {chat_room} created")
        
        return chat_room