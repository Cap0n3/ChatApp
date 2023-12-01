from django.forms import ModelForm
from django import forms
from .models import ChatServer, Room
from django.contrib.auth.models import User


class CreateServerForm(ModelForm):
    def __init__(self, *args, **kwargs):
        # Get the user from the kwargs (passed from the view)
        self.user = kwargs.pop("user", None)
        super(CreateServerForm, self).__init__(*args, **kwargs)

        if self.user:
            # Exclude the current user from the list of users to invite
            registered_users = User.objects.exclude(pk=self.user.pk)
            self.fields["members"].queryset = registered_users

    class Meta:
        model = ChatServer
        fields = ["server_name", "members", "isPublic"]
        labels = {
            "server_name": "Server Name",
            "members": "Invite registered users",
            "isPublic": "Public server",
        }
        widgets = {
            "server_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter server name",
                }
            ),
            "members": forms.SelectMultiple(
                attrs={
                    "class": "form-control selectpicker",
                    "data-live-search": "true",
                },
                choices=User.objects.all(),
            ),
            "isPublic": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

class CreateRoomForm(ModelForm):
    def __init__(self, *args, **kwargs):
        # Get the user & server instance from the kwargs (passed from the view)
        self.user = kwargs.pop("user", None)
        self.server_instance = kwargs.pop("instance", None)
        super(CreateRoomForm, self).__init__(*args, **kwargs)
        
        if self.user and self.server_instance:
            # Exclude the current user from the list of users to invite and get the list of users in the server
            chat_server_users = self.server_instance.members.all().exclude(pk=self.user.pk)
            self.fields['room_admins'].queryset = chat_server_users
    
    class Meta:
        model = Room
        fields = ["name", "room_admins"]
