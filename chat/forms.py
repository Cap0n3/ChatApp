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
            self.fields["users"].queryset = registered_users

    class Meta:
        model = ChatServer
        fields = ["server_name", "users", "isPublic"]
        labels = {
            "server_name": "Server Name",
            "users": "Invite registered users",
            "isPublic": "Public server",
        }
        widgets = {
            "server_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter server name",
                }
            ),
            "users": forms.SelectMultiple(
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
        super(CreateRoomForm, self).__init__(*args, **kwargs)
        
        if 'instance' in kwargs and kwargs['instance']:
            chat_server_users = kwargs['instance'].server.users.all()
            self.fields['room_admins'].queryset = chat_server_users
    
    class Meta:
        model = Room
        fields = ["name", "room_admins"]
