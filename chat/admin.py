from django.contrib import admin
from .models import ChatServer, Room, Message

# Register your models here.
admin.site.register(ChatServer)
admin.site.register(Room)
admin.site.register(Message)

