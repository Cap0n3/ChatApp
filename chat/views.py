from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView
from django.views import View
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        server_instance = ChatServer.objects.get(id=self.kwargs["pk"])
        context["rooms"] = Room.objects.filter(server=server_instance)
        return context


class RoomView(View):
    """
    Get the room name from the URL and return the room object. If the room does not exist, it is created.
    """

    template_name = "chat/room.html"

    def get(self, request, *args, **kwargs):
        server_instance = ChatServer.objects.get(id=self.kwargs["pk"])
        room_name = self.kwargs["room_name"]
        chat_room, created = Room.objects.get_or_create(
            server=server_instance, name=room_name
        )

        if created:
            logger.info(f"Room {chat_room} created")

        context = {"room": chat_room}

        return render(request, self.template_name, context)
