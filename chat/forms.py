from django.forms import ModelForm
from django import forms
from .models import ChatServer
from django.contrib.auth.models import User

class CreateServerForm(ModelForm):
    class Meta:
        model = ChatServer
        fields = ['name', 'users', 'isPublic']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'users': forms.SelectMultiple(attrs={'class': 'form-control selectpicker', 'data-live-search': 'true'}, choices=User.objects.all()),
            'isPublic': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }