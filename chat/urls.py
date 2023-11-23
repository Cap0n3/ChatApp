from django.urls import path
from .views import IndexView, ServerView, RoomView

urlpatterns = [
    path("home/", IndexView.as_view(), name="index"),
    path("server/<pk>/", ServerView.as_view(), name="server"),
    path("server/<pk>/<str:room_name>/", RoomView.as_view(), name="room"),
    #path("", RoomListView.as_view(), name="room_list"),
    #path("<str:room_name>/", RoomView.as_view(), name="room"),
]
