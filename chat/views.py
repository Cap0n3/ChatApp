from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView
from chat.models import ChatServer, Room, Message
from .forms import CreateServerForm
from core.settings import logger


class IndexView(ListView):
    model = ChatServer
    template_name = "chat/index.html"
    context_object_name = "servers"
    form_class = CreateServerForm

    def get_common_context(self):
        return {"servers": ChatServer.objects.all(), "form": CreateServerForm()}

    def post(self, request, *args, **kwargs):
        form = CreateServerForm(request.POST)
        current_user = User.objects.get(username=request.user.username)

        if form.is_valid():
            logger.debug(f"Form is valid: {form.cleaned_data}")
            form.instance.owner = current_user
            form.save()
            form = CreateServerForm()
        else:
            logger.warning(f"Form is invalid: {form.errors}")

        context = self.get_common_context()
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        common_context = self.get_common_context()
        context.update(common_context)
        return context


class ServerView(DetailView):
    """
    Get the server name from the URL and return the server object. If the server does not exist, it is created.
    """

    model = ChatServer
    template_name = "chat/server.html"
    context_object_name = "server"


# class RoomListView(ListView):
#     """
#     Get all the rooms and return them to the template.
#     """

#     model = Room
#     template_name = "chat/server.html"
#     context_object_name = "rooms"

#     def get_queryset(self):
#         return Room.objects.all()


# class RoomView(ListView):
#     """
#     Get the room name from the URL and return the room object. If the room does not exist, it is created.
#     """

#     model = Room
#     template_name = "chat/room.html"
#     context_object_name = "room"

#     def get_queryset(self):
#         chat_room, created = Room.objects.get_or_create(name=self.kwargs["room_name"])

#         if created:
#             logger.info(f"Room {chat_room} created")

#         return chat_room
