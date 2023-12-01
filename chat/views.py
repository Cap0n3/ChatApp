from typing import Any
from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from chat.models import ChatServer, Room, Message
from .forms import CreateServerForm, CreateRoomForm
from core.settings import logger


class IndexView(ListView):
    model = ChatServer
    template_name = "chat/index.html"
    context_object_name = "servers"
    form_class = CreateServerForm

    def instanciate_form(self):
        '''
        Create a new instance of the form with the current user (Stay DRY)
        '''
        return CreateServerForm(user=self.request.user)

    def get_common_context(self):
        return {
            "servers": ChatServer.objects.all(), 
            "form": self.instanciate_form()
    }

    def post(self, request, *args, **kwargs):
        form = CreateServerForm(request.POST)
        current_user = User.objects.get(pk=request.user.pk)

        if form.is_valid():
            logger.debug(f"Form is valid: {form.cleaned_data}")
            form.instance.owner = current_user
            form.save()
            form = self.instanciate_form()
        else:
            logger.warning(f"Form is invalid: {form.errors}")

        context = self.get_common_context()
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        common_context = self.get_common_context()
        context.update(common_context)
        return context


class ServerView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        server_instance = ChatServer.objects.get(id=self.kwargs["pk"])
        chat_rooms = Room.objects.filter(server=server_instance)

        #  check if the user is a member of the server
        if request.user not in server_instance.members.all():
            logger.warning(f"User {request.user} is not a member of server {server_instance}")
            # Return a context without the room creation form
            context = {
                "server": server_instance,
                "rooms": chat_rooms,
            }
        else:
            logger.info(f"User {request.user} is a member of server {server_instance}")
            # Return a context with the form
            context = {
                "server": server_instance,
                "form": CreateRoomForm(instance=server_instance, user=request.user),
                "rooms": chat_rooms,
            }

        return render(request, "chat/server.html", context)
    
    def post(self, request, *args, **kwargs):
        form = CreateRoomForm(request.POST)
        current_user = User.objects.get(pk=request.user.pk)
        server_instance = ChatServer.objects.get(id=self.kwargs["pk"])

        if form.is_valid():
            logger.debug(f"Form is valid: {form.cleaned_data}")
            form.instance.creator = current_user
            form.instance.server = server_instance
            form.save()
            form = CreateRoomForm(instance=server_instance, user=request.user)
        else:
            logger.warning(f"Form is invalid: {form.errors}")

        context = {
            "server": server_instance,
            "form": form,
            "rooms": Room.objects.filter(server=server_instance),
        }
        return render(request, "chat/server.html", context)

    
# class ServerView(LoginRequiredMixin, View):
#     """
#     Get the server name from the URL and return the server object. If the server does not exist, it is created.
#     """

#     template_name = "chat/server.html"

#     def get_server_instance(self):
#         return ChatServer.objects.get(id=self.kwargs["pk"])

#     def get_queryset(self):    
#         return Room.objects.filter(server=self.get_server_instance()),

#     def get_context_data(self, **kwargs):
#         context = {}
#         context["form"] = CreateRoomForm(instance=self.get_server_instance(), user=self.request.user)
#         return context
    
#     def get(self, request, *args, **kwargs):
#         queryset = Room.objects.filter(server=self.get_server_instance())
#         context = self.get_context_data()

#         # Print the name of room in the queryset with index and not name ???
#         for room in queryset:
#             print(f"Room: {room}")

#         return render(request, self.template_name, {"rooms": queryset, **context})
    
    # def post(self, request, *args, **kwargs):
    #     form = CreateRoomForm(request.POST)
    #     current_user = User.objects.get(pk=request.user.pk)
    #     server_instance = ChatServer.objects.get(id=self.kwargs["pk"])

    #     if form.is_valid():
    #         logger.info(f"Form is valid: {form.cleaned_data}")
    #         form.instance.creator = current_user
    #         form.instance.server = server_instance
    #         form.save()
    #         form = CreateRoomForm(instance=server_instance, user=request.user)
    #     else:
    #         logger.warning(f"Form is invalid: {form.errors}")

    #     context = {
    #         "server": server_instance,
    #         "form": form,
    #         "rooms": Room.objects.filter(server=server_instance),
    #     }
    #     return render(request, self.template_name, context)


# class ServerView(LoginRequiredMixin, DetailView):
#     """
#     Get the server name from the URL and return the server object. If the server does not exist, it is created.
#     """

#     model = ChatServer
#     template_name = "chat/server.html"
#     context_object_name = "server"

#     def instanciate_form(self):
#         '''
#         Create a new instance of the form with the current user and server instance (Stay DRY)
#         '''
#         return CreateRoomForm(
#             instance=ChatServer.objects.get(id=self.kwargs["pk"]), 
#             user=self.request.user
#         )

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["form"] = self.instanciate_form()
#         context["rooms"] = Room.objects.filter(server=ChatServer.objects.get(id=self.kwargs["pk"]))
#         return context
    
#     def post(self, request, *args, **kwargs):
#         form = CreateRoomForm(request.POST)
#         current_user = User.objects.get(pk=request.user.pk)
#         server_instance = ChatServer.objects.get(id=self.kwargs["pk"])
#         #context = self.get_context_data()

#         if form.is_valid():
#             logger.info(f"Form is valid: {form.cleaned_data}")
#             form.instance.creator = current_user
#             form.instance.server = server_instance
#             form.save()
#             form = self.instanciate_form()
#         else:
#             logger.warning(f"Form is invalid: {form.errors}")
#             # Update context with the form and errors
#             #context["form"] = form
#             #context["errors"] = form.errors

#         context = self.get_context_data()
#         return render(request, self.template_name, context)
        


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
