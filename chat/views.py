from typing import Any
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from chat.models import ChatServer, Room, Message
from .forms import CreateServerForm
from core.settings import logger

class IndexView(ListView):
    '''
    Get all the chat servers and return them to the template.
    '''
    model = ChatServer
    template_name = 'chat/index.html'
    context_object_name = 'servers'
    form_class = CreateServerForm

    # Handle form submission
    def post(self, request, *args, **kwargs):
        form = CreateServerForm(request.POST)
        if form.is_valid():
            logger.debug(f"Form is valid: {form.cleaned_data}")
            form.save()
            return render(request, self.template_name, {'form': form})
        else:
            logger.debug(f"Form is invalid: {form.errors}")
            return render(request, self.template_name, {'form': form})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CreateServerForm()
        return context

class ServerView(DetailView):
    '''
    Get the server name from the URL and return the server object. If the server does not exist, it is created.
    '''
    model = ChatServer
    template_name = 'chat/server.html'
    context_object_name = 'server'


class RoomListView(ListView):
    '''
    Get all the rooms and return them to the template.
    '''
    model = Room
    template_name = 'chat/server.html'
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