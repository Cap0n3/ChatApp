from django.contrib.auth.models import User
from django.db import models


class ChatServer(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    server_name = models.CharField(max_length=1000)
    users = models.ManyToManyField(User, blank=True)
    isPublic = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.server_name}"


# Create your models here.
class Room(models.Model):
    server = models.ForeignKey(ChatServer, on_delete=models.CASCADE)
    name = models.CharField(max_length=1000, unique=True)
    online = models.ManyToManyField(User, blank=True)
    room_admins = models.ManyToManyField(User, blank=True, related_name="room_admins")


    def get_online_count(self):
        return self.online.count()

    def join(self, user):
        self.online.add(user)
        self.save()

    def leave(self, user):
        self.online.remove(user)
        self.save()

    def __str__(self):
        return f"{self.name} ({self.get_online_count()}"


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    content = models.CharField(max_length=512)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.content} [{self.timestamp}]"
